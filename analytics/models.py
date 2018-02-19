from django.db import models
from django.contrib.auth.models import User
from .utilities import get_data
from datetime import datetime


class Role(models.Model):
	role = models.CharField(max_length=100)

	def __str__(self):
		return self.role

	class Meta:
		verbose_name = 'Role'
		verbose_name_plural = 'Roles'
		permissions = (
			('landing_page', 'Can  view landing'),
			('acc_trends', 'Can  view trends accounts'),
			('mrg_exp_rev', 'Can  view margin expenses and revenues KPI'),
			('budget', 'Can  view budget KPI'),
			('kpi_settings', 'Can  configure KPIs settings'),
		)


class Companies(models.Model):
	company_id = models.SmallIntegerField(primary_key=True)
	company_name = models.CharField(max_length=255)
	company_logo = models.FileField(upload_to='CompaniesLogos', null=True, blank=True)

	def __str__(self):
		return self.company_name

	class Meta:
		ordering = ['company_id']
		verbose_name = 'Company'
		verbose_name_plural = 'Companies'


class UsersSettings(models.Model):
	user = models.ForeignKey(User)
	photo = models.ImageField(blank=True, null=True, upload_to='UsersPhotos')
	language = models.CharField(max_length=2, choices=[['en', 'English'], ['ar', 'عربي']], default='en')

	def __str__(self):
		return str(self.user)

	class Meta:
		ordering = ['user']
		indexes = [
			models.Index(fields=['user']),
		]

		unique_together = (('user'),)
		verbose_name = 'User Settings'
		verbose_name_plural = 'Users Settings'


class UsersCompanies(models.Model):
	company = models.ForeignKey(Companies)
	user = models.ForeignKey(User)

	def __str__(self):
		return str(self.company)

	class Meta:
		ordering = ['company']
		indexes = [
			models.Index(fields=['company']),
			models.Index(fields=['user']),
		]
		unique_together = (('company', 'user'),)
		verbose_name = 'User Company'
		verbose_name_plural = 'Users Companies'


class AccountsTypes(models.Model):
	account_type_id = models.CharField(max_length=10, primary_key=True, verbose_name='account type id')
	account_type_name = models.CharField(max_length=100, verbose_name='account type')

	class Meta:
		unique_together = [('account_type_name',)]
		verbose_name = 'Account Type'
		verbose_name_plural = 'Accounts Types'

	def __str__(self):
		return str(self.account_type_name)


class Accounts(models.Model):
	id = models.CharField(max_length=30, primary_key=True)
	company = models.ForeignKey(Companies, on_delete=models.CASCADE)
	account_id = models.CharField(max_length=10)
	account_name = models.CharField(max_length=255)
	account_type = models.ForeignKey(AccountsTypes)
	parentid = models.CharField(max_length=10, null=True, blank=True)
	kind = models.BooleanField(default=False)
	active = models.BooleanField(default=True)
	budget_account = models.BooleanField(default=True)
	loading_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.id) + '-' + str(self.account_name)

	class Meta:
		ordering = ['company', 'account_id']
		indexes = [
			models.Index(fields=['company']),
			models.Index(fields=['account_id']),
			models.Index(fields=['account_type'])
		]
		verbose_name = 'Account'
		verbose_name_plural = 'Accounts'

	def save(self, *args, **kwargs):
		ds = Companies.objects.get(company_name=self.company)
		self.id = str(ds.company_id) + '-' + str(self.account_id)
		self.loading_date = datetime.now()
		super(Accounts, self).save(*args, ** kwargs)


class AccountsTransactions(models.Model):
	id = models.CharField(max_length=100, primary_key=True)
	company = models.ForeignKey(Companies, on_delete=models.CASCADE)
	account_id = models.CharField(max_length=15)
	center_id = models.CharField(max_length=10, blank=True, null=True)
	transaction_date = models.DateField()
	amount = models.DecimalField(max_digits=12, decimal_places=2)
	loading_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['company', 'transaction_date', 'account_id']
		indexes = [
			models.Index(fields=['company']),
			models.Index(fields=['account_id']),
			models.Index(fields=['transaction_date'])
		]
		unique_together = (("company", "account_id", "transaction_date", "center_id",),)
		verbose_name = 'Transaction'
		verbose_name_plural = 'Transactions'

	def save(self, *args, **kwargs):
		ds = Companies.objects.get(company_name=self.company)
		self.id = str(ds.company_id) + '-' + str(self.account_id) + '-' + str(self.transaction_date)
		super(AccountsTransactions, self).save(*args, **kwargs)


class BudgetYear(models.Model):
	year = models.PositiveSmallIntegerField(primary_key=True)
	status = models.CharField(max_length=1, choices=[['d', 'Draft'], ['a', 'Active'], ['c', 'Closed']], default='d')

	class Meta:
		verbose_name = 'Budget Year'
		verbose_name_plural = 'Budget - Years'
		ordering = ['year']

	def __str__(self):
		return str(self.year)


class Centers(models.Model):
	id = models.CharField(max_length=30, primary_key=True)
	company = models.ForeignKey(Companies, on_delete=models.CASCADE)
	center_id = models.CharField(max_length=10)
	center_name = models.CharField(max_length=255)
	parentid = models.CharField(max_length=10, null=True, blank=True)
	kind = models.BooleanField(default=False)
	active = models.BooleanField(default=True)
	loading_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.id) + ' - ' + str(self.center_name)

	class Meta:
		ordering = ['company', 'center_id']
		indexes = [
			models.Index(fields=['company']),
			models.Index(fields=['center_id']),
		]
		verbose_name = 'Center'
		verbose_name_plural = 'Centers'

	def save(self, *args, **kwargs):
		ds = Companies.objects.get(company_name=self.company)
		self.id = str(ds.company_id) + '-' + str(self.center_id)
		super(Centers, self).save(*args, ** kwargs)


class Budget(models.Model):
	status_lst = [
		['d', 'Draft'], ['s', 'Saved'], ['a', 'Approved']
	]
	company = models.ForeignKey(Companies, on_delete=models.CASCADE)
	year = models.ForeignKey(BudgetYear, verbose_name='Year')
	account = models.ForeignKey(Accounts, verbose_name='Account', on_delete=models.CASCADE)
	center = models.ForeignKey(Centers, verbose_name='Cost Center', on_delete=models.CASCADE)
	jan_budget_amount = models.PositiveIntegerField(default=0, verbose_name='Jan')
	feb_budget_amount = models.PositiveIntegerField(default=0, verbose_name='Feb')
	mar_budget_amount = models.PositiveIntegerField(default=0, verbose_name='Mar')
	apr_budget_amount = models.PositiveIntegerField(default=0, verbose_name='Apr')
	may_budget_amount = models.PositiveIntegerField(default=0, verbose_name='May')
	jun_budget_amount = models.PositiveIntegerField(default=0, verbose_name='Jun')
	jul_budget_amount = models.PositiveIntegerField(default=0, verbose_name='Jul')
	aug_budget_amount = models.PositiveIntegerField(default=0, verbose_name='Aug')
	sep_budget_amount = models.PositiveIntegerField(default=0, verbose_name='Sep')
	oct_budget_amount = models.PositiveIntegerField(default=0, verbose_name='Oct')
	nov_budget_amount = models.PositiveIntegerField(default=0, verbose_name='Nov')
	dec_budget_amount = models.PositiveIntegerField(default=0, verbose_name='Dec')
	status = models.CharField(max_length=1, choices=status_lst, default='d', null=True, blank=True)

	@property
	def budget_amount(self):
		budget_amount = (
				self.jan_budget_amount + self.feb_budget_amount + self.mar_budget_amount
				+ self.apr_budget_amount + self.may_budget_amount + self.jun_budget_amount
				+ self.jul_budget_amount + self.aug_budget_amount + self.sep_budget_amount
				+ self.oct_budget_amount + self.nov_budget_amount + self.dec_budget_amount
		)
		return str("{:,}".format(budget_amount))

	@property
	def account_no(self):
		account_ob = Accounts.objects.get(id=self.account_id, company=self.company)
		return account_ob.account_id

	@property
	def account_name(self):
		account_ob = Accounts.objects.get(id=self.account_id, company=self.company)
		return str(account_ob.account_id) + ' - ' + str(account_ob.account_name)

	@property
	def center_no(self):
		center_ob = Centers.objects.get(id=self.center_id, company=self.company)
		return center_ob.center_id

	@property
	def last_year(self):
		from .procedures import fn_account_amount
		return fn_account_amount(int(str(self.year)) - 1, self.company_id, str(self.account).split('-')[0], str(self.center_id).split('-')[1])

	@property
	def current_status(self):
		status = self.status
		for s in self.status_lst:
			if self.status == s[0]:
				status = s[1]
				break
		return status

	class Meta:
		ordering = ['company', 'year_id', 'account_id']
		indexes = [
			models.Index(fields=['company']),
			models.Index(fields=['year']),
			models.Index(fields=['account']),
			models.Index(fields=['center']),
			models.Index(fields=['status'])
		]
		unique_together = (("company", "year",  "account", "center"),)
		verbose_name = 'Budget'
		verbose_name_plural = 'Budget - Accounts'

	def __str__(self):
		budget_amount = (
			self.jan_budget_amount + self.feb_budget_amount + self.mar_budget_amount +
			self.apr_budget_amount + self.mar_budget_amount + self.jul_budget_amount + self.jul_budget_amount +
			self.aug_budget_amount + self.sep_budget_amount + self.oct_budget_amount + self.nov_budget_amount +
			self.dec_budget_amount
		)
		return str(self.year_id) + ' - ' + str(self.account_id) + ' - ' + str(budget_amount)

	def save(self, *args, **kwargs):
		if self.status != 'a':
			super(Budget, self).save(*args, ** kwargs)


class HRBudget(models.Model):
	status = [
		['d', 'Draft'], ['s', 'Saved'], ['a', 'Approved']
	]
	company = models.ForeignKey(Companies, on_delete=models.CASCADE)
	year = models.ForeignKey(BudgetYear, verbose_name='Year', on_delete=models.CASCADE)
	center = models.ForeignKey(Centers, verbose_name='Cost Center', on_delete=models.CASCADE)
	staff_count = models.PositiveIntegerField(verbose_name='Staff Budget')
	status = models.CharField(max_length=1, choices=status, default='d')

	@property
	def staff_actual(self):
		from .procedures import fn_hr_get
		staff = fn_hr_get(self.year, self.company_id, str(self.center).split('-')[0])
		return staff

	class Meta:
		ordering = ['company', 'year_id', 'center']
		indexes = [
			models.Index(fields=['company']),
			models.Index(fields=['year']),
			models.Index(fields=['center']),
			models.Index(fields=['status'])
		]
		unique_together = (("company", "year", "center"),)
		verbose_name = 'Budget'
		verbose_name_plural = 'Budget - HR'

	def __str__(self):
		return str(self.company) + ' - ' + str(self.year) + ' - ' + str(self.center) + ' - ' + str(self.staff_count)

	def save(self, *args, **kwargs):
		if self.status != 'a':
			super(HRBudget, self).save(*args, **kwargs)


class HR(models.Model):
	id = models.CharField(max_length=30, primary_key=True)
	company = models.ForeignKey(Companies, on_delete=models.CASCADE)
	center_id = models.CharField(max_length=10)
	employee_id = models.CharField(max_length=15)
	employee_name = models.CharField(max_length=200)
	employment_date = models.DateField()
	termination_date = models.DateField(null=True, blank=True)
	status = models.PositiveSmallIntegerField()
	loading_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['company', 'center_id', 'employee_id']
		indexes = [
			models.Index(fields=['company']),
			models.Index(fields=['center_id']),
			models.Index(fields=['status']),
			models.Index(fields=['employee_id']),
			models.Index(fields=['employment_date'])
		]
		unique_together = (("company", "employee_id"),)
		verbose_name = 'HR'
		verbose_name_plural = 'HR'

	def __str__(self):
		return str(self.company) + ' - ' + str(self.center_id) + ' - ' + str(self.employee_id) + ' - ' + str(self.employee_name)

	def save(self, *args, **kwargs):
		ds = Companies.objects.get(company_name=self.company)
		self.id = str(ds.company_id) + '-' + str(self.employee_id)
		super(HR, self).save(*args, **kwargs)


class EtlSchedule(models.Model):
	type_lst = [
		['a', 'Accounts'], ['c', 'Centers'], ['t', 'Transactions'], ['h', 'HR']
	]
	time_lst = [
		['00', '00:00'], ['01', '01:00'], ['02', '02:00'], ['03', '03:00'], ['04', '04:00'], ['05', '05:00'],
		['06', '06:00'], ['07', '07:00'], ['08', '08:00'], ['09', '09:00'], ['10', '10:00'], ['11', '11:00'],
		['12', '12:00'], ['13', '13:00'], ['14', '14:00'], ['15', '15:00'], ['16', '16:00'], ['17', '17:00'],
		['18', '18:00'], ['19', '19:00'], ['20', '20:00'], ['21', '21:00'], ['22', '22:00'], ['23', '23:00']
	]

	data_type = models.CharField(max_length=1, choices=type_lst)
	schedule_time = models.CharField(max_length=2, choices=time_lst)

	class Meta:
		ordering = ['data_type', 'schedule_time']
		indexes = [
			models.Index(fields=['data_type']),
		]
		unique_together = (('data_type', 'schedule_time'),)
		verbose_name = 'ETL Schedule'
		verbose_name_plural = 'ETL Schedule'

	def __str__(self):
		dt = self.data_type
		for i in self.type_lst:
			if i[0] == self.data_type:
				dt = i[1]
		return str(dt) + ' ' + str(self.schedule_time)


class EtlLog(models.Model):
	log_time = models.CharField(max_length=50)
	description = models.CharField(max_length=300)
	type_id = models.CharField(max_length=30, choices=[['Accounts', 'Accounts'], ['Centers', 'Centers'],
													   ['Transactions', 'Transactions'], ['HR', 'HR']]
							   )
	company = models.CharField(max_length=100)

	class Meta:
		ordering = ['log_time', 'type_id', 'company']
		indexes = [
			models.Index(fields=['type_id']),
			models.Index(fields=['company']),
		]
		verbose_name = 'ETL Log'
		verbose_name_plural = 'ETL Logs'

	def __str__(self):
		return str(self.company) + ' ' + str(self.description) + ' ' + str(self.company)


class KpiAccount(models.Model):
	company = models.ForeignKey(Companies)
	type_id = models.CharField(max_length=1, choices=[['t', 'Tax'], ['z', 'Zaka'], ['d', 'Depreciation']])
	account = models.ForeignKey(Accounts)

	def __str__(self):
		return str(self.company) + ' - ' + str(self.type_id) + ' - ' + str(self.account)

	class Meta:
		ordering = ['company', 'type_id']
		verbose_name = 'KPI Account Setting'
		verbose_name_plural = 'KPIs Accounts Settings'


class KpiCenter(models.Model):
	company = models.ForeignKey(Companies)
	type_id = models.CharField(max_length=1, choices=[['o', 'Operation Cost Centers'], ])
	center = models.ForeignKey(Centers)

	def __str__(self):
		return str(self.company) + ' - ' + str(self.type_id) + ' - ' + str(self.center)

	class Meta:
		ordering = ['company', 'type_id']
		verbose_name = 'KPI Cost Center'
		verbose_name_plural = 'KPIs Cost Centers Settings'


"""
class KpiSummary(models.Model):
	month = models.CharField(max_length=7)
	company = models.ForeignKey(Companies)
	revenue = models.DecimalField(max_digits=12, decimal_places=2)
	cost = models.DecimalField(max_digits=12, decimal_places=2)
	ebitda = models.DecimalField(max_digits=12, decimal_places=2)
	ebitda_cost = models.DecimalField(max_digits=12, decimal_places=2)
	ebitda_per = models.DecimalField(max_digits=12, decimal_places=2)
	ebit = models.DecimalField(max_digits=12, decimal_places=2)
	ebit_cost = models.DecimalField(max_digits=12, decimal_places=2)
	ebit_per = models.DecimalField(max_digits=12, decimal_places=2)
	net_profit = models.DecimalField(max_digits=12, decimal_places=2)
	net_profit_per = models.DecimalField(max_digits=12, decimal_places=2)
"""