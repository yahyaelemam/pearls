from django.contrib import admin
from .models import *
from django.contrib import messages


class MyAdminSite:
	admin.AdminSite.site_header = 'Pearls'


@admin.register(UsersSettings)
class UsersSettingsAdmin(admin.ModelAdmin):
	list_display = ('user', 'photo', )
	list_filter = ['user__username', ]
	list_select_related = ['user', ]
	readonly_fields = ['user', ]

	def save_model(self, request, obj, form, change):
		from pearls.settings import MEDIA_ROOT
		from analytics.models import UsersSettings
		import os
		obj.user = request.user
		new_photo = obj.photo.name
		if UsersSettings.objects.filter(user_id=request.user.id).count() > 0:
			current_photo = UsersSettings.objects.get(user_id=request.user.id).photo
			if current_photo.name != new_photo:
				os.remove(MEDIA_ROOT + '/' + str(current_photo.name))
		super(UsersSettingsAdmin, self).save_model(request, obj, form, change)

	def get_queryset(self, request):
		qs = super(UsersSettingsAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		else:
			return qs.filter(user=request.user)

	def has_add_permission(self, request):
		from analytics.models import UsersSettings
		if UsersSettings.objects.filter(user_id=request.user.id).count() > 0:
			return False
		else:
			return True


@admin.register(UsersCompanies)
class UsersCompaniesAdmin(admin.ModelAdmin):
	list_display = (
		'company', 'user',
	)
	list_filter = [
		'company__company_name', 'user__username',
	]
	list_select_related = [
		'company',
	]


@admin.register(EtlSchedule)
class EtlSchedule(admin.ModelAdmin):
	list_display = (
		'data_type', 'schedule_time',
	)
	list_filter = [
		'data_type', 'schedule_time',
	]


@admin.register(EtlLog)
class EtlLog(admin.ModelAdmin):
	list_display = (
		'log_time', 'type_id', 'company', 'description',
	)
	list_filter = [
		'type_id',
	]

	def has_delete_permission(self, request, obj=None):
		# Disable delete
		return False

	def has_add_permission(self, request, obj=None):
		return False


class CompaniesAdmin(admin.ModelAdmin):
	list_display = (
		'company_id', 'company_name',
	)
	list_filter = [
		'company_id', 'company_name',
	]


admin.site.register(Companies, CompaniesAdmin)


class AccountsTypesAdmin(admin.ModelAdmin):
	list_display = (
		'account_type_id', 'account_type_name',
	)
	list_filter = [
		'account_type_id', 'account_type_name',
	]


admin.site.register(AccountsTypes, AccountsTypesAdmin)


@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
	exclude = ('id',)
	list_display = (
		'company', 'account_id', 'account_name', 'account_type', 'kind', 'active',
	)
	list_filter = [
		'company__company_name', 'account_type', 'active', 'kind',
	]
	list_display_links = (
		'company', 'account_id', 'account_name', 'account_type',
	)
	list_select_related = [
		'account_type', 'company',
	]
	search_fields = ['account_name']
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		# Disable delete
		return False

	def has_add_permission(self, request, obj=None):
		return False

	def get_queryset(self, request):
		"""
		Override the initial data based on user companies
		:param request:
		:return:
		"""
		qs = super(AccountsAdmin, self).get_queryset(request)
		companies_obj = UsersCompanies.objects.filter(user=request.user.id)
		return qs.filter(company__in=[obj.company for obj in companies_obj])

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		companies_obj = UsersCompanies.objects.filter(user=request.user.id)
		if db_field.name == "company":
			kwargs["queryset"] = Companies.objects.filter(company_id__in=[obj.company_id for obj in companies_obj])
			kwargs["initial"] = kwargs["queryset"][0]
		return super(AccountsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class BudgetYearAdmin(admin.ModelAdmin):
	list_display = ['year', 'status']
	ordering = ['year']


admin.site.register(BudgetYear, BudgetYearAdmin)


def make_approved(modeladmin, request, queryset):
	for obj in queryset:
		if obj.status == 's':
			queryset.update(status='a')
			messages.add_message(request, messages.INFO, '%s has been approved' % obj)
		else:
			messages.add_message(request, messages.ERROR,
								 'Can not save %s because, only can approve save status' % obj)


make_approved.short_description = "Approved items/items"


def make_delete(modeladmin, request, queryset):
	for obj in queryset:
		if obj.status == 'd':
			obj.delete()
		else:
			messages.add_message(request, messages.ERROR, 'Can not delete %s because, only can delete draft status' % obj)


make_delete.short_description = "Delete item/items"


def make_save(modeladmin, request, queryset):
	for obj in queryset:
		if obj.status == 'd':
			queryset.update(status='s')
			messages.add_message(request, messages.INFO, '%s has been saved' % obj)
		else:
			messages.add_message(request, messages.ERROR, 'Can not save %s because, it is already in saved status' % obj)


make_save.short_description = "Save item/items"


class BudgetAdmin(admin.ModelAdmin):
	list_display = ['company', 'year', 'account', 'center', 'budget_amount', 'last_year', 'status']
	ordering = ['company', 'year']
	list_select_related = ['company', 'account', 'year', 'center']
	list_filter = ['company__company_name', 'status', 'account__account_type_id']
	readonly_fields = ['status']
	search_fields = ['center__center_name', 'account__account_name']
	actions = [make_approved, make_delete, make_save]

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		companies_obj = UsersCompanies.objects.filter(user=request.user.id)
		if db_field.name == "company":
			kwargs["queryset"] = Companies.objects.filter(company_id__in=[obj.company_id for obj in companies_obj])
			kwargs["initial"] = kwargs["queryset"][0]
		if db_field.name == "account":
			kwargs["queryset"] = Accounts.objects.filter(kind=False, active=True, company_id__in=[obj.company_id for obj in companies_obj])
		if db_field.name == "year":
			kwargs["initial"] = BudgetYear.objects.filter(status='a')[0]
		if db_field.name == "center":
			kwargs["queryset"] = Centers.objects.filter(kind=False, active=True, company_id__in=[obj.company_id for obj in companies_obj]).exclude(center_id='0')
		return super(BudgetAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def get_queryset(self, request):
		qs = super(BudgetAdmin, self).get_queryset(request)
		companies_obj = UsersCompanies.objects.filter(user=request.user.id)
		return qs.filter(company__in=[obj.company for obj in companies_obj])

	def save_model(self, request, obj, form, change):
		if obj.status in('s', 'a'):
			messages.add_message(request, messages.ERROR,
								 'Can change %s because, only can change draft status' % obj)
		elif obj.jan_budget_amount != 0:
			if obj.feb_budget_amount == 0 and obj.id is None:
				obj.feb_budget_amount = obj.jan_budget_amount

			if obj.mar_budget_amount == 0 and obj.id is None:
				obj.mar_budget_amount = obj.jan_budget_amount

			if obj.apr_budget_amount == 0 and obj.id is None:
				obj.apr_budget_amount = obj.jan_budget_amount

			if obj.may_budget_amount == 0 and obj.id is None:
				obj.may_budget_amount = obj.jan_budget_amount

			if obj.jun_budget_amount == 0 and obj.id is None:
				obj.jun_budget_amount = obj.jan_budget_amount

			if obj.jul_budget_amount == 0 and obj.id is None:
				obj.jul_budget_amount = obj.jan_budget_amount

			if obj.aug_budget_amount == 0 and obj.id is None:
				obj.aug_budget_amount = obj.jan_budget_amount

			if obj.sep_budget_amount == 0 and obj.id is None:
				obj.sep_budget_amount = obj.jan_budget_amount

			if obj.oct_budget_amount == 0 and obj.id is None:
				obj.oct_budget_amount = obj.jan_budget_amount

			if obj.nov_budget_amount == 0 and obj.id is None:
				obj.nov_budget_amount = obj.jan_budget_amount

			if obj.dec_budget_amount == 0 and obj.id is None:
				obj.dec_budget_amount = obj.jan_budget_amount

			super(BudgetAdmin, self).save_model(request, obj, form, change)

	def has_delete_permission(self, request, obj=None):
		# Disable delete
		return False

	def get_actions(self, request):
		# Disable delete
		actions = super(BudgetAdmin, self).get_actions(request)
		if request.user.groups.filter(name='budget_approved').exists():
			pass
		else:
			del actions['make_approved']
		if request.user.groups.filter(name='budget_saved').exists():
			pass
		else:
			del actions['make_save']
		if request.user.groups.filter(name='budget_delete').exists():
			pass
		else:
			del actions['make_delete']
		del actions['delete_selected']
		return actions


admin.site.register(Budget, BudgetAdmin)


@admin.register(Centers)
class CentersAdmin(admin.ModelAdmin):
	exclude = ('id',)
	list_display = (
		'company', 'center_id', 'center_name', 'kind', 'active',
	)
	list_filter = [
		'company__company_name', 'active', 'kind',
	]
	list_display_links = (
		'company', 'center_id', 'center_name',
	)
	list_select_related = [
		'company',
	]
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		# Disable delete
		return False

	def has_add_permission(self, request, obj=None):
		return False

	def get_queryset(self, request):
		"""
		Override the initial data based on user companies
		:param request:
		:return:
		"""
		qs = super(CentersAdmin, self).get_queryset(request)
		companies_obj = UsersCompanies.objects.filter(user=request.user.id)
		return qs.filter(company__in=[obj.company for obj in companies_obj])

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		companies_obj = UsersCompanies.objects.filter(user=request.user.id)
		if db_field.name == "company":
			kwargs["queryset"] = Companies.objects.filter(company_id__in=[obj.company_id for obj in companies_obj])
			kwargs["initial"] = kwargs["queryset"][0]
		return super(CentersAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class HRBudgetAdmin(admin.ModelAdmin):
	list_display = ['company', 'year', 'center', 'staff_count', 'staff_actual', 'status']
	ordering = ['company', 'year']
	list_select_related = ['company', 'year', 'center']
	list_filter = ['company__company_name', 'status']
	readonly_fields = ['status']
	search_fields = ['center__center_name']
	actions = [make_approved, make_delete, make_save]
	list_per_page = 10

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		companies_obj = UsersCompanies.objects.filter(user=request.user.id)
		if db_field.name == "company":
			kwargs["queryset"] = Companies.objects.filter(company_id__in=[obj.company_id for obj in companies_obj])
			kwargs["initial"] = kwargs["queryset"][0]
		if db_field.name == "year":
			kwargs["initial"] = BudgetYear.objects.filter(status='a')[0]
		if db_field.name == "center":
			kwargs["queryset"] = Centers.objects.filter(kind=False, active=True, company_id__in=[obj.company_id for obj in companies_obj]).exclude(center_id='0')
		return super(HRBudgetAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def get_queryset(self, request):
		qs = super(HRBudgetAdmin, self).get_queryset(request)
		companies_obj = UsersCompanies.objects.filter(user=request.user.id)
		return qs.filter(company__in=[obj.company for obj in companies_obj])

	def save_model(self, request, obj, form, change):
		if obj.status in('s', 'a'):
			messages.add_message(request, messages.ERROR,
								 'Can change %s because, only can change draft status' % obj)
		elif obj.staff_count != 0:
			super(HRBudgetAdmin, self).save_model(request, obj, form, change)

	def has_delete_permission(self, request, obj=None):
		# Disable delete
		return False

	def get_actions(self, request):
		# Disable delete
		actions = super(HRBudgetAdmin, self).get_actions(request)
		if request.user.groups.filter(name='budget_approved').exists():
			pass
		else:
			del actions['make_approved']
		if request.user.groups.filter(name='budget_saved').exists():
			pass
		else:
			del actions['make_save']
		if request.user.groups.filter(name='budget_delete').exists():
			pass
		else:
			del actions['make_delete']
		del actions['delete_selected']
		return actions


admin.site.register(HRBudget, HRBudgetAdmin)


@admin.register(KpiAccount)
class KpiAccountAdmin(admin.ModelAdmin):
	list_display = (
		'company', 'type_id', 'account',
	)
	list_select_related = ['company', 'account', ]
	list_display_links = (
		'company', 'type_id', 'account',
	)
	list_filter = [
		'company', 'type_id',
	]

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		companies_obj = UsersCompanies.objects.filter(user=request.user.id)
		if db_field.name == "company":
			kwargs["queryset"] = Companies.objects.filter(company_id__in=[obj.company_id for obj in companies_obj])
			kwargs["initial"] = kwargs["queryset"][0]
		if db_field.name == "account":
			kwargs["queryset"] = Accounts.objects.filter(company_id__in=[obj.company_id for obj in companies_obj])
		return super(KpiAccountAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def get_queryset(self, request):
		qs = super(KpiAccountAdmin, self).get_queryset(request)
		companies_obj = UsersCompanies.objects.filter(user=request.user.id)
		return qs.filter(company__in=[obj.company for obj in companies_obj])


@admin.register(KpiCenter)
class KpiCenterAdmin(admin.ModelAdmin):
	list_display = (
		'company', 'type_id', 'center',
	)
	list_select_related = ['company', 'center', ]
	list_display_links = (
		'company', 'type_id', 'center',
	)
	list_filter = [
		'company', 'type_id',
	]

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		companies_obj = UsersCompanies.objects.filter(user=request.user.id)
		if db_field.name == "company":
			kwargs["queryset"] = Companies.objects.filter(company_id__in=[obj.company_id for obj in companies_obj])
			kwargs["initial"] = kwargs["queryset"][0]
		if db_field.name == "center":
			kwargs["queryset"] = Centers.objects.filter(company_id__in=[obj.company_id for obj in companies_obj])
		return super(KpiCenterAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def get_queryset(self, request):
		qs = super(KpiCenterAdmin, self).get_queryset(request)
		companies_obj = UsersCompanies.objects.filter(user=request.user.id)
		return qs.filter(company__in=[obj.company for obj in companies_obj])

'''
	def save_formset(self, request, form, formset, change):
		instances = formset.save(commit=False)
		for instance in instances:
			# Do something with `instance`
			instance.save()
		formset.save_m2m()
		
		
		
		-------------------
		
		to ad url
		
		
	add 'url_fld' to list_display
	def url_fld(self, obj):
		from django.utils.html import format_html
		return format_html("<a href='http://www.google.com'> Google.com </a>")
	url_fld.allow_tag = True
	url_fld.short_description = "test   "
	
'''






