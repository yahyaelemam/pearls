from django.conf.urls import url
from django.contrib import admin
from . import views


app_name = 'crm'
urlpatterns = [
	url(
		r'^$',
		views.IndexView.as_view(), name='index'
	),
	url(
		r'model_object/(?P<report_id>\w{0,50})/$',
		views.model_object, name='model_object'
	),
	url(
		r'model_view/(?P<report_id>\w{0,50})/$',
		views.ModelView.as_view(), name='model_view'
	),
	url(
		r'model_record_add/(?P<report_id>\w{0,50})/add/$',
		views.model_record_add, name='model_record_add'
	),
	url(
		r'model_record_view/(?P<report_id>\w{0,50})/(?P<pk_id>\d+)/',
		views.ModelRecordView.as_view(), name='model_record_view'
	),
	url(
		r'model_record_save/$',
		views.model_record_save, name='model_record_save'
	),
	url(
		r'model_record_delete/(?P<report_id>\w{0,50})/(?P<pk_id>\d+)/delete/$',
		views.model_record_delete, name='model_record_delete'
	),
	url(
		r'customers/(?P<pk_id>\d+)/',
		views.CustomersView.as_view(), name='customers'
	),
	url(
		r'customer_detail_add/(?P<customer_id>\d+)/',
		views.customer_detail_add, name='customer_detail_add'
	),url(
		r'customer_status_rate_add/(?P<customer_id>\d+)/',
		views.customer_status_rate_add, name='customer_status_rate_add'
	),
	url(
		r'customer_detail_save/$',
		views.customer_detail_save, name='customer_detail_save'
	),
	url(
		r'customer_status_rate_save/$',
		views.customer_status_rate_save, name='customer_status_rate_save'
	),
	url(
		r'customer_status_rate_update/(?P<pk_id>\d+)/',
		views.customer_status_rate_update, name='customer_status_rate_update'
	),
	url(
		r'customer_detail_delete/$',
		views.customer_detail_delete, name='customer_detail_delete'
	),
	url(
		r'customer_status_rate_delete/$',
		views.customer_status_rate_delete, name='customer_status_rate_delete'
	),
	url(
		r'customer_detail_update/(?P<pk_id>\d+)/',
		views.customer_detail_update, name='customer_detail_update'
	),
	url(
		r'customers_event_update/(?P<pk_id>\d+)/',
		views.customers_event_update, name='customers_event_update'
	),
	url(
		r'customers_event_add/(?P<customers>\w{0,50})/$',
		views.customers_event_add, name='customers_event_add'
	),
	url(
		r'customers_event_save/$', views.customers_event_save, name='customers_event_save'
	),
	url(
		r'customers_events/$', views.CustomersActivityView.as_view(), name='customers_events'
	),
	url(
		r'customers_event_actions_add/(?P<activity_id>\d+)/',
		views.customers_event_actions_add, name='customers_event_actions_add'
	),
	url(
		r'customers_event_actions_save/$',
		views.customers_event_actions_save, name='customers_event_actions_save'
	),
	url(
		r'customers_event_actions_view/(?P<pk_id>\d+)/',
		views.customers_event_actions_view, name='customers_event_actions_view'
	),
	url(
		r'opportunity_add/(?P<customers>\w{0,50})/$',
		views.opportunity_add, name='opportunity_add'
	),
	url(
		r'opportunity_save/$', views.opportunity_save, name='opportunity_save'
	),
	url(
		r'opportunity_update/(?P<pk_id>\d+)/',
		views.opportunity_update, name='opportunity_update'
	),
	url(
		r'opportunities_calendar/$', views.OpportunitiesCalendarView.as_view(), name='opportunities_calendar'
	),
	url(
		r'customer_budget_add/(?P<customers>\w{0,50})/$',
		views.customer_budget_add, name='customer_budget_add'
	),
	url(
		r'customer_budget_save/$',
		views.customer_budget_save, name='customer_budget_save'
	),
	url(
		r'customer_budget_update/(?P<pk_id>\d+)/',
		views.customer_budget_update, name='customer_budget_update'

	),

	url(
		r'test/$', views.test, name='test'
	),
]



