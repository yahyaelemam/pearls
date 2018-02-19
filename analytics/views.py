from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .utilities import Chart_color, TableRowForm, TableRowForm_ds, reports, search_form_criteria
from .procedures import *
from .forms import LoginForm, searchform, NewForm
import datetime
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType


class LoginView(View):
	template_name = 'analytics/login.html'

	def get(self, request, *args, **kwargs):
		logout(request)
		return render(request, self.template_name, {'next': request.GET.get('next', ''), 'login_form': LoginForm()})

	def post(self, request, *args, **kwargs):
		form = LoginForm(request.POST)
		if form.is_valid():
			user_name = str(form.cleaned_data['username'])
			pass_word = str(form.cleaned_data['password'])
			next_page = request.POST['next']
			print(next_page)
			user = authenticate(username=user_name, password=pass_word)
			if user is not None:
				login(request, user)
				if len(next_page) > 0:
					return HttpResponseRedirect(next_page)
				else:
					return HttpResponseRedirect('/')
			else:
				return render(request, self.template_name, {'login_form': form})
		else:
			return render(request, self.template_name, {'login_form': form})


def logout_view(request):
	logout(request)


class IndexView(View):

	@method_decorator(login_required)
	@method_decorator(permission_required('analytics.landing_page', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(IndexView, self).dispatch(*args, **kwargs)

	template_name = 'analytics/index.html'

	labels = {
		'en': {
			'operational_profit': 'Operational Profit',
			'ebitda': 'EBITDA',
			'ebit': 'EBIT',
			'net_profit': 'Net Profit',
			'revenue': 'Revenue',
			'cost': 'Expense',

		},
		'ar': {
			'operational_profit': 'الأرباح التشغيلية',
			'ebitda': 'الدخل قبل الخصومات',
			'ebit': 'الدخل قبل الضريبة والزكاة',
			'net_profit': 'صافي الأرباح',
			'revenue': 'الإيرادات',
			'cost': 'المصروفات',

		}
	}

	def get(self, request, *args, **kwargs):
		lang = fn_get_user_lang(request.user.username)
		if int(datetime.date.today().month) == 1:
			date_from = datetime.date(datetime.date.today().year-1, 1, 1)
			date_to = datetime.date(datetime.date.today().year-1, 12, 31)
		else:
			date_from = datetime.date(datetime.date.today().year, 1, 1)
			date_to = datetime.datetime.now()
		companies = sp_companies_get(request.user.id, False)
		if len(companies) == 0:
			return render(request, 'analytics/error.html', {
				'err': 'There is no company a signed to (%s) user.' % request.user.username}
						)
		opco_lst = [[c[0], c[1], 'checked'] for c in companies]
		try:
			kpi_total_ds, kpi_ds = sp_companies_kpi(
				companies, str(date_from.strftime('%Y-%m-%d')), str(date_to.strftime('%Y-%m-%d'))
			)

			mrg_ds = sp_mrgn_revenues_vs_expenses(
				companies=companies, date_from=date_from, date_to=date_to, display_as='m', user_id=request.user.id
			)

			ebitda_trend = ''# sp_ebitda_trend(companies, date_from, date_to)
		except ZeroDivisionError:
			return render(request, 'analytics/error.html', {'err': 'Please, select proper dates.'})

		context = {
			'mrg_ds': mrg_ds, 'date_from': date_from.strftime('%Y/%m/%d'), 'date_to': date_to.strftime('%Y/%m/%d'),
			'companies': opco_lst, 'kpi_total_ds': kpi_total_ds, 'kpi_ds': kpi_ds, 'view_mode': 0, 'ebitda_trend': ebitda_trend,
			'labels': self.labels[lang]
		}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		lang = fn_get_user_lang(request.user.username)
		view_mode = str(request.POST['view_mode'])
		dates = str(request.POST['daterange']).replace(' ', '').split('-')
		date_from = datetime.datetime.strptime(str(dates[0]), '%Y/%m/%d')
		date_to = datetime.datetime.strptime(str(dates[1]), '%Y/%m/%d')
		if date_from > date_to:
			return render(request, 'analytics/error.html', {'err': 'Date To is not correct please check again.'})
		companies = request.POST.getlist('company')
		if len(companies) <= 0:
			return render(request, 'analytics/error.html', {'err': 'Please, select a company to display its KPI.'})
		opcos = sp_companies_get(request.user.id, False)
		comp_lst = list()
		indc = 0
		for c in opcos:
			for i in companies:
				if str(c[0]) == str(i):
					indc = 1
					break
			if indc == 1:
				comp_lst.append([c[0], c[1], 'checked'])
				indc = 0
			else:
				comp_lst.append([c[0], c[1], ''])
		if len([[c[0], c[1]] for c in comp_lst if c[2] == 'checked']) > 0:
			try:
				kpi_total_ds, kpi_ds = sp_companies_kpi(
					[[c[0], c[1]] for c in comp_lst if c[2] == 'checked'], str(date_from.strftime('%Y-%m-%d')),
					str(date_to.strftime('%Y-%m-%d'))
				)

				mrg_ds = sp_mrgn_revenues_vs_expenses(
					companies=[str(c[0]) for c in comp_lst if c[2] == 'checked'], date_from=date_from,
					date_to=date_to, display_as='m', user_id=request.user.id
				)

				ebitda_trend = ''# sp_ebitda_trend(companies, date_from, date_to)
			except Exception as e:
				return render(request, 'analytics/error.html', {'err': str(e)})
		else:
			ds, total_lst, mrg_ds = [], [], []

		context = {
			'mrg_ds': mrg_ds, 'date_from': date_from.strftime('%Y/%m/%d'), 'date_to': date_to.strftime('%Y/%m/%d'),
			'companies': comp_lst, 'kpi_total_ds': kpi_total_ds, 'kpi_ds': kpi_ds, 'view_mode': view_mode,
			'ebitda_trend': ebitda_trend, 'labels': self.labels[lang]
		}
		return render(request, self.template_name, context)


'''
-------------------------------Budgets----------------------------
'''


class BudgetDashboardView(View):

	@method_decorator(login_required)
	@method_decorator(permission_required('analytics.budget', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(BudgetDashboardView, self).dispatch(*args, **kwargs)

	template_name = 'analytics/budgets/budget_dashboard.html'
	chart_color_custom = ["rgba(46, 106, 255, ", "rgba(38,105,42, ", "rgba(242, 163, 17, ", "rgba(176, 100, 166, ", ]
	labels = {
		'en': {
			'net_profit': 'Net Profit',
			'revenue': 'Revenue',
			'cost': 'Expense',
			'actual': 'Actual',
			'budget': 'Budget',
			'diff': 'Diff',


		},
		'ar': {
			'net_profit': 'صافي الأرباح',
			'revenue': 'الإيرادات',
			'cost': 'المصروفات',
			'actual': 'الفعلي',
			'budget': 'المخطط',
			'diff': 'الفرق',

		}
	}

	def get(self, request, *args, **kwargs):
		lang = fn_get_user_lang(request.user.username)
		if int(datetime.date.today().month) == 1:
			date_from = datetime.date(datetime.date.today().year-1, 1, 1)
			date_to = datetime.date(datetime.date.today().year-1, 12, 31)
		else:
			date_from = datetime.date(datetime.date.today().year, 1, 1)
			date_to = datetime.datetime.now()
		companies = sp_companies_get(request.user.id, False)
		if len(companies) == 0:
			return render(request, 'analytics/error.html', {
				'err': 'There is no company a signed to (%s) user.' % request.user.username}
						)
		opco_lst = [[c[0], c[1], 'checked'] for c in companies]
		try:
			ds_all, ds_opco = sp_budget_actual_summary(
				str(date_from.strftime('%Y-%m-%d')), str(date_to.strftime('%Y-%m-%d')),
				[c[0] for c in opco_lst if c[2] == 'checked']
			)
		except Exception as e:
			return render(request, 'analytics/error.html', {'err': e})

		context = {
			'chart_color_custom': self.chart_color_custom, 'date_from': date_from.strftime('%Y/%m/%d'),
			'date_to': date_to.strftime('%Y/%m/%d'), 'companies': opco_lst, 'ds_all': ds_all, 'ds_opco': ds_opco,
			'labels': self.labels[lang]
		}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		lang = fn_get_user_lang(request.user.username)
		dates = str(request.POST['daterange']).replace(' ', '').split('-')
		date_from = datetime.datetime.strptime(str(dates[0]), '%Y/%m/%d')
		date_to = datetime.datetime.strptime(str(dates[1]), '%Y/%m/%d')
		if date_from > date_to:
			return render(request, 'analytics/error.html', {
				'err': 'Date To is not correct please check again.'}
						)
		companies = request.POST.getlist('company')
		if len(companies) <= 0:
			return render(request, 'analytics/error.html', {'err': 'Please, select a company to display its KPI.'})
		opcos = sp_companies_get(request.user.id, False)
		comp_lst = list()
		indc = 0
		for c in opcos:
			for i in companies:
				if str(c[0]) == str(i):
					indc = 1
					break
			if indc == 1:
				comp_lst.append([c[0], c[1], 'checked'])
				indc = 0
			else:
				comp_lst.append([c[0], c[1], ''])
		if len([[c[0], c[1]] for c in comp_lst if c[2] == 'checked']) > 0:
			try:
				ds_all, ds_opco = sp_budget_actual_summary(
					str(date_from.strftime('%Y-%m-%d')), str(date_to.strftime('%Y-%m-%d')),
					[c[0] for c in comp_lst if c[2] == 'checked']
				)
			except ZeroDivisionError:
				return render(request, 'analytics/error.html', {'err': 'Please, select proper dates.'})
		else:
			ds, total_lst, mrg_ds = [], [], []

		context = {
			'chart_color_custom': self.chart_color_custom, 'date_from': date_from.strftime('%Y/%m/%d'),
			'date_to': date_to.strftime('%Y/%m/%d'), 'companies': comp_lst, 'ds_all': ds_all, 'ds_opco': ds_opco,
			'labels': self.labels[lang]
		}
		return render(request, self.template_name, context)


class BudgetView(View):
	@method_decorator(login_required)
	@method_decorator(permission_required('analytics.budget', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(BudgetView, self).dispatch(*args, **kwargs)

	from .forms import BudgetViewForm
	form_class = BudgetViewForm
	template_name = 'analytics/budgets/budgets_view.html'

	def get(self, request):
		form = self.form_class()
		companies = sp_companies_get(request.user.id, False)
		form.fields['company'].choices = companies
		if len(companies) == 0:
			return render(request, 'analytics/error.html', {
				'err': 'There is no company a signed to (%s) user.' % request.user.username}
						)
		context = {
			'form': form
		}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		from .procedures import sp_budgets_get
		form = self.form_class(request.POST)
		form.fields['company'].choices = sp_companies_get(request.user.id, False)
		if form.is_valid():
			company = form.cleaned_data['company']
			year = form.cleaned_data['year']
			account_type_id = form.cleaned_data['account_type_id']
			status = form.cleaned_data['status']
			try:
				ds_category, ds_summary, ds_detail = sp_budgets_get(company, year, account_type_id, status)
				context = {
					'form': form, 'ds_category': ds_category, 'ds_summary': ds_summary,
					'ds_detail': ds_detail, 'year': year, 'prior_year': int(year) - 1
				}
				return render(request, self.template_name, context)
			except Exception as e:
				return render(request, 'analytics/error.html', {'err': e})
		else:
			context = {'form': form}
		return render(request, self.template_name, context)


'''
-------------------------------Trends KPIs----------------------------
'''


class AccountsTrendSummaryView(View):

	@method_decorator(login_required)
	@method_decorator(permission_required('analytics.acc_trends', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(AccountsTrendSummaryView, self).dispatch(*args, **kwargs)

	from .forms import AccountsTrendForm

	form_class = AccountsTrendForm
	template_name = 'analytics/accounts_trends/accounts_trends.html'
	labels = {
		'en': {
			'revenue': 'Revenue',
			'cost': 'Expense',
			'company': 'Company',
			'date_from': 'Date From',
			'date_to': 'Date TO',
			'display': 'Display as',
			'date': 'Date',
			'account_type': 'Accounts Type',
			'chart_type': 'Chart Type',
			'amount': 'Amount',
			'account': 'Account'
		},
		'ar': {
			'revenue': 'الإيرادات',
			'cost': 'المصروفات',
			'company': 'الشركة',
			'date_from': 'الفترة من',
			'date_to': 'إلى',
			'display': 'طريقة العرض',
			'date': 'التاريخ',
			'account_type': 'نوع الحسابات',
			'chart_type': 'نوع الإيضاح',
			'amount': 'المبلغ',
			'account': 'الحساب'
		}
	}

	def get(self, request, *args, **kwargs):
		lang = fn_get_user_lang(request.user.username)
		form = self.form_class()

		form.fields['company'].choices = sp_companies_get(request.user.id)
		ds, date_header, lst = sp_accountstransactions_get(
			form.fields['company'].choices[0][0], form.fields['date_from'].initial, form.fields['date_to'].initial,
			form.fields['account_type_id'].choices[0][0], form.fields['display_as'].choices[0][0],
			'summary', user_id=request.user.id
		)
		title_str = str(form.fields['company'].choices[0][1]) + ',  (' + form.fields['date_from'].initial + ' to ' + form.fields['date_to'].initial + '), ' + form.fields['account_type_id'].choices[0][1]
		context = {
			'form': form, 'ds': lst, 'header': date_header, 'Chart_color': Chart_color,
			'chart_type': str(form.fields['chart_type'].choices[0][0]), 'tbl': ds, 'title_str': title_str,
			'labels': self.labels[lang]
		}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		lang = fn_get_user_lang(request.user.username)
		form = self.form_class(request.POST)
		form.fields['company'].choices = sp_companies_get(request.user.id)
		if form.is_valid():
			company = form.cleaned_data['company']
			date_from = form.cleaned_data['date_from']
			date_to = form.cleaned_data['date_to']
			account_type_id = form.cleaned_data['account_type_id']
			display_as = form.cleaned_data['display_as']
			chart_type = form.cleaned_data['chart_type']
			ds, date_header, lst = sp_accountstransactions_get(
				company, date_from, date_to, account_type_id, display_as, 'summary', user_id=request.user.id
			)
			title_str = fn_company_name(company) + ',  (' + str(date_from) + ' to ' + str(date_to) + '), ' + fn_account_type_name(account_type_id)
			context = {
				'form': form, 'ds': lst, 'header': date_header, 'Chart_color': Chart_color,
				'chart_type': chart_type, 'tbl': ds, 'title_str': title_str, 'labels': self.labels[lang]
			}
		else:
			context = {'form': form}
		return render(request, self.template_name, context)


class AccountsTrendDetailView(View):

	@method_decorator(login_required)
	@method_decorator(permission_required('analytics.acc_trends', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(AccountsTrendDetailView, self).dispatch(*args, **kwargs)

	from .forms import AccountsTrendForm

	form_class = AccountsTrendForm
	template_name = 'analytics/accounts_trends/accounts_trends_detail.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		form.fields['company'].choices = sp_companies_get(request.user.id)
		form.fields['account_type_id'].choices = sp_accounts_types_get(1)
		ds, date_header, lst = sp_accountstransactions_get(
			form.fields['company'].choices[0][0], form.fields['date_from'].initial,
			form.fields['date_to'].initial, form.fields['account_type_id'].choices[0][0],
			form.fields['display_as'].choices[0][0], 'detail', user_id=request.user.id
		)
		title_str = str(form.fields['company'].choices[0][1]) + ',  (' + form.fields['date_from'].initial + ' to ' + form.fields['date_to'].initial + '), ' + form.fields['account_type_id'].choices[0][1]
		context = {
			'form': form, 'ds': lst, 'header': date_header, 'Chart_color': Chart_color,
			'chart_type': str(form.fields['chart_type'].choices[0][0]), 'tbl': ds, 'title_str': title_str
		}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):

		form = self.form_class(request.POST)
		form.fields['company'].choices = sp_companies_get(request.user.id)
		if form.is_valid():
			company = form.cleaned_data['company']
			date_from = form.cleaned_data['date_from']
			date_to = form.cleaned_data['date_to']
			account_type_id = form.cleaned_data['account_type_id']
			display_as = form.cleaned_data['display_as']
			chart_type = form.cleaned_data['chart_type']
			ds, date_header, lst = sp_accountstransactions_get(
				company, date_from, date_to, account_type_id, display_as, 'detail', user_id=request.user.id)
			title_str = fn_company_name(company) + ',  (' + str(date_from) + ' to ' + str(date_to) + '), ' + fn_account_type_name(account_type_id)
			context = {
				'form': form, 'ds': lst, 'header': date_header, 'Chart_color': Chart_color,
				'chart_type': chart_type, 'tbl': ds, 'title_str': title_str
			}
		else:
			context = {}
		return render(request, self.template_name, context)


class AccountsTrendAccountView(View):

		@method_decorator(login_required)
		@method_decorator(permission_required('analytics.acc_trends', raise_exception=True))
		def dispatch(self, *args, **kwargs):
			return super(AccountsTrendAccountView, self).dispatch(*args, **kwargs)

		from .forms import AccountsTrendForm

		form_class = AccountsTrendForm
		template_name = 'analytics/accounts_trends/accounts_trends_account.html'

		def post(self, request):
			company = request.POST['company']
			account_id = request.POST['account_id']
			date_from = request.POST['date_from']
			date_to = request.POST['date_to']
			display_as = request.POST['display_as']
			chart_type = request.POST['chart_type']
			ds, date_header, lst = sp_accountstransactions_get(
				company, date_from, date_to, account_id, display_as, 'account', '', request.user.id
			)
			title_str = fn_company_name(company) + ',  (' + str(date_from) + ' to ' + str(date_to) + '), ' + fn_account_name(account_id)
			context = {
				'ds': lst, 'header': date_header, 'Chart_color': Chart_color,
				'chart_type': chart_type, 'tbl': ds, 'company': company, 'date_from': date_from,
				'date_to': date_to, 'display_as': display_as, 'title_str': title_str
			}
			return render(request, self.template_name, context)


class CostCenterTrendView(View):

	@method_decorator(login_required)
	@method_decorator(permission_required('analytics.acc_trends', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(CostCenterTrendView, self).dispatch(*args, **kwargs)

	from .forms import CostCenterTrendForm

	form_class = CostCenterTrendForm
	template_name = 'analytics/accounts_trends/cost_center_trends.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		form.fields['company'].choices = sp_companies_get(request.user.id, False)
		form.fields['account_type_id'].choices = sp_accounts_types_get(1)
		ds, date_header, lst = sp_accountstransactions_get(
			form.fields['company'].choices[0][0], form.fields['date_from'].initial,
			form.fields['date_to'].initial, form.fields['account_type_id'].choices[0][0],
			form.fields['display_as'].choices[0][0], 'cost_center', user_id=request.user.id
		)
		title_str = str(form.fields['company'].choices[0][1]) + ',  (' + form.fields['date_from'].initial + ' to ' + form.fields['date_to'].initial + '), ' + form.fields['account_type_id'].choices[0][1]
		context = {
			'form': form, 'ds': lst, 'header': date_header, 'Chart_color': Chart_color,
			'chart_type': str(form.fields['chart_type'].choices[0][0]), 'tbl': ds, 'title_str': title_str
		}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		form.fields['company'].choices = sp_companies_get(request.user.id, False)
		form.fields['account_type_id'].choices = sp_accounts_types_get(1)
		if form.is_valid():
			company = form.cleaned_data['company']
			date_from = form.cleaned_data['date_from']
			date_to = form.cleaned_data['date_to']
			account_type_id = form.cleaned_data['account_type_id']
			display_as = form.cleaned_data['display_as']
			chart_type = form.cleaned_data['chart_type']
			ds, date_header, lst = sp_accountstransactions_get(
				company, date_from, date_to, account_type_id, display_as, 'cost_center', user_id=request.user.id
			)
			title_str = fn_company_name(company) + ',  (' + str(date_from) + ' to ' + str(date_to) + '), ' + fn_account_type_name(account_type_id)
			context = {
				'form': form, 'ds': lst, 'header': date_header, 'Chart_color': Chart_color,
				'chart_type': chart_type, 'tbl': ds, 'title_str': title_str
			}
		else:
			context = {}
		return render(request, self.template_name, context)
'''
------------------------------------- MARGIN KPIs -------------------------------------
'''


class MrgnRevenuesExpenses(View):

	@method_decorator(login_required)
	@method_decorator(permission_required('analytics.mrg_exp_rev', raise_exception=True))
	def dispatch(self, *args, **kwargs):
		return super(MrgnRevenuesExpenses, self).dispatch(*args, **kwargs)

	from .forms import MRGN_Revenues_ExpensesForm
	chart_color_custom = ["rgba(46, 106, 255, ", "rgba(38,105,42, ", "rgba(242, 163, 17, ", "rgba(176, 100, 166, "]
	form_class = MRGN_Revenues_ExpensesForm
	template_name = 'analytics/margins/revenues_expense_mrgn.html'
	labels = {
		'en': {
			'net_profit': 'Net Profit',
			'revenue': 'Revenue',
			'cost': 'Expense',
			'actual': 'Actual',
			'company': 'Company',
			'date_from': 'Date From',
			'date_to': 'Date TO',
			'display': 'Display as',
			'date': 'Date'
		},
		'ar': {
			'net_profit': 'صافي الأرباح',
			'revenue': 'الإيرادات',
			'cost': 'المصروفات',
			'company': 'الشركة',
			'date_from': 'الفترة من',
			'date_to': 'إلى',
			'display': 'طريقة العرض',
			'date': 'التاريخ'
		}
	}

	def get(self, request):
		lang = fn_get_user_lang(request.user.username)
		form = self.form_class()
		form.fields['company'].choices = sp_companies_get(request.user.id)
		ds = sp_mrgn_revenues_vs_expenses(
			form.fields['company'].choices[0][0],
			form.fields['date_from'].initial, form.fields['date_to'].initial,
			form.fields['display_as'].choices[0][0], user_id=request.user.id, landingpage=False
		)
		context = {
			'form': form, 'ds': ds, 'Chart_color': self.chart_color_custom, 'labels': self.labels[lang]
			#'date_format': date_format(form.fields['display_as'].choices[0][0]).replace('y', 'Y')
		}
		return render(request, self.template_name, context)

	def post(self, request):
		lang = fn_get_user_lang(request.user.username)
		form = self.form_class(request.POST)
		form.fields['company'].choices = sp_companies_get(request.user.id)
		if form.is_valid():
			company = form.cleaned_data['company']
			date_from = form.cleaned_data['date_from']
			date_to = form.cleaned_data['date_to']
			display_as = form.cleaned_data['display_as']
			ds = sp_mrgn_revenues_vs_expenses(company, date_from, date_to, display_as, request.user.id, landingpage=False)
			context = {
				'form': form, 'ds': ds, 'Chart_color': self.chart_color_custom, 'labels': self.labels[lang]
				#'date_format': date_format(display_as).replace('y', 'Y')
			}
		else:
			context = {}
		return render(request, self.template_name, context)


def test(request):
	if request.POST:
		dates = str(request.POST['daterange']).replace(' ', '').split('-')
		from_date = datetime.datetime.strptime(str(dates[0]), '%Y/%m/%d')
		to_date = datetime.datetime.strptime(str(dates[1]), '%Y/%m/%d')
	else:
		to_date = datetime.date(datetime.date.today().year, 10, 26)
		from_date = datetime.date(datetime.date.today().year, 1, 1)

	ds, ds_opco = sp_budget_actual_summary(str(from_date.strftime('%Y-%m-%d')),
								str(to_date.strftime('%Y-%m-%d')),  [1])
	context = {'to': to_date.strftime('%Y/%m/%d'), 'from': from_date.strftime('%Y/%m/%d'), 'ds': ds, 'ds_opco': ds_opco}
	return render(request, 'analytics/test.html', context)


class ModelRecordView(View):

	def get(self, request, *args, **kwargs):
		report_id = request.GET.get('report_id')
		model_name = reports[report_id]['model_name']
		frm = NewForm(model_name, hide_id=None)
		form = frm()
		for i in reports[report_id]['edit_form_read_only_fields']:
			form.fields[i].widget.attrs['readonly'] = True
		return render(request, 'analytics/test3.html', {'form': form})

	def post(self, request, *args, **kwargs):
		pk_id = request.POST['pk_id']
		report_id = request.POST['report_id']
		model_name = reports[report_id]['model_name']
		model_id = ContentType.objects.get(model=str(model_name))
		model_class = model_id.model_class()
		ds = model_class.objects.get(pk=str(pk_id))
		frm = NewForm(model_name)
		form = frm(instance=ds)
		for i in reports[report_id]['edit_form_read_only_fields']:
			form.fields[i].widget.attrs['readonly'] = True
		return render(request, 'analytics/test3.html', {'form': form, 'model_name': 'accounts'})


def test2(request):
	from analytics.models import Accounts
	if request.method == 'POST':
		selections = request.POST.getlist('slct')
		report_id = request.POST['report_id']
		its = Accounts.objects.filter(pk__in=selections)
		return render(request, 'analytics/test2.html', {'its': selections, 'report_id': report_id})


class NewEditModelView(View):
	from .forms import NewForm
	form_class = NewForm
	template_name = 'analytics/budgets/budgets_view.html'

	def get(self, request):
		form = self.form_class()
		form.fields['company'].choices = sp_companies_get(request.user.id, False)
		context = {
			'form': form
		}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		form.fields['company'].choices = sp_companies_get(request.user.id, False)
		if form.is_valid():
			company = form.cleaned_data['company']
			year = form.cleaned_data['year']
			account_type_id = form.cleaned_data['account_type_id']
			status = form.cleaned_data['status']
			try:
				ds_category, ds_summary, ds_detail = sp_budgets_get(company, year, account_type_id, status)
				context = {
					'form': form, 'ds_category': ds_category, 'ds_summary': ds_summary,
					'ds_detail': ds_detail, 'year': year, 'prior_year': int(year) - 1
				}
				return render(request, self.template_name, context)
			except Exception as e:
				return render(request, 'analytics/error.html', {'err': e})
		else:
			context = {'form': form}
		return render(request, self.template_name, context)


class ModelView(View):
	template_name = 'analytics/form_view_model.html'

	def get(self, request, *args, **kwargs):
		report_id = request.GET.get('report_id')
		if report_id is not None:
			model_name = reports[report_id]['model_name']
			form = searchform(
				model_name=model_name, fields_lst=[i[0] for i in reports[report_id]['search_fields']],
				user_id=request.user.id, all_opco=False
			)
			frm = form()
			context = {
				'model_name': model_name.upper(), 'frm': frm, 'report_id': report_id, 'title': reports[report_id]['title']
			}
			return render(request, self.template_name, context)
		else:
			return render(request, 'analytics/error.html', {'err': 'There is no selected report! please, check.'})

	def post(self, request, *args, **kwargs):
		report_id = request.POST['report_id']
		if report_id is not None:
			model_name = reports[report_id]['model_name']
			form = searchform(
				model_name=model_name, fields_lst=[i[0] for i in reports[report_id]['search_fields']],
				user_id=request.user.id, all_opco=False
			)
			frm = form(request.POST)
			search_lst = search_form_criteria(frm, report_id)
			model_id = ContentType.objects.get(model=str(model_name))
			model_class = model_id.model_class()
			model_fields = reports[report_id]['model_fields']
			ds = TableRowForm(queryset=model_class.objects.filter(**search_lst), fields=model_fields, model_name=model_name)
			context = {
				'ds': ds, 'model_name': model_name.upper(), 'frm': frm, 'report_id': report_id, 'title': reports[report_id]['title']
			}
			return render(request, self.template_name, context)
		else:
			return render(request, 'analytics/error.html', {'err': 'There is no model been chosen!.'})
