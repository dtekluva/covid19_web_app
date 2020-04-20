from django.core.management.base import BaseCommand
from django.utils import timezone
import pandas as pd
import requests, io
from main.models import *

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):

        def correct_colnames(df):
            dates = list(df.columns)[4:]
            dates = list(map(lambda x: (x + "20"), dates))
            df.columns = [ *list(df.columns)[:4], *dates]

            return df.groupby("Country/Region").sum().reset_index(), dates

        cases_url = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv"
        recov_url = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv"
        deaths_url= "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv"

        response = requests.get(cases_url)
        data_cases = correct_colnames(pd.read_csv(io.StringIO(response.content.decode('utf-8'))))[0]
        # print(data_cases.columns)

        response = requests.get(recov_url)
        data_recov = correct_colnames(pd.read_csv(io.StringIO(response.content.decode('utf-8'))))[0]
        # print(data_recov.columns)

        response = requests.get(deaths_url)
        data_deaths = correct_colnames(pd.read_csv(io.StringIO(response.content.decode('utf-8'))))[0]
        # print(data_deaths.columns)

        countries = Country.objects.all().order_by("name")

        for country in countries:

            print(country.name)
            matched_country_cases = data_cases[data_cases["Country/Region"].str.lower() == country.name.lower()]

            if len(matched_country_cases) > 0:
                dates = list(matched_country_cases)[3:]
                matched_cases_data = list(matched_country_cases.iloc[0])[3:]
                matched_country_deaths = list(data_deaths[data_deaths["Country/Region"].str.lower() == country.name.lower()].iloc[0])[3:]
                matched_country_recov = list(data_recov[data_recov["Country/Region"].str.lower() == country.name.lower()].iloc[0])[3:]

                for date, cases, deaths, recovs in zip(dates, matched_cases_data, matched_country_deaths, matched_country_recov):

                    date = date.split("/")
                    date = f"{date[2]}-{date[0]}-{date[1]}"

                    datapoint = Datapoint.objects.get_or_create(date = date, country = country)[0]
                    
                    # datapoint.country = country
                    datapoint.cases = cases
                    datapoint.deaths = deaths
                    datapoint.recoveries = recovs
                    # print(recovs)

                    datapoint.save()



            # print(country, len(matched_country_cases))

        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)