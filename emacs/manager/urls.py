from django.conf.urls import patterns, url
from manager import views

urlpatterns = patterns('',
	url(r'^$', views.ManagerIndexView.as_view(), name='index'),
	url(r'^settings/$', views.UserSettingIndexView.as_view(), name='user_settings'),
    url(r'new/$', views.NewUserSettingView.as_view(), name='new_user_setting'),
    url(r'edit/$', views.UpdateUserSettingView.as_view(), name='update_user_setting'),
)