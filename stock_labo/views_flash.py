# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from fonction import *
from models import *
from forms import *
from django.conf import settings
#from lib_linautom.python import mysql

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def flash(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Flash", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Flash", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Flash", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))

	cb = LocalScanCB()
	list1 = Table(p=False)
	onglet = Onglets(request.user)
	onglet.set_actif_by_id(9)
#	bouton = Boutons()
#	bouton.add_bouton("Panier dans<br/>le stock<br/>personnel", title="Créer un nouvel ingrédient", href="#")
#	bouton.add_bouton("Ranger<br/>le panier<br/>en stock", title="Importer un fichier", href="#")
	rech_def = {}

	flash_mode_form = FlashModeForm(initial=rech_def)
	if request.GET.has_key("mode"):
		rech_def.update({"mode":request.GET["mode"]})
	else:
		rech_def.update({"mode":"---"})

	if len(request.GET) > 0:
		if request.GET.has_key("contenant") and request.GET["contenant"]:
			rech_def.update({"contenant":request.GET["contenant"]})
		if request.GET.has_key("empl_flash") and request.GET["empl_flash"]:
			rech_def.update({"empl_flash":request.GET["empl_flash"]})
		if request.GET.has_key("flash_point") and request.GET["flash_point"]:
			rech_def.update({"flash_point":float(request.GET["flash_point"].replace(",", "."))})

		if rech_def["mode"] == "C":
			if rech_def["contenant"] != "" and rech_def["empl_flash"] != "":
				try:
					empl = FlashPointMachine.objects.filter(pk=rech_def["empl_flash_id"])
				except :
					info.update({"erreur" : "Emplacement flash inconnu"})
				try:
					cont = Contenant.objects.filter(code=rech_def["contenant"])	
				except :
					info.update({"erreur" : "Contenant inconnu"})

				if len(empl) == 0:
					info.update({"erreur" : "L'emplacement flash est inconnu"})
				elif len(empl) > 1:
					info.update({"erreur" : "Plusieurs emplacement flash on le même code"})
				else:
					if empl.nomenclature_lot == None:
						info.update({"erreur" : "L'emplacement flash n'est pas vide"})


				if rech_def["erreur"] == None:
					rech_def["contenant"] = ""
					rech_def["empl_flash"] = ""
			flash_mode_form = FlashModeChargeForm(initial=rech_def)
		elif rech_def["mode"] == "E":
			if rech_def["contenant"] != "" and rech_def["flash_point"] != "" and rech_def["empl_sortie"] != "":




				if rech_def["erreur"] == None:
					rech_def["contenant"] = ""
					rech_def["flash_point"] = ""
					rech_def["empl_sortie"] = ""
			flash_mode_form = FlashModeEnregistrementForm(initial=rech_def)
		else:
			flash_mode_form = FlashModeForm(initial=rech_def)

		print rech_def
		"""
		Liste des contenants
		"""

		cont = Contenant.objects.filter()
		nouvelle_liste = Table(caption="Machine Flash", summary="Machine flash", style="width:100%;", entete=False, table_class="list_table")

		if rech_def.has_key("site"):
			cont = cont.filter(actuel_site=rech_def["site"], actuel_entrepot=rech_def["entrepot"], actuel_magasin=rech_def["magasin"])
		cont = cont.order_by("actuel_emplacement", "code")

		l = Table.Ligne(ligne_class="list_thead")
		l.add_cellule("Contenant", title="Code contenant", style=None, cellule_class="list_thead_th")
		l.add_cellule("Emplacement", title="Emplacement Flash", style=None, cellule_class="list_thead_th")
		l.add_cellule("Code", title="Code Article", style=None, cellule_class="list_thead_th")
		l.add_cellule("Article", title="Description article", style=None, cellule_class="list_thead_th")
		nouvelle_liste.add_headers(l.get_ligne())

		nouvelle_liste.liste.update({"n_ligne_total" : cont.count()})

		for c in cont:
			l = Table.Ligne(style="line-height: 180%;")
			l.add_cellule(c.code)
			l.add_cellule(c.actuel_emplacement)
			l.add_cellule(c.nomenclature_lot.nomenclature.code)
			l.add_cellule(c.nomenclature_lot.nomenclature.description)
			if rech_def.has_key("id_panier") and p.id == int(rech_def["id_panier"]):
				l.ligne["ligne_class"] == None
				for c in l.ligne["cellules"]:
					c["cellule_class"] = "list_body_td"
					nouvelle_liste.add_headers(l.get_ligne())
					if len(nouvelle_liste.liste["liste"]) > 10:
						nouvelle_liste.add_ligne(l.get_ligne(), class_paire="list_body_tr_p", class_impaire="list_body_tr_i")
			else:
				l.ligne["ligne_class"] == None 
				for c in l.ligne["cellules"]:
					c["cellule_class"] = "list_body_td"
				nouvelle_liste.add_ligne(l.get_ligne(), class_paire="list_body_tr_p", class_impaire="list_body_tr_i")

		list1 = nouvelle_liste


	mode_choix = [
		["---", "Selectionner action"],
		["C", "Chargement machine"],
		["E", "Enregistrement FP"],
		]
	flash_mode_form.fields["mode"].choices = mode_choix
	return render(request, "stock_labo_flash.html", {
			"header": header.get_headers(),
			"onglet" : onglet.get_onglets(),
			"flash_mode_form" : flash_mode_form,
			"info" : rech_def,
			"list1" : list1.get_liste(),
			"recherche" : None,
			})

