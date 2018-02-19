from django import forms
import datetime
from .utilities import chart_type, time_range


class LoginForm(forms.Form):
	username = forms.CharField(label="User ", max_length=20)
	password = forms.CharField(label="Password ", widget=forms.PasswordInput)


class IndexViewForm(forms.Form):
	date_from = forms.DateField(label="Date From ", initial=datetime.date(datetime.date.today().year, 1, 1).strftime('%Y-%m-%d'))
	date_to = forms.DateField(label="Date To ", initial=datetime.date.today().strftime('%Y-%m-%d'))
	company = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,)


class AccountsTrendForm(forms.Form):
	from .procedures import sp_accounts_types_get
	company = forms.ChoiceField(required=False)
	date_from = forms.DateField(initial=datetime.date(datetime.date.today().year-1, 1, 1).strftime('%Y-%m-%d'),
								label='Date From')
	date_to = forms.DateField(initial=datetime.date.today().strftime('%Y-%m-%d'), label='Date To')
	account_type_id = forms.ChoiceField(choices=sp_accounts_types_get())
	display_as = forms.ChoiceField(choices=time_range)
	chart_type = forms.ChoiceField(choices=chart_type)


class AccountsTrendDetailForm(forms.Form):
	from .procedures import sp_accounts_types_get
	company = forms.ChoiceField(required=False)
	date_from = forms.DateField(initial=datetime.date(datetime.date.today().year-1, 1, 1).strftime('%Y-%m-%d'),
								label='Date From')
	date_to = forms.DateField(initial=datetime.date.today().strftime('%Y-%m-%d'), label='Date To')
	account_type_id = forms.ChoiceField(choices=sp_accounts_types_get())
	account = forms.ChoiceField(required=False)
	display_as = forms.ChoiceField(choices=time_range)
	chart_type = forms.ChoiceField(choices=chart_type)
	""" 
	company = forms.MultipleChoiceField(
		required=False,
		widget=forms.CheckboxSelectMultiple,
	)
	"""

"""
class AccountsForm(forms.ModelForm):
	class Meta:
		model = Accounts
		fields = ['company', 'account_id', 'account_name', 'account_type_id', 'parent_id',
				  'currency_id', 'kind', 'active'
				  ]
"""


class MRGN_Revenues_ExpensesForm(forms.Form):
	company = forms.ChoiceField(required=False)
	date_from = forms.DateField(initial=datetime.date(datetime.date.today().year-1, 1, 1).strftime('%Y-%m-%d'),
								label='Date From')
	date_to = forms.DateField(initial=datetime.date.today().strftime('%Y-%m-%d'), label='Date To')
	display_as = forms.ChoiceField(choices=time_range)


class CostCenterTrendForm(forms.Form):
	from .procedures import sp_accounts_types_get

	company = forms.ChoiceField(required=False)
	date_from = forms.DateField(initial=datetime.date(datetime.date.today().year-1, 1, 1).strftime('%Y-%m-%d'),
								label='Date From')
	date_to = forms.DateField(initial=datetime.date.today().strftime('%Y-%m-%d'), label='Date To')
	account_type_id = forms.ChoiceField(choices=sp_accounts_types_get(1))
	display_as = forms.ChoiceField(choices=time_range)
	chart_type = forms.ChoiceField(choices=chart_type)


class BudgetViewForm(forms.Form):
	from .procedures import sp_budget_year, sp_accounts_types_get
	status = [
		['d', 'Draft'], ['s', 'Saved'], ['a', 'Approved']
	]
	company = forms.ChoiceField(required=False)
	year = forms.ChoiceField(choices=sp_budget_year, required=False)
	account_type_id = forms.ChoiceField(choices=sp_accounts_types_get(0), label='Account Type')
	status = forms.ChoiceField(choices=status, required=False, initial='a')


def NewForm(model_name, hide_id=None):
	from django.contrib.contenttypes.models import ContentType
	model_id = ContentType.objects.get(model=str(model_name))
	model_class = model_id.model_class()

	class form(forms.ModelForm):
		class Meta:
			model = model_class
			fields = '__all__'
			if hide_id is not None:
				widgets = {hide_id: forms.HiddenInput()}

	return form


class FormSearchAccounts(forms.ModelForm):

	class Meta:
		from .models import Accounts
		model = Accounts
		fields = ['company', 'account_type', 'parentid', 'active', 'kind']


def searchform(model_name, fields_lst, user_id, all_opco=False):
	from django.contrib.contenttypes.models import ContentType
	from .procedures import sp_companies_get
	model_id = ContentType.objects.get(model=str(model_name))
	model_class = model_id.model_class()

	class form(forms.ModelForm):

		class Meta:
			model = model_class
			fields = fields_lst

		def __init__(self, *args, **kwargs):
			super(form, self).__init__(*args, **kwargs)
			for key in self.fields:
				if self.fields[key].widget.input_type == 'checkbox':
					self.fields[key] = forms.NullBooleanField()
				if key != 'company':
					self.fields[key].required = False
				else:
					if all_opco:
						self.fields[key].required = False
					self.fields[key].choices = sp_companies_get(user_id, False)
			#self.fields['report_id'].widget = forms.HiddenInput()
	return form
