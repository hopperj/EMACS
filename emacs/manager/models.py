from django.db import models

from device.models import Device

class UserSetting(models.Model):
	# set the value for a speceific device
	device = models.ForeignKey(Device, null=False)
	# tempature, pressure, etc....
	measure = models.CharField(max_length=64)
	# degree, ohm...
	value = models.CharField(max_length=64)

