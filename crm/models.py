from django.db import models
from django.contrib.auth.models import User
from analytics.models import Companies, Accounts, BudgetYear
import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404

class SalesAgents(models.Model):

	sale_agent_id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User)
	company = models.ForeignKey(Companies, on_delete=models.PROTECT)
	sale_agent = models.CharField(max_length=200, unique=True)
	mobile_no = models.CharField(max_length=20)

	def __str__(self):
		return str(self.sale_agent)

	class Meta:
		ordering = ['company_id', 'user']
		indexes = [
			models.Index(fields=['company']),
			models.Index(fields=['user']),
		]
		unique_together = ('user', 'company', )

		verbose_name = 'Sale Agent'
		verbose_name_plural = 'Sales Agents'


class CustomersCategories(models.Model):

	customer_category_id = models.AutoField(primary_key=True)
	customer_category = models.CharField(max_length=200, unique=True)

	def __str__(self):
		return str(self.customer_category)

	class Meta:
		verbose_name = 'Customer Category'
		verbose_name_plural = 'Customers Categories'

	def save(self, *args, **kwargs):
		# Check how the current values differ from ._loaded_values. For example,
		# prevent changing the creator_id of the model. (This example doesn't
		# support cases where 'creator_id' is deferred).
		if self.customer_category == 'test':
			raise ValueError("Can't Update.")
		super().save(*args, **kwargs)


class CustomersIndustries(models.Model):

	customer_industry_id = models.AutoField(primary_key=True)
	customer_industry = models.CharField(max_length=200, unique=True)

	def __str__(self):
		return str(self.customer_industry)

	class Meta:
		verbose_name = 'Customer Industry'
		verbose_name_plural = 'Customers Industries'


class Countries(models.Model):

	country_id = models.AutoField(primary_key=True)
	country = models.CharField(max_length=50, unique=True)

	def __str__(self):
		return str(self.country)

	class Meta:
		verbose_name = 'Country'
		verbose_name_plural = 'Countries'


class States(models.Model):

	state_id = models.AutoField(primary_key=True)
	country = models.ForeignKey(Countries, on_delete=models.PROTECT)
	state = models.CharField(max_length=50, unique=True)

	def __str__(self):
		return str(self.state)

	class Meta:
		verbose_name = 'State'
		verbose_name_plural = 'States'


class Cities(models.Model):

	city_id = models.AutoField(primary_key=True)
	state = models.ForeignKey(States, on_delete=models.PROTECT)
	city = models.CharField(max_length=50, unique=True)

	def __str__(self):
		return str(self.city)

	@property
	def country(self):
		from .procedures import sp_country_name
		country_obj = sp_country_name(self.city_id)
		return str(country_obj)

	class Meta:
		verbose_name = 'City'
		verbose_name_plural = 'Cities'


class Customers(models.Model):
	status_lst = {'n': 'New', 'a': 'Active', 's': 'Suspended', 'r': 'Archived'}

	customer_id = models.AutoField(primary_key=True)
	customer_code = models.CharField(max_length=20, unique=True, verbose_name='ID')
	customer_name = models.CharField(max_length=200, unique=True, verbose_name='Name')
	customer_category = models.ForeignKey(CustomersCategories, verbose_name='Category', on_delete=models.PROTECT)
	customer_industry = models.ForeignKey(CustomersIndustries, verbose_name='Industry', on_delete=models.PROTECT)
	website_url = models.URLField(blank=True, null=True)
	city = models.ForeignKey(Cities, blank=True, null=True, on_delete=models.PROTECT)
	address = models.TextField(blank=True, null=True)
	street = models.CharField(max_length=100, blank=True, null=True)
	block_no = models.CharField(max_length=50, blank=True, null=True)
	building_no = models.CharField(max_length=50, blank=True, null=True)
	location_x = models.CharField(max_length=20, blank=True, null=True, verbose_name='longitude')
	location_y = models.CharField(max_length=20, blank=True, null=True, verbose_name='latitude')
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)

	def __str__(self):
		return str(self.customer_name)

	class Meta:
		ordering = ['customer_category', 'customer_industry', 'customer_name']
		indexes = [
			models.Index(fields=['customer_code']),
		]

		verbose_name = 'Customer'
		verbose_name_plural = 'Customers'


class CustomersStatus(models.Model):
	status_lst = {'n': 'New', 'a': 'Active', 'd': 'Dormant', 'r': 'Archived'}
	rate_lst = {'n': 'Not Rated', 'a': 'Accepted', 'g': 'Good', 'v': 'V.Good', 'e': 'Excellent'}

	customer = models.ForeignKey(Customers, on_delete=models.PROTECT)
	company = models.ForeignKey(Companies, on_delete=models.PROTECT)
	rate = models.CharField(
		max_length=1, choices=[[k, v] for k, v in rate_lst.items()], default='n',
		blank=True, null=True
	)
	status = models.CharField(
		max_length=1, choices=[[k, v] for k, v in status_lst.items()], default='n',
		blank=True, null=True
	)
	event_date = models.DateField(default=datetime.date.today(), null=True, blank=True)
	user = models.ForeignKey(User)

	@property
	def current_status(self):
		return self.status_lst[str(self.status)]

	@property
	def current_rate(self):
		return self.rate_lst[str(self.rate)]

	def __str__(self):
		return str(self.customer) + ' - ' + str(self.current_status) + ' - ' + str(self.current_rate)

	class Meta:
		ordering = ['company', 'rate', 'status']
		indexes = [
			models.Index(fields=['rate']),
			models.Index(fields=['status']),
			models.Index(fields=['customer']),
			models.Index(fields=['company']),
		]
		unique_together = [
			("customer", "company"),
		]

		verbose_name = 'Customer Status & Rate'
		verbose_name_plural = 'Customers Status & Rate'


class CustomersDetails(models.Model):
	status_lst = {'n': 'New', 'a': 'Active', 'd': 'Dormant', 'r': 'Archived'}
	rate_lst = [['n', 'Not Rated'], ['a', 'Accepted'], ['g', 'Good'], ['v', 'V.Good'], ['e', 'Excellent']]

	customer_detail_id = models.AutoField(primary_key=True)
	customer = models.ForeignKey(Customers, on_delete=models.PROTECT)
	contact_person_name = models.CharField(max_length=50)
	contact_person_phone = models.CharField(max_length=50, blank=True, null=True)
	contact_person_facebook = models.CharField(max_length=50, blank=True, null=True)
	contact_person_linkedin = models.CharField(max_length=50, blank=True, null=True)
	contact_person_instagram = models.CharField(max_length=50, blank=True, null=True)
	registration_date = models.DateField(default=datetime.date.today())
	notes = models.TextField(blank=True, null=True)
	account = models.CharField(max_length=10, blank=True, null=True, verbose_name='GL/Account')
	company = models.ForeignKey(Companies, on_delete=models.PROTECT)
	user = models.ForeignKey(User, on_delete=models.PROTECT)

	def __str__(self):
		return str(self.contact_person_name)

	class Meta:
		ordering = ['contact_person_name']
		indexes = [
			models.Index(fields=['registration_date']),
		]
		unique_together = ("account", "customer", "company"),

		verbose_name = 'Customer Detail'
		verbose_name_plural = 'Customers Details'


class CategoriesBudget(models.Model):
	status_lst = {'d': 'Draft', 's': 'Saved', 'a': 'Approved'}

	customer_category = models.ForeignKey(CustomersCategories, verbose_name='Category')
	company = models.ForeignKey(Companies, on_delete=models.PROTECT)
	year = models.ForeignKey(BudgetYear, verbose_name='Year', on_delete=models.PROTECT, limit_choices_to={'status': 'a'})
	new_customers = models.PositiveIntegerField(default=0)
	budget_amount = models.PositiveIntegerField(default=0)
	status = models.CharField(
		max_length=1, default='d', choices=[[k, v] for k, v in status_lst.items()],
		blank=True, null=True
	)

	@property
	def current_status(self):
		return self.status_lst[str(self.status)]

	@property
	def amount(self):
		return str("{:,}".format(self.budget_amount))

	def __str__(self):
		return str(self.year) + str(self.customer_category) + str(self.budget_amount)

	class Meta:
		unique_together = ("year", "customer_category", "company"),
		indexes = [
			models.Index(fields=['year']),
			models.Index(fields=['customer_category']),
			models.Index(fields=['status']),
		]

		verbose_name = 'Category Budget'
		verbose_name_plural = 'Categories Budget'


class IndustriesBudget(models.Model):
	status_lst = {'d': 'Draft', 's': 'Saved', 'a': 'Approved'}

	customer_industry = models.ForeignKey(CustomersIndustries, verbose_name='Industry')
	company = models.ForeignKey(Companies, on_delete=models.PROTECT)
	year = models.ForeignKey(BudgetYear, verbose_name='Year', on_delete=models.PROTECT, limit_choices_to={'status': 'a'})
	new_customers = models.PositiveIntegerField(default=0)
	budget_amount = models.PositiveIntegerField(default=0)
	status = models.CharField(
		max_length=1, default='d', choices=[[k, v] for k, v in status_lst.items()],
		blank=True, null=True
	)

	@property
	def current_status(self):
		return self.status_lst[str(self.status)]

	@property
	def amount(self):
		return str("{:,}".format(self.budget_amount))

	def __str__(self):
		return str(self.year) + str(self.customer_industry) + str(self.budget_amount)

	class Meta:
		unique_together = ("year", "customer_industry", "company"),
		indexes = [
			models.Index(fields=['year']),
			models.Index(fields=['customer_industry']),
			models.Index(fields=['status']),
		]

		verbose_name = 'Industry Budget'
		verbose_name_plural = 'Industries Budget'


class SalesAgentsBudget(models.Model):
	status_lst = {'d': 'Draft', 's': 'Saved', 'a': 'Approved'}

	sale_agent_id = models.ForeignKey(SalesAgents, verbose_name='Industry', on_delete=models.PROTECT)
	customer_category = models.ForeignKey(CustomersCategories, on_delete=models.PROTECT, null=True, blank=True)
	customer_industry = models.ForeignKey(CustomersIndustries, on_delete=models.PROTECT, null=True, blank=True)
	new_customers = models.PositiveIntegerField(default=0)
	year = models.ForeignKey(
		BudgetYear, verbose_name='Year', on_delete=models.PROTECT, limit_choices_to={'status': 'a'}
	)
	budget_amount = models.PositiveIntegerField(default=0)
	status = models.CharField(
		max_length=1, default='d', choices=[[k, v] for k, v in status_lst.items()],
		blank=True, null=True
	)

	@classmethod
	def title(cls, field, lang='en'):
		fields = {
			'sale_agent_id': {'en': 'Sale Agent', 'ar': 'مندوب التسويق', 'search_criteria': '__exact'},
			'year': {'en': 'Year', 'ar': 'السنة', 'search_criteria': '__exact'},
			'budget_amount': {'en': 'Budget Amount', 'ar': 'مبلغ الميزانية', 'search_criteria': '__exact'},
			'status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__exact'},
			'amount': {'en': 'Status', 'ar': 'المبلغ', 'search_criteria': '__exact'},
			'current_status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__exact'}
		}
		return fields[field][lang]

	@property
	def amount(self):
		return str("{:,}".format(self.budget_amount))

	@property
	def current_status(self):
		return self.status_lst[str(self.status)]

	def __str__(self):
		return str(self.year) + str(self.sale_agent_id) + str(self.budget_amount)

	class Meta:
		unique_together = ("year", "sale_agent_id", "customer_industry", "customer_category"),
		indexes = [
			models.Index(fields=['year']),
			models.Index(fields=['sale_agent_id']),
			models.Index(fields=['status']),
		]

		verbose_name = 'Industry Budget'
		verbose_name_plural = 'Industries Budget'

	def save(self, *args, **kwargs):
		if self.customer_category is None and self.customer_industry is None:
			raise ValueError("Please, select the customer category or customer industry")
		super().save(*args, **kwargs)


class CustomersBudget(models.Model):
	status_lst = {'d': 'Draft', 's': 'Saved', 'a': 'Approved'}

	customer = models.ForeignKey(Customers, on_delete=models.PROTECT)
	company = models.ForeignKey(Companies, on_delete=models.PROTECT)
	sale_agent = models.ForeignKey(SalesAgents, on_delete=models.PROTECT)
	year = models.ForeignKey(
		BudgetYear, verbose_name='Year', on_delete=models.PROTECT, limit_choices_to={'status': 'a'}
	)
	budget_amount = models.PositiveIntegerField(default=0)
	status = models.CharField(
		max_length=1, default='d', choices=[[k, v] for k, v in status_lst.items()],
		blank=True, null=True
	)
	user = models.ForeignKey(User, on_delete=models.PROTECT)

	@property
	def amount(self):
		return str("{:,}".format(self.budget_amount))

	@property
	def current_status(self):
		return self.status_lst[str(self.status)]

	def __str__(self):
		return str(self.year) + ' - ' + str(self.customer) + ' - ' + str(self.sale_agent) + ' - ' + str(self.budget_amount)

	class Meta:
		unique_together = ("year", "customer", "sale_agent", ),
		indexes = [
			models.Index(fields=['status']),
		]

		verbose_name = 'Customer Budget'
		verbose_name_plural = 'Customers Budget'


class ActivitiesTypes(models.Model):
	activity_type = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.activity_type

	class Meta:
		verbose_name = 'Activity Type'
		verbose_name_plural = 'Activities Types'


class CustomersActivities(models.Model):
	status_lst = {'o': 'Open', 'c': 'Closed'}

	activity_id = models.AutoField(primary_key=True)
	activity_type = models.ForeignKey(ActivitiesTypes, on_delete=models.PROTECT)
	subject = models.CharField(max_length=200)
	activity_date = models.DateField(default=datetime.date.today())
	customer = models.ForeignKey(Customers, on_delete=models.PROTECT)
	company = models.ForeignKey(Companies, on_delete=models.PROTECT)
	description = models.TextField()
	sale_agent = models.ForeignKey(SalesAgents, on_delete=models.PROTECT)
	activity_reference = models.CharField(max_length=50)
	status = models.CharField(
		max_length=1, default='o', choices=[[k, v] for k, v in status_lst.items()],
		blank=True, null=True
	)
	user = models.ForeignKey(User, on_delete=models.PROTECT)

	@property
	def current_status(self):
			return self.status_lst[str(self.status)]

	class Meta:
		unique_together = ("activity_type", "activity_reference", "customer", "company"),
		indexes = [
			models.Index(fields=['activity_date']),
			models.Index(fields=['activity_reference']),
			models.Index(fields=['status']),
		]

		verbose_name = 'Customer Activity'
		verbose_name_plural = 'Customers Activities'

	def __str__(self):
		return self.subject

	def save(self, *args, **kwargs):
		# Check how the current values differ from ._loaded_values. For example,
		if self.activity_date <= datetime.date.today():
			raise ValueError("Activity Date %s should not be less than today." % self.activity_date)
		super().save(*args, **kwargs)


class CustomersActivitiesActions(models.Model):
	status_lst = {'o': 'Open', 'c': 'Closed'}

	activity_action_id = models.AutoField(primary_key=True)
	activity_id = models.ForeignKey(CustomersActivities)
	action_time = models.DateTimeField(default=timezone.localtime(timezone.now()))
	contacted_person_name = models.CharField(max_length=100)
	description = models.TextField()
	feedback = models.TextField()
	actions = models.TextField(blank=True, null=True)
	actions_date = models.DateField(blank=True, null=True)
	status = models.CharField(
		max_length=1, default='o', choices=[[k, v] for k, v in status_lst.items()],
		blank=True, null=True
	)
	user = models.ForeignKey(User, on_delete=models.PROTECT)

	@property
	def customer(self):
		print(self.activity_id)
		activity = get_object_or_404(CustomersActivities, activity_id=self.activity_id.pk)
		customer_obj = get_object_or_404(Customers, customer_id=activity.customer_id)
		return str(customer_obj.customer_name)

	@property
	def current_status(self):
		return self.status_lst[str(self.status)]

	@property
	def action_date_time(self):
		return timezone.localtime(self.action_time).strftime('%Y-%m-%d %H:%m')

	class Meta:
		unique_together = ("status", "activity_id", ),
		indexes = [
			models.Index(fields=['action_time']),
			models.Index(fields=['status']),
		]

		verbose_name = 'Customer Activity Action'
		verbose_name_plural = 'Customers Activities Actions'

	def save(self, *args, **kwargs):
		# Check how the current values differ from ._loaded_values. For example,
		if CustomersActivities.objects.filter(pk=self.activity_id.pk, status__exact='c').exists():
			raise ValueError("Can't do action for activity that is already closed.")
		if self.action_time.strftime('%Y-%m-%d') > datetime.datetime.now().strftime('%Y-%m-%d'):
			raise ValueError("Action time %s should not be grater than today." % str(self.action_time))
		if self.actions_date is not None and self.actions_date.strftime('%Y-%m-%d') \
				<= datetime.date.today().strftime('%Y-%m-%d'):
			raise ValueError("Action Date %s should not be less than today." % self.actions_date)

		if self.status == 'c':
			# print(self)
			CustomersActivities.objects.filter(pk__exact=self.activity_id.pk).update(status='c')

		super().save(*args, **kwargs)


class MissedOpportunitiesReasons(models.Model):
	missed_reason = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.missed_reason

	class Meta:
		verbose_name = 'Missed Opportunity Reason'
		verbose_name_plural = 'Missed Opportunities Reasons'


class Opportunities(models.Model):
	status_lst = {'o': 'Open', 'm': 'Missed', 's': 'Success'}

	customer = models.ForeignKey(Customers, on_delete=models.PROTECT)
	company = models.ForeignKey(Companies, on_delete=models.PROTECT)
	opportunity_date = models.DateField()
	amount = models.PositiveIntegerField()
	description = models.CharField(max_length=150)
	notes = models.TextField(blank=True, null=True)
	status = models.CharField(max_length=1, default='o', choices=[[k, v] for k, v in status_lst.items()], blank=True, null=True)
	missed_reason = models.ForeignKey(MissedOpportunitiesReasons, on_delete=models.PROTECT, blank=True, null=True)
	missed_notes = models.TextField(blank=True, null=True)
	user = models.ForeignKey(User, on_delete=models.PROTECT)

	@property
	def current_status(self):
		return self.status_lst[str(self.status)]

	@property
	def opportunity_amount(self):
		return str("{:,}".format(self.amount))

	def __str__(self):
		return self.description

	class Meta:
		unique_together = ("customer", "company", "status", ),
		indexes = [
			models.Index(fields=['opportunity_date']),
			models.Index(fields=['status']),
		]

		verbose_name = 'Opportunity'
		verbose_name_plural = 'Opportunities'

		permissions = (
			('opportunities_add', 'Can  Add Opportunity'),
			('Update_Opportunity', 'Can uUpdate Opportunity')
		)

	def save(self, *args, **kwargs):
		if self.status != 'm' and self.missed_reason is not None:
			raise ValueError("Can't write misses reason unless the opportunity is lost")
		elif self.status == 'm' and self.missed_reason is None:
			raise ValueError("You forget to define the reasons as the opportunity is lost")
		elif self.status == 's' and self.missed_notes is not None:
			raise ValueError("Status is success, so please remove the missed notes of missing opportunity")
		super().save(*args, **kwargs)
