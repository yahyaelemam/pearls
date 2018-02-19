"""pearls URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
	url(r'^$', views.main_view, name='main_view'),
	url(r'^pearls/login/$', views.LoginView.as_view(), name='login_user'),
	url(r'^pearls/ar_lang/$', views.change_user_lang_ar, name='ar_lang'),
	url(r'^pearls/en_lang/$', views.change_user_lang_en, name='en_lang'),
	url(r'^pearls/', admin.site.urls),
	url(r'^analytics/',  include('analytics.urls')),
	url(r'^crm/',  include('crm.urls')),
			  ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
			  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
