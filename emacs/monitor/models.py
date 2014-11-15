from django.db import models
from device.models import Device

# Class that can accept any sensor data
class Record(models.Model):
	#device id
	device = models.ForeignKey(Device, null=False)
	#sensor_name
	sensor_name = models.CharField(max_length=64)
    #value -- units come from types table
	value = models.FloatField()
	#the time of the sample
	created_at = models.IntegerField()


class SensorTypes(models.Model):
	# tempature, pressure, etc....
	measure = models.CharField(max_length=64)
	# degree, ohm...
	unit = models.CharField(max_length=64)