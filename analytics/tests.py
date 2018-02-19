from django.test import TestCase

# Create your tests here.


def sp_budget_actual_summary(from_date, to_date, lst_opcos):
    lst_periods = fn_quarters_periods(to_date)
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
                budget_revenue += fn_budget_month(datetime.strptime(str(period[1]), '%Y-%m-%d').year,
                                           months_dct[str(m)], '4', opco)
                budget_expense += fn_budget_month(datetime.strptime(str(period[1]), '%Y-%m-%d').year,
                                           months_dct[str(m)], '5', opco)

            actual_revenue += fn_actual_account_amount(datetime.strptime(str(period[1]), '%Y-%m-%d'),
                                                       datetime.strptime(str(period[2]), '%Y-%m-%d'),
                                                       opco, account_type='4')
            actual_expense += fn_actual_account_amount(datetime.strptime(str(period[1]), '%Y-%m-%d'),
                                                       datetime.strptime(str(period[2]), '%Y-%m-%d'),
                                                       opco, account_type='5')
            budget_revenue_all += budget_revenue
            budget_expense_all += budget_expense
            actual_revenue_all += actual_revenue
            actual_expense_all += actual_expense
            revenue_diff = actual_revenue - budget_revenue
            revenue_per = (revenue_diff / actual_revenue) * 100
            expense_diff = actual_expense - budget_expense
            expense_per = (expense_diff / actual_expense) * 100
            opco_dct = {
                'budget_revenue': format(int(budget_revenue), ',d'),
                'budget_expense': format(int(budget_expense), ',d'),
                'actual_revenue': format(int(actual_revenue), ',d'),
                'actual_expense': format(int(actual_expense), ',d'),
                'revenue_diff': format(int(revenue_diff), ',d'),
                'expense_diff': format(int(expense_diff), ',d'),
                'revenue_per': round(revenue_per, 2),
                'expense_per': round(expense_per, 2)
            }
            budget_ocpos_lst.append([period[0], fn_company_name(opco), opco_dct])

        revenue_diff_all = actual_revenue_all - budget_revenue_all
        expense_diff_all = actual_expense_all - budget_expense_all
        revenue_per_all = (revenue_diff_all / actual_revenue_all) * 100
        expense_per_all = (expense_diff_all / actual_expense_all) * 100
        all_dct = {
            'budget_revenue_all': format(int(budget_revenue_all), ',d'),
            'budget_expense_all': format(int(budget_expense_all), ',d'),
            'actual_revenue_all': format(int(actual_revenue_all), ',d'),
            'actual_expense_all': format(int(actual_expense_all), ',d'),
            'revenue_diff_all': format(int(revenue_diff_all), ',d'),
            'expense_diff_all': format(int(expense_diff_all), ',d'),
            'revenue_per_all': round(revenue_per_all, 2),
            'expense_per_all': round(expense_per_all, 2)
        }
        budget_lst.append([period[0], all_dct])
    return budget_lst, budget_ocpos_lst



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
	return data_lst, [format(int(total_revenue / 1000), ',d'), format(int(total_cost / 1000), ',d'),
					  format(int(total_margin / 1000), ',d')]