from django import forms
import datetime
from .models import *
from analytics.procedures import sp_companies_get
from analytics.models import UsersCompanies, Accounts, Centers


def NewForm(model_name, fields_lst, user_id, hide_id=None):
	from django.contrib.contenttypes.models import ContentType
	model_id = ContentType.objects.get(model=str(model_name))
	model_class = model_id.model_class()
	fields_labels = {f[0]: f[1] for f in fields_lst}

	class Form(forms.ModelForm):
		class Meta:
			model = model_class
			fields = '__all__'

		def __init__(self, *args, **kwargs):
			super(Form, self).__init__(*args, **kwargs)
			for key in self.fields:
				if key == 'company':
					self.fields[key].choices = sp_companies_get(user_id, False)
				if key == 'account':
					companies = UsersCompanies.objects.filter(user_id=user_id)
					self.fields[key].queryset = Accounts.objects.filter(
						kind=False, active=True, company__in=[obj.company for obj in companies])
				if key == 'center':
					companies = UsersCompanies.objects.filter(user_id=user_id)
					self.fields[key].queryset = Centers.objects.filter(
						kind=False, active=True, company__in=[obj.company for obj in companies]).exclude(center_id='0')
				if key == 'status':
					self.fields['status'].initial = model_class._meta.get_field('status').get_default()
				if key == 'sale_agent' and model_name != 'salesagents':
					sale_agent = SalesAgents.objects.filter(user_id=user_id)
					if sale_agent:
						self.fields['sale_agent'].initial = sale_agent[0].pk
					else:
						self.fields['sale_agent'].initial = None

				self.fields[key].label = fields_labels[key]
				'''if 'date' in key:
					self.fields[key] = forms.DateField(widget=forms.TextInput(attrs=
					{
						'class': 'datepicker'
					}))'''

	return Form


class FormSearchAccounts(forms.ModelForm):

	class Meta:
		from .models import Accounts
		model = Accounts
		fields = ['company', 'account_type', 'parentid', 'active', 'kind']


def searchform(model_name, fields_lst, user_id, all_opco=False):
	from django.contrib.contenttypes.models import ContentType
	model_id = ContentType.objects.get(model=str(model_name))
	model_class = model_id.model_class()
	fields_labels = {f[0]: f[1] for f in fields_lst}

	class Form(forms.ModelForm):

		class Meta:
			model = model_class
			fields = [f[0] for f in fields_lst]

		def __init__(self, *args, **kwargs):
			super(Form, self).__init__(*args, **kwargs)
			for key in self.fields:
				if self.fields[key].widget.input_type == 'checkbox':
					self.fields[key] = forms.NullBooleanField()
				if key != 'company':
					self.fields[key].required = False
				else:
					if all_opco:
						self.fields[key].required = False
						self.fields[key].choices = sp_companies_get(user_id, True)
					else:
						self.fields[key].choices = sp_companies_get(user_id, False)
				if key == 'status':
					self.fields[key].initial = None
				if key == 'rate':
					self.fields[key].initial = None
				if key == 'account':
					companies = UsersCompanies.objects.filter(user_id=user_id)
					self.fields[key].queryset = Accounts.objects.filter(
						kind=False, active=True, company__in=[obj.company for obj in companies])
				if key == 'center':
					companies = UsersCompanies.objects.filter(user_id=user_id)
					self.fields[key].queryset = Centers.objects.filter(
						kind=False, active=True, company__in=[obj.company for obj in companies]).exclude(center_id='0')
				if key == 'year':
					self.fields[key].queryset = BudgetYear.objects.all()
				self.fields[key].label = fields_labels[key]
				self.fields[key].initial = None
	return Form


def form_filter(user_id, form=forms.ModelForm, all_opco=False):
	for key in form.fields:
		if key != 'company':
			if all_opco:
				form.fields[key].choices = sp_companies_get(user_id, True)
			else:
				form.fields[key].choices = sp_companies_get(user_id, False)
		if key == 'account':
			companies = UsersCompanies.objects.filter(user_id=user_id)
			form.fields[key].queryset = Accounts.objects.filter(
				kind=False, active=True, company__in=[obj.company for obj in companies])
		if key == 'center':
			companies = UsersCompanies.objects.filter(user_id=user_id)
			form.fields[key].queryset = Centers.objects.filter(
				kind=False, active=True, company__in=[obj.company for obj in companies]).exclude(center_id='0')

