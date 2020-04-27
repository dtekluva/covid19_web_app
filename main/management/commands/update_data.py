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

        import requests
        from bs4 import BeautifulSoup as soup


        html = requests.get(wiki_url).content
        bs = soup(html, features="lxml")
        table = bs.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="thetable") 

        rows = table.findAll(lambda tag: tag.name=='tr')

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
                print(country)
                country.cases = cases      
                country.deaths = deaths
                country.recoveries = recovs

                country.save()
                print(row_data.text, country.cases, country.deaths, country.recoveries)
                
                datapoint = Datapoint.objects.get_or_create(date = datetime.datetime.now(), country = country)[0]
            
                datapoint.country = country
                datapoint.cases = country.cases
                datapoint.deaths = country.deaths
                datapoint.recoveries = country.recoveries

                datapoint.save()


        print("Still working..!!")
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)