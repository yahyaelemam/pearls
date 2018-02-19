from .utilities import get_data, date_format, insert_data, months_dct
from datetime import datetime
import calendar


def ap_insert_etl_log(type_id, company, description):
	sql_str = """
		Insert into analytics_etllog (description, type_id, company, log_time)
		Value( """ + str(type_id) + """, """ + str(company) + """, """ + str(description) + """, 
				""" + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + """)
	"""
	insert_data(sql_str)


def sp_accounts_types_get(level=0):
	sql_str = ''
	if level == 0:
		sql_str = """
		SELECT 0 as account_type_id, '-- All Account Types --' as account_type_name
		Union
		SELECT account_type_id, account_type_name FROM pearls.analytics_accountstypes
		"""
	elif level == 1:
		sql_str = """
		SELECT account_type_id, account_type_name FROM pearls.analytics_accountstypes
		Order By account_type_id
		"""
	return get_data(sql_str)


def sp_companies_get(user, all_opco=True):
	companies_count = get_data('Select count(*) from analytics_userscompanies Where user_id =' + str(user))
	if companies_count[0][0] > 1 and all_opco:
		level = 0
	else:
		level = 1
	sql_str = ''
	if level == 0:
		sql_str = """
		Select 0, '-------' union
		Select company_id, company_name from analytics_companies 
		where company_id in(select company_id from analytics_userscompanies 
		where user_id = """ + str(user) + """)"""
	elif level == 1:
		sql_str = """
		Select company_id, company_name from analytics_companies 
		where company_id in(select company_id from analytics_userscompanies 
		where user_id = """ + str(user) + """) And company_id <> 0 """
	return get_data(sql_str)


def sp_accounts(account_type_id, company_id):
	sql_str = """
	Select account_id, account_name From analytics_accounts 
	Where company_id = """ + str(company_id) + """ And account_type_id = '""" + str(account_type_id) + """'"""
	return get_data(sql_str)


def sp_accounts_id(company_id):
	sql_str = """
	Select id, concat(account_id, concat('-', account_name)) as account_name 
	From analytics_accounts 
	Where company_id = """ + str(company_id) + """ And kind = 0 And active = 1"""
	return get_data(sql_str)


def sp_budget_year():
	sql_str = """
	Select year, year from analytics_budgetyear order by year Desc
	"""
	return get_data(sql_str)


def fn_get_user_photo(username):
	from .models import UsersSettings
	try:
		obj_image = UsersSettings.objects.get(user__username=username)
		try:
			img = obj_image.photo.url
			return img
		except:
			return '#'
	except UsersSettings.DoesNotExist:
		return '#'


def fn_get_user_lang(username):
	from .models import UsersSettings
	try:
		obj = UsersSettings.objects.get(user__username=username)
		try:
			lang = obj.language
			return lang
		except:
			return 'en'
	except UsersSettings.DoesNotExist:
		return 'en'


def center_get(company):
	sql_str = """
	SELECT id, concat(center_id, concat('-', center_name)) as center_name 
	FROM pearls.analytics_centers
	Where kind = 0 and center_id <> 0 And company_id = """ + str(company)
	return get_data(sql_str)


def fn_status_get(status):
	status_dct = {'d': 'Draft', 's': 'Saved', 'a': 'Approved'}
	return status_dct[status]


def fn_account_name(account_id):
	parent_name = get_data("""Select account_name from analytics_accounts 
							Where account_id = '""" + account_id + """'""")
	if parent_name:
		return parent_name[0][0]
	else:
		return account_id


def fn_company_name(company_id):
	company_name = get_data(""" Select company_name from analytics_companies Where company_id = """ + str(company_id))
	if company_name:
		return company_name[0][0]
	else:
		return company_id


def fn_account_type_name(account_type_id):
	if account_type_id == '0':
		return 'All Account Types'
	account_type_name = get_data(
		""" Select account_type_name from analytics_accountstypes Where account_type_id = '""" + str(
			account_type_id) + """'""")
	if account_type_name:
		return account_type_name[0][0]
	else:
		return account_type_name


def fn_company_amount(company_id, date_from, date_to, type_id):
	ds = get_data(
		"""
		Select IFNULL(sum(amount), 0) From pearls.analytics_accountstransactions
		Where company_id =  """ + str(company_id) + """ 
			And account_id IN(Select id From analytics_accounts Where account_type_id = """ + str(type_id) + """)
			And transaction_date between '""" + str(date_from) + """' and '""" + str(date_to) + """' 
		"""
	)
	return ds[0][0]


def fn_account_amount(year, company, account='0', center='None', account_type='0'):
	sql_str = """
		Select FORMAT(IFNULL(sum(amount), 0), 0) as mount From analytics_accountstransactions 
		Where DATE_FORMAT(transaction_date,'%Y') = '""" + str(year) + """'
			And company_id = """ + str(company) + """
			And (account_id = '""" + str(company) + """-""" + str(account) + """' Or '""" + str(account) + """' = '0') 
			And (center_id = '""" + str(center) + """' Or '""" + str(center) + """' = 'None')
			And ('""" + str(account_type) + """' = '0' Or account_id IN (Select id From analytics_accounts 
					Where account_type_id = '""" + str(account_type) + """'))
	"""
	return get_data(sql_str)[0][0]


def fn_hr_get(year, company, center='None'):
	sql_str = """
		Select count(*) From analytics_hr 
		Where DATE_FORMAT(employment_date,'%Y') <= '""" + str(year) + """' 
			And company_id = """ + str(company) + """
			And (center_id = '""" + str(center) + """' Or '""" + str(center) + """' = 'None')
			And status = 1
	"""
	return get_data(sql_str)[0][0]


def fn_completed_quarter(dt):
	prev_quarter_map = ((4, -1), (1, 0), (2, 0), (3, 0))
	quarter, yd = prev_quarter_map[(dt.month - 1) // 3]
	return dt.year + yd, quarter


def fn_quarters_periods(to_date):
	periods_lst = list()
	dt = datetime.strptime(str(to_date), '%Y-%m-%d')
	if dt > datetime.today():
		dt = datetime(datetime.today().year, datetime.today().month,
					  calendar.monthrange(datetime.today().year, datetime.today().month)[1])
	year, q = fn_completed_quarter(dt)

	if year == dt.year:
		if q >= 1 or (dt.month == 1 and dt.day == 31):
			periods_lst.append([str(dt.year) + '-Q1', str(dt.year) + '-01-01', str(dt.year) + '-03-31', 'q'])
		if q >= 2 or (dt.month == 3 and dt.day == calendar.monthrange(dt.year, 2)[1]):
			periods_lst.append([str(dt.year) + '-Q2', str(dt.year) + '-04-01', str(dt.year) + '-06-30', 'q'])
		if q >= 3 or (dt.month == 9 and dt.day == 30):
			periods_lst.append([str(dt.year) + '-Q3', str(dt.year) + '-07-01', str(dt.year) + '-09-30', 'q'])
		if (q == 4) or (dt.month == 12 and dt.day == 31):
			periods_lst.append([str(dt.year) + '-Q4', str(dt.year) + '-10-01', str(dt.year) + '-12-31', 'q'])

	periods_lst.append([str(dt.year) + '-01-01 - ' + str(dt.strftime('%Y-%m-%d')), str(dt.year) + '-01-01',
						str(dt.strftime('%Y-%m-%d')), 'a'])

	if datetime(dt.year, 1, 31) < dt:
		periods_lst.append([str(dt.year) + '-Jan', str(dt.year) + '-01-01', str(dt.year) + '-01-31', 'm'])
	if datetime(dt.year, 2, calendar.monthrange(dt.year, 2)[1]) < dt:
		periods_lst.append([str(dt.year) + '-Feb', str(dt.year) + '-02-01',
							str(dt.year) + '-02-' + str(calendar.monthrange(dt.year, 2)[1]), 'm'])
	if datetime(dt.year, 3, 31) <= dt:
		periods_lst.append([str(dt.year) + '-Mar', str(dt.year) + '-03-01', str(dt.year) + '-03-31', 'm'])
	if datetime(dt.year, 4, 30) <= dt:
		periods_lst.append([str(dt.year) + '-Apr', str(dt.year) + '-04-01', str(dt.year) + '-04-30', 'm'])
	if datetime(dt.year, 5, 31) <= dt:
		periods_lst.append([str(dt.year) + '-May', str(dt.year) + '-05-01', str(dt.year) + '-05-31', 'm'])
	if datetime(dt.year, 6, 30) <= dt:
		periods_lst.append([str(dt.year) + '-Jun', str(dt.year) + '-06-01', str(dt.year) + '-06-30', 'm'])
	if datetime(dt.year, 7, 31) <= dt:
		periods_lst.append([str(dt.year) + '-Jul', str(dt.year) + '-07-01', str(dt.year) + '-07-31', 'm'])
	if datetime(dt.year, 8, 31) <= dt:
		periods_lst.append([str(dt.year) + '-Aug', str(dt.year) + '-08-01', str(dt.year) + '-08-31', 'm'])
	if datetime(dt.year, 9, 30) <= dt:
		periods_lst.append([str(dt.year) + '-Sep', str(dt.year) + '-09-01', str(dt.year) + '-09-30', 'm'])
	if datetime(dt.year, 10, 31) <= dt:
		periods_lst.append([str(dt.year) + '-Oct', str(dt.year) + '-10-01', str(dt.year) + '-10-31', 'm'])
	if datetime(dt.year, 11, 30) <= dt:
		periods_lst.append([str(dt.year) + '-Nov', str(dt.year) + '-11-01', str(dt.year) + '-11-30', 'm'])
	if datetime(dt.year, 12, 31) <= dt:
		periods_lst.append([str(dt.year) + '-Dec', str(dt.year) + '-12-01', str(dt.year) + '-12-31', 'm'])
	return periods_lst


def fn_budget_month(year, month, account, company=0):
	sql_str = """
		Select sum(""" + str(month).replace(' ', '') + """_budget_amount) From analytics_budget
		Where (company_id = """ + str(company) + """ Or """ + str(company) + """ = 0)
			And year_id = """ + str(year) + """
			And account_id like '""" + str(company) + """-""" + str(account) + """%'
	"""
	ds = get_data(sql_str)
	if ds[0][0]:
		return ds[0][0]
	else:
		return 0


def fn_actual_account_amount(
		date_from, date_to, company, account='0', center='None', account_type='0', exclude_tax=False
):
	if exclude_tax:
		ds_accounts = get_data(
			"""
			SELECT account_id FROM analytics_kpiaccount 
			WHERE type_id in ('t', 'z', 'd') And (company_id = """ + str(company) + """ Or """ + str(company) + """ = 0)
		"""
		)
		accounts_eliminated = ''
		for i in ds_accounts:
			accounts_eliminated += " And account_id not like '" + str(i[0]) + "%'"
	else:
		accounts_eliminated = ''

	sql_str = """
		Select sum(amount) as mount From analytics_accountstransactions 
		Where transaction_date between '""" + str(date_from) + """' and '""" + str(date_to) + """'
			And (company_id = """ + str(company) + """ Or """ + str(company) + """ = 0)
			And (account_id = '""" + str(company) + """-""" + str(account) + """' Or '""" + str(account) + """' = '0') 
			And (center_id = '""" + str(center) + """' Or '""" + str(center) + """' = 'None')
			And ('""" + str(account_type) + """' = '0' Or account_id IN (Select id From analytics_accounts 
					Where account_type_id = '""" + str(account_type) + """'))
					""" + str(accounts_eliminated) + """
	"""
	ds = get_data(sql_str)
	if ds[0][0]:
		return ds[0][0]
	else:
		return 0


def fn_company_operation_profit(company_id, date_from, date_to):
	ds_accounts = get_data(
		"""
		SELECT account_id FROM analytics_kpiaccount 
		WHERE type_id in ('t', 'z', 'd') And (company_id = """ + str(company_id) + """ Or """ + str(company_id) + """ = 0)
	"""
	)
	accounts_eliminated = ''
	for i in ds_accounts:
		accounts_eliminated += " And account_id not like '" + str(i[0]) + "%'"

	ds_centers = get_data(
		"""
		SELECT center_id FROM analytics_kpicenter 
		WHERE type_id = 'o' And (company_id = """ + str(company_id) + """ Or """ + str(company_id) + """ = 0)
	"""
	)
	centers_eliminated = ""
	for i in ds_centers:
		centers_eliminated += " And concat(concat(company_id, '-'), center_id) not like '" + str(i[0]) + "%'"

	sql_str = """
		Select IFNULL(sum(IF(right(left(account_id, 3), 1) = '4', amount * -1, amount) * -1), 0) From pearls.analytics_accountstransactions
		Where (company_id =  """ + str(company_id) + """ Or """ + str(company_id) + """ = 0)
			And transaction_date between '""" + str(date_from) + """' and '""" + str(date_to) + """' 
			And account_id in (Select id from analytics_accounts Where account_type_id in ('4', '5'))
			""" + str(accounts_eliminated) + """ """ + str(centers_eliminated) + """
	"""
	operation_profit = get_data(sql_str)[0][0]

	revenue = fn_actual_account_amount(date_from, date_to, company_id, account_type='4')

	operation_profit_per = 0
	if operation_profit and revenue:
		if revenue != 0:
			operation_profit_per = round((operation_profit / revenue) * 100, 2)

	return operation_profit, operation_profit_per, revenue


def fn_company_ebitda(company_id, date_from, date_to):
	ds_accounts = get_data(
		"""
		SELECT account_id FROM analytics_kpiaccount 
		WHERE type_id in ('t', 'z', 'd') And (company_id = """ + str(company_id) + """ Or """ + str(company_id) + """ = 0)
	"""
	)
	accounts_eliminated = ''
	for i in ds_accounts:
		accounts_eliminated += " And account_id not like '" + str(i[0]) + "%'"

	sql_str = """
		Select IFNULL(sum(IF(right(left(account_id, 3), 1) = '4', amount * -1, amount ) * -1), 0) From pearls.analytics_accountstransactions
		Where (company_id =  """ + str(company_id) +  """ Or """ + str(company_id) + """ = 0)
			And transaction_date between '""" + str(date_from) + """' and '""" + str(date_to) + """' 
			And account_id in (Select id from analytics_accounts Where account_type_id in ('4', '5'))
			""" + str(accounts_eliminated) + """
	"""
	ebitda = get_data(sql_str)[0][0]

	revenue = fn_actual_account_amount(date_from, date_to, company_id, account_type='4')

	ebitda_per = 0
	if ebitda and revenue:
		if revenue != 0:
			ebitda_per = round((ebitda / revenue) * 100, 2)

	return ebitda, ebitda_per, revenue


def fn_company_ebit(company_id, date_from, date_to):
	ds_accounts = get_data(
		"""
		SELECT account_id FROM analytics_kpiaccount 
		WHERE type_id in ('t', 'z') And (company_id = """ + str(company_id) + """ Or """ + str(company_id) + """ = 0)
	"""
	)
	accounts_eliminated = ''
	for i in ds_accounts:
		accounts_eliminated += " And account_id not like '" + str(i[0]) + "%'"

	sql_str = """
		Select IFNULL(sum(IF(right(left(account_id, 3), 1) = '4', amount * -1, amount ) * -1), 0) From pearls.analytics_accountstransactions
		Where (company_id =  """ + str(company_id) + """ Or """ + str(company_id) + """ = 0)
			And transaction_date between '""" + str(date_from) + """' and '""" + str(date_to) + """' 
			And account_id in (Select id from analytics_accounts Where account_type_id in ('4', '5'))
			""" + str(accounts_eliminated) + """
	"""
	ebit = get_data(sql_str)[0][0]

	revenue = fn_actual_account_amount(date_from, date_to, company_id, account_type='4')

	ebit_per = 0
	if ebit and revenue:
		if revenue != 0:
			ebit_per = round((ebit / revenue) * 100, 2)

	return ebit, ebit_per, revenue


def fn_company_net_profit(company_id, date_from, date_to):
	sql_str = """
		Select IFNULL(sum(IF(right(left(account_id, 3), 1) = '4', amount * -1, amount ) * -1), 0) 
		From pearls.analytics_accountstransactions
		Where (company_id =  """ + str(company_id) + """ Or """ + str(company_id) + """ = 0)
			And transaction_date between '""" + str(date_from) + """' and '""" + str(date_to) + """' 
			And account_id in (Select id from analytics_accounts Where account_type_id in ('4', '5'))
	"""
	net_profit = get_data(sql_str)[0][0]

	revenue = fn_actual_account_amount(date_from, date_to, company_id, account_type='4')

	net_profit_per = 0
	if net_profit and revenue:
		if revenue != 0:
			net_profit_per = round((net_profit / revenue) * 100, 2)

	return net_profit, net_profit_per, revenue


def sp_ebitda_trend(companies, date_from, date_to):
	opcos = ''
	first_item = True
	for i in list(companies):
		if first_item:
			opcos += str(i[0])
			first_item = False
		else:
			opcos += ',' + str(i[0])
	ds_accounts = get_data(
		"""
		SELECT account_id FROM analytics_kpiaccount 
		WHERE type_id in ('t', 'z', 'd') And company_id in (""" + str(opcos) + """ )
	"""
	)
	accounts_eliminated = ''
	for i in ds_accounts:
		accounts_eliminated += " And account_id not like '" + str(i[0]) + "%'"

	sql_str = """
		Select IFNULL(sum(IF(right(left(account_id, 3), 1) = '4', amount * -1, amount ) * -1), 0),
			DATE_FORMAT(transaction_date, '%Y-%m')
		From pearls.analytics_accountstransactions
		Where company_id in (""" + str(opcos) + """ )
			And transaction_date between '""" + str(date_from) + """' and '""" + str(date_to) + """' 
			And account_id in (Select id from analytics_accounts Where account_type_id in ('4', '5'))
			""" + str(accounts_eliminated) + """
		Group By DATE_FORMAT(transaction_date, '%Y-%m')
		Order By DATE_FORMAT(transaction_date, '%Y-%m')
	"""
	ds = get_data(sql_str)
	ebitda_ds = list()
	for i in ds:
		print("""
			Select IFNULL(sum(amount), 0) From pearls.analytics_accountstransactions
			Where 
				account_id in (Select id from analytics_accounts Where account_type_id = '4')
				And company_id in (""" + str(opcos) + """ )
				And DATE_FORMAT(transaction_date, '%Y-%m') = '""" + str(i[1]) + """'
		""")
		revenue = get_data("""
			Select IFNULL(sum(amount), 0) From pearls.analytics_accountstransactions
			Where 
				account_id in (Select id from analytics_accounts Where account_type_id = '4')
				And company_id in (""" + str(opcos) + """ )
				And DATE_FORMAT(transaction_date, '%Y-%m') = '""" + str(i[1]) + """'
		""")[0][0]
		cost = get_data("""
					Select IFNULL(sum(amount), 0) From pearls.analytics_accountstransactions
					Where 
						account_id in (Select id from analytics_accounts Where account_type_id = '5')
						And company_id in (""" + str(opcos) + """ )
						""" + str(accounts_eliminated) + """
						And DATE_FORMAT(transaction_date, '%Y-%m') = '""" + str(i[1]) + """'
				""")[0][0]

		ebitda_per = 0
		if i[0]:
			if revenue != 0:
				ebitda_per = round((i[0] / revenue) * 100, 2)

		ebitda_ds.append({
			'EBITDA': int(i[0]), 'month': i[1], 'revenue': int(revenue), 'cost': int(cost), 'ebitda_per': ebitda_per
		})

	return ebitda_ds


'''
------------------------------------- Budgets -------------------------------------
'''


def sp_budgets_get(company_id, year_id, account_type_id, status):
	sql_str_detail = """
		SELECT B.id, C.company_name, A.account_id, A.account_name,
			concat(N.center_id, concat(' - ', N.center_name)) as center, B.status,
			format(B.jan_budget_amount + B.feb_budget_amount + B.mar_budget_amount + B.apr_budget_amount
					+ B.may_budget_amount + B.jun_budget_amount + B.jul_budget_amount + B.aug_budget_amount
					+ B.sep_budget_amount + B.oct_budget_amount + B.nov_budget_amount
					+ B.dec_budget_amount, 0) as amount
		FROM pearls.analytics_budget B, analytics_accounts A, analytics_companies C, analytics_centers N
		Where   B.account_id = A.id And B.center_id = N.id And B.company_id = C.company_id
			And B.company_id = """ + str(company_id) + """
			And N.company_id = """ + str(company_id) + """
			And B.year_id = """ + str(year_id) + """
			And (A.account_type_id = '""" + str(account_type_id) + """' Or '""" + str(account_type_id) + """' = '0')
			And B.status = '""" + str(status) + """'
		Order by A.account_id 
	"""
	sql_str_summary = """
		SELECT C.company_name, A.account_id, A.account_name, B.status, 
				Format(sum(B.jan_budget_amount + B.feb_budget_amount + B.mar_budget_amount + B.apr_budget_amount
					+ B.may_budget_amount + B.jun_budget_amount + B.jul_budget_amount + B.aug_budget_amount
					+ B.sep_budget_amount + B.oct_budget_amount + B.nov_budget_amount
					+ B.dec_budget_amount), 0)
		FROM pearls.analytics_budget B, pearls.analytics_accounts A, analytics_companies C
		Where   B.account_id = A.id And B.company_id = C.company_id
			And	B.company_id = """ + str(company_id) + """
			And B.year_id = """ + str(year_id) + """
			And (A.account_type_id = '""" + str(account_type_id) + """' Or '""" + str(account_type_id) + """' = '0')
			And B.status = '""" + str(status) + """'
		Group By C.company_name, A.account_id, A.account_name, B.status
		Order by A.account_id

	"""
	sql_str_category = """
		SELECT C.company_name, concat(concat(AT.account_type_id, ' - '), AT.account_type_name) as account_type_name, B.status, 
				Format(sum(B.jan_budget_amount + B.feb_budget_amount + B.mar_budget_amount + B.apr_budget_amount
					+ B.may_budget_amount + B.jun_budget_amount + B.jul_budget_amount + B.aug_budget_amount
					+ B.sep_budget_amount + B.oct_budget_amount + B.nov_budget_amount
					+ B.dec_budget_amount), 0)
		FROM pearls.analytics_budget B, pearls.analytics_accounts A, analytics_companies C, analytics_accountstypes AT
		Where   B.account_id = A.id And B.company_id = C.company_id And A.account_type_id = AT.account_type_id
			And	B.company_id = """ + str(company_id) + """
			And B.year_id = """ + str(year_id) + """
			And (A.account_type_id = '""" + str(account_type_id) + """' Or '""" + str(account_type_id) + """' = '0')
			And B.status = '""" + str(status) + """'
		Group By C.company_name, AT.account_type_id, AT.account_type_name, B.status
		Order by AT.account_type_name

	"""
	ds_summary = get_data(sql_str_summary)
	lst_summary = list()
	for i in ds_summary:
		lst_temp = list(i)
		lst_temp[3] = fn_status_get(lst_temp[3])
		previous_year_amount = fn_account_amount(year=str(int(year_id) - 1), company=company_id, account=str(i[1]))
		lst_temp.append(previous_year_amount)
		if previous_year_amount != '0':
			lst_temp.append('{0:.1f}'.format(
				(int(str(i[4]).replace(',', '')) - int(str(previous_year_amount).replace(',', ''))) / int(
					str(previous_year_amount).replace(',', '')) * 100))
		else:
			lst_temp.append('-100')
		lst_summary.append(lst_temp)

	ds_detail = get_data(sql_str_detail)
	lst_detail = list()
	for i in ds_detail:
		lst_temp = list(i)
		lst_temp[5] = fn_status_get(lst_temp[5])
		previous_year_amount = fn_account_amount(year=str(int(year_id) - 1), company=company_id, account=str(i[2]),
												 center=i[4].split('-')[0].replace(' ', ''))
		lst_temp.append(previous_year_amount)
		if previous_year_amount != '0':
			lst_temp.append('{0:.1f}'.format(
				(int(str(i[6]).replace(',', '')) - int(str(previous_year_amount).replace(',', ''))) / int(
					str(previous_year_amount).replace(',', '')) * 100))
		else:
			lst_temp.append('-100')
		lst_detail.append(lst_temp)

	ds_category = get_data(sql_str_category)
	lst_category = list()
	for i in ds_category:
		lst_temp = list(i)
		lst_temp[2] = fn_status_get(lst_temp[2])
		previous_year_amount = fn_account_amount(year=str(int(year_id) - 1), company=company_id,
												 account_type=i[1].split('-')[0].replace(' ', ''))
		lst_temp.append(previous_year_amount)
		if previous_year_amount != '0':
			lst_temp.append('{0:.1f}'.format(
				(int(str(i[3]).replace(',', '')) - int(str(previous_year_amount).replace(',', ''))) / int(
					str(previous_year_amount).replace(',', '')) * 100))
		else:
			lst_temp.append('-100')
		lst_category.append(lst_temp)
	return lst_category, lst_summary, lst_detail


'''
------------------------------------- TRENDS KPIs -------------------------------------
'''


def sp_accountstransactions_get(company, date_from, date_to, account_type_id, display_as,
								level='summary', parentid='', user_id=''):
	day_format = date_format(display_as)

	sql_str = ''
	if level == 'summary':
		sql_str = """
		Select DATE_FORMAT(T.transaction_date,'""" + day_format + """'), P.account_type_name, 
		FORMAT(sum(T.amount),0) as mount From analytics_accountstransactions T, analytics_accounts A,
		analytics_accountstypes P
		Where T.account_id = A.id and A.account_type_id = P.account_type_id
		And ((T.company_id = """ + str(company) + """ ) or ( """ + str(company) + """ = 0 And A.company_id in (Select company_id From 
								analytics_userscompanies Where user_id = """ + str(user_id) + """)))
		And (T.transaction_date between '""" + str(date_from) + """' and '""" + str(date_to) + """"')
		And (P.account_type_id = """ + str(account_type_id) + """ or """ + str(account_type_id) + """ = 0)
		Group by P.account_type_name, DATE_FORMAT(T.transaction_date , '""" + day_format + """')    
		Order by DATE_FORMAT(T.transaction_date , '""" + day_format + """'), P.account_type_name
		"""
	elif level == 'detail':
		sql_str = """
			Select DATE_FORMAT(T.transaction_date,'""" + day_format + """'), concat(concat(C.account_id, ' : '), C.Account_name) as Account_name, 
			FORMAT(sum(T.amount),0) as mount From analytics_accountstransactions T, analytics_accounts A,
			analytics_accounts C
			Where T.account_id = A.id And A.account_id like concat(C.account_id, '%')
			And ((T.company_id = """ + str(company) + """ ) or ( """ + str(company) + """ = 0 And A.company_id in (Select company_id From 
									analytics_userscompanies Where user_id = """ + str(user_id) + """)))
			And ((C.company_id = """ + str(company) + """ ) or ( """ + str(company) + """ = 0 And A.company_id in (Select company_id From 
									analytics_userscompanies Where user_id = """ + str(user_id) + """)))
			And (DATE_FORMAT(T.transaction_date, '%Y-%m-%d') between '""" + str(date_from) + """' and '""" + str(
			date_to) + """"')
			And (A.account_type_id = """ + str(account_type_id) + """ or """ + str(account_type_id) + """ = 0)
			And (C.kind = 1) And  CHAR_LENGTH(C.parentid) = 2
			Group by concat(concat(C.account_id, ' : '), C.Account_name), DATE_FORMAT(T.transaction_date , '""" + day_format + """')    
			Order by DATE_FORMAT(T.transaction_date , '""" + day_format + """'), concat(concat(C.account_id, ' : '), C.Account_name)
		"""
	elif level == 'account':
		account_id = str(account_type_id).split(' : ')[0]
		sql_str = """
			Select DATE_FORMAT(T.transaction_date,'""" + day_format + """'), concat(concat(A.account_id, ' : '), A.Account_name) as Account_name, 
			FORMAT(sum(T.amount),0) as Amount From analytics_accountstransactions T, 
				analytics_accounts A, analytics_accounts C
			Where T.account_id = A.id And A.parentid = C.account_id
			And (T.company_id = """ + str(company) + """ or """ + str(company) + """ = 0)        
			And (C.company_id = """ + str(company) + """ or """ + str(company) + """ = 0) 
			And (T.transaction_date between '""" + str(date_from) + """' and '""" + str(date_to) + """"')
			And (A.account_id like '""" + str(account_id) + """%')
			Group by concat(concat(A.account_id, ' : '), A.Account_name), DATE_FORMAT(T.transaction_date , '""" + day_format + """')    
			Order by DATE_FORMAT(T.transaction_date , '""" + day_format + """')
		"""
	elif level == 'cost_center':
		sql_str = """
			 Select DATE_FORMAT(T.transaction_date,'""" + day_format + """'), C.center_name,
				FORMAT(sum(T.amount),0) as Amount From analytics_accountstransactions T, 
				analytics_centers C
			Where T.center_id = C.center_id
				And (T.company_id = """ + str(company) + """ or """ + str(company) + """ = 0)        
				And (T.transaction_date between '""" + str(date_from) + """' and '""" + str(date_to) + """"')   
			Group by C.center_name, DATE_FORMAT(T.transaction_date , '""" + day_format + """')    
			Order by DATE_FORMAT(T.transaction_date , '""" + day_format + """')
		"""
	ds = get_data(sql_str)
	from itertools import groupby
	account_header = list()
	date_header = [key for key, valuesiter in groupby(ds, lambda x: x[0])]

	for i in ds:
		if i[1] not in account_header:
			account_header.append(i[1])
	result = list()
	lst = list()
	for ah in account_header:
		for h in date_header:
			v = 0
			for i in ds:
				if i[0] == h and i[1] == ah:
					v = i[2]
					break
			result.append(v)
		lst.append([ah, result])
		result = []
	return ds, date_header, lst


# DATE_FORMAT(I.reporting_date, '%Y-%m-%d')


'''
------------------------------------- MARGIN KPIs -------------------------------------
'''


def sp_mrgn_revenues_vs_expenses(companies, date_from, date_to, display_as, user_id='', landingpage=True):
	day_format = date_format(display_as)
	if landingpage:
		opcos = ''
		first_item = True
		for i in list(companies):
			if first_item:
				opcos += str(i[0])
				first_item = False
			else:
				opcos += ',' + str(i[0])
		sql_str = """    
			SELECT DATE_FORMAT(T.transaction_date,'""" + day_format + """'), AT.account_type_name, 
				FORMAT(sum(T.amount),0) as amount 
			FROM pearls.analytics_accountstransactions T, pearls.analytics_accounts A, analytics_accountstypes AT
			Where T.account_id = A.id 
					And A.account_type_id = AT.account_type_id
					And AT.account_type_id in('4', '5')  
					And (T.transaction_date between '""" + str(date_from) + """' and '""" + str(date_to) + """"')
					And (T.company_id in (""" + str(opcos) + """ ))
			group by DATE_FORMAT(T.transaction_date,'""" + day_format + """'), AT.account_type_name
			Order BY DATE_FORMAT(T.transaction_date,'""" + day_format + """'), AT.account_type_name; 
		"""
	else:
		sql_str = """    
			SELECT DATE_FORMAT(T.transaction_date,'""" + day_format + """'), AT.account_type_name, 
				FORMAT(sum(T.amount),0) as amount 
			FROM pearls.analytics_accountstransactions T, pearls.analytics_accounts A, analytics_accountstypes AT
			Where T.account_id = A.id 
					And A.account_type_id = AT.account_type_id
					And AT.account_type_id in('4', '5')  
					And (T.transaction_date between '""" + str(date_from) + """' and '""" + str(date_to) + """"')
					And ((T.company_id = """ + str(companies) + """ ) or ( """ + str(companies) + """ = 0 
						And T.company_id in (Select company_id From analytics_userscompanies 
							Where user_id = """ + str(user_id) + """)))
			group by DATE_FORMAT(T.transaction_date,'""" + day_format + """'), AT.account_type_name
			Order BY DATE_FORMAT(T.transaction_date,'""" + day_format + """'), AT.account_type_name; 
		"""
	ds = get_data(sql_str)
	from itertools import groupby
	lst_dct = {key: {} for key, valuesiter in groupby(ds, lambda x: x[0])}
	account_header = [key for key, valuesiter in groupby(ds, lambda x: x[1])]

	for ah in account_header:
		for dh in lst_dct.keys():
			v = 0
			for i in ds:
				if i[0] == dh and i[1] == ah:
					v = i[2]
					break
			lst_dct[dh][ah] = v

	final_lst = list()
	for k in sorted(lst_dct.keys()):
		lst_dct[k]['Margins'] = format(
			int(str(lst_dct[k]['Revenues']).replace(',', '')) - int(str(lst_dct[k]['Expenses']).replace(',', '')), ',d')
		if str(lst_dct[k]['Revenues']).replace(',', '') == '0':
			lst_dct[k]['%'] = 0.00
		else:
			lst_dct[k]['%'] = round(int(str(lst_dct[k]['Margins']).replace(',', '')) / int(
				str(lst_dct[k]['Revenues']).replace(',', '')) * 100, 2)

		if (int(str(lst_dct[k]['Revenues']).replace(',', '')) < 0) and (int(str(lst_dct[k]['Expenses']).replace(',', '')) > 0):
			lst_dct[k]['%'] = lst_dct[k]['%'] * -1

		final_lst.append([k, lst_dct[k]['Revenues'], lst_dct[k]['Expenses'], lst_dct[k]['Margins'], lst_dct[k]['%']])

	return final_lst


'''
------------------------------------- Landing Pag -------------------------------------
'''


def sp_companies_amount(opco, date_from, date_to):
	company_lst = list(opco)
	ds = list()
	data_lst = list()
	total_revenue = 0
	total_cost = 0
	total_margin = 0

	for opco in company_lst:
		revenue = int(fn_company_amount(opco[0], date_from, date_to, '4'))
		cost = int(fn_company_amount(opco[0], date_from, date_to, '5'))
		margin = revenue - cost
		ds.append([opco[1], revenue, cost, margin])
		total_revenue += revenue
		total_cost += cost
		total_margin += margin

	ds.sort(key=lambda tup: tup[1], reverse=True)

	for i in ds:
		per_revenue = int((i[1] / total_revenue) * 100)
		if len(ds) > 1:
			per_cost = int((i[2] / total_cost) * 100)
			per_margin = int((i[3] / total_margin) * 100)
		else:
			per_cost = int((i[2] / total_revenue) * 100)
			per_margin = int((i[3] / total_revenue) * 100)
		data_lst.append(
			[i[0], format(int(i[1] / 1000), ',d'), format(int(i[2] / 1000), ',d'), format(int(i[3] / 1000), ',d'),
			 per_revenue, per_cost, per_margin])
	return data_lst, [
		format(int(total_revenue / 1000), ',d'), format(int(total_cost / 1000), ',d'),
		format(int(total_margin / 1000), ',d')
	]


def sp_companies_kpi(opco, date_from, date_to):
	company_lst = list(opco)
	kpi_total_dct = {
		'total_revenue': 0, 'total_op_profit': 0, 'total_ebitda': 0, 'total_ebit': 0, 'total_net_profit': 0,
		'total_cost': 0,
		'op_profit_per': 0, 'ebitda_per': 0, 'ebit_per': 0, 'net_profit_per': 0, 'cost_per': 0
	}
	kpi_dct = {
		'EBITDA': [], 'EBIT': [], 'Net_Profit': [], 'Operation_Profit': [], 'Revenue': [], 'Cost': []
	}
	kpi_trend_dct = {
		'EBITDA': [], 'EBIT': [], 'Net_Profit': [], 'Operation_Profit': [], 'Revenue': []
	}
	for opco in company_lst:
		op_profit, op_profit_per, revenue = fn_company_operation_profit(opco[0], date_from, date_to)
		ebitda, ebitda_per, revenue = fn_company_ebitda(opco[0], date_from, date_to)
		ebit, ebit_per, revenue = fn_company_ebit(opco[0], date_from, date_to)
		net_profit, net_profit_per, revenue = fn_company_net_profit(opco[0], date_from, date_to)
		cost = int(fn_company_amount(opco[0], date_from, date_to, '5'))
		kpi_dct['EBITDA'].append([opco[1], ebitda, round(ebitda_per, 0)])
		kpi_dct['EBIT'].append([opco[1], ebit, round(ebit_per, 0)])
		kpi_dct['Net_Profit'].append([opco[1], net_profit, round(net_profit_per, 0)])
		kpi_dct['Operation_Profit'].append([opco[1], op_profit, round(op_profit_per, 0)])
		kpi_dct['Revenue'].append([opco[1], revenue, 0])
		kpi_dct['Cost'].append([opco[1], cost, 0])

		kpi_total_dct['total_revenue'] += revenue
		kpi_total_dct['total_op_profit'] += op_profit
		kpi_total_dct['total_ebitda'] += ebitda
		kpi_total_dct['total_ebit'] += ebit
		kpi_total_dct['total_net_profit'] += net_profit
		kpi_total_dct['total_cost'] += cost

	if kpi_total_dct['total_revenue'] != 0:
		kpi_total_dct['op_profit_per'] = round((kpi_total_dct['total_op_profit'] / kpi_total_dct['total_revenue']) * 100, 2)
		kpi_total_dct['ebitda_per'] = round((kpi_total_dct['total_ebitda'] / kpi_total_dct['total_revenue']) * 100, 2)
		kpi_total_dct['ebit_per'] = round((kpi_total_dct['total_ebit'] / kpi_total_dct['total_revenue']) * 100, 2)
		kpi_total_dct['net_profit_per'] = round((kpi_total_dct['total_net_profit'] / kpi_total_dct['total_revenue']) * 100, 2)
		kpi_total_dct['cost_per'] = round((kpi_total_dct['total_cost'] / kpi_total_dct['total_revenue']) * 100, 2)

		lst_temp = kpi_dct['Operation_Profit']
		kpi_dct['Operation_Profit'] = []
		for i in lst_temp:
			op_profit_per_total = round((i[1] / kpi_total_dct['total_op_profit']) * 100, 0)
			kpi_dct['Operation_Profit'].append([i[0], format(int(round(i[1] / 1000, 2)), ',d'), i[2], op_profit_per_total])
		kpi_dct['Operation_Profit'].sort(key=lambda tup: tup[0])

		lst_temp = kpi_dct['EBITDA']
		kpi_dct['EBITDA'] = []
		for i in lst_temp:
			ebitda_per_total = round((i[1] / kpi_total_dct['total_ebitda']) * 100, 0)
			kpi_dct['EBITDA'].append([i[0], format(int(round(i[1] / 1000, 2)), ',d'), i[2], ebitda_per_total])
		kpi_dct['EBITDA'].sort(key=lambda tup: tup[0])

		lst_temp = kpi_dct['EBIT']
		kpi_dct['EBIT'] = []
		for i in lst_temp:
			ebit_per_total = round((i[1] / kpi_total_dct['total_ebit']) * 100, 0)
			kpi_dct['EBIT'].append([i[0], format(int(round(i[1] / 1000, 2)), ',d'), i[2], ebit_per_total])
		kpi_dct['EBIT'].sort(key=lambda tup: tup[0])

		lst_temp = kpi_dct['Net_Profit']
		kpi_dct['Net_Profit'] = []
		for i in lst_temp:
			net_profit_per_total = round((i[1] / kpi_total_dct['total_net_profit']) * 100, 0)
			kpi_dct['Net_Profit'].append([i[0], format(int(round(i[1] / 1000, 2)), ',d'), i[2], net_profit_per_total])
		kpi_dct['Net_Profit'].sort(key=lambda tup: tup[0])

		lst_temp = kpi_dct['Revenue']
		kpi_dct['Revenue'] = []
		for i in lst_temp:
			revenue_per_total = round((i[1] / kpi_total_dct['total_revenue']) * 100, 0)
			kpi_dct['Revenue'].append([i[0], format(int(round(i[1] / 1000, 2)), ',d'), i[2], revenue_per_total])
		kpi_dct['Revenue'].sort(key=lambda tup: tup[0])

		lst_temp = kpi_dct['Cost']
		kpi_dct['Cost'] = []
		for i in lst_temp:
			cost_per_total = round((i[1] / kpi_total_dct['total_cost']) * 100, 0)
			kpi_dct['Cost'].append([i[0], format(int(round(i[1] / 1000, 2)), ',d'), i[2], cost_per_total])
		kpi_dct['Cost'].sort(key=lambda tup: tup[0])

	kpi_total_dct['total_op_profit'] = format(int(kpi_total_dct['total_op_profit'] / 1000), ',d')
	kpi_total_dct['total_ebitda'] = format(int(kpi_total_dct['total_ebitda'] / 1000), ',d')
	kpi_total_dct['total_ebit'] = format(int(kpi_total_dct['total_ebit'] / 1000), ',d')
	kpi_total_dct['total_net_profit'] = format(int(kpi_total_dct['total_net_profit'] / 1000), ',d')
	kpi_total_dct['total_revenue'] = format(int(kpi_total_dct['total_revenue']/ 1000), ',d')
	kpi_total_dct['total_cost'] = format(int(kpi_total_dct['total_cost'] / 1000), ',d')

	return kpi_total_dct, kpi_dct


def sp_budget_actual_summary(from_date, to_date, lst_opcos):
	dt = datetime.strptime(to_date, '%Y-%m-%d')
	if dt > datetime.today():
		dt = datetime.today()
	lst_periods = fn_quarters_periods(dt.strftime('%Y-%m-%d'))
	budget_lst = list()
	budget_ocpos_lst = list()
	for period in lst_periods:
		month_from = datetime.strptime(str(period[1]), '%Y-%m-%d').month
		month_to = datetime.strptime(str(period[2]), '%Y-%m-%d').month
		budget_revenue_all, budget_expense_all = 0, 0
		actual_revenue_all, actual_expense_all, revenue_diff_all, expense_diff_all = 0, 0, 0, 0
		for opco in lst_opcos:
			budget_revenue, budget_expense, actual_revenue, actual_expense, revenue_diff, expense_diff = 0, 0, 0, 0, 0, 0
			for m in range(month_from, month_to + 1):
				budget_revenue += fn_budget_month(
					datetime.strptime(str(period[1]), '%Y-%m-%d').year, months_dct[str(m)], '4', opco
				)
				budget_expense += fn_budget_month(
					datetime.strptime(str(period[1]), '%Y-%m-%d').year, months_dct[str(m)], '5', opco
				)

			actual_revenue += fn_actual_account_amount(
				datetime.strptime(str(period[1]), '%Y-%m-%d'), datetime.strptime(str(period[2]), '%Y-%m-%d'),
				opco, account_type='4'
			)
			actual_expense += fn_actual_account_amount(
				datetime.strptime(str(period[1]), '%Y-%m-%d'), datetime.strptime(str(period[2]), '%Y-%m-%d'),
				opco, account_type='5', exclude_tax=True
			)
			budget_revenue_all += budget_revenue
			budget_expense_all += budget_expense
			actual_revenue_all += actual_revenue
			actual_expense_all += actual_expense
			revenue_diff = actual_revenue - budget_revenue
			if actual_revenue != 0:
				revenue_per = (revenue_diff / actual_revenue) * 100
			else:
				revenue_per = 0
			expense_diff = budget_expense - actual_expense
			if actual_expense != 0:
				expense_per = (expense_diff / actual_expense) * 100
			else:
				expense_per = 0
			opco_dct = {
				'budget_revenue': format(int(budget_revenue), ',d'),
				'budget_expense': format(int(budget_expense), ',d'),
				'actual_revenue': format(int(actual_revenue), ',d'),
				'actual_expense': format(int(actual_expense), ',d'),
				'revenue_diff': format(int(revenue_diff), ',d'),
				'expense_diff': format(int(expense_diff), ',d'),
				'revenue_per': round(revenue_per, 2),
				'expense_per': round(expense_per, 2),
				'budget_margin': format(int(budget_revenue - budget_expense), ',d'),
				'actual_margin': format(int(actual_revenue - actual_expense), ',d'),
				'margin_diff': format(int((actual_revenue - actual_expense) - (budget_revenue - budget_expense)), ',d'),

			}
			if actual_revenue != 0 and actual_expense != 0:
				opco_dct['margin_per'] = format(int((((actual_revenue - actual_expense) - (budget_revenue - budget_expense)) / (
				actual_revenue - actual_expense)) * 100), ',d')
			else:
				opco_dct['margin_per'] = 0
			budget_ocpos_lst.append([period[0], fn_company_name(opco), opco_dct, str(period[3])])

		revenue_diff_all = actual_revenue_all - budget_revenue_all
		expense_diff_all = budget_expense_all - actual_expense_all
		if actual_revenue_all != 0:
			revenue_per_all = (revenue_diff_all / actual_revenue_all) * 100
		else:
			revenue_per_all = 0
		if actual_expense_all != 0:
			expense_per_all = (expense_diff_all / actual_expense_all) * 100
		else:
			expense_per_all = 0
		all_dct = {
			'budget_revenue_all': format(int(budget_revenue_all), ',d'),
			'budget_expense_all': format(int(budget_expense_all), ',d'),
			'actual_revenue_all': format(int(actual_revenue_all), ',d'),
			'actual_expense_all': format(int(actual_expense_all), ',d'),
			'revenue_diff_all': format(int(revenue_diff_all), ',d'),
			'expense_diff_all': format(int(expense_diff_all), ',d'),
			'revenue_per_all': round(revenue_per_all, 2),
			'expense_per_all': round(expense_per_all, 2),
			'budget_margin_all': format(int(budget_revenue_all - budget_expense_all), ',d'),
			'actual_margin_all': format(int(actual_revenue_all - actual_expense_all), ',d'),
			'margin_diff_all': format(
				int((actual_revenue_all - actual_expense_all) - (budget_revenue_all - budget_expense_all)), ',d'),
		}
		if actual_revenue_all != 0 and actual_expense_all!= 0:
			all_dct['margin_per_all'] = format(int((((actual_revenue_all - actual_expense_all) - (
				budget_revenue_all - budget_expense_all)) / (actual_revenue_all - actual_expense_all)) * 100), ',d')
		else:
			all_dct['margin_per_all'] = 0
		budget_lst.append([period[0], all_dct, str(period[3])])
		opcos_lst = list()
	for opco in lst_opcos:
		lst = list()
		for i in budget_ocpos_lst:
			if i[1] == fn_company_name(opco):
				lst.append(i)
		opcos_lst.append([{'opco': fn_company_name(opco)}, lst])
	return budget_lst, opcos_lst


"""
vars()['i_var'] = 'no'
eval('i_var')
"""