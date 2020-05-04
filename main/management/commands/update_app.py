from django.core.management.base import BaseCommand
from django.utils import timezone
import pandas as pd, numpy as np
from sklearn.metrics import r2_score
from main.models import *

class Command(BaseCommand):
    help = 'Loads Data for Nigerian states'

    def handle(self, *args, **kwargs):

        print(f"update_global_data Successfull ---> {update_global_data()}")
        print(f"update_nigeria_data Successfull ---> {update_nigeria_data()}")
        print(f"update_predictions Successfull ---> {update_predictions()}")
            
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)

def update_nigeria_data():

    try:
        country_name = ""
        cases = 0
        deaths = 0
        recoveries = 0

        total_cases = 0
        total_deaths = 0
        total_recoveries = 0

        wiki_url = "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Nigeria"

        dfs = pd.read_html(wiki_url,header=0)
        dataframe = dfs[2][:-2] # REMOVE THE LAST 2 UNWANTED ROWS IN THE DATA FRAME (TOTAL & DESCRIPTION)

        state_name = ""
        cases = 0
        deaths = 0
        recoveries = 0


        for i in range(len(dataframe)):
            data = (dataframe.iloc[i])

            if True :
                if not isinstance(data[0], float):

                    state_name = data["State"].split("[")[0]
                    cases = data["Cases"]
                    deaths = data["Deaths"]
                    recoveries = data["Recovered"]
                    
                    country = Country.objects.get(name = "Nigeria")
                    state = State.objects.get_or_create(state_name = state_name, country = country)[0]

                    state.country = country
                    state.cases = cases      
                    state.deaths = deaths     
                    state.recoveries = recoveries

                    state.save()

                    print((state_name), (cases), (deaths), (recoveries), (recoveries).isnumeric())

        return True

    except:
        return False

def update_global_data():
    
    try:
        
        country_name = ""
        cases = 0
        deaths = 0
        recoveries = 0

        total_cases = 0
        total_deaths = 0
        total_recoveries = 0

        wiki_url = "https://en.wikipedia.org/wiki/2019%E2%80%9320_coronavirus_pandemic_by_country_and_territory#Pandemic_by_country_and_territory"

        import requests
        from bs4 import BeautifulSoup as soup


        html = requests.get(wiki_url).content
        bs = soup(html, features="lxml")
        table = bs.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="thetable") 

        rows = table.findAll(lambda tag: tag.name=='tr')

        total = bs.findAll(lambda tag: tag.name=='b' ) 

        country = Country.objects.get_or_create(name = "Global")[0]
        country.cases = int(total[3].text.replace(",", ""))
        country.deaths = int(total[4].text.replace(",", ""))
        country.recoveries = int(total[5].text.replace(",", ""))

        country.save()
        print(country.cases, country.deaths, country.recoveries)
        
        datapoint = Datapoint.objects.get_or_create(date = datetime.datetime.now(), country = country)[0]
    
        datapoint.country = country
        datapoint.cases = country.cases
        datapoint.deaths = country.deaths
        datapoint.recoveries = country.recoveries

        datapoint.save()

        for row in rows:

            row_data = row.find(lambda tag: tag.name=='a')
            children = row.findAll(lambda tag: tag.name=='td')
            cases = 0
            deaths = 0
            recovs = 0
            name = False

            try:

                name = row_data.text

            except:
                pass

            if len(children) > 2:

                cases = children[0].text.replace(",", "").replace("—\n", "0")
                deaths = children[1].text.replace(",", "").replace("—\n", "0")
                recovs = children[2].text.replace(",", "").replace("—\n", "0")

            else:
                continue

            if True :

                country = Country.objects.get_or_create(name = name)[0]
                # print(country)
                country.cases = cases      
                country.deaths = deaths
                country.recoveries = recovs

                country.save()
                # print(row_data.text, country.cases, country.deaths, country.recoveries)
                
                datapoint = Datapoint.objects.get_or_create(date = datetime.datetime.now(), country = country)[0]
            
                datapoint.country = country
                datapoint.cases = country.cases
                datapoint.deaths = country.deaths
                datapoint.recoveries = country.recoveries

                datapoint.save()

        return True

    except:

        return False

def update_predictions():
    
    try:
        
        for country in Country.objects.all():
            datapoints = country.datapoint_set.all().order_by("date").values("cases")
            values = pd.DataFrame(list(datapoints))[-30:]
            values["_index"] = np.arange(len(values))

            if not datapoints:continue;

            predictor, accuracy = create_model(values)

            country.predicted = predictor(len(values)+5)
            country.accuracy = accuracy
            # country.save()

            print(country.name, country.predicted, country.accuracy )

    except:
        pass

def create_model(data):
                    
    model = np.polyfit(data["_index"], data.cases, 3 )
    predict = np.poly1d(model)

    accuracy = r2_score(data.cases, predict(data["_index"]))

    return predict, accuracy