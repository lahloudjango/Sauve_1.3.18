# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

import django
print django.VERSION
if django.VERSION[:2] == (1,4):
	from django.conf.urls.defaults import patterns, url, include
elif django.VERSION[:2] < (1,8):
	from django.conf.urls import patterns, url, include
else:
	from django.conf.urls import url, include
	def patterns(a,*u):
		return [z for z in u]

from django.contrib import admin

#from dajaxice.core import dajaxice_autodiscover
#from django.conf import settings
#dajaxice_autodiscover()


admin.autodiscover()


from views import menu

if sys.path[0].endswith("dev") or sys.path[0].endswith("prod"):
	urlpatterns = patterns('',
		url(r'^$', menu, name='menu'),
		url(r"^menu/", menu, name="menu"),

		url(r"^stock_labo/", include("stock_labo.urls", namespace="stock_labo")),
		url(r"^stock_labo_pistolet/", include("stock_labo_pistolet.urls", namespace="stock_labo_pistolet")),
		url(r"^utilisateur/", include("utilisateur.urls", namespace="stock_labo_utilisateur")),

		url(r"^admin/", include(admin.site.urls)),

		url(r"^admin_doc/", include("django.contrib.admindocs.urls")),
		
#		(r"^%s/" % settings.DAJAXICE_MEDIA_PREFIX, include("dajaxice.urls")),
	)

else:
	urlpatterns = patterns('',
		url(r'^django/$', menu, name='menu'),
		url(r"^django/menu/", menu, name="menu"),

		url(r"^django/stock_labo/", include("stock_labo.urls", namespace="stock")),
		url(r"^django/stock_labo_pistolet/", include("stock_labo_pistolet.urls", namespace="stock_labo_pistolet")),
    	url(r"^django/utilisateur/", include("utilisateur.urls", namespace="stock_utilisateur")),

		url(r"^django/admin/", include(admin.site.urls)),

		url(r"^django/admin_doc/", include("django.contrib.admindocs.urls")),
		
#		(r"^django/%s/" % settings.DAJAXICE_MEDIA_PREFIX, include("dajaxice.urls")),
	)

