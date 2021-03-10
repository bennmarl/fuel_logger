from django.db import models
from django.forms import ModelForm
from organizations.models import Organization, OrganizationUser

#organzation
class Organization(Organization):
    class Meta:
        proxy = True

class AccountUser(OrganizationUser):
    class Meta:
        proxy = True


# this is unnecessary
#class Organization (models.Model):
#    name = models.CharField(max_length = 100)
#    def __str__(self):
#        return '%s' % self.name


class User (models.Model):
    email = models.EmailField(max_length = 100)
    #encrypt password!
    password = models.CharField(max_length = 50)
    organization = models.ForeignKey(Organization, null = True, on_delete=models.SET_NULL)
    admin = models.BooleanField(default = 'false')
    organization = models.ForeignKey(Organization, null = True, on_delete=models.SET_NULL)


class Campaign (models.Model):
    SEASONAL = "S"
    BEFORE_AFTER = "BA"
    PERIOD = "P"

    TIME_PERIOD_CHOICES = [
        (SEASONAL, 'Seasonal'),
        (BEFORE_AFTER, 'Before/After'),
        (PERIOD, 'One Time Period')
        ]


    name = models.CharField(max_length=200)
    organization = models.ForeignKey(Organization, null = True, on_delete=models.SET_NULL)
    time = models.CharField(choices=TIME_PERIOD_CHOICES,
                            default = PERIOD, max_length=100
                            )
    public = models.BooleanField()
    # Use external library for country, region
    town = models.CharField(max_length=100)

    def __str__(self):
        return '%s' % self.name
    

class Household (models.Model):
    householdNumber = models.IntegerField()
    organization = models.ForeignKey(Organization, null = True, on_delete=models.SET_NULL)

    def __str__(self):
        return '%s' % self.householdNumber

class HouseholdAdditionalData (models.Model):
    type = models.CharField(max_length=100)
    value = models.TextField()
    household = models.ForeignKey(Household, null = True, on_delete=models.SET_NULL)

class Stove (models.Model):
    stoveType = models.CharField(max_length = 100)
    organization = models.ManyToManyField(Organization)

class Fuel (models.Model):
    fuelType = models.CharField(max_length = 100)
    organization = models.ManyToManyField(Organization)

class Datafile (models.Model):
    household = models.ForeignKey(Household, null = True, on_delete=models.SET_NULL)
    campaign = models.ForeignKey(Campaign, null = True, on_delete=models.SET_NULL)
    # Add location
    adultEquiv = models.FloatField()
    numStoves = models.IntegerField()
    numPmMeasurementLocations = models.IntegerField()
    numFUEL = models.IntegerField()
    numLogs = models.IntegerField()
    typeStoveData = models.CharField(max_length = 250)

class DatafileAdditionalData (models.Model):
    type = models.CharField(max_length=100)
    value = models.TextField()
    datafile = models.ForeignKey(Datafile, null = True, on_delete = models.SET_NULL)

class StoveMetadata (models.Model):
    datafile = models.ForeignKey(Datafile, null = True, on_delete=models.SET_NULL)
    stove = models.ForeignKey(Stove, null = True, on_delete=models.SET_NULL)
    fuel = models.ForeignKey(Fuel, null = True, on_delete=models.SET_NULL)
    cookingEventsDay = models.IntegerField()
    cookingTime = models.FloatField()
    numDaysLastUse = models.IntegerField()
    totalFuel = models.FloatField()
    AvgDailyFuel = models.FloatField()
    fuelCalibrationValue = models.FloatField()
    fuelTareOffset = models.FloatField()

class StoveAdditionalData (models.Model):
    type = models.CharField(max_length=100)
    value = models.TextField()
    stove = models.ForeignKey(StoveMetadata, null = True, on_delete = models.SET_NULL)

class UsageData (models.Model):
    stove = models.ForeignKey(StoveMetadata, null = True, on_delete=models.SET_NULL)
    timeStamp = models.DateTimeField()
    usage = models.FloatField()

class TemperatureData (models.Model):
    stove = models.ForeignKey(StoveMetadata, null = True, on_delete=models.SET_NULL)
    timeStamp = models.DateTimeField()
    usage = models.FloatField()

class FuelData (models.Model):
    stove = models.ForeignKey(StoveMetadata, null = True, on_delete=models.SET_NULL)
    timeStamp = models.DateTimeField()
    usage = models.FloatField()









    

