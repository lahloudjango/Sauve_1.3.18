# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from fonction import *
from models import *
from forms import *
from django.conf import settings
from lib_linautom.python import mysql
from django.db.models import Q, F
from lib_linautom.python import mail


@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def stock_perso(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Stock Perso", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Stock Perso", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Stock Perso", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))
	onglet = Onglets(request.user)
	onglet.set_actif_by_id(4)

	rech_def = {}
	info = {}

	if request.GET.has_key("emplacement") and request.GET["emplacement"] != "":
		if request.GET["emplacement"] == "TOUT":
			rech_def.update({"emplacement_sql" : ""})
		elif request.GET["emplacement"] == "SANS":
			rech_def.update({"emplacement_sql" : "AND actuel_emplacement = \"\""})
		elif request.GET["emplacement"] == "NONPROP":
			rech_def.update({"emplacement_sql" : "AND ( stock_site_id != %d OR stock_entrepot_id != %d OR stock_magasin_id != %d )" %(user_param.site_perso.id, user_param.entrepot_perso.id, user_param.magasin_perso.id) })
		else:
			rech_def.update({"emplacement_sql" : "AND actuel_emplacement = \"%s\"" %(request.GET["emplacement"])})
		rech_def.update({"emplacement":request.GET["emplacement"]})
	else:
		rech_def.update({"emplacement":"SANS"})
		rech_def.update({"emplacement_sql" : "AND actuel_emplacement = \"\""})

	if len(request.GET) > 0:
		if request.GET.has_key("cb") and request.GET["cb"] != "":
			try:
				cont = Contenant.objects.get(code=request.GET["cb"])
			except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
				info.update({"erreur": "Contenant inconnu : déplacement impossible"})
			else:
				if cont.date_suppression != None:
					info.update({"erreur": "Le contenant est supprimé : déplacement en stock impossible"})
				elif cont.actuel_site == cont.stock_site and cont.actuel_entrepot == cont.stock_entrepot and cont.actuel_magasin == cont.stock_magasin:
					info.update({"erreur": "Le contenant est déjà en stock, pas de déplacement"})
					if user_param.site_perso == cont.stock_site and user_param.entrepot_perso == cont.stock_entrepot and user_param.magasin_perso == cont.stock_magasin:
						info.update({"info": "Le contenant appartient à mon stock personnel"})
				else:
					if user_param.site_perso == cont.stock_site and user_param.entrepot_perso == cont.stock_entrepot and user_param.magasin_perso == cont.stock_magasin:
						info.update({"erreur": "Je suis propriétaire, rapatriement"})
					cont.actuel_site = cont.stock_site
					cont.actuel_entrepot = cont.stock_entrepot
					cont.actuel_magasin = cont.stock_magasin
					cont.panier_user = None
					cont.responsable_mouvement = request.user
					cont.save()
					info.update({"info": "Contenant %s ([%s] %s) est déplacé en stock %s %s" %(request.GET["cb"], cont.nomenclature_lot.nomenclature.code, cont.nomenclature_lot.nomenclature.description, cont.stock_entrepot, cont.actuel_magasin)})
	
		if request.GET.has_key("tout_en_stock") and request.GET["tout_en_stock"] != "":
			cont = Contenant.objects.filter(actuel_site=user_param.site_perso, actuel_entrepot=user_param.entrepot_perso, actuel_magasin=user_param.magasin_perso)
			cont = cont.filter( date_suppression__isnull=True )
			cont = cont.filter( ~Q(actuel_site=F("stock_site")) | ~Q(actuel_entrepot=F("stock_entrepot")) | ~Q(actuel_magasin=F("stock_magasin")) )

			if cont.count() > 0:
				for c in cont:
					c.actuel_site = c.stock_site
					c.actuel_entrepot = c.stock_entrepot
					c.actuel_magasin = c.stock_magasin
					c.panier_user = None
					c.responsable_mouvement = request.user
					c.save()
				i = "<br/>".join([ 
					"Contenant %s ([%s] %s) => stock %s %s" %(c.code, c.nomenclature_lot.nomenclature.code, c.nomenclature_lot.nomenclature.description, c.stock_entrepot, c.actuel_magasin)
					for c in cont ])
				info.update({"info": i})

				if request.user.email != None and request.user.email != "":
					max_len = max([ len(c.nomenclature_lot.nomenclature.description) for c in cont ])
					# Envoie email
					model = "Contenant %%s ([%%s] %%-%ss) => stock %%s %%s" %(max_len)
					mail_corps = "\nLes contenants suivant doivent être remis dans leur emplacement de stockage\n\n"
					mail_corps += "\n".join([ model %(c.code, c.nomenclature_lot.nomenclature.code, c.nomenclature_lot.nomenclature.description, c.stock_entrepot, c.actuel_magasin) for c in cont ])
					m = mail.MailAttach(mail_corps)
					m.from_("Application_stockparis@takasago.com")
					m.reply_to("charly.gontero@linautom.fr")  #"TEPL-gestion-pt@takasago.com"
					m.to([request.user.email, "charly.gontero@linautom.fr",])
					if version.status_developement["data"] == "prod":
						m.subject("Stock Labo Paris, Déplacement de groupés")
					else:
						m.subject("Ne pas tenir compte de cette email, je fait des tests sur le serveur, charly")
					#m.attach(dico_fichier_xlsx["fichier_xlsx"])
					#log_print("Mail to %s ... " %(m.list_to))
					#m.send(smtp="smtp.laposte.net", expediteur="charly.gontero@laposte.net", user="charly.gontero", password="1Addyson", starttls=False)
					m.send(smtp="par-srv-cas01.eu.takasago.com", expediteur="Application_stockparis@takasago.com", user=None , password=None, starttls=False)


	list1 = Liste(caption="Liste du stock personnel", summary="Liste du stock personnel")
	my=mysql.Mysql()
	my.open(mysql_host=settings.DATABASES["default"]["HOST"], mysql_port=int(settings.DATABASES["default"]["PORT"]), mysql_user=settings.DATABASES["default"]["USER"], mysql_password=settings.DATABASES["default"]["PASSWORD"] )
	querry = """
		SELECT stock_labo_contenant.id as contenant_id,
			stock_labo_contenant.code as contenant_code,
			stock_labo_nomenclature.code as nomenclature_code,
			stock_labo_nomenclature.description as nomenclature_description,
			stock_labo_nomenclaturelot.code as nomenclaturelot_code, 
			stock_labo_nomenclaturelot.poids_reference as nomenclaturelot_poids_reference,
			stock_labo_contenant.date_creation as contenant_date_creation,
			stock_labo_contenant.date_fin_validite as contenant_date_fin_validite,
			stock_labo_contenant.actuel_site_id as contenant_actuel_site_id,
			stock_labo_contenant.actuel_entrepot_id as contenant_actuel_entrepot_id,
			stock_labo_contenant.actuel_magasin_id as contenant_actuel_magasin_id,
			stock_labo_contenant.stock_site_id as contenant_stock_site_id,
			stock_labo_contenant.stock_entrepot_id as contenant_stock_entrepot_id,
			stock_labo_contenant.stock_magasin_id as contenant_stock_magasin_id,
			stock_labo_contenant.poids as contenant_poids
		FROM %s.stock_labo_contenant
			LEFT JOIN %s.stock_labo_nomenclaturelot  ON stock_labo_contenant.nomenclature_lot_id = stock_labo_nomenclaturelot.id
			LEFT JOIN %s.stock_labo_nomenclature     ON stock_labo_nomenclaturelot.nomenclature_id = stock_labo_nomenclature.id
		WHERE actuel_site_id = %d AND actuel_entrepot_id = %d AND actuel_magasin_id = %d
			AND stock_labo_contenant.date_suppression IS NULL %s""" %(settings.DATABASES["default"]["NAME"],
																	settings.DATABASES["default"]["NAME"],
																	settings.DATABASES["default"]["NAME"],
																	user_param.site_perso.id,
																	user_param.entrepot_perso.id,
																	user_param.magasin_perso.id,
																	rech_def["emplacement_sql"])
	ing = my.execute(querry)
	list1.liste.update({"n_ligne_total" : len(ing)})

	l = Liste.Ligne()
	l.add_cellule(Contenant._meta.fields[1].nom_colonne, title=Contenant._meta.fields[1].nom_long, width="10%")										#code contenant
	l.add_cellule(Nomenclature._meta.fields[1].nom_colonne, title=Nomenclature._meta.fields[1].nom_long, width="10%")								#code article
	l.add_cellule(Nomenclature._meta.fields[2].nom_colonne, title=Nomenclature._meta.fields[2].nom_long)											#description
	l.add_cellule(NomenclatureLot._meta.fields[1].nom_colonne, title=NomenclatureLot._meta.fields[1].nom_long, width="10%")							#lot
	l.add_cellule(Contenant._meta.fields[13].nom_colonne, title=Contenant._meta.fields[13].nom_long)												#poids
	l.add_cellule(Contenant._meta.fields[14].nom_colonne, title=Contenant._meta.fields[14].nom_long, width="10%")									#date_creation
	l.add_cellule(Contenant._meta.fields[17].nom_colonne, title=Contenant._meta.fields[17].nom_long, width="10%")									#date_fin_validite
	l.add_cellule("<center>Prop</center>", title="Propriétaire", width="2%")																		#propiétaire
	if request.user.has_perm("stock_labo.panier"):
		l.add_cellule("<center>P</center>", title="Panier", width="2%")																					#Panier
	list1.add_headers(l.get_ligne())

	for i in ing:
		l = Liste.Ligne()
		l.add_cellule(i["contenant_code"], href="/django/stock_labo/stock_perso_contenant_edit/%s" %(make_addr_param({"id_contenant":i["contenant_id"]})))
		l.add_cellule(i["nomenclature_code"])
		l.add_cellule(i["nomenclature_description"])
		l.add_cellule(i["nomenclaturelot_code"])
		l.add_cellule(i["contenant_poids"], title="")
		l.add_cellule(i["contenant_date_creation"].strftime(Contenant._meta.fields[14].format_date_time))
		l.add_cellule(i["contenant_date_fin_validite"].strftime(Contenant._meta.fields[17].format_date_time))
		if i["contenant_stock_site_id"] == user_param.site_perso.id and i["contenant_stock_entrepot_id"] == user_param.entrepot_perso.id and i["contenant_stock_magasin_id"] == user_param.magasin_perso.id:
			l.add_cellule(u"<center>X</center>", title=u"Je suis propriétaire du contenant")
		else:
			l.add_cellule(u"<center> </center>", title=u"Je ne suis pas propriétaire du contenant")
		if request.user.has_perm("stock_labo.panier"):
			l.add_cellule(u"<center><img src=\"/static/svg/edit-undo.svg\" height=\"24\" alt=\"Mettre dans le stock personnel\"/></center>", title=u"Mettre dans le panier", href="/django/stock_labo/stock_perso_contenant_panier/%s" %(make_addr_param({"id_contenant":i["contenant_id"], "ajouter":"yes"})))

		list1.add_ligne(l.get_ligne())

	scan = ScanCBPistoletForm()
	filtre = StockPersoFiltreForm(initial=rech_def)
	filtre_default = [
		["SANS","Sans emplacement"],
		["TOUT","Afficher tout"],
		["NONPROP","Non propriétaire"],
		]

	querry = """
		SELECT DISTINCT actuel_emplacement
		FROM %s.stock_labo_contenant
		WHERE actuel_site_id = %d AND actuel_entrepot_id = %d AND actuel_magasin_id = %d
			AND date_suppression IS NULL AND actuel_emplacement != \"\" """ %(settings.DATABASES["default"]["NAME"],
																	user_param.site_perso.id,
																	user_param.entrepot_perso.id,
																	user_param.magasin_perso.id)
	emp = my.execute(querry)

	my.close()
	filtre.fields["emplacement"].choices = filtre_default + [ [c["actuel_emplacement"], c["actuel_emplacement"]] for c in emp ]
	return render(request, "stock_labo_stock_perso_liste.html", 
			{
			"header": header.get_headers(),
			"onglet" : onglet.get_onglets(),
			"list" : list1.get_liste(),
			"scan": scan,
			"filtre": filtre,
			"info" : info,
			})

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def stock_perso_contenant_edit(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Stock Perso", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Stock Perso", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Stock Perso", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))
	onglet = Onglets(request.user)
	onglet.set_actif_by_id(0)
	if len(request.GET) > 0:
		if request.GET.has_key("annuler"):
			return HttpResponseRedirect("/django/stock_labo/stock_perso/")
		elif request.GET.has_key("valider") or request.GET.has_key("nouveau") or request.GET.has_key("dupliquer"):
			code_barre = None
			if request.GET["id_contenant"] == "" or request.GET.has_key("nouveau") or request.GET.has_key("dupliquer"):
				form = ContenantForm(request.GET)
				if form.is_valid():
					cont = form.save(commit=True)
					cont.code = "2%0.9d" %(cont.id)
					cont.date_creation = datetime.date.today()
					cont.save()
					log = django_models.LogEntry()
					log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
					log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
					log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())		#Le type de contenu (ContentType) de l’objet modifié.
					log.object_id = cont.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
					log.object_repr = unicode(cont)																		#La représentation repr() de l’objet après sa modification.
					log.action_flag = django_models.ADDITION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
					log.change_message = "stock_perso_contenant_edit"													#Description de la modification
					log.save()
					if request.GET["id_nomenclature_lot"] == "":
						return HttpResponseRedirect("/django/stock_labo/stock_perso/")
					else:
						return HttpResponseRedirect("/django/stock_labo/stock_perso/")
				else:
					return render(request, "stock_labo_stock_perso_contenant_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "code_barre" : code_barre})
			else:
				code_barre = request.GET["id_contenant"]
				cont = Contenant.objects.get(pk=int(request.GET["id_contenant"]))
				form = ContenantForm(request.GET, instance=cont)
				if form.is_valid():
					cont = form.save(commit=True)
					log = django_models.LogEntry()
					log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
					log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
					log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())		#Le type de contenu (ContentType) de l’objet modifié.
					log.object_id = cont.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
					log.object_repr = unicode(cont)																		#La représentation repr() de l’objet après sa modification.
					log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
					log.change_message = "stock_perso_contenant_edit"													#Description de la modification
					log.save()
					return HttpResponseRedirect("/django/stock_labo/stock_perso/")
				else:
					return render(request, "stock_labo_stock_perso_contenant_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "code_barre" : code_barre})
		elif request.GET.has_key("supprimer"):
			cont = Contenant.objects.get(pk=int(request.GET["id_contenant"]))
			log = django_models.LogEntry()
			log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
			log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
			log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())		#Le type de contenu (ContentType) de l’objet modifié.
			log.object_id = cont.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
			log.object_repr = unicode(cont)																		#La représentation repr() de l’objet après sa modification.
			log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
			log.change_message = "stock_perso_contenant_edit : suppression"										#Description de la modification
			log.save()
			cont.suppression(request.user)
			cont.suppression_parent(request.user)
			return HttpResponseRedirect("/django/stock_labo/stock_perso/")
		elif request.GET.has_key("print_empalacement"):
			printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_contenant_imprimante.id)
			imp = Impression.objects.get(pk=user_param.etiquette_contenant.id)
			imp_d = ImpressionDetail.objects.filter(impression=imp)
			obj = Contenant.objects.get(pk=request.GET["id_contenant"])
			return etiquette_print(printer, imp=imp, imp_d=imp_d, **{"user_param":user_param, "obj":obj, "return_url":"/django/stock_labo/stock_perso/"})
		else:
			defaut = {}
			code_barre = None
			nomenclature_d = None
			nomenclature_lot_d = None
			if request.GET.has_key("id_contenant"):
				cont = Contenant.objects.get(pk=int(request.GET["id_contenant"]))
				code_barre = cont.code
				nomenclature_lot_d = cont.nomenclature_lot.code
				nomenclature_d = cont.nomenclature_lot.nomenclature.__unicode__()
				defaut.update({"id_nomenclature" : cont.nomenclature_lot.nomenclature.id})
				defaut.update({"id_nomenclature_lot" : cont.nomenclature_lot.id})
				defaut.update({"id_contenant" : cont.id})
				form = ContenantForm(instance=cont, initial=defaut)
			elif request.GET.has_key("id_nomenclature_lot"):
				lot = NomenclatureLot.objects.get(pk=int(request.GET["id_nomenclature_lot"]))
				nomenclature_lot_d = lot.code
				nomenclature_d = lot.nomenclature.__unicode__()
				defaut.update({"id_nomenclature" : lot.nomenclature.id})
				defaut.update({"id_nomenclature_lot" : lot.id})
				form = ContenantForm(initial=defaut)
			else:
				form = ContenantForm()
			return render(request, "stock_labo_stock_perso_contenant_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "nomenclature_d" : nomenclature_d, "nomenclature_lot_d" : nomenclature_lot_d, "form" : form, "code_barre" : code_barre})

		form = ContenantForm()
		return render(request, "stock_labo_stock_perso_contenant_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form})

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def stock_perso_contenant_panier(request):
	if request.GET.has_key("id_contenant"):
		user_param = UserPreference.objects.get(user=request.user)
		ing = Contenant.objects.get(pk=int(request.GET["id_contenant"]))
		log = django_models.LogEntry()
		if request.GET.has_key("ajouter"):
			ing.panier_user = request.user
			log.change_message = "stock_perso_contenant_panier : entrée"								#Description de la modification
		if request.GET.has_key("supprimer"):
			ing.panier_user = None
			log.change_message = "stock_perso_contenant_panier : sortie"								#Description de la modification
		ing.save()
		log.user = request.user																			#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
		log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())	#Le type de contenu (ContentType) de l’objet modifié.
		log.object_id = ing.id																			#La représentation textuelle de la clé primaire de l’objet modifié.
		log.object_repr = unicode(ing)																	#La représentation repr() de l’objet après sa modification.
		log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
		log.save()
	return HttpResponseRedirect("/django/stock_labo/stock_perso/")
