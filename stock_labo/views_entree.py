# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from fonction import *
from models import *
from forms import *


@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def entree(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Entrée", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Entrée", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Entrée", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))
	onglet = Onglets(request.user)
	onglet.set_actif_by_id(6)
	if len(request.GET) > 0:
		if request.GET.has_key("annuler"):
			return HttpResponseRedirect("/django/stock_labo/nomenclature/")
		elif request.GET.has_key("valider") and request.GET.has_key("emplacement") and request.GET.has_key("code") and request.GET.has_key("extention") and request.GET.has_key("fin_de_ligne"):
			if request.GET.has_key("type_fichier") and request.GET["type_fichier"] == "f_rox_ex":
				formule = decode_roxane_export(request.GET["emplacement"], request.GET["code"], request.GET["extention"], FormuleImportForm._FIN_DE_LIGNE[request.GET["fin_de_ligne"]])
				return HttpResponseRedirect("/django/stock_labo/nomenclature/")
			elif request.GET.has_key("type_fichier") and request.GET["type_fichier"] == "f_rox_ex_new":
				formule = decode_roxane_export_new(request.GET["emplacement"], request.GET["code"], request.GET["extention"], FormuleImportForm._FIN_DE_LIGNE[request.GET["fin_de_ligne"]])
				return HttpResponseRedirect("/django/stock_labo/nomenclature/")
#			elif request.GET.has_key("type_fichier") and request.GET["type_fichier"] == "ing_cont":
#				formule = type_ingr.add_momenclature_ingredient_contexa(request.GET["emplacement"], request.GET["code"], request.GET["extention"], FormuleImportForm._FIN_DE_LIGNE[request.GET["fin_de_ligne"]])
#				return HttpResponseRedirect("/django/stock_labo/nomenclature/")
			elif request.GET.has_key("type_fichier") and request.GET["type_fichier"] == "gen":
				import_generic(request.GET["emplacement"], request.GET["code"], request.GET["extention"], FormuleImportForm._FIN_DE_LIGNE[request.GET["fin_de_ligne"]])
			elif request.GET.has_key("type_fichier") and request.GET["type_fichier"] == "sap_nav":
				import_navette_sap(request.GET["emplacement"], request.GET["code"], request.GET["extention"], FormuleImportForm._FIN_DE_LIGNE[request.GET["fin_de_ligne"]])
			elif request.GET.has_key("type_fichier") and request.GET["type_fichier"] == "sol_vin":
				import_solution_vincent(request.GET["emplacement"], request.GET["code"], request.GET["extention"], FormuleImportForm._FIN_DE_LIGNE[request.GET["fin_de_ligne"]])
			elif request.GET.has_key("type_fichier") and request.GET["type_fichier"] == "collection":
				import_status_collection(request.GET["emplacement"], request.GET["code"], request.GET["extention"], FormuleImportForm._FIN_DE_LIGNE[request.GET["fin_de_ligne"]])
			elif request.GET.has_key("type_fichier") and request.GET["type_fichier"] == "validite":
				import_duree_validite(request.GET["emplacement"], request.GET["code"], request.GET["extention"], FormuleImportForm._FIN_DE_LIGNE[request.GET["fin_de_ligne"]])
			elif request.GET.has_key("type_fichier") and request.GET["type_fichier"] == "article":
				import_article(request.GET["emplacement"], request.GET["code"], request.GET["extention"], FormuleImportForm._FIN_DE_LIGNE[request.GET["fin_de_ligne"]])
			elif request.GET.has_key("type_fichier") and request.GET["type_fichier"] == "flash":
				import_flash_point(request.GET["emplacement"], request.GET["code"], request.GET["extention"], FormuleImportForm._FIN_DE_LIGNE[request.GET["fin_de_ligne"]])



		form = FormuleImportForm(request.GET)
		return render(request, "stock_labo_import_fichier.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form})

	defaut = {}
	defaut.update({"emplacement" : "/var/www/django/%s/" %(version.VERSION)})
	defaut.update({"code" : ""})
	defaut.update({"extention" : ""})
	form = FormuleImportForm(initial=defaut)
	return render(request, "stock_labo_import_fichier.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form})
