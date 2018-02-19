from analytics.etl import etl_accounts_all, etl_centers_all, etl_transactions_all
import datetime
from analytics.utilities import get_data


current_hour = str(datetime.datetime.now().strftime('%m'))
ds = get_data("Select * from analytics_etlschedule")
for i in ds:
    if i[2] == current_hour:
        if i[1] == 'a':
            etl_accounts_all()
        elif i[1] == 'c':
            etl_centers_all()
        elif i[1] == 't':
            etl_transactions_all()

