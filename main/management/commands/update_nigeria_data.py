from django.core.management.base import BaseCommand
from django.utils import timezone
import pandas as pd
from main.models import *

class Command(BaseCommand):
    help = 'Loads Data for Nigerian states'

    def handle(self, *args, **kwargs):

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
            # except TypeError:
            #     pass
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)