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

urlpatterns = patterns("",
	url(r"^$", views.menu, name="menu"),
	url(r"^menu/$", views.menu, name="menu"),
	url(r"^reception/$", views.reception, name="reception"),
	url(r"^mouvement/$", views.mouvement, name="mouvement"),
	url(r"^statut/$", views.statut, name="statut"),
	)



