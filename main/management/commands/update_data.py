from django.core.management.base import BaseCommand
from django.utils import timezone
import pandas as pd
from main.models import *

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):

        country_name = ""
        cases = 0
        deaths = 0
        recoveries = 0

        total_cases = 0
        total_deaths = 0
        total_recoveries = 0

        wiki_url = "https://en.wikipedia.org/wiki/2019%E2%80%9320_coronavirus_pandemic_by_country_and_territory#Pandemic_by_country_and_territory"

        dfs = pd.read_html(wiki_url,header=0)
        dataframe = dfs[0]

        dataframe.columns = ["province", "countries", "cases", "deaths", "recoveries", "err1"]
        dataframe = dataframe.drop(columns = ["province"])
        dataframe.replace( "—", 0 )

        country_name = ""
        cases = 0
        deaths = 0
        recoveries = 0

        global_data = dataframe.iloc[0]
        # print(global_data)

        global_cases = int(global_data["countries"].encode("ascii", errors="ignore").decode().replace(",",""))
        global_deaths = int(global_data["cases"].encode("ascii", errors="ignore").decode().replace(",",""))
        global_recoveries = int(global_data["deaths"].encode("ascii", errors="ignore").decode().replace(",",""))

        country = Country.objects.get_or_create(name = "Global")[0]

        country.cases = global_cases    
        country.deaths = global_deaths  
        country.recoveries = global_recoveries 

        country.save()

        for i in range(1,len(dataframe)):
            data = (dataframe.iloc[i])

            try :
                if not isinstance(data[0], float):

                    country_name = data["countries"].split("[")[0]
                    cases = data["cases"]
                    deaths = data["deaths"]
                    recoveries = data["recoveries"]
                    
                    if not any([len(country_name) > 35, len(cases) > 35, len(deaths) > 35, len(recoveries) > 35]):

                        country = Country.objects.get_or_create(name = country_name)[0]
                        country.cases = cases if (cases).isnumeric()  else 0      
                        country.deaths = deaths if (deaths).isnumeric()   else 0       
                        country.recoveries = recoveries if (recoveries).isnumeric() else 0 

                        country.save()
                        
                        datapoint = Datapoint.objects.get_or_create(date = datetime.datetime.now(), country = country)[0]
                    
                        datapoint.country = country
                        datapoint.cases = country.cases
                        datapoint.deaths = country.deaths
                        datapoint.recoveries = country.recoveries

                        datapoint.save()




            except TypeError:
                pass
            print("Still working..!!")
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)