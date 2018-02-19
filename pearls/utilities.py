from django.db import connection


Chart_color = [
    "rgba(46, 106, 255, ", "rgba(242, 163, 17, ", "rgba(126,148,180, ", "rgba(164, 0, 0, ", "rgba(151,187,205, ",
    "rgba(241,234,15 , ", "rgba(230, 182, 216, ",  "rgba(213,230 , 186, ", "rgba(220,220,220, ", "rgba(0, 191, 255, ",
    "rgba(46, 106, 255, ", "rgba(242, 163, 17, ", "rgba(126,148,180, ",
] * 10

chart_type = [['bar', 'Bar'], ['horizontalBar', 'horizontalBar'], ['line', 'Line']]

time_range = [['y', 'Year'], ['m', 'Month'], ['d', 'Day']]


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


