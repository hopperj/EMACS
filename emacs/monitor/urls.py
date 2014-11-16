from django.conf.urls import patterns, url
from monitor import views

urlpatterns = patterns('',
    url(r'new/$', views.new_record, name='new_record'),
    url(r'all/$', views.RecordListView.as_view(), name='all_records'),
    url(r'tempapi/$', views.TempatureLineChartJSONView.as_view(), name='tempature_line_chart'),
    url(r'pressureapi/$', views.PressureLineChartJSONView.as_view(), name='pressure_line_chart'),
    url(r'humidityapi/$', views.HumidityLineChartJSONView.as_view(), name='humidity_line_chart'),
)