from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	(r'^$', include('device.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^device/', include('device.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
