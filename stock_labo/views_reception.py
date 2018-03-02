# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from fonction import *
from models import *
from forms import *

def reception_fonction(request):
	cb = LocalScanCB()
	info = {}
	defaut = {}

	if len(request.GET) > 0:
		if request.GET.has_key("cb") and request.GET["cb"] != "":
			if request.GET.has_key("contenant"):
				defaut.update({"contenant":request.GET["contenant"]})
			if request.GET.has_key("site"):
				defaut.update({"site":request.GET["site"]})
			if request.GET.has_key("entrepot"):
				defaut.update({"entrepot":request.GET["entrepot"]})
			if request.GET.has_key("magasin"):
				defaut.update({"magasin":request.GET["magasin"]})
			if request.GET.has_key("emplacement"):
				defaut.update({"emplacement":request.GET["emplacement"]})
			if request.GET.has_key("reception_d") and request.GET["reception_d"] == "on":
				defaut.update({"reception_d":"on"})
			else:
				defaut.update({"reception_d":""})
			if request.GET.has_key("contenant_type"):
				defaut.update({"contenant_type":request.GET["contenant_type"]})

			cb.format_cb(request.GET["cb"])
			if cb.decode_cb():
				if cb.cb["type"] == "sap":
					if cb.cb["format"] == "10c":
						if defaut["contenant"] == cb.cb["contenant"]:
							try:
								cont = Contenant.objects.get(code=cb.cb["contenant"])
							except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
								info.update({"erreur": "Le contenant est %s n'existe pas" %(cb.cb["contenant"])})
							else:
								if cont.date_reception == None:
									site = StockSite.objects.get(pk=defaut["site"])
									entrepot = StockEntrepot.objects.get(pk=defaut["entrepot"])
									magasin = StockMagasin.objects.get(pk=defaut["magasin"])
									emplacement = defaut["emplacement"]
									cont.stock_site = site
									cont.stock_entrepot = entrepot
									cont.stock_magasin = magasin
									cont.stock_emplacement = emplacement
									cont.actuel_site = site
									cont.actuel_entrepot = entrepot
									cont.actuel_magasin = magasin
									cont.actuel_emplacement = emplacement
									cont.date_reception = datetime.date.today()
									cont.date_fin_validite = cont.fin_validite()
									cont.type_contenant = ContenantType.objects.get(pk=defaut["contenant_type"])
									log = django_models.LogEntry()
									log.action_time = datetime.datetime.now()														#La date et l’heure de l’action.
									log.user = request.user																			#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
									log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())	#Le type de contenu (ContentType) de l’objet modifié.
									log.object_id = cont.id																			#La représentation textuelle de la clé primaire de l’objet modifié.
									log.object_repr = unicode(cont)																	#La représentation repr() de l’objet après sa modification.
									log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
									log.change_message = "reception"																#Description de la modification
									log.save()
									if defaut["reception_d"] == "on":
										cont.nomenclature_lot.nomenclature.reception_site = site
										cont.nomenclature_lot.nomenclature.reception_entrepot = entrepot
										cont.nomenclature_lot.nomenclature.reception_magasin = magasin
										cont.nomenclature_lot.nomenclature.reception_emplacement = emplacement
										cont.nomenclature_lot.nomenclature.save()
										log = django_models.LogEntry()
										log.action_time = datetime.datetime.now()														#La date et l’heure de l’action.
										log.user = request.user																			#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
										log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())	#Le type de contenu (ContentType) de l’objet modifié.
										log.object_id = cont.id																			#La représentation textuelle de la clé primaire de l’objet modifié.
										log.object_repr = unicode(cont)																	#La représentation repr() de l’objet après sa modification.
										log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
										log.change_message = "reception : enregistrement emplacement de réception"						#Description de la modification
										log.save()
									cont.save()
									defaut = {}
									info.update({"info": "Le contenant est %s est réceptionné" %(cb.cb["contenant"])})
								else:
									info.update({"erreur": "Le contenant est %s déjà réceptionné" %(cb.cb["contenant"])})
						else:
							try:
								cont = Contenant.objects.get(code=cb.cb["contenant"])
							except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
								info.update({"erreur": "Le contenant est %s n'existe pas" %(cb.cb["contenant"])})
							else:
								if cont.date_reception == None:
									defaut["contenant"] = cont.code
									defaut["site"] = cont.nomenclature_lot.nomenclature.reception_site.id
									defaut["entrepot"] = cont.nomenclature_lot.nomenclature.reception_entrepot.id
									defaut["magasin"] = cont.nomenclature_lot.nomenclature.reception_magasin.id
									defaut["emplacement"] = cont.nomenclature_lot.nomenclature.reception_emplacement
									defaut["contenant_type"] = cont.type_contenant.id
								else:
									info.update({"erreur": "Le contenant %s est déjà réceptionné" %(cb.cb["contenant"])})
				if cb.cb["type"] == "linautom":
					if cb.cb["format"] == "003":
						site = StockSite.objects.filter(code=cb.cb["site"])
						if len(site) > 0:
							defaut["site"] = site[0].id
						else:
							info.update({"erreur": "code barres emplacement invalide"})
						entrepot = StockEntrepot.objects.filter(code=cb.cb["entrepot"])
						if len(entrepot) > 0:
							defaut["entrepot"] = entrepot[0].id
						else:
							info.update({"erreur": "code barres emplacement invalide"})
						magasin = StockMagasin.objects.filter(code=cb.cb["magasin"])
						if len(magasin) > 0:
							defaut["magasin"] = magasin[0].id
						else:
							info.update({"erreur": "code barres emplacement invalide"})
						if cb.cb.has_key("emplacement"):
							defaut["emplacement"] = cb.cb["emplacement"]
					if cb.cb["format"] == "004":
						c_type = ContenantType.objects.filter(code=cb.cb["contenant_type"])
						if len(c_type) > 0:
							defaut["contenant_type"] = c_type[0].id
						else:
							info.update({"erreur": "code barres type contenant invalide"})

	return defaut, info



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
		return HttpResponseRedirect("/django/stock_labo/nomenclature/")

	defaut, info = reception_fonction(request)

	scan = ScanCBForm()
	form = ReceptionForm(initial=defaut)
	return render(request, "stock_labo_reception.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "scan" : scan, "info" : info})




