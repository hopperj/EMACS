from django.db import models

# Holds the manufacturer id and name of a given sensor
class Device(models.Model):
    manufacturer_id = models.CharField(max_length=32)
    device_name = models.CharField(max_length=32)
