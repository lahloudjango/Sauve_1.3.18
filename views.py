# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils.http import urlquote
from django.contrib.auth.decorators import login_required

import version

from formss import *


def menu(request):
	info = version.status_developement

	if len(request.GET) > 0:
		menu_form = MenuSelectForm(request.GET)
		if menu_form.is_valid():
			if menu_form.cleaned_data["menu"] == "0":
				return HttpResponseRedirect("/django/menu/")
			elif menu_form.cleaned_data["menu"] == "1":
				return HttpResponseRedirect("/django/stock_labo/nomenclature/")
			elif menu_form.cleaned_data["menu"] == "2":
				return HttpResponseRedirect("/django/stock_labo_pistolet/menu/")
			elif menu_form.cleaned_data["menu"] == "3":
				return HttpResponseRedirect("/django/utilisateur/menu/")
			elif menu_form.cleaned_data["menu"] == "98":
				return HttpResponseRedirect("/django/stock_labo_pistolet/menu/")
			elif menu_form.cleaned_data["menu"] == "99":
				return HttpResponseRedirect("/django/utilisateur/logout/")
			elif menu_form.cleaned_data["menu"] == "a":
				return HttpResponseRedirect("/django/admin/")
			elif menu_form.cleaned_data["menu"] == "d":
				return HttpResponseRedirect("/django/admin_doc/")
			else:
				return render(request, "stock_labo_menu.html", { "menu_selection_form": menu_form, "VERSION": version.VERSION, "user": request.user, "info" : info})
		else:
			return render(request, "stock_labo_menu.html", { "menu_selection_form": menu_form, "VERSION": version.VERSION, "user": request.user, "info" : info})
	else:
		menu_form = MenuSelectForm()
		return render(request, "stock_labo_menu.html", { "menu_selection_form": menu_form, "VERSION": version.VERSION, "user": request.user, "info" : info})












