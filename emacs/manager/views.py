from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from .models import	UserSetting
from django.views.generic import ListView


# new device form
class NewUserSettingView(CreateView):
	model = UserSetting
	fields = ['device', 'measure', 'value']
	success_url = reverse_lazy('index')
    
	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		return super(NewUserSettingView, self).form_valid(form)

# new device form
class UpdateUserSettingView(UpdateView):
	model = UserSetting
	fields = ['device', 'measure', 'value']
	success_url = reverse_lazy('index')
    
	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		return super(UpdateUserSettingView, self).form_valid(form)

class UserSettingListView(ListView):
    model = UserSetting
    template_name = "manager/user_settings_list.html"
    
    def get_queryset(self):
        settings = Collection.objects.all()
        return settings


class UserSettingIndexView(TemplateView):

	template_name = 'manager/settings.html'

	def get_context_data(self, **kwargs):
		context = super(UserSettingIndexView, self).get_context_data(**kwargs)
		context['user_settings'] = UserSetting.objects.all()
		return context

         
class ManagerIndexView(TemplateView):

	template_name = 'manager/index.html'

	def get_context_data(self, **kwargs):
		context = super(ManagerIndexView, self).get_context_data(**kwargs)
		return context
