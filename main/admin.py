from django.contrib import admin
from .models import *

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', "increase_rate")

class StateAdmin(admin.ModelAdmin):
    list_display = ["country"]

class DatapointAdmin(admin.ModelAdmin):
    list_display = ('country', 'cases', 'deaths', 'recoveries', 'date', 'user', 'is_verified')

admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Datapoint, StateAdmin)