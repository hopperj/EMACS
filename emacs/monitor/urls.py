from django.conf.urls import patterns, url
from monitor import views

urlpatterns = patterns('',
    url(r'new/$', views.new_record, name='new_record'),
    url(r'all/$', views.RecordListView.as_view(), name='all_records'),
    url(r'api/$', views.LineChartJSONView.as_view(), name='line_chart_json'),
)