from django.forms import ModelForm
from .models import Device


class DeviceForm(ModelForm):
     class Meta:
         model = Device
         fields = ['manufacturer_id', 'device_name', 'tempature_control', 'pressure_control', 'humidity_control']