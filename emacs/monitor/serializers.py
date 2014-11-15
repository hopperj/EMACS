from django.forms import widgets
import json
from rest_framework.serializers import ModelSerializer
from .models import Record


class RecordSerializer(ModelSerializer):
    class Meta:
        model = Record
        fields = (
                  'device',
                  'sensor_name',
                  'value',
                  'created_at'
        )
