# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from fonction import *
from formss import *
from classs import *

import django.core.exceptions
import django.db


from stock_labo.views_mouvement import mouvement_fonction
from stock_labo.views_reception import reception_fonction

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def menu(request):
	if len(request.GET) > 0:
		
		menu_form = MenuSelectForm(request.GET)
		if menu_form.is_valid():
			if menu_form.cleaned_data["menu"] == "0":
				return HttpResponseRedirect("/django/menu/")
			elif menu_form.cleaned_data["menu"] == "1":
				return HttpResponseRedirect("/django/stock_labo_pistolet/statut/")
			elif menu_form.cleaned_data["menu"] == "2":
				return HttpResponseRedirect("/django/stock_labo_pistolet/reception")
			elif menu_form.cleaned_data["menu"] == "3":
				return HttpResponseRedirect("/django/stock_labo_pistolet/mouvement")
			elif menu_form.cleaned_data["menu"] == "99":
				return HttpResponseRedirect("/django/utilisateur/logout/")
			else:
				return render(request, "stock_labo_pistolet_menu.html", { "menu_selection_form": menu_form})
		else:
			return render(request, "stock_labo_pistolet_menu.html", { "menu_selection_form": menu_form})
	else:
		menu_form = MenuSelectForm()
		return render(request, "stock_labo_pistolet_menu.html", { "menu_selection_form": menu_form})


@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def mouvement(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Mouvement", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Mouvement", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Mouvement", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))
	onglet = Onglets(request.user)
	onglet.set_actif_by_id(2)

	if request.GET.has_key("annuler"):
		return HttpResponseRedirect("/django/stock_labo_pistolet/menu/")
	if request.GET.has_key("cb"):
		if request.GET["cb"] == "0":
			return HttpResponseRedirect("/django/stock_labo_pistolet/menu/")
		elif request.GET["cb"] == "99":
			return HttpResponseRedirect("/django/utilisateur/logout/")

	defaut, info = mouvement_fonction(request)

	scan = ScanCBPistoletForm()
	form = MouvementForm(initial=defaut)
	return render(request, "stock_labo_pistolet_mouvement.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "scan" : scan, "info" : info})


@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def reception(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Reception", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Reception", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Reception", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))
	onglet = Onglets(request.user)
	onglet.set_actif_by_id(7)

	if request.GET.has_key("annuler"):
		return HttpResponseRedirect("/django/stock_labo_pistolet/menu/")
	if request.GET.has_key("cb"):
		if request.GET["cb"] == "0":
			return HttpResponseRedirect("/django/stock_labo_pistolet/menu/")
		elif request.GET["cb"] == "99":
			return HttpResponseRedirect("/django/utilisateur/logout/")

	defaut, info = reception_fonction(request)

	scan = ScanCBPistoletForm()
	form = ReceptionForm(initial=defaut)
	return render(request, "stock_labo_pistolet_reception.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "scan" : scan, "info" : info})


@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def statut(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Statut", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Statut", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Statut", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))
	onglet = Onglets(request.user)
	onglet.set_actif_by_id(7)

	info = {}

	if request.GET.has_key("annuler"):
		return HttpResponseRedirect("/django/stock_labo_pistolet/menu/")
	if request.GET.has_key("cb"):
		if request.GET["cb"] == "0":
			return HttpResponseRedirect("/django/stock_labo_pistolet/menu/")
		elif request.GET["cb"] == "99":
			return HttpResponseRedirect("/django/utilisateur/logout/")

		cont = models_contenant.Contenant.objects.filter(code=request.GET["cb"])

		info.update({"code": cont[0].code})
		info.update({"article": cont[0].nomenclature_lot.nomenclature.code})
		info.update({"description": cont[0].nomenclature_lot.nomenclature.description})
		info.update({"emplacement_stock": cont[0].stock_emplacement_nom_court()})
		info.update({"emplacement_actuel": cont[0].actuel_emplacement_nom_court()})
		info.update({"panier": cont[0].panier_user})
		info.update({"creation": cont[0].f_date_creation()})
		info.update({"reception": cont[0].f_date_reception()})
		info.update({"date_suppression": cont[0].f_date_suppression()})
		info.update({"fin_validite": cont[0].f_date_fin_validite()})

	scan = ScanCBPistoletForm()
	return render(request, "stock_labo_pistolet_statut.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "scan" : scan, "info" : info})









