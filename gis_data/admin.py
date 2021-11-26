from django.contrib import admin

# Register your models here.
from gis_data import models
admin.site.register(models.CityAirQualityInfo)
