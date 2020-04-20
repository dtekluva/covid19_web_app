from django.contrib import admin
from .models import *

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', "increase_rate")

class StateAdmin(admin.ModelAdmin):
    list_display = ["country", "created_at"]

class DatapointAdmin(admin.ModelAdmin):
    list_display = ('country', 'cases', 'deaths', 'recoveries', 'date', 'user', 'is_verified')

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('ip', 'hits', "name",)

admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Datapoint, StateAdmin)
admin.site.register(Visitor, VisitorAdmin)