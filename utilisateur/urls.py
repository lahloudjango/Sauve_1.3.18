# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import django
if django.VERSION[:2] == (1,4):
	from django.conf.urls.defaults import patterns, url, include
elif django.VERSION[:2] < (1,8):
	from django.conf.urls import patterns, url, include
else:
	from django.conf.urls import url, include
	def patterns(a,*u):
		return [z for z in u]

import views

urlpatterns = patterns('',
	url(r'^$', views.menu, name='menu'),
	url(r'^menu/$', views.menu, name='menu'),
	url(r'^login/$', views.user_login, name='user_login'),
	url(r'^change/$', views.user_change, name='user_change'),
	url(r'^password/$', views.user_password_change, name='user_password_change'),
	url(r'^logout/$', views.user_logout, name='user_logout'),


#	url(r'^admin/', include(admin.site.urls)),
#	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
#	url(r'^login/$', views.login, name='login'),
	)


