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

class CollectionListView(ListView):
    model = UserSetting
    template_name = "manager/user_settings_list.html"
    
    def get_queryset(self):
        settings = Collection.objects.all
        return settings
         
class ManagerIndexView(TemplateView):

	template_name = 'manager/index.html'

	def get_context_data(self, **kwargs):
		context = super(ManagerIndexView, self).get_context_data(**kwargs)
		xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
		ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]
		chartdata = {'x': xdata, 'y': ydata}
		charttype = "pieChart"
		chartcontainer = 'piechart_container'
		data = {
    		'charttype': charttype,
    		'chartdata': chartdata,
    		'chartcontainer': chartcontainer,
    		'extra': {
        		'x_is_date': False,
        		'x_axis_format': '',
        		'tag_script_js': True,
        		'jquery_on_ready': False,
    		}
		}

		context['data'] = data
		context['device_1'] = [(1,15), (2,16), (3,12), (4,26), (5,17), (6,9), (7,9), (8,8), (9,3), (10, 4)]
		context['device_2'] = [(1,4), (2,4), (3,6), (4,3), (5,19), (6,20), (7,20), (8,21), (9,22), (10, 1)]
		return context
