from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.views.generic.list import ListView
from rest_framework.renderers import JSONRenderer
from serializers import RecordSerializer
from device.models import Device
from monitor.models import Record

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
		return JSONResponse(serializer.data, status=201)
	return JSONResponse(serializer.errors, status=400)

class RecordListView(ListView):
	
	model = Record

	def get_context_data(self, **kwargs):
		context = super(RecordListView, self).get_context_data(**kwargs)
		context['records'] = Record.objects.all()
		return context