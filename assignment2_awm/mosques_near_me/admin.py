# Register your models here.
from django.contrib.gis import admin
from .models import WorldBorder, Mosques

admin.site.register(WorldBorder, admin.OSMGeoAdmin)
admin.site.register(Mosques, admin.OSMGeoAdmin)
