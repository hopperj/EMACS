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


class LineChartJSONView(BaseLineChartView):	
    def get_labels(self):
        
        records = Record.objects.all()
        times = [record.created_at for record in records]
        return times

    def get_data(self):
        records = Record.objects.all()
        value_map = dict()
        for record in records:
        	if not record.device in value_map:
        		value_map[record.device] = list()
        	
        	value_map[record.device].append(record.value)

        value_lists = list()
        for device in value_map:
        	value_lists.append(value_map[device])

        return value_lists