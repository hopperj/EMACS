from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from .models import	Device

# new device form
class NewDeviceView(CreateView):
	model = Device
	fields = ['manufacturer_id', 'device_name', 'tempature_control', 'pressure_control', 'humidity_control']
	success_url = reverse_lazy('index')
    
	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		return super(NewDeviceView, self).form_valid(form)


class DeviceDetailView(DetailView):
	model = Device

	def get_context_data(self, **kwargs):
		context = super(DeviceDetailView, self).get_context_data(**kwargs)
		return context 


class DeviceIndexView(View):

	def get(self, request, *args, **kwargs):
		return HttpResponse('That worked.')