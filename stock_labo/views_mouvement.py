# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from fonction import *
from models import *
from forms import *


def mouvement_fonction(request):
	scan_cb = ScanCBForm()
	cb = LocalScanCB()
	defaut = {}
	info = {}


	user_param = UserPreference.objects.get(user=request.user)
	if len(request.GET) == 0:
		defaut.update({"site":user_param.site_perso.id})
		defaut.update({"entrepot":user_param.entrepot_perso.id})
		defaut.update({"magasin":user_param.magasin_perso.id})
#		defaut.update({"emplacement":user_param.emplacement_perso})
		mag = StockMagasin.objects.get(pk=int(defaut["magasin"]))
	else:
		if request.GET.has_key("d"):
			defaut.update({"d":request.GET["d"]})
		if request.GET.has_key("site"):
			defaut.update({"site":request.GET["site"]})
		if request.GET.has_key("entrepot"):
			defaut.update({"entrepot":request.GET["entrepot"]})
		if request.GET.has_key("magasin"):
			defaut.update({"magasin":request.GET["magasin"]})
		if request.GET.has_key("emplacement"):
			defaut.update({"emplacement":request.GET["emplacement"]})
		mag = StockMagasin.objects.get(pk=int(defaut["magasin"]))

		if request.GET.has_key("etiquette"):
			printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_emplacement_imprimante.id)
			imp = Impression.objects.get(pk=user_param.etiquette_emplacement.id)
			imp_d = ImpressionDetail.objects.filter(impression=imp)
			class ObjClass(object):
				def init(self):
					self.actuel_site = StockSite.objects.get(pk=request.GET["site"])
					self.actuel_entrepot = StockEntrepot.objects.get(pk=request.GET["entrepot"])
					self.actuel_magasin = StockMagasin.objects.get(pk=request.GET["magasin"])
					self.actuel_emplacement = request.GET["emplacement"]
					self.stock_site = StockSite.objects.get(pk=request.GET["site"])
					self.stock_entrepot = StockEntrepot.objects.get(pk=request.GET["entrepot"])
					self.stock_magasin = StockMagasin.objects.get(pk=request.GET["magasin"])
					self.stock_emplacement = request.GET["emplacement"]
				def actuel_emplacement_code(self):
					return "%s-%s-%s-%s" %(self.actuel_site.code, self.actuel_entrepot.code, self.actuel_magasin.code, self.actuel_emplacement)
				def stock_emplacement_code(self):
					return "%s-%s-%s-%s" %(self.stock_site.code, self.stock_entrepot.code, self.stock_magasin.code, self.stock_emplacement)
				def actuel_emplacement_cb(self):
					return "003:%s:%s:%s:%s" %(self.actuel_site.code, self.actuel_entrepot.code, self.actuel_magasin.code, self.actuel_emplacement)
				def stock_emplacement_cb(self):
					return "003:%s:%s:%s:%s" %(self.stock_site.code, self.stock_entrepot.code, self.stock_magasin.code, self.stock_emplacement)
				def actuel_emplacement_nom(self):
					return "%s - %s - %s - %s" %(self.actuel_site.description, self.actuel_entrepot.description, self.actuel_magasin.description, self.actuel_emplacement)
				def stock_emplacement_nom(self):
					return "%s - %s - %s - %s" %(self.stock_site.description, self.stock_entrepot.description, self.stock_magasin.description, self.stock_emplacement)
				def actuel_emplacement_nom_court(self):
					return "%s - %s" %(self.actuel_entrepot.description, self.actuel_magasin.description)
				def stock_emplacement_nom_court(self):
					return "%s - %s" %(self.stock_entrepot.description, self.stock_magasin.description)
			obj = ObjClass()
			obj.init()
			info.update({"info": "L'ettiquette emplacement est imprimée"})
			etiquette_print(printer, imp=imp, imp_d=imp_d, **{"user_param":user_param, "obj":obj, "return_url":"/django/stock_labo/mouvement/%s" %(make_addr_param({"site":request.GET["site"], "entrepot":request.GET["entrepot"], "magasin":request.GET["magasin"], "emplacement":request.GET["emplacement"]}))})
			return defaut, info
		if request.GET.has_key("cb") and request.GET["cb"] != "":
			cb.format_cb(request.GET["cb"])
			if cb.decode_cb():
				if cb.cb["type"] == "sap":
					if cb.cb["format"] == "10c":
						try:
							cont = Contenant.objects.get(code=cb.cb["contenant"])
						except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
							info.update({"erreur": "Le contenant %s n'existe pas" %(cb.cb["contenant"])})
						else:
							if cont.date_suppression == None:
								site = StockSite.objects.get(pk=defaut["site"])
								entrepot = StockEntrepot.objects.get(pk=defaut["entrepot"])
								magasin = StockMagasin.objects.get(pk=defaut["magasin"])
								cont.actuel_site = site
								cont.actuel_entrepot = entrepot
								cont.actuel_magasin = magasin
								cont.actuel_emplacement = defaut["emplacement"]
								cont.responsable_mouvement = request.user
								log = django_models.LogEntry()
								log.action_time = datetime.datetime.now()													#La date et l’heure de l’action.
								log.user = request.user																		#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
								log.content_type = ContentType.objects.get(app_label="stock_labo", model="contenant")		#Le type de contenu (ContentType) de l’objet modifié.
								log.object_id = cont.id																		#La représentation textuelle de la clé primaire de l’objet modifié.
								log.object_repr = unicode(cont)																#La représentation repr() de l’objet après sa modification.
								log.action_flag = django_models.CHANGE 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
								log.change_message = "mouvement déplacement"												#Description de la modification
								log.save()
								if mag.stock_magasin_type == StockMagasin.STOCK_MAGASIN_TYPE[3][0]:
									info.update({"info": "Le contenant %s est détruit" %(cb.cb["contenant"])})
									cont.suppression(request.user)
									cont.suppression_parent(request.user)
									cont.responsable_mouvement = None
									cont.panier_user = None
									log = django_models.LogEntry()
									log.action_time = datetime.datetime.now()													#La date et l’heure de l’action.
									log.user = request.user																		#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
									log.content_type = ContentType.objects.get(app_label="stock_labo", model="contenant")		#Le type de contenu (ContentType) de l’objet modifié.
									log.object_id = cont.id																		#La représentation textuelle de la clé primaire de l’objet modifié.
									log.object_repr = unicode(cont)																#La représentation repr() de l’objet après sa modification.
									log.action_flag = django_models.CHANGE 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
									log.change_message = "mouvement : suppression"												#Description de la modification
									log.save()
								else:
									if request.user.has_perm("stock_labo.panier"):
										if cont.stock_site == user_param.site_perso and cont.stock_entrepot == user_param.entrepot_perso and cont.stock_magasin == user_param.magasin_perso:
											cont.panier_user = request.user
										else:
											cont.panier_user = None
									if request.GET.has_key("stock_d") and request.GET["stock_d"] == "on":
										cont.stock_site = site
										cont.stock_entrepot = entrepot
										cont.stock_magasin = magasin
										cont.stock_emplacement = defaut["emplacement"]
										log = django_models.LogEntry()
										log.action_time = datetime.datetime.now()													#La date et l’heure de l’action.
										log.user = request.user																		#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
										log.content_type = ContentType.objects.get(app_label="stock_labo", model="contenant")		#Le type de contenu (ContentType) de l’objet modifié.
										log.object_id = cont.id																		#La représentation textuelle de la clé primaire de l’objet modifié.
										log.object_repr = unicode(cont)																#La représentation repr() de l’objet après sa modification.
										log.action_flag = django_models.CHANGE 														#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
										log.change_message = "mouvement enregistrement emplacement stockage"						#Description de la modification
										log.save()
									if request.GET.has_key("reception_d") and request.GET["reception_d"] == "on":
										cont.nomenclature_lot.nomenclature.reception_site = site
										cont.nomenclature_lot.nomenclature.reception_entrepot = entrepot
										cont.nomenclature_lot.nomenclature.reception_magasin = magasin
										cont.nomenclature_lot.nomenclature.reception_emplacement = defaut["emplacement"]
										cont.nomenclature_lot.nomenclature.save()
										log = django_models.LogEntry()
										log.action_time = datetime.datetime.now()													#La date et l’heure de l’action.
										log.user = request.user																		#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
										log.content_type = ContentType.objects.get(app_label="stock_labo", model="contenant")		#Le type de contenu (ContentType) de l’objet modifié.
										log.object_id = cont.id																		#La représentation textuelle de la clé primaire de l’objet modifié.
										log.object_repr = unicode(cont)																#La représentation repr() de l’objet après sa modification.
										log.action_flag = django_models.CHANGE 														#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
										log.change_message = "mouvement enregistrement emplacement reception"						#Description de la modification
										log.save()
									info.update({"info": "Le contenant %s est déplacé en<br/>%s" %(cb.cb["contenant"], cont.actuel_emplacement_nom())})
								cont.save()
							else:
								info.update({"erreur": "Le contenant %s est supprimé<br/>déplacement impossible" %(cb.cb["contenant"])})
					else:
						info.update({"erreur": "Code barre non reconnu"})
				elif cb.cb["type"] == "linautom":
					if cb.cb["format"] == "003":
						site = StockSite.objects.get(code=cb.cb["site"])
						entrepot = StockEntrepot.objects.get(code=cb.cb["entrepot"])
						magasin = StockMagasin.objects.get(code=cb.cb["magasin"])
						defaut.update({"site" : site.id})
						defaut.update({"entrepot" : entrepot.id})
						defaut.update({"magasin" : magasin.id})
						if cb.cb.has_key("emplacement"):
							defaut.update({"emplacement" : cb.cb["emplacement"]})
					else:
						info.update({"erreur": "Code barre non reconnu"})
				else:
					info.update({"erreur": "Code barre non reconnu"})
			else:
				info.update({"erreur": "Code barre non reconnu"})


	mag = StockMagasin.objects.get(pk=int(defaut["magasin"]))
	if not info.has_key("erreur"):
		if mag.stock_magasin_type == StockMagasin.STOCK_MAGASIN_TYPE[3][0]:
			info.update({"erreur": "!!! Emplacement de destruction !!!" })
			
	return defaut, info

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

	defaut, info = mouvement_fonction(request)

	form = MouvementForm(initial=defaut)
	scan = ScanCBForm()

	return render(request, "stock_labo_mouvement.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "scan" : scan, "info" : info})




