from django.conf.urls import patterns, url
from device import views

urlpatterns = patterns('',
	url(r'^$', views.DeviceIndexView.as_view(), name='index'),
    url(r'^(?P<device_id>\d+)/$', views.DeviceDetailView.as_view(), name='device_detail'),
    url(r'new/$', views.NewDeviceView.as_view(), name='new_device'),
)