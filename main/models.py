import sys
from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import json, datetime, random
from covid19.settings import BASE_DIR
from cors.models import *
from django.utils import timezone
import pandas as pd


# Create your models here.
class Country(models.Model):
    name         = models.CharField(max_length = 100)
    lng          = models.FloatField(default=0)
    lat          = models.FloatField(default=0)
    increase_rate= models.FloatField(default=0)
    cases        = models.IntegerField(default=0)
    deaths       = models.IntegerField(default=0)
    recoveries   = models.IntegerField(default=0)
    predicted    = models.FloatField(default=0)
    coefficient  = models.FloatField(default=0)
    accuracy     = models.FloatField(default=0)
    updated_at   = models.DateTimeField(default=timezone.now)

    def get_global_reading(self):
        global_reads = Country.objects.get(name = "Global").__dict__

        del global_reads["_state"]
        global_reads["updated_at"] = str(global_reads["updated_at"])

        return global_reads

    def get_all_countries(self):
        countries = Country.objects.all().order_by("name", "cases").values("name", "lng", "increase_rate", "cases", "deaths", "recoveries", "predicted", "accuracy")

        # print(list(countries))

        return list(countries)

    def fetch_data(self, country_list):

        response = []

        for country in country_list:
            if country == "false": continue;
            country_object = Country.objects.filter(name__iexact = country.lower())[0]

            country_data = {"name": country_object.name,
                                "today":{
                                    "cases": country_object.cases,
                                    "deaths": country_object.deaths,
                                    "recoveries": country_object.recoveries
                                }
                                }
            try:
                
                datapoints = country_object.datapoint_set.all().values("cases", "deaths", "recoveries", "date")

                points_dataframe = pd.DataFrame(data = datapoints)
                points_dataframe["date"] = points_dataframe["date"].astype("str")

                response.append({"country": country_data, "data":points_dataframe.to_dict('records') }) #CONVERT TO RECORDS TYPE PANDAS DICT

            except:
                response.append({"country": country_data,  "data":[{'cases': 0, 'deaths': 0, 'recoveries': 0, 'date': '2020-04-02'}]*30 })

        return response

    def get_moving_difference(self):

        try:

            datapoints = self.datapoint_set.all().values("cases")
            points_dataframe = pd.DataFrame(data = datapoints)

            points_dataframe = points_dataframe.diff(axis=0)

            return list(points_dataframe["cases"])[1:]

        except:
            return [0,0,0,0,0,0,0,0,0,0,0]

    def __str__(self):
        return self.name

class State(models.Model):
    country    = models.ForeignKey(Country, on_delete=models.CASCADE, blank = True, null = True)
    state_name = models.CharField(max_length = 100)
    capital    = models.CharField(max_length = 100, default= "")
    cases      = models.CharField(max_length = 100, default=0)
    deaths     = models.CharField(max_length = 100, default=0)
    recoveries = models.CharField(max_length = 100, default=0)
    increase_rate = models.FloatField(default=0)
    created_at    = models.DateTimeField(default=timezone.now)

    def get_states_data(self, country):
        datapoints = State.objects.all().values("state_name", "cases", "recoveries", "deaths")

        return list(datapoints)
        

    def __str__(self):
        return self.state_name
    

class Datapoint(models.Model):
    country    = models.ForeignKey(Country, on_delete=models.CASCADE, blank = True, null = True)
    state      = models.ForeignKey(State, on_delete=models.CASCADE, blank = True, null = True)
    cases      = models.IntegerField(default=0)
    deaths     = models.IntegerField(default=0)
    recoveries = models.IntegerField(default=0)
    date       = models.DateField(default=0)
    created_at   = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.country.name

class Visitor(models.Model):

    ip         = models.CharField(max_length = 60, default = "null")
    hits       = models.IntegerField(default = 0)
    name       = models.CharField(max_length = 60, default = "null")
    user_agent = models.CharField(max_length = 60, default = "null")
    last_visit = models.DateTimeField(auto_now=True)

    def record(self, request):
        try:
            ip = request.META.get('REMOTE_ADDR', "No IP")
            useragent = request.META.get('REMOTE_ADDR', "No user agent")
            name = request.META.get('COMPUTERNAME', "No name")

            visitor = Visitor.objects.get_or_create(ip = ip)[0]
            visitor.hits += 1
            visitor.name = name
            visitor.user_agent = useragent
            visitor.last_visit = datetime.datetime.now()
            visitor.save()
        except:
            print("UNABLE TO LOG VISITOR")

    def __str__(self):
        return self.ip
