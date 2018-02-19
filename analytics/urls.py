from django.conf.urls import url
from . import views


app_name = 'analytics'
urlpatterns = [
	url(r'login/$', views.LoginView.as_view(), name='login_user'),
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'budget_view/$', views.BudgetView.as_view(), name='budget_view'),
	url(r'budget_dashboard/$', views.BudgetDashboardView.as_view(), name='budget_dashboard'),
	url(r'account_trends/$', views.AccountsTrendSummaryView.as_view(), name='account_trends_summary'),
	url(r'account_trends_detail/$', views.AccountsTrendDetailView.as_view(), name='account_trends_detail'),
	url(r'account_trends_account/$', views.AccountsTrendAccountView.as_view(), name='account_trends_account'),
	url(r'cost_center_trends$', views.CostCenterTrendView.as_view(), name='cost_center_trends'),
	url(r'mrgn_revenues_expense/$', views.MrgnRevenuesExpenses.as_view(), name='mrgn_revenues_expense'),
	url(r'model_view/$', views.ModelView.as_view(), name='model_view'),

	url(r'test/$', views.test, name='test'),
	url(r'test2/$', views.test2, name='test2'),
	url(r'model_record_view/$', views.ModelRecordView.as_view(), name='model_record_view'),
]
