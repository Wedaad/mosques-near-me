# Register your models here.
from django.contrib.gis import admin
from .models import Mosques

admin.site.register(Mosques, admin.OSMGeoAdmin)
