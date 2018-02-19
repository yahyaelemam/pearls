from django.db import connection
import django.forms
from analytics.procedures import fn_get_user_lang
from django.contrib.contenttypes.models import ContentType


models_objects = {
	'customers':
		{
			'app_name': 'crm',
			'model_name': 'customers',
			'title': {'en': 'Customers', 'ar': 'العملاء'},
			'record_url': '/crm/customers/',
			'all_fields': {
				'customer_id': {'en': 'ID', 'ar': 'الرقم', 'search_criteria': '__exact'},
				'customer_code': {'en': 'Code', 'ar': 'الرقم', 'search_criteria': '__contains'},
				'customer_name': {'en': 'Customer Name', 'ar': 'الاسم', 'search_criteria': '__contains'},
				'customer_category': {'en': 'Category', 'ar': 'التصنيف', 'search_criteria': '__exact'},
				'customer_industry': {'en': 'Industry', 'ar': 'النشاط', 'search_criteria': '__exact'},
				'city': {'en': 'City', 'ar': 'المدينة', 'search_criteria': '__exact'},
				'website_url': {'en': 'Website URL', 'ar': 'الموقع الإلكتروني', 'search_criteria': '__contains'},
				'address': {'en': 'Address', 'ar': 'العنوان', 'search_criteria': '__contains'},
				'street': {'en': 'Street', 'ar': 'الشارع', 'search_criteria': '__contains'},
				'block_no': {'en': 'Block NO', 'ar': 'المربع', 'search_criteria': '__contains'},
				'building_no': {'en': 'Building NO', 'ar': 'البناية', 'search_criteria': '__contains'},
				'location_x': {'en': 'Latitude', 'ar': 'الموقع الجغرافي الرأسي', 'search_criteria': '__exact'},
				'location_y': {'en': 'Longitude', 'ar': 'الموقع الجغرافي الأفقي', 'search_criteria': '__exact'},
				'user': {'en': 'User', 'ar': 'المستخدم', 'search_criteria': '__exact'},

			},
			'model_fields': [
				'customer_code', 'customer_name', 'customer_category', 'customer_industry', 'city'
			],
			'search_fields': [
				'customer_code', 'customer_name', 'customer_category', 'customer_industry', 'city'
			],
			'edit_form_read_only_fields': ['user'],
			'action': {
				'delete': {'en': 'Delete selected records', 'ar': 'حذف ما تم اختياره', 'status_from': 'd', 'status_to': 'a'},
				'event': {'en': 'Add event/activity', 'ar': 'تسجيل تواصل ونشاط', 'status_from': 'd', 'status_to': 'a'},
				'opportunity': {'en': 'Add opportunity', 'ar': 'تسجيل فرصة جديدة', 'status_from': '', 'status_to': ''},
				'budget': {'en': 'Add budget', 'ar': 'تسجيل ميزانية', 'status_from': '', 'status_to': ''}
			}
		},
	'customersstatus':
		{
			'app_name': 'crm',
			'model_name': 'customersstatus',
			'title': {'en': 'Customers Rate and Status', 'ar': 'حالة وتقييم العملاء'},
			'record_url': '/crm/customer_status_rate_update/',
			'all_fields': {
				'customer': {'en': 'Customer', 'ar': 'العميل', 'search_criteria': '__exact'},
				'company': {'en': 'Company', 'ar': 'الشركة', 'search_criteria': '__exact'},
				'status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__exact'},
				'rate': {'en': 'Rate', 'ar': 'التقييم', 'search_criteria': '__exact'},
				'event_date': {'en': 'Date', 'ar': 'التاريخ', 'search_criteria': '__exact'},
				'user': {'en': 'User', 'ar': 'المستخدم', 'search_criteria': '__exact'},
				'current_status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__exact'},
				'current_rate': {'en': 'Rate', 'ar': 'التقييم', 'search_criteria': '__exact'},

			},
			'model_fields': [
				'customer', 'company', 'current_status', 'current_rate', 'event_date', 'user'
			],
			'search_fields': [
				'company', 'rate', 'status',
			],
			'edit_form_read_only_fields': ['user', 'status', 'event_date'],
			'action': {
				'delete': {
					'en': 'Delete selected records',
					'ar': 'حذف ما تم اختياره',
					'status_from': 'd', 'status_to': 'a'
				},

			}
		},
	'customersdetails':
		{
			'app_name': 'crm',
			'model_name': 'customersdetails',
			'title': {'en': 'Customers Contacts', 'ar': 'تفاصيل العملاء'},
			'record_url': '/crm/customer_detail_update/',
			'all_fields': {
				'customer_detail_id': {'en': 'ID', 'ar': 'الرقم', 'search_criteria': '__exact'},
				'customer': {'en': 'Customer ID', 'ar': 'العميل', 'search_criteria': '__exact'},
				'contact_person_name': {'en': 'Contact Name', 'ar': 'الاسم', 'search_criteria': '__contains'},
				'contact_person_phone': {'en': 'Phone', 'ar': 'التلفوت', 'search_criteria': '__contains'},
				'contact_person_facebook': {'en': '<i class="fa fa-facebook-square"></i> Facebook', 'ar': '<i class="fa fa-facebook-square"></i> فيسبوك', 'search_criteria': '__contains'},
				'contact_person_linkedin': {'en': '<i class="fa fa-linkedin-square"></i> LinkedIn', 'ar': '<i class="fa fa-linkedin-square"></i> لينكدان', 'search_criteria': '__contains'},
				'contact_person_instagram': {'en': '<i class="fa fa-instagram"></i> Instagram', 'ar': '<i class="fa fa-instagram"></i> انستقرام', 'search_criteria': '__contains'},
				'registration_date': {'en': 'Registration Date', 'ar': 'تاريخ التسجيل', 'search_criteria': '__contains'},
				'notes': {'en': 'Notes', 'ar': 'ملاحظات', 'search_criteria': '__contains'},
				'account': {'en': 'Account', 'ar': 'الحساب', 'search_criteria': '__exact'},
				'company': {'en': 'Company', 'ar': 'الشركة', 'search_criteria': '__exact'},
				'user': {'en': 'User', 'ar': 'المستخدم', 'search_criteria': '__exact'},

			},
			'model_fields': [
				'contact_person_name', 'registration_date', 'account', 'company',
			],
			'search_fields': [
				'account', 'contact_person_name', 'registration_date', 'company', 'user',
			],
			'edit_form_read_only_fields': ['user', ],
			'action': {
				'delete': {'en': 'Delete selected records', 'ar': 'حذف ما تم اختياره', 'status_from': 'd', 'status_to': 'a'},
			}
		},
	'customerscategories':
		{
			'app_name': 'crm',
			'model_name': 'customerscategories',
			'title': {'en': 'Customers Categories', 'ar': 'تصنيف العملاء'},
			'all_fields': {
				'customer_category_id': {'en': 'Category ID', 'ar': 'رقم التصنيف', 'search_criteria': '__exact'},
				'customer_category': {'en': 'Category', 'ar': 'التصنيف', 'search_criteria': '__contains'}
			},
			'model_fields': [
				'customer_category_id', 'customer_category',
			],
			'search_fields': [
				'customer_category_id', 'customer_category',
			],
			'edit_form_read_only_fields': [],
			'action': {
				'delete': {'en': 'Delete selected records', 'ar': 'حذف ما تم اختياره', 'status_from': 'd', 'status_to': 'a'},

			},
		},
	'customersindustries':
		{
			'app_name': 'crm',
			'model_name': 'customersindustries',
			'title': {'en': 'Customer Industry', 'ar': 'أنشطة العملاء'},
			'all_fields': {
				'customer_industry_id': {'en': 'Industry ID', 'ar': 'رقم النشاط', 'search_criteria': '__exact'},
				'customer_industry': {'en': 'Industry', 'ar': 'النشاط', 'search_criteria': '__contains'}
			},
			'model_fields': [
				'customer_industry_id', 'customer_industry',
			],
			'search_fields': [
				'customer_industry_id', 'customer_industry',
			],
			'edit_form_read_only_fields': [],
			'action': {
				'delete': {'en': 'Delete selected records', 'ar': 'حذف ما تم اختياره', 'status_from': 'd', 'status_to': 'a'},

			}
		},
	'countries':
		{
			'app_name': 'crm',
			'model_name': 'countries',
			'title': {'en': 'Countries', 'ar': 'الدول'},
			'all_fields': {
				'country_id': {'en': 'Country ID', 'ar': 'رقم الدولة', 'search_criteria': '__exact'},
				'country': {'en': 'Country', 'ar': 'اسم الدولة', 'search_criteria': '__contains'}
			},
			'model_fields': [
				'country_id', 'country',
			],
			'search_fields': [
				'country_id', 'country',
			],
			'edit_form_read_only_fields': [],
			'action': {
				'delete': {'en': 'Delete selected records', 'ar': 'حذف ما تم اختياره', 'status_from': 'd', 'status_to': 'a'},

			}
		},
	'states':
		{
			'app_name': 'crm',
			'model_name': 'states',
			'title': {'en': 'States', 'ar': 'الولايات'},
			'all_fields': {
				'state_id': {'en': 'State ID', 'ar': 'رقم الولاية', 'search_criteria': '__exact'},
				'country': {'en': 'Country', 'ar': 'اسم الدولة', 'search_criteria': '__exact'},
				'state': {'en': 'Country', 'ar': 'اسم الولاية', 'search_criteria': '__contains'}
			},
			'model_fields': [
				'state_id', 'country', 'state'
			],
			'search_fields': [
				'country', 'state',
			],
			'edit_form_read_only_fields': [],
			'action': {
				'delete': {'en': 'Delete selected records', 'ar': 'حذف ما تم اختياره', 'status_from': 'd', 'status_to': 'a'},

			}
		},
	'cities':
		{
			'app_name': 'crm',
			'model_name': 'cities',
			'title': {'en': 'Cities', 'ar': 'المدن'},
			'all_fields': {
				'city_id': {'en': 'City ID', 'ar': 'رقم المدينة', 'search_criteria': '__exact'},
				'state': {'en': 'State', 'ar': 'اسم الولاية', 'search_criteria': '__exact'},
				'city': {'en': 'City', 'ar': 'اسم المدينة', 'search_criteria': '__contains'}
			},
			'model_fields': [
				'city_id', 'state', 'city'
			],
			'search_fields': [
				'state', 'city'
			],
			'edit_form_read_only_fields': [],
			'action': {
				'delete': {'en': 'Delete selected records', 'ar': 'حذف ما تم اختياره', 'status_from': 'd', 'status_to': 'a'},

			}
		},
	'salesagents':
		{
			'app_name': 'crm',
			'model_name': 'salesagents',
			'title': {'en': 'Sales Agents', 'ar': 'موظفي التسويق'},
			'all_fields': {
				'sale_agent_id': {'en': 'ID', 'ar': 'الرقم', 'search_criteria': '__exact'},
				'user': {'en': 'User', 'ar': 'اسم المستخدم', 'search_criteria': '__exact'},
				'company': {'en': 'Company', 'ar': 'الشركة', 'search_criteria': '__exact'},
				'sale_agent': {'en': 'Agent Name', 'ar': 'اسم موظف التسويق', 'search_criteria': '__contains'},
				'mobile_no': {'en': 'Mobile No', 'ar': 'رقم الموبايل', 'search_criteria': '__contains'}
			},
			'model_fields': [
				'company', 'sale_agent', 'user', 'mobile_no'
			],
			'search_fields': [
				'company', 'sale_agent', 'user', 'mobile_no'
			],
			'edit_form_read_only_fields': [],
			'action': {
				'delete': {'en': 'Delete selected records', 'ar': 'حذف ما تم اختياره', 'status_from': 'd', 'status_to': 'a'},

			}
		},
	'categoriesbudget':
		{
			'app_name': 'crm',
			'model_name': 'categoriesbudget',
			'title': {'en': 'Categories Budget', 'ar': 'الميزانية علي مستوي التصنيفات'},
			'all_fields': {
				'customer_category': {'en': 'Customer Category', 'ar': 'تصنيف العميل', 'search_criteria': '__exact'},
				'company': {'en': 'Company', 'ar': 'الشركة', 'search_criteria': '__exact'},
				'year': {'en': 'Year', 'ar': 'السنة', 'search_criteria': '__exact'},
				'new_customers': {'en': 'New Customers', 'ar': 'عدد العملاء الجدد', 'search_criteria': '__exact'},
				'budget_amount': {'en': 'Budget Amount', 'ar': 'مبلغ الميزانية', 'search_criteria': '__exact'},
				'status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__exact'},
				'current_status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__exact'},
				'amount': {'en': 'Budget Amount', 'ar': 'مبلغ الميزانية', 'search_criteria': '__exact'},

			},
			'model_fields': [
				'customer_category', 'company', 'new_customers', 'year', 'amount', 'current_status'
			],
			'search_fields': [
				'customer_category', 'company', 'year', 'status'
			],
			'edit_form_read_only_fields': ['status'],
			'action': {
				'delete': {
					'en': 'Delete selected records',
					'ar': 'حذف ما تم اختياره',
					'status_from': 'd', 'status_to': 'a'
				},
				'save': {
					'en': 'Change selected records to Saved',
					'ar': 'تحويل حالة ماتم اختياره من جديد إلى مراجعه',
					'status_from': 'd', 'status_to': 's'
				},
				'approve': {
					'en': 'Change selected records to Approved',
					'ar': 'تحويل حالة ماتم اختياره إلى مصدقة',
					'status_from': 's', 'status_to': 'a'
				},

			}
		},
	'industriesbudget':
		{
			'app_name': 'crm',
			'model_name': 'industriesbudget',
			'title': {'en': 'Industries Budget', 'ar': 'الميزانية - النشاط التجاري'},
			'all_fields': {
				'customer_industry': {'en': 'Customer Industry', 'ar': 'النشاط التجاري للعميل', 'search_criteria': '__exact'},
				'company': {'en': 'Company', 'ar': 'الشركة', 'search_criteria': '__exact'},
				'year': {'en': 'Year', 'ar': 'السنة', 'search_criteria': '__exact'},
				'new_customers': {'en': 'New Customers', 'ar': 'عدد العملاء الجدد', 'search_criteria': '__exact'},
				'budget_amount': {'en': 'Budget Amount', 'ar': 'مبلغ الميزانية', 'search_criteria': '__exact'},
				'status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__exact'},
				'current_status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__exact'},
				'amount': {'en': 'Budget Amount', 'ar': 'مبلغ الميزانية', 'search_criteria': '__exact'},


			},
			'model_fields': [
				'customer_industry', 'company', 'new_customers', 'year', 'amount', 'current_status'
			],
			'search_fields': [
				'customer_industry', 'company', 'year', 'status'
			],
			'edit_form_read_only_fields': ['status'],
			'action': {
				'delete': {
					'en': 'Delete selected records',
					'ar': 'حذف ما تم اختياره',
					'status_from': 'd', 'status_to': 'a'
				},
				'save': {
					'en': 'Change selected records to Saved',
					'ar': 'تحويل حالة ماتم اختياره من جديد إلى مراجعه',
					'status_from': 'd', 'status_to': 's'
				},
				'approve': {
					'en': 'Change selected records to Approved',
					'ar': 'تحويل حالة ماتم اختياره إلى مصدقة',
					'status_from': 's', 'status_to': 'a'
				},

			}
		},
	'salesagentsbudget':
		{
			'app_name': 'crm',
			'model_name': 'salesagentsbudget',
			'title': {'en': 'Sales Agents Budget', 'ar': 'الميزانية - موظفي التسويق'},
			'all_fields': {
				'sale_agent_id': {'en': 'Sale Agent', 'ar': 'مندوب التسويق', 'search_criteria': '__exact'},
				'customer_category': {'en': 'Customer Category', 'ar': 'تصنيف العميل', 'search_criteria': '__exact'},
				'customer_industry': {'en': 'Customer Industry', 'ar': 'النشاط التجاري للعميل', 'search_criteria': '__exact'},
				'year': {'en': 'Year', 'ar': 'السنة', 'search_criteria': '__exact'},
				'new_customers': {'en': 'New Customers', 'ar': 'عدد العملاء الجدد', 'search_criteria': '__exact'},
				'budget_amount': {'en': 'Budget Amount', 'ar': 'مبلغ الميزانية', 'search_criteria': '__exact'},
				'status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__exact'},
				'amount': {'en': 'Status', 'ar': 'المبلغ', 'search_criteria': '__exact'},
				'current_status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__exact'}

			},
			'model_fields': [
				'sale_agent_id', 'customer_category', 'customer_industry', 'year', 'amount', 'new_customers', 'current_status',
			],
			'search_fields': [
				'sale_agent_id', 'year', 'customer_category', 'customer_industry', 'status'
			],
			'edit_form_read_only_fields': ['status'],
			'action': {
				'delete': {
					'en': 'Delete selected records',
					'ar': 'حذف ما تم اختياره',
					'status_from': 'd', 'status_to': 'a'
				},
				'save': {
					'en': 'Change selected records to Saved',
					'ar': 'تحويل حالة ماتم اختياره من جديد إلى مراجعه',
					'status_from': 'd', 'status_to': 's'
				},
				'approve': {
					'en': 'Change selected records to Approved',
					'ar': 'تحويل حالة ماتم اختياره إلى مصدقة',
					'status_from': 's', 'status_to': 'a'
				},

			}
		},
	'customersbudget':
		{
			'app_name': 'crm',
			'model_name': 'customersbudget',
			'title': {'en': 'Customers Budget', 'ar': 'الميزانية - العملاء'},
			'record_url': '/crm/customer_budget_update/',
			'add_new': False,
			'all_fields': {
				'customer': {'en': 'Customer', 'ar': 'العميل', 'search_criteria': '__contains'},
				'company': {'en': 'Company', 'ar': 'الشركة', 'search_criteria': '__exact'},
				'sale_agent': {'en': 'Sale Agent', 'ar': 'مندوب التسويق', 'search_criteria': '__exact'},
				'year': {'en': 'Year', 'ar': 'السنة', 'search_criteria': '__exact'},
				'budget_amount': {'en': 'Budget Amount', 'ar': 'مبلغ الميزانية', 'search_criteria': '__exact'},
				'status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__exact'},
				'amount': {'en': 'Status', 'ar': 'المبلغ', 'search_criteria': '__exact'},
				'current_status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__exact'},
				'user': {'en': 'User', 'ar': 'المستخدم', 'search_criteria': '__exact'}
			},
			'model_fields': [
				'customer', 'company', 'sale_agent', 'year', 'amount', 'current_status',
			],
			'search_fields': [
				'customer', 'company', 'sale_agent', 'year', 'status',
			],
			'edit_form_read_only_fields': ['user', 'status'],
			'action': {
				'delete': {
					'en': 'Delete selected records',
					'ar': 'حذف ما تم اختياره',
					'status_from': 'd', 'status_to': 'a'
				},
				'save': {
					'en': 'Change selected records to Saved',
					'ar': 'تحويل حالة ماتم اختياره إلى مراجعه',
					'status_from': 'd', 'status_to': 's'
				},
				'approve': {
					'en': 'Change selected records to Approved',
					'ar': 'تحويل حالة ماتم اختياره إلى مصدقة',
					'status_from': 's', 'status_to': 'a'
				},

			}
		},
	'budgetyear':
		{
			'app_name': 'analytics',
			'model_name': 'budgetyear',
			'title': {'en': 'Budget Year', 'ar': 'سنة الميزانية'},
			'all_fields': {
				'year': {'en': 'Year', 'ar': 'السنة', 'search_criteria': '__exact'},
				'status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__exact'},
			},
			'model_fields': [
				'year', 'status',
			],
			'search_fields': [
				'year', 'status'
			],
			'edit_form_read_only_fields': [],
			'action': {
				'delete': {
					'en': 'Delete selected records',
					'ar': 'حذف ما تم اختياره',
					'status_from': 'd', 'status_to': 'a'
				},
				'Active': {
					'en': 'Change selected records to Saved',
					'ar': 'تحويل حالة ماتم اختياره من جديد إلى نشط|فاعل',
					'status_from': 'd', 'status_to': 'a'
				},
				'close': {
					'en': 'Change selected records to Closed',
					'ar': 'تحويل حالة ماتم اختياره من نشط إلى مقفلة',
					'status_from': 'a', 'status_to': 'c'
				},

			}
		},
	'activitiestypes':
		{
			'app_name': 'crm',
			'model_name': 'activitiestypes',
			'title': {'en': 'Activities Types', 'ar': 'طرق التواصل مع العملاء'},
			'all_fields': {
				'activity_type': {'en': 'Activity Type', 'ar': 'طريقة التواصل', 'search_criteria': '__contains'},
			},
			'model_fields': [
				'activity_type',
			],
			'search_fields': [
				'activity_type',
			],
			'edit_form_read_only_fields': [],
			'action': {
				'delete': {
					'en': 'Delete selected records',
					'ar': 'حذف ما تم اختياره',
					'status_from': 'd', 'status_to': 'a'
				},
			}
		},
	'customersactivities':
		{
			'app_name': 'crm',
			'model_name': 'customersactivities',
			'title': {'en': 'Customers Activities', 'ar': 'التواصل مع العملاء'},
			'record_url': '/crm/customers_event_update/',
			'add_new': False,
			'all_fields': {
				'activity_id': {'en': 'Activity ID', 'ar': 'الرقم', 'search_criteria': '__contains'},
				'activity_type': {'en': 'Activity Type', 'ar': 'نوع التواصل', 'search_criteria': '__contains'},
				'subject': {'en': 'Subject', 'ar': 'عنوان التواصل', 'search_criteria': '__contains'},
				'activity_date': {'en': 'Activity Date', 'ar': 'تاريخ التواصل', 'search_criteria': '__contains'},
				'customer': {'en': 'Customer', 'ar': 'العميل', 'search_criteria': '__contains'},
				'company': {'en': 'Company', 'ar': 'الشركة', 'search_criteria': '__exact'},
				'description': {'en': 'Description', 'ar': 'البيان', 'search_criteria': '__contains'},
				'sale_agent': {'en': 'Sale Agent', 'ar': 'موظف التسويق', 'search_criteria': '__contains'},
				'activity_reference': {'en': 'Tag #', 'ar': 'مرجع', 'search_criteria': '__contains'},
				'status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__contains'},
				'current_status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__exact'},
				'user': {'en': 'User', 'ar': 'المستخدم', 'search_criteria': '__exact'}

			},
			'model_fields': [
				'activity_type', 'subject', 'activity_date', 'customer', 'company', 'activity_reference', 'current_status',
			],
			'search_fields': [
				'activity_type', 'company', 'activity_reference', 'status', 'activity_date',
			],
			'edit_form_read_only_fields': ['user'],
			'action': {

			}
		},
	'customersactivitiesactions':
		{
			'app_name': 'crm',
			'model_name': 'customersactivitiesactions',
			'title': {'en': 'Customers Activities Actions', 'ar': 'نتائج ومخرجات التواصل مع العملاء'},
			'record_url': '/crm/customers_event_actions_view/',
			'add_new': False,
			'all_fields': {
				'activity_action_id': {'en': 'Activity Action ID', 'ar': 'الرقم', 'search_criteria': '__contains'},
				'activity_id': {'en': 'Activity Subject', 'ar': 'عنوان التواصل', 'search_criteria': '__contains'},
				'action_time': {'en': 'Action time', 'ar': 'تاريخ التواصل', 'search_criteria': '__contains'},
				'contacted_person_name': {'en': 'Contacted Person', 'ar': 'اسم المتصل عليه', 'search_criteria': '__contains'},
				'description': {'en': 'Description', 'ar': 'البيان', 'search_criteria': '__contains'},
				'sale_agent': {'en': 'Sale Agent', 'ar': 'موظف التسويق', 'search_criteria': '__contains'},
				'feedback': {'en': 'Feed-back', 'ar': 'تعليقات وتوصيات العميل', 'search_criteria': '__contains'},
				'actions': {'en': 'Actions', 'ar': 'المخرجات التي يجب اتخاذها', 'search_criteria': '__contains'},
				'actions_date': {'en': 'Actions planned Date', 'ar': 'تاريخ تنفيذ المخرجات', 'search_criteria': '__contains'},
				'status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__contains'},
				'current_status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__exact'},
				'user': {'en': 'User', 'ar': 'المستخدم', 'search_criteria': '__exact'},
				'action_date_time':  {'en': 'Action time', 'ar': 'تاريخ التواصل', 'search_criteria': '__contains'},
				'customer': {'en': 'Customer', 'ar': 'العميل', 'search_criteria': '__exact'}
			},
			'model_fields': [
				'activity_id', 'customer', 'action_date_time', 'feedback', 'actions', 'actions_date', 'current_status',
			],
			'search_fields': [
				'user', 'action_time', 'status', 'actions_date'
			],
			'edit_form_read_only_fields': ['user', 'status'],
			'action': {

			}
		},
	'missedopportunitiesreasons':
		{
			'app_name': 'crm',
			'model_name': 'missedopportunitiesreasons',
			'title': {'en': 'Missed Opportunities Reasons', 'ar': 'اسباب ضياع الفرص'},
			'all_fields': {
				'missed_reason': {'en': 'Missed Reason', 'ar': 'سبب ضياع الفرص', 'search_criteria': '__contains'},
			},
			'model_fields': [
				'missed_reason',
			],
			'search_fields': [
				'missed_reason',
			],
			'edit_form_read_only_fields': [],
			'action': {

			}
		},
	'opportunities':
		{
			'app_name': 'crm',
			'model_name': 'opportunities',
			'title': {'en': 'Opportunities', 'ar': 'فرص استقطاب العملاء'},
			'record_url': '/crm/opportunity_update/',
			'add_new': False,
			'all_fields': {
				'customer': {'en': 'Customer', 'ar': 'العميل', 'search_criteria': '__contains'},
				'company': {'en': 'Company', 'ar': 'الشركة', 'search_criteria': '__exact'},
				'opportunity_date': {'en': 'Opportunity Date', 'ar': 'تاريخ الاستقطاب', 'search_criteria': '__contains'},
				'amount': {'en': 'Amount', 'ar': 'المبلغ', 'search_criteria': '__exact'},
				'description': {'en': 'Opportunity Description', 'ar': 'بيان الفرصة', 'search_criteria': '__contains'},
				'notes': {'en': 'Notes', 'ar': 'البيان', 'search_criteria': '__contains'},
				'status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__exact'},
				'current_status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__exact'},
				'missed_reason': {'en': 'Missed Reason', 'ar': 'سبب ضياع الفرصة', 'search_criteria': '__exact'},
				'missed_notes': {'en': 'Missed Reason Notes', 'ar': 'توضيح اسباب ضياع الفرصة', 'search_criteria': '__contains'},
				'user': {'en': 'User', 'ar': 'المستخدم', 'search_criteria': '__exact'},
				'opportunity_amount': {'en': 'Amount', 'ar': 'المبلغ', 'search_criteria': '__exact'},

			},
			'model_fields': [
				'customer', 'company', 'opportunity_date', 'opportunity_amount', 'current_status', 'missed_reason', 'user',
			],
			'search_fields': [
				'company', 'status', 'opportunity_date', 'missed_reason', 'user',
			],
			'edit_form_read_only_fields': ['user', ],
			'action': {

			}
		},
	'budget':
		{
			'app_name': 'analytics',
			'model_name': 'budget',
			'title': {'en': 'Budget', 'ar': 'الميزانية'},
			'all_fields': {
				'company': {'en': 'Company', 'ar': 'الشركة', 'search_criteria': '__exact'},
				'year': {'en': 'Year', 'ar': 'السنة', 'search_criteria': '__exact'},
				'center': {'en': 'Cost Center', 'ar': 'مركز التكلفة', 'search_criteria': '__exact'},
				'account': {'en': 'Account', 'ar': 'الحساب', 'search_criteria': '__exact'},
				'jan_budget_amount': {'en': 'Jan Amount', 'ar': 'المبلغ - يناير', 'search_criteria': '__exact'},
				'feb_budget_amount': {'en': 'Feb Amount', 'ar': 'المبلغ - فبراير', 'search_criteria': '__exact'},
				'mar_budget_amount': {'en': 'Mar Amount', 'ar': 'المبلغ - مارس', 'search_criteria': '__exact'},
				'apr_budget_amount': {'en': 'Apr Amount', 'ar': 'المبلغ - ابريل', 'search_criteria': '__exact'},
				'may_budget_amount': {'en': 'May Amount', 'ar': 'المبلغ - مايو', 'search_criteria': '__exact'},
				'jun_budget_amount': {'en': 'Jun Amount', 'ar': 'المبلغ - يونيو', 'search_criteria': '__exact'},
				'jul_budget_amount': {'en': 'Jul Amount', 'ar': 'المبلغ - يوليو', 'search_criteria': '__exact'},
				'aug_budget_amount': {'en': 'Aug Amount', 'ar': 'المبلغ - اغسطس', 'search_criteria': '__exact'},
				'sep_budget_amount': {'en': 'Sep Amount', 'ar': 'المبلغ - سبتمبر', 'search_criteria': '__exact'},
				'oct_budget_amount': {'en': 'Oct Amount', 'ar': 'المبلغ - اكتوبر', 'search_criteria': '__exact'},
				'nov_budget_amount': {'en': 'Nov Amount', 'ar': 'المبلغ - نوفمبر', 'search_criteria': '__exact'},
				'dec_budget_amount': {'en': 'Dec Amount', 'ar': 'المبلغ - ديسمبر', 'search_criteria': '__exact'},
				'status': {'en': 'Status', 'ar': 'الحالة', 'search_criteria': '__exact'},
				'budget_amount': {'en': 'Amount', 'ar': 'المبلغ', 'search_criteria': '__exact'},
				'account_name': {'en': 'Account', 'ar': 'الحساب', 'search_criteria': '__exact'}

			},
			'model_fields': [
				'company', 'year', 'center', 'account_name', 'budget_amount', 'status'
			],
			'search_fields': [
				'company', 'year', 'center', 'account', 'status'
			],
			'edit_form_read_only_fields': ['status'],
			'action': {
				'delete': {
					'en': 'Delete selected records',
					'ar': 'حذف ما تم اختياره',
					'status_from': 'd', 'status_to': 'a'
				},
				'save': {
					'en': 'Change selected records to Saved',
					'ar': 'تحويل حالة ماتم اختياره من جديد إلى نشط|فاعل',
					'status_from': 'd', 'status_to': 's'
				},
				'approve': {
					'en': 'Change selected records to Approved',
					'ar': 'تحويل حالة ماتم اختياره من نشط إلى الأرشفة',
					'status_from': 's', 'status_to': 'a'
				},

			}
		},

}


class ModelClass:

	def __init__(self, model_name, username):
		self.model = models_objects[model_name]
		self.lang = fn_get_user_lang(username)
		self.title = self.model['title'][self.lang]
		self.model_name = self.model['model_name']
		self.search_fields = list((f, self.model['all_fields'][f][self.lang]) for f in self.model['search_fields'])
		self.model_fields = list((f, self.model['all_fields'][f][self.lang]) for f in self.model['model_fields'])
		self.read_only_fields = list(self.model['edit_form_read_only_fields'])
		self.all_fields = list((f, self.model['all_fields'][f][self.lang]) for f in self.model['all_fields'])
		self.fields_labels = list([self.model['all_fields'][f][self.lang] for f in self.model['model_fields']])
		self.model_class = ContentType.objects.get(model=str(self.model_name)).model_class()
		self.actions = list((i,  self.model['action'][i][self.lang]) for i in self.model['action'])
		if 'record_url' in self.model.keys():
			self.record_url = self.model['record_url']
		else:
			self.record_url = 'default'
		if 'add_new' in self.model.keys():
			self.can_add_new = self.model['add_new']
		else:
			self.can_add_new = True

	def search_criteria(self, field):
		return str(self.model['all_fields'][field]['search_criteria'])

	def action_status_from(self, action):
		return str(self.model['action'][action]['status_from'])

	def action_status_to(self, action):
		return str(self.model['action'][action]['status_to'])


def insert_data(sql_str):
	with connection.cursor() as cursor:
		cursor.execute(str(sql_str))
		cursor.execute("Select LAST_INSERT_ID()")
		connection.commit()
		ds = cursor.fetchone()
		return ds


def get_data(sql_str):
	with connection.cursor() as cursor:
		cursor.execute(str(sql_str))
		row = cursor.fetchall()
		return row


def date_format(time_format):
	if time_format == 'd':
		return '%Y-%m-%d'
	elif time_format == 'm':
		return '%Y-%m'
	elif time_format == 'y':
		return '%Y'


def permission_check(app_name, model_name, user, action):
	# action in [add, change, delete]
	if action in ['add', 'change', 'delete']:
		perm_str = str(app_name) + '.' + str(action) + '_' + str(model_name)
		return user.has_perm(perm_str)
	else:
		return False


def search_form_criteria(model_class, form=django.forms.Form, report_id=None):
	search_dct = dict()
	for f in form.fields:
		if form[f].value() is not None and f != 'report_id' and form[f].value() != '':
			if f == 'company' and form[f].value() == '0':
				pass
			else:
				search_dct[str(f) + str(model_class.search_criteria(f))] = str(form[f].value())
	return search_dct


def model_delete(mdl_object, pk_id_lst, companies=[]):
	if 'status' in [f[0] for f in mdl_object.all_fields]:
		status_check = True
	else:
		status_check = False
	if status_check:
		if len(companies) > 0:
			mdl_object.model_class.objects.filter(pk__in=pk_id_lst, status__in=['d', 'n'], company__in=list(companies)).delete()
		else:
			mdl_object.model_class.objects.filter(pk__in=pk_id_lst, status__in=['d', 'n']).delete()
	else:
		if len(companies) > 0:
			mdl_object.model_class.objects.filter(pk__in=pk_id_lst, company__in=list(companies)).delete()
		else:
			mdl_object.model_class.objects.filter(pk__in=pk_id_lst).delete()


def model_update(model_name, pk_id_lst, status_from, status_to, companies=[]):
	from django.contrib.contenttypes.models import ContentType
	model_id = ContentType.objects.get(model=str(model_name))
	model_class = model_id.model_class()
	if len(companies) > 0:
		model_class.objects.filter(pk__in=pk_id_lst, status__exact=status_from, company__in=list(companies)).update(status=status_to)
	else:
		model_class.objects.filter(pk__in=pk_id_lst, status__exact=status_from).update(
			status=status_to)


class TableRowForm:

	def __init__(self, queryset, fields, model_name=None, lang='en', record_url='default', actions_count=0):
		if not fields:
			raise Exception('A TableRowForm must be supplied both queryset and fields')
		self.queryset = queryset
		self.fields = fields
		self.model_name = model_name
		self.actions_count = actions_count
		self.tbl_dir = ''
		if lang == 'ar':
			self.tbl_dir = 'dir="rtl"'
		self.fields_labels = {f[0]: f[1].upper().replace('_', ' ') for f in fields}
		if record_url == 'default':
			self.url = '''/crm/model_record_view/''' + str(self.model_name) + '''/'''
		else:
			self.url = record_url

	def __str__(self):
		if not self.queryset:
			return ''
		res = '<table id="dtbl" class="display nowrap"  width="100%"' + str(self.tbl_dir) + '>'
		if self.actions_count > 0:
			res += "<thead>\n <tr> <th width='15px'> <input type='checkbox'  name='slct_all' id='slct_all'/></th>"
		else:
			res += '<thead>\n <tr> '
		for f in self.fields:
			res += "<th>" + self.fields_labels[f[0]] + "</th>"
		res += "</tr>\n </thead> \n <tbody> \n"
		for obj in self.queryset:
			res += '<tr>'
			if self.actions_count > 0:
				res += '<td width="15px"><input type="checkbox"  class="chkRow" name="slct" id="%s" value="%s"/> </td> <td>'% (obj.pk, obj.pk)
			else:
				res += '<td>'
			vals = [getattr(obj, x[0]) for x in self.fields]
			for x in vals:
				if self.model_name:
					res += '''<a href="''' + self.url + str(obj.pk) + '''/"> %s </a> </td><td>''' % (str(x).replace('None', ''))
				else:
					res += '%s</td><td>'%(str(x))
			res = res[:-4]
			res += '</tr>\n'
		res += '''	
			</tbody>
			</table>
		'''
		return res


class TableRowForm_ds:

	def __init__(self, queryset, fields, model_name=None, pk_id=None):
		if not fields:
			raise Exception('A TableRowForm must be supplied both queryset and fields')
		self.queryset = queryset
		self.fields = fields
		self.model_name = model_name
		self.pk_id = pk_id

	def __str__(self):
		if not self.queryset: return '<tr><td>No data...<td></tr>'
		res = '<table id="dtbl" class="table table-striped table-bordered table-hover" style="width:100%;">'
		res += "<thead>\n <tr> <th width='15px'> <input type='checkbox'  name='slct_all' id='slct_all'/></th>"
		for f in self.fields:
			if f != self.fields[self.pk_id]:
				res += "<th>"+ f.upper() + "</th>"
		res += "</tr>\n </thead> \n <tbody> \n"
		for obj in self.queryset:
			res += '<tr>'
			if self.pk_id is not None:
				res += '<td width="15px"><input type="checkbox"  class="chkRow" name="slct" id="%s" value="%s"/> </td> <td>'%(obj[self.pk_id],obj[self.pk_id])

			vals = [x for x in obj if x != obj[self.pk_id]]
			for x in vals:
				if self.model_name:
					res += '''<a href="#" onclick='get_record("''' + str(self.model_name) + '''", "''' + str(obj[self.pk_id]) + '''")'> %s </a> </td><td>''' % (str(x))
				else:
					res += '%s</td><td>'%(str(x))
			res = res[:-4]
			res += '</tr>\n'
		res += '</tbody> \n	</table>'
		return res

