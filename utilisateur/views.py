# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from forms import *
from formss import *

from fonction import *

def menu(request):
	if len(request.GET) > 0:
		menu_form = MenuSelectForm(request.GET)
		if menu_form.is_valid():
			if menu_form.cleaned_data["menu"] == "0":
				return HttpResponseRedirect("/django/menu/")
			elif menu_form.cleaned_data["menu"] == "1":
				return HttpResponseRedirect("/django/utilisateur/login/")
			elif menu_form.cleaned_data["menu"] == "2":
				return HttpResponseRedirect("/django/utilisateur/change")
			elif menu_form.cleaned_data["menu"] == "3":
				return HttpResponseRedirect("/django/utilisateur/pawword/")
			elif menu_form.cleaned_data["menu"] == "99":
				return HttpResponseRedirect("/django/utilisateur/logout/")
			else:
				return render(request, "stock_labo_user_menu.html", {"menu_form": menu_form, "user" : request.user})
		else:
			return render(request, "stock_labo_user_menu.html", {"menu_form": menu_form, "user" : request.user})
	else:
		menu_form = MenuSelectForm()
		return render(request, "stock_labo_user_menu.html", {"menu_form": menu_form, "user" : request.user})


def user_login(request):
	if len(request.GET) > 0:
		user_login_form = UserLoginForm(request.GET)
		if request.GET.has_key("annuler"):
			return HttpResponseRedirect("/django/utilisateur/menu/")
		else:
			if user_login_form.is_valid():
				user = authenticate(username=user_login_form.cleaned_data["username"], password=user_login_form.cleaned_data["password"])
				if user is not None:
					if user.is_active:
						login(request, user)
						if request.GET["redirect"] == "":
							return HttpResponseRedirect("/django/menu/")
						else:
							return HttpResponseRedirect(request.GET["redirect"])
					else:
						return HttpResponseRedirect("/django/utilisateur/menu/")
				else:
					return HttpResponseRedirect("/django/utilisateur/menu/")
			else:
				return render(request, "stock_labo_user_login_form.html", {"user_login_form": user_login_form, "GET" : request.GET, "user" : request.user, "GET" : request.GET})
	else:
		user_login_form = UserLoginForm()
		return render(request, "stock_labo_user_login_form.html", {"user_login_form": user_login_form, "GET" : request.GET, "user" : request.user, "GET" : request.GET})


@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def user_change(request):

	default = {}
	user = User.objects.get(username=request.user.username)
	try:
		user_param = UserPreference.objects.get(user__id=user.id)
		default.update({"username" : user.username})
		default.update({"email" : user.email})
		default.update({"first_name" : user.first_name})
		default.update({"last_name" : user.last_name})

		try:
			default.update({"unit_masse" : user_param.unit_masse.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.unit_masse.id icorrect !!!!")
		try:
			default.update({"site_perso" : user_param.site_perso.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.site_perso.id icorrect !!!!")
		try:
			default.update({"entrepot_perso" : user_param.entrepot_perso.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.entrepot_perso.id icorrect !!!!")
		try:
			default.update({"magasin_perso" : user_param.magasin_perso.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.magasin_perso.id icorrect !!!!")
		try:
			default.update({"emplacement_perso" : user_param.emplacement_perso})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.emplacement_perso.id icorrect !!!!")
		try:
			default.update({"etiquette_contenant" : user_param.etiquette_contenant.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.etiquette_contenant.id icorrect !!!!")
		try:
			default.update({"etiquette_lot" : user_param.etiquette_lot.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.etiquette_lot.id icorrect !!!!")
		try:
			default.update({"etiquette_nomenclature" : user_param.etiquette_nomenclature.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.etiquette_nomenclature.id icorrect !!!!")
		try:
			default.update({"etiquette_login" : user_param.etiquette_login.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.etiquette_login.id icorrect !!!!")
		try:
			default.update({"etiquette_emplacement" : user_param.etiquette_emplacement.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.etiquette_emplacement.id icorrect !!!!")
	except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
		user_param = UserPreference(user=user)
		user_param.save()

	if len(request.GET) > 0:
		user_change_form = UserChangeForm(request.GET)
		if request.GET.has_key("annuler"):
			return HttpResponseRedirect("/django/utilisateur/menu/")
		else:
			default.update({"email" : request.GET["email"]}	)
			default.update({"first_name" : request.GET["first_name"]})
			default.update({"last_name" : request.GET["last_name"]})

			default.update({"unit_masse" : int(request.GET["unit_masse"])})
			default.update({"site_perso" : int(request.GET["site_perso"])})
			default.update({"entrepot_perso" : int(request.GET["entrepot_perso"])})
			default.update({"magasin_perso" : int(request.GET["magasin_perso"])})
			default.update({"emplacement_perso" : request.GET["emplacement_perso"]})
			default.update({"etiquette_contenant" : int(request.GET["etiquette_contenant"])})
			default.update({"etiquette_lot" : int(request.GET["etiquette_lot"])})
			default.update({"etiquette_nomenclature" : int(request.GET["etiquette_nomenclature"])})
			default.update({"etiquette_login" : int(request.GET["etiquette_login"])})
			default.update({"etiquette_emplacement" : int(request.GET["etiquette_emplacement"])})

			user_change_form = UserChangeForm(default)

			if user_change_form.is_valid():
				user.email = default["email"]
				user.first_name = default["first_name"]
				user.last_name = default["last_name"]
				user_param.unit_masse = UnitMasse.objects.get(id=default["unit_masse"])
				user_param.site_perso = StockSite.objects.get(id=default["site_perso"])
				user_param.entrepot_perso = StockEntrepot.objects.get(id=default["entrepot_perso"])
				user_param.magasin_perso = StockMagasin.objects.get(id=default["magasin_perso"])
				user_param.emplacement_perso = default["emplacement_perso"]
				user_param.etiquette_contenant = Impression.objects.get(id=default["etiquette_contenant"])
				user_param.etiquette_lot = Impression.objects.get(id=default["etiquette_lot"])
				user_param.etiquette_nomenclature = Impression.objects.get(id=default["etiquette_nomenclature"])
				user_param.etiquette_login = Impression.objects.get(id=default["etiquette_login"])
				user_param.etiquette_emplacement = Impression.objects.get(id=default["etiquette_emplacement"])

				user.save()
				user_param.save()

				if request.user.username != user_change_form.cleaned_data["username"]:
					user.username = user_change_form.cleaned_data["username"]
					user.save()
					return HttpResponseRedirect("/django/utilisateur/logout")
				else:
					return HttpResponseRedirect("/django/utilisateur/menu/")
			else:
				return render(request, "stock_labo_user_change_form.html", {"user_change_form": user_change_form, "user" : request.user})
	else:
		user_change_form = UserChangeForm(default)
		return render(request, "stock_labo_user_change_form.html", {"user_change_form": user_change_form, "user" : request.user})


@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def user_password_change(request):
	if len(request.GET) > 0:
		user_password_change_form = UserPasswordChangeForm(request.GET)
		if request.GET.has_key("annuler"):
			return HttpResponseRedirect("/django/utilisateur/menu/")
		else:
			if user_password_change_form.is_valid() and user_password_change_form.cleaned_data["password"] == user_password_change_form.cleaned_data["password1"]:
				user = User.objects.get(username=request.user.username)
				user.set_password(user_password_change_form.cleaned_data["password"])
				user.save()
			return HttpResponseRedirect("/django/utilisateur/menu/")
	else:
		user_password_change_form = UserPasswordChangeForm()
		return render(request, "stock_labo_user_password_change_form.html", {"user_password_change_form": user_password_change_form, "user" : request.user})


def user_logout(request):
	logout(request)
	return HttpResponseRedirect("/django/utilisateur/login")



