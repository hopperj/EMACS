from django.db import models

# Holds the manufacturer id and name of a given sensor
class Device(models.Model):
    manufacturer_id = models.CharField(max_length=32)
    device_name = models.CharField(max_length=32)
<<<<<<< HEAD
    pressure_control = models.BooleanField(default=False)
    humidity_control = models.BooleanField(default=False)
=======
>>>>>>> 26c404b8bea56bf4d13f0b14e4cdf17245a49815
