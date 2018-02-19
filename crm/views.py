from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.views import View
from analytics.procedures import *
from analytics.models import UsersCompanies, Accounts, Centers
import datetime
from analytics.procedures import fn_get_user_lang
from .utilities import *
from django.contrib.contenttypes.models import ContentType
from .forms import *
from django.shortcuts import get_object_or_404


class IndexView(View):
	template_name = 'crm/index.html'

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, {})

	def post(self, request, *args, **kwargs):
		return render(request, self.template_name, {})


class CustomersView(View):
	template_name = 'crm/customers.html'
	labels = {
		'en': {
			'classification': 'Classification',
			'address': 'Address',
			'location': 'Location',
			'contacts': 'Detail',
			'status_rate': 'Status & Rate',
			'event': 'Activities-Events'
		},
		'ar': {
			'classification': 'التصنيف',
			'address': 'العنوان',
			'location': 'الموقع',
			'contacts': 'التفاصيل',
			'status_rate': 'الحالة والتقييم',
			'event': 'التواصل والأنشطة'
		}
	}

	def get(self, request, pk_id, *args, **kwargs):
		pk_id = pk_id
		report_id = 'customers'
		lang = fn_get_user_lang(request.user.username)
		if not permission_check('crm', report_id, request.user, 'change'):
			return render(request, 'crm/error.html', {'err': "You don't have permission."})
		mdl_object = ModelClass(report_id, request.user.username)
		ds = get_object_or_404(mdl_object.model_class, pk=str(pk_id))
		frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
		form = frm(instance=ds)
		#  contacts

		mdl_object2 = ModelClass('customersdetails', request.user.username)
		qs = mdl_object2.model_class.objects.filter(customer=pk_id).order_by('-pk')
		ds = TableRowForm(
			queryset=qs, fields=mdl_object2.model_fields, model_name=mdl_object2.model_name,
			lang=mdl_object2.lang, record_url=mdl_object2.record_url, actions_count=len(mdl_object2.actions)
		)

		mdl_object3 = ModelClass('customersstatus', request.user.username)
		qs3 = mdl_object3.model_class.objects.filter(customer=pk_id).order_by('-pk')
		ds3 = TableRowForm(
			queryset=qs3, fields=mdl_object3.model_fields, model_name=mdl_object3.model_name,
			lang=mdl_object3.lang, record_url=mdl_object3.record_url, actions_count=len(mdl_object3.actions)
		)

		mdl_object4 = ModelClass('customersactivities', request.user.username)
		qs4 = mdl_object4.model_class.objects.filter(customer=pk_id).order_by('-pk')
		ds4 = TableRowForm(
			queryset=qs4, fields=mdl_object4.model_fields, model_name=mdl_object4.model_name,
			lang=mdl_object4.lang, record_url=mdl_object4.record_url, actions_count=len(mdl_object4.actions)
		)

		return render(request, self.template_name, {
			'form': form, 'model_name': mdl_object.model_name, 'hidden_fields': mdl_object.read_only_fields,
			'title': mdl_object.title, 'pk_id': pk_id, 'labels': self.labels[lang], 'ds': ds,
			'model_name2': mdl_object2.model_name, 'title2': mdl_object2.title,
			'actions': mdl_object2.actions,
			'model_name3': mdl_object3.model_name, 'title3': mdl_object3.title,
			'actions3': mdl_object3.actions, 'ds3': str(ds3).replace('dtbl', 'dtbl3').replace('slct_all', 'slct_all3'),
			'model_name4': mdl_object4.model_name, 'title4': mdl_object4.title,
			'actions4': mdl_object4.actions, 'ds4': str(ds4).replace('dtbl', 'dtbl4').replace('slct_all', 'slct_all4'),
		})

	def post(self, request, *args, **kwargs):
		lang = fn_get_user_lang(request.user.username)
		mdl_object = ModelClass(request.POST['model_name'], request.user.username)
		pk_id = request.POST['pk_id']
		if not permission_check('crm', mdl_object.model_name, request.user, 'change'):
			return render(request, 'crm/error.html', {'err': "You don't have permission."})
		ds = get_object_or_404(mdl_object.model_class, pk=pk_id)
		ds_data = request.POST
		ds_data._mutable = True
		if 'user' in [f[0] for f in mdl_object.all_fields] and 'user' in mdl_object.read_only_fields:
			ds_data['user'] = request.user.id
		frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
		form = frm(instance=ds, data=ds_data)
		if form.is_valid():
			try:
				form.save()
			except Exception as e:
				return render(request, 'crm/error.html', {'err': str(e)})
		else:
			return render(request, self.template_name, {
				'form': form, 'model_name': mdl_object.model_name, 'hidden_fields': mdl_object.read_only_fields,
				'title': mdl_object.title, 'pk_id': pk_id
			})

		ds = get_object_or_404(mdl_object.model_class, pk=str(pk_id))
		frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
		form = frm(instance=ds)

		mdl_object2 = ModelClass('customersdetails', request.user.username)
		qs = mdl_object2.model_class.objects.filter(customer=pk_id).order_by('-pk')
		ds = TableRowForm(
			queryset=qs, fields=mdl_object2.model_fields, model_name=mdl_object2.model_name,
			lang=mdl_object2.lang, record_url=mdl_object2.record_url, actions_count=len(mdl_object2.actions)
		)

		mdl_object3 = ModelClass('customersstatus', request.user.username)
		qs3 = mdl_object3.model_class.objects.filter(customer=pk_id).order_by('-pk')
		ds3 = TableRowForm(
			queryset=qs3, fields=mdl_object3.model_fields, model_name=mdl_object3.model_name,
			lang=mdl_object3.lang, record_url=mdl_object3.record_url, actions_count=len(mdl_object3.actions)
		)

		return render(request, self.template_name, {
			'form': form, 'model_name': mdl_object.model_name, 'hidden_fields': mdl_object.read_only_fields,
			'title': mdl_object.title, 'pk_id': pk_id, 'labels': self.labels[lang], 'ds': ds,
			'model_name2': mdl_object2.model_name, 'title2': mdl_object2.title,
			'actions': mdl_object2.actions,
			'model_name3': mdl_object3.model_name, 'title3': mdl_object3.title,
			'actions3': mdl_object3.actions, 'ds3': str(ds3).replace('dtbl', 'dtbl3').replace('slct_all', 'slct_all3'),

		})


def customer_detail_add(request, customer_id):
	mdl_object = ModelClass('customersdetails', request.user.username)
	frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
	form = frm(initial={'customer': customer_id, 'user': request.user})
	form.fields['company'].choices = sp_companies_get(request.user.id)
	context = {
		'customer_id': customer_id, 'form': form, 'hidden_fields': mdl_object.read_only_fields,
		'url': "{% url 'crm:model_record_save' %}", 'pk_id': ''
	}
	return render(request, 'crm/customers_details.html', context)


def customer_detail_update(request, pk_id):
	mdl_object = ModelClass('customersdetails', request.user.username)
	ds = get_object_or_404(mdl_object.model_class, pk=pk_id)
	if ds.company_id not in [i[0] for i in sp_companies_get(request.user.id, False)]:
		return render(request, 'crm/error.html', {'err': "You don't have permission to %s."% str(ds.company)})
	frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
	form = frm(instance=ds)
	form.fields['company'].choices = sp_companies_get(request.user.id)
	context = {
		'customer_id': ds.customer_id, 'form': form, 'hidden_fields': mdl_object.read_only_fields,
		'ur': "{% url 'crm:model_record_save' %}", 'pk_id': pk_id
	}
	return render(request, 'crm/customers_details.html', context)


def customer_detail_delete(request):
	if request.POST:
		selections = eval(request.POST['selected_records'])
		action = request.POST['action']
		if action == 'delete':
			if not permission_check('crm', 'customersdetails', request.user, 'delete'):
				return render(request, 'crm/error.html', {'err': "You don't have permission."})
			try:
				mdl_object = ModelClass('customersdetails', request.user.username)
				companies = sp_companies_get(request.user.id, False)
				companies_lst = [i[0] for i in companies]
				model_delete(mdl_object, list(selections), companies_lst)
			except Exception as e:
				return render(request, 'analytics/error.html', {'err': str(e)})

		return HttpResponseRedirect('/crm/customers/' + str(request.POST['customer_id']) + '/')


def customer_detail_save(request):
	if request.POST:
		customer_id = request.POST['customer']
		pk_id = request.POST['pk_id']
		mdl_object = ModelClass('customersdetails', request.user.username)
		if not permission_check('crm', mdl_object.model_name, request.user, 'change'):
			return render(request, 'crm/error.html', {'err': "You don't have permission."})
		ds_data = request.POST
		ds_data._mutable = True
		ds_data['user'] = request.user.id
		frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
		if pk_id:
			qs = get_object_or_404(mdl_object.model_class, pk=pk_id)
			form = frm(instance=qs, data=ds_data)
		else:
			form = frm(data=ds_data)
		if form.is_valid():
			try:
				form.save()
			except Exception as e:
				return render(request, 'crm/error.html', {'err': e})
		else:
			if 'company' in [f[0] for f in mdl_object.all_fields]:
				form.fields['company'].choices = sp_companies_get(request.user.id, False)
			context = {'customer_id': customer_id, 'form': form, 'hidden_fields': mdl_object.read_only_fields}
			return render(request, 'crm/customers_details.html', context)

		return HttpResponseRedirect('/crm/customers/' + str(customer_id) + '/')


def customer_status_rate_add(request, customer_id):
	mdl_object = ModelClass('customersstatus', request.user.username)
	frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
	form = frm(initial={'customer': customer_id, 'user': request.user})
	form.fields['rate'].required = True
	form.fields['company'].choices = sp_companies_get(request.user.id)
	context = {
		'customer_id': customer_id, 'form': form, 'hidden_fields': mdl_object.read_only_fields,
		'url': "{% url 'crm:model_record_save' %}", 'pk_id': ''
	}
	return render(request, 'crm/customers_status_rate.html', context)


def customer_status_rate_update(request, pk_id):
	mdl_object = ModelClass('customersstatus', request.user.username)
	ds = get_object_or_404(mdl_object.model_class, pk=pk_id)
	if ds.company_id not in [i[0] for i in sp_companies_get(request.user.id, False)]:
		return render(request, 'crm/error.html', {'err': "You don't have permission to %s."% str(ds.company)})
	frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
	form = frm(instance=ds)
	form.fields['rate'].required = True
	form.fields['company'].choices = sp_companies_get(request.user.id)
	context = {
		'customer_id': ds.customer_id, 'form': form, 'hidden_fields': mdl_object.read_only_fields,
		'ur': "{% url 'crm:model_record_save' %}", 'pk_id': pk_id
	}
	return render(request, 'crm/customers_status_rate.html', context)


def customer_status_rate_save(request):
	if request.POST:
		customer_id = request.POST['customer']
		pk_id = request.POST['pk_id']
		mdl_object = ModelClass('customersstatus', request.user.username)
		if not permission_check('crm', mdl_object.model_name, request.user, 'change'):
			return render(request, 'crm/error.html', {'err': "You don't have permission."})
		ds_data = request.POST
		if ds_data['rate'] is None:
			return render(request, 'crm/error.html', {'err': "Please, add customer rate."})
		ds_data._mutable = True
		ds_data['user'] = request.user.id
		frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
		if pk_id:
			qs = get_object_or_404(mdl_object.model_class, pk=pk_id)
			form = frm(instance=qs, data=ds_data)
		else:
			form = frm(data=ds_data)
		if form.is_valid():
			try:
				form.save()
			except Exception as e:
				return render(request, 'crm/error.html', {'err': e})
		else:
			if 'company' in [f[0] for f in mdl_object.all_fields]:
				form.fields['company'].choices = sp_companies_get(request.user.id, False)
			context = {'customer_id': customer_id, 'form': form, 'hidden_fields': mdl_object.read_only_fields}
			return render(request, 'crm/customers_status_rate.html', context)

		return HttpResponseRedirect('/crm/customers/' + str(customer_id) + '/')


def customer_status_rate_delete(request):
	if request.POST:
		selections = eval(request.POST['selected_records'])
		action = request.POST['action']
		if action == 'delete':
			if not permission_check('crm', 'customersstatus', request.user, 'delete'):
				return render(request, 'crm/error.html', {'err': "You don't have permission."})
			try:
				mdl_object = ModelClass('customersstatus', request.user.username)
				companies = sp_companies_get(request.user.id, False)
				companies_lst = [i[0] for i in companies]
				model_delete(mdl_object, list(selections), companies_lst)
			except Exception as e:
				return render(request, 'analytics/error.html', {'err': str(e)})

		return HttpResponseRedirect('/crm/customers/' + str(request.POST['customer_id']) + '/')


def model_object(request, report_id):
	report_id = report_id
	mdl_object = ModelClass(report_id, request.user.username)
	if report_id is not None:
		form = searchform(
			model_name=mdl_object.model_name, fields_lst=mdl_object.search_fields, user_id=request.user.id,
			all_opco=False
		)
		frm = form()
		context = {
			'model_name': mdl_object.model_name.upper(), 'frm': frm, 'report_id': report_id,
			'title': mdl_object.model_name.title
		}
		return render(request, 'crm/form_view_model.html', context)
	else:
		return render(request, 'analytics/error.html', {'err': 'There is no selected report! please, check.'})


class ModelView(View):
	template_name = 'crm/form_view_model.html'

	def get(self, request, report_id, *args, **kwargs):
		report_id = report_id
		if not permission_check('crm', report_id, request.user, 'change'):
			return render(request, 'crm/error.html', {'err': "You don't have permission."})
		mdl_object = ModelClass(report_id, request.user.username)
		if report_id is not None:
			form = searchform(
				model_name=mdl_object.model_name, fields_lst=mdl_object.search_fields, user_id=request.user.id, all_opco=True
			)
			frm = form()
			search_lst = dict()
			if 'company' in [f[0] for f in mdl_object.all_fields]:
				frm.fields['company'].choices = sp_companies_get(request.user.id)
				if str(frm.fields['company'].choices[0][0]) != '0':
					search_lst['company__exact'] = str(frm.fields['company'].choices[0][0])
			if 'account' in [f[0] for f in mdl_object.all_fields]:
				companies = UsersCompanies.objects.filter(user=request.user.id)
				frm.fields['account'].queryset = Accounts.objects.filter(
					kind=False, active=True, company__in=[obj.company for obj in companies])
			if 'center' in [f[0] for f in mdl_object.all_fields]:
				companies = UsersCompanies.objects.filter(user=request.user.id)
				frm.fields['center'].queryset = Centers.objects.filter(
					kind=False, active=True, company__in=[obj.company for obj in companies]).exclude(center_id='0')
			# print(search_lst)
			qs = mdl_object.model_class.objects.filter(**search_lst).order_by('-pk')[:50]
			ds = TableRowForm(
				queryset=qs, fields=mdl_object.model_fields, model_name=mdl_object.model_name,
				lang=mdl_object.lang, record_url=mdl_object.record_url, actions_count=len(mdl_object.actions)
			)
			context = {
				'ds': ds, 'model_name': mdl_object.model_name.upper(), 'frm': frm, 'report_id': report_id,
				'title': mdl_object.title, 'actions': mdl_object.actions, 'can_add_new': mdl_object.can_add_new
			}
			return render(request, self.template_name, context)
		else:
			return render(request, 'crm/error.html', {'err': 'There is no selected report! please, check.'})

	def post(self, request, *args, **kwargs):
		report_id = request.POST['report_id']
		mdl_object = ModelClass(report_id, request.user.username)
		if report_id is not None:
			# Actions ------------------------------------------------------
			if request.POST['selected_records'] and request.POST['action']:
				selections = eval(request.POST['selected_records'])
				action = request.POST['action']
				if action == 'delete':
					try:
						if not permission_check('crm', report_id, request.user, 'delete'):
							return render(request, 'crm/error.html', {'err': "You don't have permission."})
						if 'company' in [f[0] for f in mdl_object.all_fields]:
							model_delete(mdl_object, list(selections), [i[0] for i in sp_companies_get(request.user.id, False)])
						else:
							model_delete(mdl_object, list(selections))
					except Exception as e:
						return render(request, 'crm/error.html', {'err': str(e)})
				elif action == 'event':
					if not request.user.groups.filter(name=mdl_object.model_name + '_' + action).exists():
						return render(
							request, 'crm/error.html', {'err': "You don't have permission to  %s" % str(' ' + mdl_object.model_name + '_' + action)}
						)
					return customers_event_add(request, selections)
				elif action == 'opportunity':
					if not request.user.groups.filter(name=mdl_object.model_name + '_' + action).exists():
						return render(
							request, 'crm/error.html', {'err': "You don't have permission to  %s" % str(' ' + mdl_object.model_name + '_' + action)}
						)
					return opportunity_add(request, selections)
				elif action == 'budget':
					if not request.user.groups.filter(name=mdl_object.model_name + '_' + action).exists():
						return render(
							request, 'crm/error.html', {'err': "You don't have permission to  %s" % str(' ' + mdl_object.model_name + '_' + action)}
						)
					return customer_budget_add(request, selections)
				else:
					if not request.user.groups.filter(name=mdl_object.model_name + '_' + action).exists():
						return render(request, 'crm/error.html', {'err': "You don't have permission to  %s" % str(' ' + mdl_object.model_name + '_' + action)})
					if 'company' in [f[0] for f in mdl_object.all_fields]:
						model_update(
							mdl_object.model_name, list(selections), mdl_object.action_status_from(action),
							mdl_object.action_status_to(action), [i[0] for i in sp_companies_get(request.user.id, False)]
						)
					else:
						model_update(
							mdl_object.model_name, list(selections), mdl_object.action_status_from(action),
							mdl_object.action_status_to(action)
						)
			# END of Actions ------------------------------------------------
			form = searchform(
				model_name=mdl_object.model_name, fields_lst=mdl_object.search_fields, user_id=request.user.id, all_opco=True
			)
			frm = form(request.POST)
			search_lst = search_form_criteria(mdl_object, frm, report_id)
			qs = mdl_object.model_class.objects.filter(**search_lst).order_by('-pk')
			ds = TableRowForm(
				queryset=qs, fields=mdl_object.model_fields, model_name=mdl_object.model_name,
				lang=mdl_object.lang, record_url=mdl_object.record_url, actions_count=len(mdl_object.actions)
			)
			context = {
				'ds': ds, 'model_name': mdl_object.model_name.upper(), 'frm': frm, 'report_id': report_id,
				'title': mdl_object.title, 'actions': mdl_object.actions, 'can_add_new': mdl_object.can_add_new
			}
			return render(request, self.template_name, context)
		else:
			return render(request, 'crm/error.html', {'err': 'There is no model been chosen!.'})


class ModelRecordView(View):
	template_name = 'crm/form_view_record.html'

	def get(self, request, report_id, pk_id, *args, **kwargs):
		pk_id = pk_id
		report_id = report_id
		mdl_object = ModelClass(report_id, request.user.username)
		ds = get_object_or_404(mdl_object.model_class, pk=str(pk_id))
		frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
		form = frm(instance=ds)

		return render(request, self.template_name, {
			'form': form, 'model_name': mdl_object.model_name, 'hidden_fields': mdl_object.read_only_fields,
			'title': mdl_object.title, 'pk_id': pk_id
		})

	def post(self, request, *args, **kwargs):
		mdl_object = ModelClass(request.POST['model_name'], request.user.username)
		pk_id = request.POST['pk_id']
		ds = get_object_or_404(mdl_object.model_class, pk=pk_id)
		if 'company' in [f[0] for f in mdl_object.all_fields]:
			if ds.company_id not in [i[0] for i in sp_companies_get(request.user.id, False)]:
				return render(request, 'crm/error.html', {'err': "You don't have permission to %s." % str(ds.company)})
		ds_data = request.POST
		ds_data._mutable = True
		if 'user' in [f[0] for f in mdl_object.all_fields] and 'user' in mdl_object.read_only_fields:
			ds_data['user'] = request.user.id
		frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
		form = frm(instance=ds, data=ds_data)
		if form.is_valid():
			try:
				form.save()
			except Exception as e:
				return render(request, 'analytics/error.html', {'err': str(e)})
		else:
			if 'company' in [f[0] for f in mdl_object.all_fields]:
				form.fields['company'].choices = sp_companies_get(request.user.id)
			if 'account' in [f[0] for f in mdl_object.all_fields]:
				companies = UsersCompanies.objects.filter(user=request.user.id)
				form.fields['account'].queryset = Accounts.objects.filter(
					kind=False, active=True, company__in=[obj.company for obj in companies])
			if 'center' in [f[0] for f in mdl_object.all_fields]:
				companies = UsersCompanies.objects.filter(user=request.user.id)
				form.fields['center'].queryset = Centers.objects.filter(
					kind=False, active=True, company__in=[obj.company for obj in companies]).exclude(center_id='0')
			return render(request, self.template_name, {
				'form': form, 'model_name': mdl_object.model_name, 'hidden_fields': mdl_object.read_only_fields,
				'title': mdl_object.title, 'pk_id': pk_id
			})
		return HttpResponseRedirect('/crm/model_view/' + str(mdl_object.model_name) + '/')


def model_record_delete(request, report_id, pk_id):
	pk_id = pk_id
	report_id = report_id
	if not permission_check('crm', report_id, request.user, 'delete'):
		return render(request, 'crm/error.html', {'err': "You don't have permission."})
	mdl_object = ModelClass(report_id, request.user.username)
	ds = get_object_or_404(mdl_object.model_class, pk=str(pk_id))
	try:
		ds.delete()
	except Exception as e:
		return render(request, 'analytics/error.html', {'err': str(e)})
	return HttpResponseRedirect('/crm/model_view/' + str(mdl_object.model_name) + '/')


def model_record_add(request, report_id, *args, **kwargs):
	template_name = 'crm/form_record_add.html'
	report_id = report_id
	if not permission_check('crm', report_id, request.user, 'add'):
		return render(request, 'crm/error.html', {'err': "You don't have permission."})
	mdl_object = ModelClass(report_id, request.user.username)
	if not mdl_object.can_add_new:
		return render(request, 'crm/error.html', {'err': "Can not add to this %s Model."% str(mdl_object.model_name)})
	frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
	form = frm()
	print(form)

	return render(request, template_name, {
		'form': form, 'model_name': mdl_object.model_name, 'hidden_fields': mdl_object.read_only_fields,
		'title': mdl_object.title, 'report_id': report_id
	})


def model_record_save(request):
	template_name = 'crm/form_view_record.html'
	if request.POST:
		mdl_object = ModelClass(request.POST['model_name'], request.user.username)
		if not permission_check('crm', mdl_object.model_name, request.user, 'change'):
			return render(request, 'crm/error.html', {'err': "You don't have permission."})
		ds_data = request.POST
		ds_data._mutable = True
		frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
		form = frm(data=ds_data)
		if 'user' in list([f[0] for f in mdl_object.all_fields]):
			form.data['user'] = request.user.id
		if form.is_valid():
			try:
				new_record = form.save()
			except Exception as e:
				return render(request, 'crm/error.html', {'err': str(e)})
		else:
			if 'company' in [f[0] for f in mdl_object.all_fields]:
				form.fields['company'].choices = sp_companies_get(request.user.id, False)
			return render(request, template_name, {
				'form': form, 'model_name': mdl_object.model_name, 'hidden_fields': mdl_object.read_only_fields,
				'title': mdl_object.title, 'pk_id': ''
			})
		return HttpResponseRedirect('/crm/model_view/' + str(mdl_object.model_name) + '/')


def customers_event_add(request, customers):
	customers = list(customers)
	if len(list(customers)) > 0:
		mdl_object = ModelClass('customersactivities', request.user.username)
		qs = Customers.objects.filter(pk__in=list(customers))
		frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
		form = frm()
		form.fields['company'].choices = sp_companies_get(request.user.id)
		del form.fields["customer"]
		#form.fields['customer'].widget = forms.HiddenInput()
		context = {
			'customers': customers, 'form': form, 'hidden_fields': mdl_object.read_only_fields + ['status'],
			'url': "{% url 'crm:model_record_save' %}", 'title': mdl_object.title, 'qs': qs
		}
		return render(request, 'crm/customers_event.html', context)


def customers_event_update(request, pk_id):
	mdl_object = ModelClass('customersactivities', request.user.username)
	ds = get_object_or_404(mdl_object.model_class, pk=pk_id)
	customers = [ds.customer_id]
	qs = Customers.objects.filter(pk__in=list(customers))
	if ds.status == 'c':
		mdl_object_actions = ModelClass('customersactivitiesactions', request.user.username)
		qs_action = CustomersActivitiesActions.objects.filter(activity_id=ds.activity_id)
		ds_actions = TableRowForm(
			queryset=qs_action, fields=mdl_object_actions.model_fields, model_name=mdl_object_actions.model_name,
			lang=mdl_object_actions.lang, record_url=mdl_object_actions.record_url, actions_count=len(mdl_object_actions.actions)
		)
	else:
		ds_actions = ''
	if ds.company_id not in [i[0] for i in sp_companies_get(request.user.id, False)]:
		return render(request, 'crm/error.html', {'err': "You don't have permission to %s." % str(ds.company)})
	frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
	form = frm(instance=ds)
	del form.fields["customer"]
	form.fields['company'].choices = sp_companies_get(request.user.id)
	context = {
		'customers': customers, 'form': form, 'hidden_fields': mdl_object.read_only_fields + ['status'],
		'url': "{% url 'crm:model_record_save' %}", 'title': mdl_object.title, 'qs': qs, 'pk_id': pk_id,
		'ds_actions': ds_actions
	}
	return render(request, 'crm/customers_event.html', context)


def customers_event_save(request):
	if request.POST:
		customers = list(eval(request.POST['customers']))
		pk_id = request.POST['pk_id']
		mdl_object = ModelClass('customersactivities', request.user.username)
		ds_data = request.POST
		ds_data._mutable = True
		frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
		for i in list(customers):
			ds_data['customer'] = i
			ds_data['user'] = request.user.id
			if pk_id:
				qs = get_object_or_404(mdl_object.model_class, pk=pk_id)
				form = frm(instance=qs, data=ds_data)
			else:
				form = frm(data=ds_data)
			try:
				if form.is_valid():
					form.save()
			except Exception as e:
				return render(request, 'crm/error.html', {'err': e})
		if len(list(customers)) > 1:
			return HttpResponseRedirect('/crm/model_view/customersactivities/')
		elif len(list(customers)) == 1:
			return HttpResponseRedirect('/crm/customers/%s/' % customers[0])


class CustomersActivityView(View):
	template_name = 'crm/activities_calendar.html'
	labels = {
		'en': {
			'from_date': 'Date From',
			'to_date': 'Date To'
		},
		'ar': {
			'from_date': 'التاريخ من',
			'to_date': 'التاريخ إلى'
		}
	}

	def get(self, request):
		if not permission_check('crm', 'customersactivities', request.user, 'change'):
			return render(request, 'crm/error.html', {'err': "You don't have permission."})
		import calendar
		lang = fn_get_user_lang(request.user.username)
		date_from = datetime.datetime(
			datetime.datetime.today().year,	datetime.datetime.today().month, 1
		).strftime('%Y-%m-%d')
		date_to = datetime.datetime(
			datetime.datetime.today().year,	datetime.datetime.today().month,
			calendar.monthrange(datetime.datetime.today().year, datetime.datetime.today().month)[1]
		).strftime('%Y-%m-%d')
		companies = UsersCompanies.objects.filter(user_id=request.user.id)
		customers_events = CustomersActivities.objects.filter(
			activity_date__range=(date_from, date_to), company__in=[obj.company for obj in companies]
		)
		events = list()
		for obj in customers_events:
			events.append(
				[
					str(obj.activity_type) + ':' + obj.subject + ':' + str(obj.customer) + ':'
					+ str(obj.sale_agent) + ':' + obj.current_status,
					obj.activity_date, obj.activity_date, obj.activity_id, obj.current_status
				])
		context = {
			'date_from': date_from, 'date_to': date_to, 'labels': self.labels[lang], 'events': events
		}
		return render(request, self.template_name, context)

	def post(self, request):
		if not permission_check('crm', 'customersactivities', request.user, 'change'):
			return render(request, 'crm/error.html', {'err': "You don't have permission."})
		lang = fn_get_user_lang(request.user.username)
		date_from = request.POST['date_from']
		date_to = request.POST['date_to']
		companies = UsersCompanies.objects.filter(user_id=request.user.id)
		customers_events = CustomersActivities.objects.filter(
			activity_date__range=(date_from, date_to), company__in=[obj.company for obj in companies]
		)
		events = list()
		for obj in customers_events:
			events.append(
				[
					str(obj.activity_type) + ':' + obj.subject + ':' + str(obj.customer) + ':'
					+ str(obj.sale_agent) + ':' + obj.current_status,
					obj.activity_date, obj.activity_date, obj.activity_id, obj.current_status
				]
			)
		context = {
			'date_from': date_from, 'date_to': date_to, 'labels': self.labels[lang], 'events': events
		}
		return render(request, self.template_name, context)


def customers_event_actions_add(request, activity_id):
	mdl_object = ModelClass('customersactivitiesactions', request.user.username)
	if not CustomersActivities.objects.filter(pk=activity_id).exists():
		return render(request, 'crm/error.html', {'err': "This activity %s is not exist." % str(activity_id)})
	frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
	form = frm()
	del form.fields["activity_id"]
	context = {
		'activity_id': activity_id, 'form': form, 'hidden_fields': mdl_object.read_only_fields,
		'title': mdl_object.title
	}
	return render(request, 'crm/customers_activity_actions.html', context)


def customers_event_actions_save(request):
	if request.POST:
		mdl_object = ModelClass('customersactivitiesactions', request.user.username)
		ds_data = request.POST
		ds_data._mutable = True
		frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
		ds_data['user'] = request.user.id
		if not ds_data['actions']:
			ds_data['actions_date'] = ''
		ds_data['activity_id'] = int(ds_data['activity_id'])
		ds_data['status'] = 'c'
		form = frm(data=ds_data)
		try:
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/crm/customers_event_update/%s/' % str(ds_data['activity_id']))
			else:
				context = {
					'activity_id': ds_data['activity_id'], 'form': form, 'hidden_fields': mdl_object.read_only_fields,
					'title': mdl_object.title
				}
				return render(request, 'crm/customers_activity_actions.html', context)
		except Exception as e:
			return render(request, 'crm/error.html', {'err': e})


def customers_event_actions_view(request, pk_id):
	mdl_object = ModelClass('customersactivitiesactions', request.user.username)
	ds = get_object_or_404(mdl_object.model_class, pk=pk_id)

	mdl_object_activities = ModelClass('customersactivities', request.user.username)
	ds_mdl_object_activities = get_object_or_404(mdl_object_activities.model_class, pk=ds.activity_id.pk)

	if ds_mdl_object_activities.company_id not in [i[0] for i in sp_companies_get(request.user.id, False)]:
		return render(request, 'crm/error.html', {'err': "You don't have permission to %s." % str(ds_mdl_object_activities.company)})
	frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
	form = frm(instance=ds)
	context = {
		'activity_id': ds.activity_id.pk, 'form': form, 'hidden_fields': mdl_object.read_only_fields,
		'title': mdl_object.title
	}
	return render(request, 'crm/customers_activity_actions.html', context)


def test(request):
	mdl_object = ModelClass('customersactivitiesactions', request.user.username)
	frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
	form = frm()
	if request.POST:
		form = frm(data=request.POST)
	return render(request, 'crm/test.html', {'form': form})


def opportunity_add(request, customer):
	if len(list(customer)) > 1:
		return render(request, 'crm/error.html', {'err': "Please, select a single customer."})
	elif len(list(customer)) == 1:
		qs = get_object_or_404(Customers, pk=list(customer)[0])
		mdl_object = ModelClass('opportunities', request.user.username)
		frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
		form = frm()
		del form.fields["customer"]
		del form.fields["missed_notes"]
		del form.fields["missed_reason"]
		context = {
			'customer': qs.pk, 'form': form, 'hidden_fields': mdl_object.read_only_fields + ['status'],
			'title': mdl_object.title, 'customer_name': qs.customer_name
		}
		return render(request, 'crm/opportunity.html', context)
	else:
		return HttpResponseRedirect('/crm/model_view/customers/')


def opportunity_save(request):
	if request.POST:
		ds_data = request.POST
		pk_id = request.POST['pk_id']
		ds_data._mutable = True
		mdl_object = ModelClass('opportunities', request.user.username)
		frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
		ds_data['user'] = request.user.id
		if pk_id:
			qs = get_object_or_404(mdl_object.model_class, pk=pk_id)
			form = frm(instance=qs, data=ds_data)
		else:
			ds_data['status'] = 'o'
			form = frm(data=ds_data)
		try:
			print(form.errors)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/crm/model_view/opportunities/')
			else:
				context = {
					'customer': ds_data.pk, 'form': form, 'hidden_fields': mdl_object.read_only_fields,
					'title': mdl_object.title, 'customer_name': ds_data.customer_name, 'pk_id': pk_id
				}
				return render(request, 'crm/opportunity.html', context)

		except Exception as e:
			return render(request, 'crm/error.html', {'err': e})


def opportunity_update(request, pk_id):
	mdl_object = ModelClass('opportunities', request.user.username)
	ds = get_object_or_404(mdl_object.model_class, pk=pk_id)
	frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
	qs = get_object_or_404(Customers, pk=ds.customer_id)
	form = frm(instance=ds)
	del form.fields["customer"]
	form.fields["status"].required = True
	context = {
		'customer': qs.pk, 'form': form, 'hidden_fields': mdl_object.read_only_fields,
		'title': mdl_object.title, 'customer_name': qs.customer_name, 'pk_id': pk_id
	}
	return render(request, 'crm/opportunity.html', context)


class OpportunitiesCalendarView(View):
	template_name = 'crm/opportunities_calendar.html'
	labels = {
		'en': {
			'from_date': 'Date From',
			'to_date': 'Date To'
		},
		'ar': {
			'from_date': 'التاريخ من',
			'to_date': 'التاريخ إلى'
		}
	}

	def get(self, request):
		if not permission_check('crm', 'opportunities', request.user, 'change'):
			return render(request, 'crm/error.html', {'err': "You don't have permission."})
		import calendar
		lang = fn_get_user_lang(request.user.username)
		date_from = datetime.datetime(
			datetime.datetime.today().year,	datetime.datetime.today().month, 1
		).strftime('%Y-%m-%d')
		date_to = datetime.datetime(
			datetime.datetime.today().year,	datetime.datetime.today().month,
			calendar.monthrange(datetime.datetime.today().year, datetime.datetime.today().month)[1]
		).strftime('%Y-%m-%d')
		companies = UsersCompanies.objects.filter(user_id=request.user.id)
		customers_events = Opportunities.objects.filter(
			opportunity_date__range=(date_from, date_to), company__in=[obj.company for obj in companies]
		)
		events = list()
		for obj in customers_events:
			events.append(
				[
					str(obj.description) + ':' + str(obj.customer) + ':' + obj.current_status,
					obj.opportunity_date, obj.opportunity_date, obj.pk, obj.current_status
				])
		context = {
			'date_from': date_from, 'date_to': date_to, 'labels': self.labels[lang], 'events': events
		}
		return render(request, self.template_name, context)

	def post(self, request):
		if not permission_check('crm', 'opportunities', request.user, 'change'):
			return render(request, 'crm/error.html', {'err': "You don't have permission."})
		lang = fn_get_user_lang(request.user.username)
		date_from = request.POST['date_from']
		date_to = request.POST['date_to']
		companies = UsersCompanies.objects.filter(user_id=request.user.id)
		customers_events = Opportunities.objects.filter(
			opportunity_date__range=(date_from, date_to), company__in=[obj.company for obj in companies]
		)
		events = list()
		for obj in customers_events:
			events.append(
				[
					str(obj.description) + ':' + str(obj.customer) + ':' + obj.current_status,
					obj.opportunity_date, obj.opportunity_date, obj.pk, obj.current_status
				]
			)
		context = {
			'date_from': date_from, 'date_to': date_to, 'labels': self.labels[lang], 'events': events
		}
		return render(request, self.template_name, context)


def customer_budget_add(request, customer):
	if len(list(customer)) > 1:
		return render(request, 'crm/error.html', {'err': "Please, select a single customer."})
	elif len(list(customer)) == 1:
		qs = get_object_or_404(Customers, pk=list(customer)[0])
		mdl_object = ModelClass('customersbudget', request.user.username)
		qs = get_object_or_404(Customers, pk=list(customer)[0])
		frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
		form = frm()
		form.fields['company'].choices = sp_companies_get(request.user.id)
		del form.fields["customer"]
		context = {
			'customer': qs.pk, 'form': form, 'hidden_fields': mdl_object.read_only_fields,
			'title': mdl_object.title, 'customer_name': qs.customer_name
		}
		return render(request, 'crm/customers_budget.html', context)
	else:
		return HttpResponseRedirect('/crm/model_view/customers/')


def customer_budget_save(request):
	if request.POST:
		ds_data = request.POST
		pk_id = request.POST['pk_id']
		ds_data._mutable = True
		qs = get_object_or_404(Customers, pk=request.POST['customer'])
		mdl_object = ModelClass('customersbudget', request.user.username)
		frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
		ds_data['user'] = request.user.id
		if pk_id:
			qs = get_object_or_404(mdl_object.model_class, pk=pk_id)
			form = frm(instance=qs, data=ds_data)
		else:
			ds_data['status'] = 'd'
			form = frm(data=ds_data)
		try:
			print(form.errors)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/crm/model_view/customersbudget/')
			else:
				context = {
					'customer': qs.pk, 'form': form, 'hidden_fields': mdl_object.read_only_fields,
					'title': mdl_object.title, 'customer_name': qs.customer_name, 'pk_id': pk_id
				}
				return render(request, 'crm/customers_budget.html', context)

		except Exception as e:
			return render(request, 'crm/error.html', {'err': e})


def customer_budget_update(request, pk_id):
	mdl_object = ModelClass('customersbudget', request.user.username)
	ds = get_object_or_404(mdl_object.model_class, pk=pk_id)
	frm = NewForm(mdl_object.model_name, mdl_object.all_fields, request.user.id)
	qs = get_object_or_404(Customers, pk=ds.customer_id)
	form = frm(instance=ds)
	del form.fields["customer"]
	form.fields["status"].required = True
	context = {
		'customer': qs.pk, 'form': form, 'hidden_fields': mdl_object.read_only_fields,
		'title': mdl_object.title, 'customer_name': qs.customer_name, 'pk_id': pk_id
	}
	return render(request, 'crm/customers_budget.html', context)
