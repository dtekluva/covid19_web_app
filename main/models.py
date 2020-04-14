import sys
from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import json, datetime, random
from covid19.settings import BASE_DIR
from cors.models import *
from django.utils import timezone


# Create your models here.
class Country(models.Model):
    name         = models.CharField(max_length = 100)
    lng          = models.FloatField(default=0)
    lat          = models.FloatField(default=0)
    increase_rate= models.FloatField(default=0)
    cases        = models.IntegerField(default=0)
    deaths       = models.IntegerField(default=0)
    recoveries   = models.IntegerField(default=0)
    updated_at   = models.DateTimeField(default=timezone.now)

    def get_global_reading(self):
        global_reads = Country.objects.get(name = "Global").__dict__

        del global_reads["_state"]
        global_reads["updated_at"] = str(global_reads["updated_at"])

        return global_reads

    def __str__(self):
        return self.name

class State(models.Model):
    country    = models.ForeignKey(Country, on_delete=models.CASCADE, blank = True, null = True)
    name       = models.CharField(max_length = 100)
    capital    = models.CharField(max_length = 100, default= "")
    cases      = models.IntegerField(default=0)
    deaths     = models.IntegerField(default=0)
    recoveries = models.IntegerField(default=0)
    increase_rate = models.FloatField(default=0)
    created_at    = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Datapoint(models.Model):
    country    = models.ForeignKey(Country, on_delete=models.CASCADE, blank = True, null = True)
    state      = models.ForeignKey(State, on_delete=models.CASCADE, blank = True, null = True)
    cases      = models.IntegerField(default=0)
    deaths     = models.IntegerField(default=0)
    recoveries = models.IntegerField(default=0)
    date       = models.DateField(default=0)
    created_at   = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.state