# Create your models here.
from django.contrib.auth.models import User
from django.contrib.gis.db import models


class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2, null=True)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name


# Extending in-built user model with one-to-one relationship
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, primary_key=True)
    email = models.CharField(max_length=50, null=True)
    user_location = models.PointField(null=True)
    # favourite_mosque = models.CharField(max_length=50, null=True)


class Mosques(models.Model):
    # location = models.CharField(max_length=100, null=True)
    mosque_goer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mosque_name = models.CharField(max_length=100, null=True)

