from django.db import connection
from .procedures import ap_insert_etl_log
import pymssql
import datetime


opco_cnn = {
    '1': {'company': 'WS', 'host': r"10.25.0.225", 'user': 'sa', 'password': 'kist', 'database': 'newwst'},
    '2': {'company': 'SAR', 'host': r"10.25.0.150", 'user': 'sa', 'password': 'qwer-123', 'database': 'union_sar'},
    '3': {'company': 'SINNAR', 'host': r"10.25.0.2", 'user': 'sa', 'password': 'kist', 'database': 'pearls'},
    '4': {'company': 'INDONILE', 'host': r"10.25.0.2", 'user': 'sa', 'password': 'kist', 'database': 'indo_pearls'},

}

date_from = datetime.date(datetime.date.today().year, 1, 1).strftime('%Y-%m-%d')
date_to = str(datetime.datetime.now().strftime('%Y-%m-%d'))


def mysql_insert_many(sql):
    with connection.cursor() as cursor:
        cursor.execute(str(sql))
        connection.commit()


def mssql_data(sql, opco):
    cnn = pymssql.connect(host=opco_cnn[str(opco)]['host'],
                          user=opco_cnn[str(opco)]['user'],
                          password=opco_cnn[str(opco)]['password'],
                          database=opco_cnn[str(opco)]['database']
                          )
    m = cnn.cursor()
    q = str(sql)
    m.execute(q)
    ds = m.fetchall()
    cnn.close()
    return ds


def etl_accounts_balances(company_id, datefrom, dateto, account_type):
    sql = """
        Select E.AccountID, isNull(Sum(E.Debit - E.Credit), 0), CONVERT(VARCHAR(10),T.TransactionDate, 111), E.centerid
        From Entries E inner join Transactions T On T.TransactionID = E.TransactionID 
        Where T.TransactionStatusID >1	
                And T.TransactionDate >= '""" + datefrom + """'
                And T.TransactionDate <= '""" + dateto + """'
                And E.AccountID like '""" + str(account_type) + """' Group By E.AccountID, T.TransactionDate, E.centerid
    """
    if str(company_id) in ('2', '5'):
        sql = """
            Select E.AccountID, isNull(Sum(E.Debit - E.Credit), 0), CONVERT(VARCHAR(10),B.BatchDate, 111), E.centerid
            From Entries E inner join Transactions T On T.TransactionID = E.TransactionID inner join Batches B
            On T.BatchID = B.BatchID
            Where T.TransactionStatusID > 1	And B.BatchDate >= '""" + datefrom + """'
                 And B.BatchDate <= '""" + dateto + """' And E.AccountID like '""" + str(account_type) + """' 
            Group By E.AccountID, B.BatchDate, E.centerid
        """

    data = mssql_data(sql, company_id)

    sql_str = """
        insert into analytics_accountstransactions (id, account_id, company_id, transaction_date, amount, 
        loading_date, center_id) values 
    """

    cnt = 0
    for i in data:
        if str(i[2][-5:]).replace('/', '') != '0101':
            account_id = str(company_id) + '-' + str(i[0])
            if account_type == '4%':
                amount = i[1] * -1
            else:
                amount = i[1]
            transaction_date = i[2]
            center_id = i[3]
            id_key = str(company_id) + '-' + str(account_id) + '-' + str(transaction_date)
            if cnt == 0:
                cnt = 1
            else:
                sql_str += ","
            sql_str += "('" + str(id_key) + "','" + str(account_id) + "'," + str(company_id) + ",'" + transaction_date + "'," + str(amount) + ",'" + str(datetime.datetime.now()) + "','" + str(center_id) + "')"

    sql_str += ' ON DUPLICATE KEY UPDATE amount = Values(amount);'
    mysql_insert_many(sql_str)


def etl_accounts(companyid):
    if str(companyid) in ('2', '5'):
        sql_str = """ 
            Select AccountID, AccountName, classificationid, ParentID, CurrencyID, Kind, Active   
            From accounts Where classificationid like '5%' or classificationid like '4%' 
        """
    else:
        sql_str = """
            Select AccountID, AccountName, AccountTypeID, ParentID, CurrencyID, Kind, Active 
            From accounts Where accounttypeid like '5%' or accounttypeid like '4%' 
        """
    data = mssql_data(sql_str, companyid)
    sql_str = """
        insert into analytics_accounts (id, Company_ID, account_id, account_name, account_type_id, 
        parentid, kind, active, loading_date, budget_account) values 
    """
    cnt = 0
    for i in data:
        accountid = i[0]
        accountname = i[1]
        accounttypeid = i[2][0:1]
        budget_account = 1
        parentid = i[3]
        id_key = str(companyid) + '-' + str(accountid)
        if i[5]:
            kind = 1
        else:
            kind = 0
        if i[6]:
            active = 1
        else:
            active = 0
        if cnt == 0:
            cnt = 1
        else:
            sql_str += ","
        sql_str += "('" + str(id_key) + "'," + str(companyid) + ",'" + str(accountid) + "','" + str(accountname) + "','" + str(accounttypeid) + "','" + str(parentid) + "'," + str(kind) + "," + str(active) + ",'" + str(datetime.datetime.now()) + "'," + str(budget_account) + ")"

    sql_str += """ 
            ON DUPLICATE KEY UPDATE account_name = Values(account_name), account_type_id = Values(account_type_id), 
            parentid =Values(parentid), kind = Values(kind), active = Values(active), loading_date = Values(loading_date);
    """
    mysql_insert_many(sql_str)


def etl_centers(companyid):
    if str(companyid) in ('2', '5'):
        sql_str = "select CenterID, CenterName, ParentID, Kind, Active from centers"
    else:
        sql_str = "select CenterID, CenterName, ParentID, Kind, Active from centers"
    data = mssql_data(sql_str, companyid)
    sql_str = """
        insert into analytics_centers (id, Company_ID, Center_id, Center_name, parentid, kind, active, loading_date) values 
    """
    cnt = 0
    for i in data:
        Centerid = i[0]
        Centername = i[1]
        parentid = i[2]
        id_key = str(companyid) + '-' + str(Centerid)
        if i[3]:
            kind = 1
        else:
            kind = 0
        if i[4]:
            active = 1
        else:
            active = 0
        if cnt == 0:
            cnt = 1
        else:
            sql_str += ","
        sql_str += "('" + str(id_key) + "'," + str(companyid) + ",'" + str(Centerid) + "','" + str(Centername) + "','" + str(parentid) + "'," + str(kind) + "," + str(active) + ",'" + str(datetime.datetime.now()) + "')"

    sql_str += """
        ON DUPLICATE KEY UPDATE Center_name = Values(Center_name), parentid =Values(parentid), kind = Values(kind), 
        active = Values(active), loading_date = Values(loading_date);
    """
    mysql_insert_many(sql_str)


def etl_accounts_all():
    for k in opco_cnn.keys():
        try:
            etl_accounts(k)
        except Exception as e:
            ap_insert_etl_log('Accounts', k, e)


def etl_centers_all():
    for k in opco_cnn.keys():
        try:
            etl_centers(k)
        except Exception as e:
            ap_insert_etl_log('Centers', k, e)


def etl_transactions_all():
    if int(str(datetime.datetime.now().strftime('%m'))) > 3:
        start_date = date_from
    else:
        start_date = datetime.date(datetime.date.today().year - 1, 1, 1).strftime('%Y-%m-%d')

    for k in opco_cnn.keys():
        try:
            etl_accounts_balances(k, start_date, date_to, str('4' + '%'))
        except Exception as e:
            ap_insert_etl_log('Transactions', k, e)
        try:
            etl_accounts_balances(k, start_date, date_to, str('5' + '%'))
        except Exception as e:
            ap_insert_etl_log('Transactions', k, e)

