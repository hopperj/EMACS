import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.views.generic.list import ListView
from rest_framework.renderers import JSONRenderer
from serializers import RecordSerializer
from device.models import Device
from monitor.models import Record
from chartjs.views.lines import BaseLineChartView
from random import randint
from django.views.generic import TemplateView
from manager.models import UserSetting


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def new_record(request):
	

	record = JSONParser().parse(request)
	device = Device.objects.get(manufacturer_id=record['device_id'])
	#del record['device_id']
	record['device'] = device.id
	
	device_state = device.__dict__
	del device['_state']


	serializer = RecordSerializer(data=record)
	if serializer.is_valid():
		# save record
		record = serializer.save()
		device_sensor_settings = UserSetting.objects.filter(device_id=record.device_id)

		prepared_settings = list()
		for setting in device_sensor_settings:
			setting_dict = setting.__dict__
			del setting_dict['_state']
			prepared_settings.append(setting_dict)


		return JSONResponse(prepared_settings, status=201)
	return JSONResponse(serializer.errors, status=400)


class RecordListView(ListView):
	
	model = Record

	def get_context_data(self, **kwargs):
		context = super(RecordListView, self).get_context_data(**kwargs)
		context['records'] = Record.objects.all()
		return context


class TempatureLineChartJSONView(BaseLineChartView):	
    def get_labels(self):
        
        records = Record.objects.filter(sensor_name="tempature").order_by('created_at')
        times = [record.created_at for record in records]
        return times

    def get_data(self):
        records = Record.objects.filter(sensor_name="tempature").order_by('created_at')
        value_map = dict()
        for record in records:
        	if not record.device.device_name in value_map:
        		value_map[record.device.device_name] = list()
        	
        	value_map[record.device.device_name].append(record.value)

        	for name in value_map:
        		if record.device.device_name != name:
        			value_map[name].append('')

        	for name in value_map:
        		i = 0
        		while i < len(value_map[name]):
        			if value_map[name][i] == '':
        				if i != 0 and i != (len(value_map[name]) -1):
        					value_map[name][i] = (value_map[name][i-1] + value_map[name][i+1])/2


        			i+=1		


        value_lists = list()
        for device_name in value_map:
        	value_lists.append(value_map[device_name])

        return value_lists


class HumidityLineChartJSONView(BaseLineChartView):	
    def get_labels(self):
        
        records = Record.objects.filter(sensor_name="humidity")
        times = [record.created_at for record in records]
        return times

    def get_data(self):
        records = Record.objects.filter(sensor_name="humidity")
        value_map = dict()
        for record in records:
        	if not record.device.device_name in value_map:
        		value_map[record.device.device_name] = list()
        	
        	value_map[record.device.device_name].append(record.value)

        value_lists = list()
        for device_name in value_map:
        	value_lists.append(value_map[device_name])

        return value_lists


class PressureLineChartJSONView(BaseLineChartView):	
    def get_labels(self):
        
        records = Record.objects.filter(sensor_name="pressure")
        times = [record.created_at for record in records]
        return times

    def get_data(self):
        records = Record.objects.filter(sensor_name="pressure")
        value_map = dict()
        for record in records:
        	if not record.device.device_name in value_map:
        		value_map[record.device.device_name] = list()
        	
        	value_map[record.device.device_name].append(record.value)

        value_lists = list()
        for device_name in value_map:
        	value_lists.append(value_map[device_name])

        return value_lists