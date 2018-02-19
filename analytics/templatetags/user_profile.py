from django import template
from django.template.defaultfilters import stringfilter
from analytics.procedures import fn_get_user_photo, fn_get_user_lang

register = template.Library()


@register.assignment_tag
def user_photo(username):
	return str(fn_get_user_photo(username))


@register.assignment_tag
def user_lang(username):
	lang = fn_get_user_lang(username)
	if lang == 'ar':
		form_dir = 'rtl'
	else:
		form_dir = 'ltr'
	return {'lang': lang, 'form_dir': form_dir}


@register.assignment_tag
def user_profile(username):
	from analytics.models import UsersSettings
	profile = {
		'img': '#',
		'lang': 'en',
		'form_dir': 'ltr',
	}
	try:
		obj = UsersSettings.objects.get(user__username=username)
		try:
			if obj.photo.url:
				profile['img'] = obj.photo.url
			if obj.language:
				profile['lang'] = obj.language
				if profile['lang'] == 'ar':
					profile['form_dir'] = 'rtl'
				else:
					profile['form_dir'] = 'ltr'
			return profile
		except:
			return profile
	except UsersSettings.DoesNotExist:
		return profile


@register.assignment_tag
def app_links(app_name):
	import json
	import os
	app_roles = json.loads(open(os.path.dirname(__file__) + '/roles.json').read())
	return app_roles[str(app_name)]


@register.assignment_tag
def user_apps(username):
	import json
	import os
	app_roles = json.loads(open(os.path.dirname(__file__) + '/roles.json').read())
	return app_roles
