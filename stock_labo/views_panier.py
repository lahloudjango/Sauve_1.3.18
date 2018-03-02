# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from fonction import *
from models import *
from forms import *


@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def panier(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Panier", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Panier", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Panier", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))
	onglet = Onglets(request.user)
	onglet.set_actif_by_id(3)

	bouton = Boutons()
#	bouton.add_bouton("Panier dans<br/>le stock<br/>personnel", title="Créer un nouvel ingrédient", href="#")
#	bouton.add_bouton("Ranger<br/>le panier<br/>en stock", title="Importer un fichier", href="#")

	list1 = Liste(caption="Liste des contenants du panier", summary="Liste des contenants du panier")
#	ing = Contenant.objects.filter(panier_user=request.user, date_suppression__isnull=True)
	ing = Contenant.objects.filter(panier_user=request.user)
	list1.liste.update({"n_ligne_affiche" : len(ing)})

	l = Liste.Ligne()
	l.add_cellule(Contenant._meta.fields[1].nom_colonne, title=Contenant._meta.fields[1].nom_long, width="10%")										#code contenant
	l.add_cellule(Nomenclature._meta.fields[1].nom_colonne, title=Nomenclature._meta.fields[1].nom_long, width="10%")								#code article
	l.add_cellule(Nomenclature._meta.fields[2].nom_colonne, title=Nomenclature._meta.fields[2].nom_long)											#description
	l.add_cellule("Emplacement A.", title="Emplacement actuel")																						#emplacement
	l.add_cellule("Emplacement S.", title="Emplacement de stockage normal")																			#stockage
	l.add_cellule(NomenclatureLot._meta.fields[1].nom_colonne, title=NomenclatureLot._meta.fields[1].nom_long, width="10%")							#lot
#	l.add_cellule(Contenant._meta.fields[13].nom_colonne, title=Contenant._meta.fields[13].nom_long)												#poids
	l.add_cellule(Contenant._meta.fields[14].nom_colonne, title=Contenant._meta.fields[14].nom_long, width="10%")									#date_creation
	l.add_cellule(Contenant._meta.fields[17].nom_colonne, title=Contenant._meta.fields[17].nom_long, width="10%")									#date_fin_validite
	l.add_cellule("<center>R</center>", title="Ranger", width="2%")																					#R
	l.add_cellule("<center>S.P.</center>", title="Mettre dans le stock personnel", width="2%")														#S.P.
	list1.add_headers(l.get_ligne())

	for i in ing:
		l = Liste.Ligne()
		l.add_cellule(i.code, href="/django/stock_labo/panier_contenant_edit/%s" %(make_addr_param({"id_contenant":i.id})))
		l.add_cellule(i.nomenclature_lot.nomenclature.code)
		l.add_cellule(i.nomenclature_lot.nomenclature.description)
		l.add_cellule(i.actuel_emplacement_nom_court(), title=i.actuel_emplacement_nom())
		l.add_cellule(i.stock_emplacement_nom_court(), title=i.stock_emplacement_nom())
		l.add_cellule(i.nomenclature_lot.code)
#		l.add_cellule(i.poids)
		l.add_cellule(i.f_date_creation(Contenant._meta.fields[14].format_date_time))
		l.add_cellule(i.f_date_fin_validite(Contenant._meta.fields[17].format_date_time))
		l.add_cellule(u"<center><img src=\"/static/svg/edit-undo.svg\" height=\"24\" alt=\"Remettre en stock\"/></center>", title=u"Remettre en stock", href="/django/stock_labo/panier_contenant_panier/%s" %(make_addr_param({"supprimer":"yes", "id_contenant":i.id})))
		l.add_cellule(u"<center><img src=\"/static/svg/edit-redo.svg\" height=\"24\" alt=\"Mettre dans le stock personnel\"/></center>", title=u"Mettre dans le stock personnel", href="/django/stock_labo/panier_contenant_panier/%s" %(make_addr_param({"ajouter":"yes", "id_contenant":i.id})))

		list1.add_ligne(l.get_ligne())




	return render(request, "stock_labo_panier_liste.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "list" : list1.get_liste(), "bouton" : bouton.get_boutons()})

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def panier_contenant_edit(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Panier", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Panier", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Panier", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))
	onglet = Onglets(request.user)
	onglet.set_actif_by_id(0)
	if len(request.GET) > 0:
		if request.GET.has_key("annuler"):
			return HttpResponseRedirect("/django/stock_labo/panier/")
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
					log.action_flag = django_models.ADDITION 																	#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
					log.change_message = "panier_contenant_edit"														#Description de la modification
					log.save()
					if request.GET["id_nomenclature_lot"] == "":
						return HttpResponseRedirect("/django/stock_labo/panier/")
					else:
						return HttpResponseRedirect("/django/stock_labo/panier/")
				else:
					return render(request, "stock_labo_panier_contenant_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "code_barre" : code_barre})
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
					log.action_flag = django_models.CHANGE 																	#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
					log.change_message = "panier_contenant_edit"														#Description de la modification
					log.save()
					return HttpResponseRedirect("/django/stock_labo/panier/")
				else:
					return render(request, "stock_labo_panier_contenant_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "code_barre" : code_barre})
		elif request.GET.has_key("supprimer"):
			cont = Contenant.objects.get(pk=int(request.GET["id_contenant"]))
			log = django_models.LogEntry()
			log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
			log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
			log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())		#Le type de contenu (ContentType) de l’objet modifié.
			log.object_id = cont.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
			log.object_repr = unicode(cont)																		#La représentation repr() de l’objet après sa modification.
			log.action_flag = django_models.CHANGE 																	#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
			log.change_message = "panier_contenant_edit : suppression"														#Description de la modification
			log.save()
			cont.suppression(request.user)
			cont.suppression_parent(request.user)
			return HttpResponseRedirect("/django/stock_labo/panier/")
		elif request.GET.has_key("print_empalacement"):
			printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_contenant_imprimante.id)
			imp = Impression.objects.get(pk=user_param.etiquette_contenant.id)
			imp_d = ImpressionDetail.objects.filter(impression=imp)
			obj = Contenant.objects.get(pk=request.GET["id_contenant"])
			return etiquette_print(printer, imp=imp, imp_d=imp_d, **{"user_param":user_param, "obj":obj, "return_url":"/django/stock_labo/panier/"})
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
			return render(request, "stock_labo_panier_contenant_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "nomenclature_d" : nomenclature_d, "nomenclature_lot_d" : nomenclature_lot_d, "form" : form, "code_barre" : code_barre})

		form = ContenantForm()
		return render(request, "stock_labo_panier_contenant_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form})

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def panier_contenant_panier(request):
	if request.GET.has_key("id_contenant"):
		ing = Contenant.objects.get(pk=int(request.GET["id_contenant"]))
		log = django_models.LogEntry()
		if request.GET.has_key("ajouter"):
			user_param = UserPreference.objects.get(user=request.user)
			ing.actuel_site = user_param.site_perso
			ing.actuel_entrepot = user_param.entrepot_perso
			ing.actuel_magasin = user_param.magasin_perso
			ing.actuel_emplacement = user_param.emplacement_perso
			ing.panier_user = None
			log.change_message = "panier_contenant_panier : entrer emplacement perso"						#Description de la modification
		if request.GET.has_key("supprimer"):
			ing.actuel_site = ing.stock_site
			ing.actuel_entrepot = ing.stock_entrepot
			ing.actuel_magasin = ing.stock_magasin
			ing.actuel_emplacement = ing.stock_emplacement
			ing.panier_user = None
			log.change_message = "panier_contenant_panier : remetre en stock"								#Description de la modification
		ing.save()
		log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
		log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
		log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())		#Le type de contenu (ContentType) de l’objet modifié.
		log.object_id = ing.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
		log.object_repr = unicode(ing)																		#La représentation repr() de l’objet après sa modification.
		log.action_flag = django_models.CHANGE 																	#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
		log.change_message = "panier_contenant_panier"														#Description de la modification
		log.save()
	return HttpResponseRedirect("/django/stock_labo/panier/")


