from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import LoginForm


class LoginView(View):
	template_name = 'pearls/login.html'

	def get(self, request, *args, **kwargs):
		logout(request)
		return render(request, self.template_name, {'next': request.GET.get('next', ''), 'login_form': LoginForm()})

	def post(self, request, *args, **kwargs):
		form = LoginForm(request.POST)
		if form.is_valid():
			user_name = str(form.cleaned_data['username'])
			pass_word = str(form.cleaned_data['password'])
			next_page = request.POST['next']
			user = authenticate(username=user_name, password=pass_word)
			if user is not None:
				login(request, user)
				if len(next_page) > 0:
					return HttpResponseRedirect(next_page)
				else:
					return HttpResponseRedirect('/analytics/')
			else:
				return render(request, self.template_name, {'login_form': form})
		else:
			return render(request, self.template_name, {'login_form': form})


def logout_view(request):
	logout(request)


def change_user_lang_ar(request):
	from analytics.models import UsersSettings
	next_url = request.GET['next']
	print(next_url)
	try:
		obj = UsersSettings.objects.get(user=request.user)
		obj.language = 'ar'
	except:
		obj = UsersSettings(user=request.user, language='ar')
	obj.save()
	return HttpResponseRedirect(eval(next_url))


def change_user_lang_en(request):
	from analytics.models import UsersSettings
	next_url = request.GET['next']
	print(next_url)
	try:
		obj = UsersSettings.objects.get(user=request.user)
		obj.language = 'en'
	except:
		obj = UsersSettings(user=request.user, language='en')
	obj.save()
	return HttpResponseRedirect(eval(next_url))


@login_required
def main_view(request):
	return render(request, 'analytics/main.html', {})
