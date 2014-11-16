from django.forms import ModelForm
from django import forms
from .models import UserSetting
from device.models import Device

class UserSettingForm(ModelForm):

	device = forms.ChoiceField(choices=[(device.id, device.device_name) for device in Device.objects.all()])
	class Meta:
		model = UserSetting
		fields = ['device', 'measure', 'value']
		widgets = {
          'device': forms.Select(attrs={'class': 'select'}),
      	}