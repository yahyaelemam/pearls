from django.db import connection
import django.forms

Chart_color = [
	"rgba(46, 106, 255, ", "rgba(242, 163, 17, ", "rgba(126,148,180, ", "rgba(164, 0, 0, ", "rgba(151,187,205, ",
	"rgba(241,234,15 , ", "rgba(230, 182, 216, ",  "rgba(213,230 , 186, ", "rgba(220,220,220, ", "rgba(0, 191, 255, ",
	"rgba(46, 106, 255, ", "rgba(242, 163, 17, ", "rgba(126,148,180, ",
] * 10

chart_type = [['bar', 'Bar'], ['horizontalBar', 'horizontalBar'], ['line', 'Line']]

time_range = [['y', 'Year'], ['m', 'Month'], ['d', 'Day']]

months_dct = {
	'1': 'jan',
	'2': 'feb',
	'3': 'mar',
	'4': 'apr',
	'5': 'may',
	'6': 'jun',
	'7': 'jul',
	'8': 'aug',
	'9': 'sep',
	'10': 'oct',
	'11': 'nov',
	'12': 'dec'
}


reports = {
	'accounts':
		{
			'model_name': 'accounts',
			'model_fields': [
				'company', 'account_id', 'account_name',
				'parentid', 'active', 'kind', 'account_type'
			],
			'search_fields': [
				['company', '__exact'], ['account_name', '__contains'],
				['parentid', '__startswith'], ['active', '__exact'],
				['kind', '__exact'], ['account_type', '__exact']
			],
			'edit_form_read_only_fields': ['id'],
			'title': 'Accounts'
		},
	'accountstypes':
		{
			'model_name': 'accountstypes',
			'model_fields': [
				'account_type_id', 'account_type_name'
			],
			'search_fields': [
				['account_type_name', '__contains']
			],
			'edit_form_read_only_fields': ['account_type_id'],
			'title': 'Accounts Types'
		},
	'accountstransactions':
		{
			'model_name': 'accountstransactions',
			'model_fields': [
				'company', 'transaction_date', 'amount', 'account_id', 'center_id'
			],
			'search_fields': [
				['company', '__exact'], ['center_id', '__exact'],
				['account_id', '__startswith'], ['transaction_date', '__startswith']
			],
			'edit_form_read_only_fields': ['id'],
			'title': 'Transactions'
		},
	'budgets':
		{
			'model_name': 'budget',
			'model_fields': [
				'year', 'account', 'center', 'budget_amount', 'last_year', 'current_status'
			],
			'search_fields': [
				['company', '__exact'], ['year', '__exact'], ['status', '__exact']
			],
			'edit_form_read_only_fields': [],
			'title': 'Budgets'
		}
}


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


def get_search_sighn(search_fields_lst, field):
	for i in search_fields_lst:
		if i[0] == field:
			return str(i[1])
	return ''


def search_form_criteria(form=django.forms.Form, report_id=None):
	search_dct = dict()
	for f in form.fields:
		if form[f].value() is not None and f != 'report_id' and form[f].value() != '':
			search_dct[str(f) + str(get_search_sighn(reports[report_id]['search_fields'], f))] = str(form[f].value())
	return search_dct


class TableRowForm:

	def __init__(self, queryset, fields, model_name=None):
		if not fields:
			raise Exception('A TableRowForm must be supplied both queryset and fields')
		self.queryset = queryset
		self.fields = fields
		self.model_name = model_name

	def __str__(self):
		if not self.queryset: return '<tr><td>No data...<td></tr>'
		res = '<table id="dtbl" class="table table-striped table-bordered table-hover" style="width:100%;">'
		res += "<thead>\n <tr> <th width='15px'> <input type='checkbox'  name='slct_all' id='slct_all'/></th>"
		for f in self.fields:
			#print(str(self.queryset[0]._meta.get_field(f).get_internal_type()))
			try:
				header = (self.queryset[0]._meta.get_field(f).verbose_name).upper()
			except:
				header = f.upper().replace('_', ' ')
			res += "<th>"+ header+"</th>"
		res += "</tr>\n </thead> \n <tbody> \n"
		for obj in self.queryset:
			res += '<tr>'
			res += '<td width="15px"><input type="checkbox"  class="chkRow" name="slct" id="%s" value="%s"/> </td> <td>'%(obj.pk,obj.pk)

			vals = [getattr(obj, x) for x in self.fields]
			for x in vals:
				if self.model_name:
					res += '''<a href="#" onclick='get_record("''' + str(self.model_name) + '''", "''' + str(obj.pk) + '''")'> %s </a> </td><td>''' % (str(x))
				else:
					res += '%s</td><td>'%(str(x))
			res = res[:-4]
			res += '</tr>\n'
		#res += '<tr><th><span style="font-size:9pt;"><b>Row(s):</b> ' + str(len(self.queryset)) + '</span></th></tr>'

		# Add the javascript that implements functionality
		res += '''\
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

