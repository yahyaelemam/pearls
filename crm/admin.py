from django.contrib import admin
from django.contrib import messages
from .models import *
from django.forms import Textarea
# Register your models here.


@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ('country_id', 'country', )
    readonly_fields = ['country_id', ]


@admin.register(States)
class StatesAdmin(admin.ModelAdmin):
    list_display = ('state_id', 'country', 'state', )
    list_filter = ['country__country']
    list_select_related = ['country', ]
    readonly_fields = ['state_id', ]


@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ('city_id', 'city', 'country', 'state', )
    list_filter = ['state__country__country', 'state__state', ]
    list_select_related = ['state', ]
    readonly_fields = ['city_id', ]


@admin.register(CustomersIndustries)
class CustomersIndustriesAdmin(admin.ModelAdmin):
    list_display = ('customer_industry', )
    ordering = ['customer_industry', ]
    search_fields = ['customer_industry', ]


@admin.register(CustomersCategories)
class CustomersCategoriesAdmin(admin.ModelAdmin):
    list_display = ('customer_category', )
    ordering = ['customer_category', ]
    search_fields = ['customer_category', ]


@admin.register(SalesAgents)
class SalesAgentsAdmin(admin.ModelAdmin):
    list_display = ('sale_agent', 'user', 'company', 'mobile_no',)
    ordering = ['company', 'user', ]
    list_select_related = ['user', 'company', ]
    search_fields = ['sale_agent', 'mobile_no', ]
    list_filter = ['company__company_name']


class CustomersDetailsInline(admin.StackedInline):
    model = CustomersDetails
    extra = 1
    fieldsets = (
        (None, {'fields': ('contact_person_name', 'contact_person_phone')}),
        ('Social Media Information', {'fields': ('contact_person_facebook', 'contact_person_linkedin',
                                                 'contact_person_instagram')}),
        ('Other Information', {'fields': ('registration_date', 'notes', 'account')}),
        (None, {'fields': ('status', 'user')})
    )
    readonly_fields = ['user']
    list_select_related = ['customer']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 5,
                   'cols': 45})},
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["initial"] = request.user
        return super(CustomersDetailsInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if datetime.datetime.strftime(obj.registration_date) > datetime.datetime.today():
            messages.add_message(request, messages.ERROR,
                                 'Can not register date of %s because, date can not be a future date' % str(obj.registration_date))
        else:
            obj.user = request.user
            super(CustomersDetailsInline, self).save_model(request, obj, form, change)


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):

    inlines = (CustomersDetailsInline,)
    fieldsets = (
        (None, {
            'fields': ('customer_code', 'customer_name')
        }),
        ('Category', {
            'fields': ('customer_category', 'customer_industry')
        }),
        ('Address', {
            'fields': ('website_url', 'city', 'address', 'street', 'block_no', 'building_no')
        }),
        ('Location', {
            'fields': ('location_x', 'location_y')
        }),
    )
    list_display = ['customer_code', 'customer_name', 'customer_category', 'customer_industry', 'city']
    ordering = ['customer_name', 'customer_category', 'customer_industry', ]
    list_select_related = ['user', 'customer_category', 'customer_industry', 'city']
    search_fields = ['customer_name', 'Address', 'customer_code']
    list_filter = ['city__state', 'customer_category', 'customer_industry']
    readonly_fields = ['user', ]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 7,
                   'cols': 45})},
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["initial"] = request.user
        return super(CustomersAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(CustomersAdmin, self).save_model(request, obj, form, change)


