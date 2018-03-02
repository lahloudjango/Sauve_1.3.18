# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from fonction import *
from models import *
from forms import *
from daemon import django_clean
import settings_default


@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def nettoyage(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Article", user="%s" %(request.user), panier=Contenant.objects.filter(panier_user=request.user).count())
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Article", user="%s" %(request.user), panier=Contenant.objects.filter(panier_user=request.user).count())
	else:
		header = Headers(page="Article", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=Contenant.objects.filter(panier_user=request.user).count())

	onglet = Onglets(request.user)
	onglet.set_actif_by_id(0)

	info = {}
	if len(request.GET) > 0:
		if request.GET.has_key("rechercher"):

			liste_recherche = django_clean.recherche()

			dico_fichier_xlsx = django_clean.construction_xlsx(liste_recherche)

			response = HttpResponse(open(dico_fichier_xlsx["fichier_xlsx"], "r").read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
			response["Content-Disposition"] = "attachment; filename=\"%s\"" %(dico_fichier_xlsx["fichier_xlsx"])
			return response


#			return render(request, "stock_labo_nomenclature_nettoyage.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "info": info})
		if request.GET.has_key("annuler"):
			return HttpResponseRedirect("/django/stock_labo/nomenclature/")
	else:
		return render(request, "stock_labo_nomenclature_nettoyage.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "info": info, "brython" : True})

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def nomenclature(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Article", user="%s" %(request.user), panier=Contenant.objects.filter(panier_user=request.user).count())
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Article", user="%s" %(request.user), panier=Contenant.objects.filter(panier_user=request.user).count())
	else:
		header = Headers(page="Article", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=Contenant.objects.filter(panier_user=request.user).count())

	onglet = Onglets(request.user)
	onglet.set_actif_by_id(0)
	list1 = None
	list2 = None
	list3 = None
	list4 = None
	bouton = Boutons()
	bouton.add_bouton("Article MP", title="Créer un nouvel ingrédient", href="/django/stock_labo/nomenclature_edit/")
#	bouton.add_bouton("Nouveau<br/>concentré", title="Créer un nouveau ingrédient", href="/django/stock_labo/nomenclature_edit2/")
	bouton.add_bouton("Serie/coupage", title="Créer une nouvelle serie de formule/coupage", href="/django/stock_labo/nomenclature_edit3/")
#	bouton.add_bouton("Nouveau<br/>Concentré<br/>Roxane", title="Créer un nouvel article/lot/contenant depuis une formule Roxane", href="/django/stock_labo/nomenclature_edit4/")
	bouton.add_bouton("Concentré", title="Créer un nouvel article/lot/contenant depuis une formule Roxane ou manuellement", href="/django/stock_labo/nomenclature_edit5/")
	if request.user.has_perm("stock_labo.article_nettoyage"):
		bouton.add_bouton("Nettoyage", title="Génère un fichier.xlsx de suives du nettoyage", href="/django/stock_labo/nomenclature_nettoyage/", new_windows=True)

	rech_def = {}
	if request.GET.has_key("limit_du"):
		rech_def.update({"limit_du":int(request.GET["limit_du"])})
	else:
		rech_def.update({"limit_du":0})
	if request.GET.has_key("limit_au"):
		rech_def.update({"limit_au":int(request.GET["limit_au"])})
	else:
		rech_def.update({"limit_au":25})
	if request.GET.has_key("suivant"):
		if rech_def["limit_au"] <= rech_def["limit_du"]:
			pas = rech_def["limit_au"]
			rech_def["limit_au"] = rech_def["limit_du"] + pas
		else:
			pas = rech_def["limit_au"] - rech_def["limit_du"]
			rech_def["limit_au"] += pas
			rech_def["limit_du"] += pas
	if request.GET.has_key("recherche"):
		if rech_def["limit_au"] <= rech_def["limit_du"]:
			pas = rech_def["limit_au"]
			rech_def["limit_au"] = rech_def["limit_du"] + pas
		else:
			pas = rech_def["limit_au"] - rech_def["limit_du"]
			rech_def["limit_au"] = pas
			rech_def["limit_du"] = 0

	if request.GET.has_key("code"):
		rech_def.update({"code":request.GET["code"]})
	if request.GET.has_key("description"):
		rech_def.update({"description":request.GET["description"]})
	if request.GET.has_key("type_nomenclature"):
		rech_def.update({"type_nomenclature":request.GET["type_nomenclature"]})
	if request.GET.has_key("date_du"):
		rech_def.update({"date_du":request.GET["date_du"]})
	if request.GET.has_key("date_au"):
		rech_def.update({"date_au":request.GET["date_au"]})
	if request.GET.has_key("collection"):
		rech_def.update({"collection":request.GET["collection"]})
	if request.GET.has_key("sup"):
		rech_def.update({"sup":request.GET["sup"]})
	if request.GET.has_key("commentaire"):
		rech_def.update({"commentaire":request.GET["commentaire"]})
	recherche = RechercheNomenclatureForm(initial=rech_def)



	list1 = Liste(caption=Nomenclature.__doc__, summary=Nomenclature.__doc__)

	if rech_def.has_key("sup") and rech_def["sup"] == "on":
		ing = Nomenclature.objects.filter(date_suppression__isnull=False)
	else:
		ing = Nomenclature.objects.filter(date_suppression__isnull=True)
	list1.liste.update({"n_ligne_total" : ing.count()})

	if rech_def.has_key("code") and rech_def["code"] != "":
		ing = ing.filter(code__icontains=rech_def["code"])
	if rech_def.has_key("description") and rech_def["description"] != "":
		ing = ing.filter(description__icontains=rech_def["description"])
	if rech_def.has_key("type_nomenclature") and rech_def["type_nomenclature"] != "":
		ing = ing.filter(nomenclature_type__code__icontains=rech_def["type_nomenclature"])
	if rech_def.has_key("date_du") and rech_def["date_du"] != "":
		ing = ing.filter(date_creation__gte=rech_def["date_au"])
	if rech_def.has_key("date_au") and rech_def["date_du"] != "":
		ing = ing.filter(date_creation__lte=rech_def["date_au"])
	if rech_def.has_key("commentaire") and rech_def["commentaire"] != "":
		ing = ing.filter(commentaire__icontains=rech_def["commentaire"])
	if rech_def.has_key("collection"):
		ing = ing.filter(collection=True)

	list1.liste.update({"n_ligne_affiche" : ing.count()})
	ing = ing[rech_def["limit_du"]:rech_def["limit_au"]]
	list1.liste.update({"n_ligne_limit" : ing.count()})

	l = Liste.Ligne()
	l.add_cellule(Nomenclature._meta.fields[1].nom_colonne, title=Nomenclature._meta.fields[1].nom_long, width="10%")								#code
	l.add_cellule(Nomenclature._meta.fields[2].nom_colonne, title=Nomenclature._meta.fields[2].nom_long)											#description
	l.add_cellule("<center>C</center>", title="Commentaire", width="50px")																			#C
	l.add_cellule(NomenclatureType._meta.fields[1].nom_colonne, title=NomenclatureType._meta.fields[1].nom_long, width="70px")						#type
	l.add_cellule(Nomenclature._meta.fields[9].nom_colonne, title=Nomenclature._meta.fields[9].nom_long, width="10%")								#date création
	l.add_cellule("<center>Col</center>", title=Nomenclature._meta.fields[12].nom_long, width="50px")												#collection
	l.add_cellule("<center>Lot</center>", title="Recherche des lots pour cette article", width="50px")												#Recherche Lot
#	l.add_cellule("<center>Imp. É.</center>", title="Imprimer une nouvelle etiquette ingrédient", width="50px")										#Etiquette
	l.add_cellule("<center>N. Lot</center>", title="Créer un nouveau Lot", width="50px")															#Ajouter
	list1.add_headers(l.get_ligne())

	for i in ing:
		l = Liste.Ligne()
		l.add_cellule(i.code, title="Editer fiche", href="/django/stock_labo/nomenclature_edit/%s" %(make_addr_param({"id_nomenclature":i.id})))
		l.add_cellule(i.description)
		if i.commentaire == "" or i.commentaire == None:
			l.add_cellule(" ")
		else:
			l.add_cellule("<center><img src=\"/static/svg/attention.svg\" height=\"24\" alt=\"Commentaire\"/></center>", title=i.commentaire, style="background:OrangeRed;")
		l.add_cellule("<center>%s</center>" %(i.nomenclature_type.code), title=i.nomenclature_type.description)
		l.add_cellule(i.f_date_creation(Nomenclature._meta.fields[10].format_date_time))
		if i.collection == True:
			l.add_cellule("<center>X</center>")
		else:
			l.add_cellule(" ")
		l.add_cellule("<center><img src=\"/static/svg/system-search.svg\" height=\"24\" alt=\"Etiquette\"/></center>", title="Rechercher lot", href="/django/stock_labo/nomenclature/%s" %(make_addr_param(rech_def, {"id_nomenclature":i.id})))
#		l.add_cellule("<center><img src=\"/static/svg/document-print.svg\" height=\"24\" alt=\"Etiquette\"/></center>", title="Impression étiquette", href="/django/stock_labo/nomenclature_etiquette_print/%s" %(make_addr_param(rech_def, {"id_nomenclature":i.id})))
		l.add_cellule("<center><img src=\"/static/svg/list-add.svg\" height=\"24\" alt=\"Ajouter\"/></center>", title="Nouveau lot", href="/django/stock_labo/nomenclature_lot_edit/%s" %(make_addr_param({"id_nomenclature":i.id})))

		list1.add_ligne(l.get_ligne())


	if len(request.GET) > 0:
		if request.GET.has_key("id_nomenclature"):

			nomenclature = Nomenclature.objects.get(pk=int(request.GET["id_nomenclature"]))
			l = Liste.Ligne()
			l.add_cellule(nomenclature.code, title="Editer fiche", href="/django/stock_labo/nomenclature_edit/%s" %(make_addr_param({"id_nomenclature":nomenclature.id})))
			l.add_cellule(nomenclature.description)
			if nomenclature.commentaire == "" or nomenclature.commentaire == None:
				l.add_cellule(" ")
			else:
				l.add_cellule("<center><img src=\"/static/svg/format-justify-fill.svg\" height=\"24\" alt=\"Commentaire\"/></center>", title=nomenclature.commentaire)
			l.add_cellule(nomenclature.nomenclature_type.code, title=nomenclature.nomenclature_type.description)
			l.add_cellule(nomenclature.f_date_creation(Nomenclature._meta.fields[10].format_date_time))
			if nomenclature.collection == True:
				l.add_cellule("<center>X</center>")
			else:
				l.add_cellule(" ")
			l.add_cellule("<center><img src=\"/static/svg/system-search.svg\" height=\"24\" alt=\"Etiquette\"/></center>", title="Rechercher lot", href="/django/stock_labo/nomenclature/%s" %(make_addr_param(rech_def, {"id_nomenclature":nomenclature.id})))
#			l.add_cellule("<center><img src=\"/static/svg/document-print.svg\" height=\"24\" alt=\"Etiquette\"/></center>", title="Impression étiquette", href="/django/stock_labo/nomenclature_etiquette_print/%s" %(make_addr_param(rech_def, {"id_nomenclature":nomenclature.id})))
			l.add_cellule("<center><img src=\"/static/svg/list-add.svg\" height=\"24\" alt=\"Ajouter\"/></center>", title="Nouveau lot", href="/django/stock_labo/nomenclature_lot_edit/%s" %(make_addr_param({"id_nomenclature":nomenclature.id})))
			list1.add_headers(l.get_ligne())

			if rech_def.has_key("sup") and rech_def["sup"] == "on":
				nomenclature_lot = NomenclatureLot.objects.filter(nomenclature=int(request.GET["id_nomenclature"])).filter(date_suppression__isnull=False)
			else:
				nomenclature_lot = NomenclatureLot.objects.filter(nomenclature=int(request.GET["id_nomenclature"])).filter(date_suppression__isnull=True)

			list2 = Liste(caption="Liste des lots de [%s] %s" %(nomenclature.code, nomenclature.description), summary=NomenclatureLot.__doc__)
			l = Liste.Ligne()
			l.add_cellule(NomenclatureLot._meta.fields[1].nom_colonne, title=NomenclatureLot._meta.fields[1].nom_long)	#code lot
#			l.add_cellule(NomenclatureLot._meta.fields[2].nom_colonne, title=NomenclatureLot._meta.fields[2].nom_long)				#Description
			l.add_cellule(NomenclatureLot._meta.fields[3].nom_colonne, title=NomenclatureLot._meta.fields[3].nom_long, width="12%")	#Date création
			l.add_cellule(NomenclatureLot._meta.fields[4].nom_colonne, title=NomenclatureLot._meta.fields[4].nom_long, width="12%")	#Date création
			l.add_cellule("<center>Contenant</center>", title="Rechercher contenant", width="2%")											#Rechercher
			l.add_cellule("<center>Compo</center>", title="Liste de composition", width="2%")											#Définition disponible
#			l.add_cellule("<center>Imp. É</center>", title="Imprimer une nouvelle etiquette", width="50px")								#Etiquette
			l.add_cellule("<center>Nouveau. C.</center>", title="Créer un nouveau contenant", width="100px")									#ajouter
			list2.add_headers(l.get_ligne())
			for lot in nomenclature_lot:
				l = Liste.Ligne()
				l.add_cellule(lot.code, href="/django/stock_labo/nomenclature_lot_edit/%s" %(make_addr_param({"id_nomenclature":lot.nomenclature.id, "id_nomenclature_lot":lot.id})))
#				l.add_cellule(lot.description)
				l.add_cellule(lot.f_date_creation(NomenclatureLot._meta.fields[3].format_date_time))
				l.add_cellule(lot.f_date_fin_validite(NomenclatureLot._meta.fields[4].format_date_time))
				l.add_cellule("<center><img src=\"/static/svg/system-search.svg\" height=\"24\" alt=\"Etiquette\"/></center>", title="Rechercher contenant", href="/django/stock_labo/nomenclature/%s" %(make_addr_param(rech_def, {"contenant":"yes", "id_nomenclature":lot.nomenclature.id, "id_nomenclature_lot":lot.id})))
				if lot.definition == False:
					l.add_cellule(" ")
				else:
					l.add_cellule("<center><img src=\"/static/svg/system-search.svg\" height=\"24\" alt=\"Etiquette\"/></center>", title=NomenclatureLot._meta.fields[6].nom_long, href="/django/stock_labo/nomenclature/%s" %(make_addr_param(rech_def, {"definition":"yes", "id_nomenclature":lot.nomenclature.id, "id_nomenclature_lot":lot.id})))
#				l.add_cellule("<center><img src=\"/static/svg/document-print.svg\" height=\"24\" alt=\"Etiquette\"/></center>", title="Impression etiquette lot", href="/django/stock_labo/nomenclature_lot_etiquette_print/%s" %(make_addr_param({"id_nomenclature":lot.nomenclature.id, "id_nomenclature_lot":lot.id})))
				l.add_cellule("<center><img src=\"/static/svg/list-add.svg\" height=\"24\" alt=\"Ajouter\"/></center>", title="Nouveau contenant", href="/django/stock_labo/nomenclature_contenant_edit/%s" %(make_addr_param({"id_nomenclature":lot.nomenclature.id, "id_nomenclature_lot":lot.id})))
				list2.add_ligne(l.get_ligne())


		if request.GET.has_key("id_nomenclature_lot"):

			if request.GET.has_key("contenant"):

				nom_lot = NomenclatureLot.objects.get(pk=int(request.GET["id_nomenclature_lot"]))

				l = Liste.Ligne()
				l.add_cellule(nom_lot.code, href="/django/stock_labo/nomenclature_lot_edit/%s" %(make_addr_param({"id_nomenclature":nom_lot.nomenclature.id, "id_nomenclature_lot":nom_lot.id})))
#				l.add_cellule(nom_lot.description)
				l.add_cellule(nom_lot.f_date_creation(NomenclatureLot._meta.fields[3].format_date_time))
				l.add_cellule(nom_lot.f_date_fin_validite(NomenclatureLot._meta.fields[4].format_date_time))
				l.add_cellule("<center><img src=\"/static/svg/system-search.svg\" height=\"24\" alt=\"Etiquette\"/></center>", title="Rechercher contenant", href="/django/stock_labo/nomenclature/%s" %(make_addr_param(rech_def, {"contenant":"yes","id_nomenclature":nom_lot.nomenclature.id, "id_nomenclature_lot":nom_lot.id})))
				if nom_lot.definition == False:
					l.add_cellule(" ")
				else:
					l.add_cellule("<center><img src=\"/static/svg/system-search.svg\" height=\"24\" alt=\"Etiquette\"/></center>", title=NomenclatureLot._meta.fields[6].nom_long, href="/django/stock_labo/nomenclature/%s" %(make_addr_param(rech_def, {"definition":"yes","id_nomenclature":lot.nomenclature.id, "id_nomenclature_lot":lot.id})))
#				l.add_cellule("<center><img src=\"/static/svg/document-print.svg\" height=\"24\" alt=\"Etiquette\"/></center>", title="Impression etiquette contenant", href="/django/stock_labo/nomenclature_lot_etiquette_print/%s" %(make_addr_param({"id_nomenclature":nom_lot.nomenclature.id, "id_nomenclature_lot":nom_lot.id})))
				l.add_cellule("<center><img src=\"/static/svg/list-add.svg\" height=\"24\" alt=\"Ajouter\"/></center>", title="Nouveau contenant", href="/django/stock_labo/nomenclature_contenant_edit/%s" %(make_addr_param({"id_nomenclature":nom_lot.nomenclature.id, "id_nomenclature_lot":nom_lot.id})))
				list2.add_headers(l.get_ligne())

				if rech_def.has_key("sup") and rech_def["sup"] == "on":
					cont = Contenant.objects.filter(nomenclature_lot=int(request.GET["id_nomenclature_lot"])).filter(date_suppression__isnull=False)
				else:
					cont = Contenant.objects.filter(nomenclature_lot=int(request.GET["id_nomenclature_lot"])).filter(date_suppression__isnull=True)

				list3 = Liste(caption="Liste des contenants du lot %s de l'article [%s] %s" %(nom_lot.code, nom_lot.nomenclature.code, nom_lot.nomenclature.description), summary=Contenant.__doc__)
				l = Liste.Ligne()
				l.add_cellule(Contenant._meta.fields[1].nom_colonne, title=Contenant._meta.fields[1].nom_long, width="10%")				#code
				l.add_cellule(ContenantType._meta.fields[1].nom_colonne, title=ContenantType._meta.fields[1].nom_long, width="5%")		#type_contenant
#				l.add_cellule(StockSite._meta.fields[1].nom_colonne, title=StockSite._meta.fields[1].nom_long, width="8%")				#stock_site
				l.add_cellule(StockEntrepot._meta.fields[1].nom_colonne, title=StockEntrepot._meta.fields[1].nom_long)					#stock_entrepot
				l.add_cellule(StockMagasin._meta.fields[1].nom_colonne, title=StockMagasin._meta.fields[1].nom_long)					#stock_magasin
#				l.add_cellule(Contenant._meta.fields[11].nom_colonne, title=Contenant._meta.fields[11].nom_long)						#emplacement
#				l.add_cellule(Contenant._meta.fields[13].nom_colonne, title=Contenant._meta.fields[13].nom_long)						#poids
				l.add_cellule(Contenant._meta.fields[14].nom_colonne, title=Contenant._meta.fields[14].nom_long, width="12%")			#date_creation
				l.add_cellule(Contenant._meta.fields[15].nom_colonne, title=Contenant._meta.fields[15].nom_long, width="12%")			#date_reception
				l.add_cellule(Contenant._meta.fields[17].nom_colonne, title=Contenant._meta.fields[17].nom_long, width="12%")			#date_fin_validite
				l.add_cellule("<center>Imp. É</center>", title="Imprimer une nouvelle etiquette", width="50px")							#Etiquette
				if request.user.has_perm("stock_labo.panier"):
					l.add_cellule("<center>Panier</center>", title="Ajouter/Supprimer du panier", width="50px")								#Panier
				list3.add_headers(l.get_ligne())
				for c in cont:
					l = Liste.Ligne()
					l.add_cellule(c.code, href="/django/stock_labo/nomenclature_contenant_edit/%s" %(make_addr_param({"id_nomenclature":c.nomenclature_lot.nomenclature.id, "id_nomenclature_lot":c.nomenclature_lot.id,"id_contenant":c.id})))
					l.add_cellule(c.type_contenant.code, title=c.type_contenant.description)
#					l.add_cellule(c.actuel_site.code, title=c.actuel_site.description)
					l.add_cellule(c.actuel_entrepot.description, title=c.actuel_entrepot.code)
					l.add_cellule(c.actuel_magasin.description, title=c.actuel_magasin.code)
#					l.add_cellule(c.actuel_emplacement)
#					l.add_cellule(c.poids)
					l.add_cellule(c.f_date_creation(Contenant._meta.fields[14].format_date_time))
					l.add_cellule(c.f_date_reception(Contenant._meta.fields[15].format_date_time))
					l.add_cellule(c.f_date_fin_validite(Contenant._meta.fields[17].format_date_time))
					if c.date_suppression != None:
						l.add_cellule("<center><img src=\"/static/svg/process-stop.svg\" height=\"24\" /></center>", title=u"Le contenant est supprimé")
					else:
						l.add_cellule(
							"<center><img src=\"/static/svg/document-print.svg\" height=\"24\" alt=\"Etiquette\"/></center>",
							title="Impression etiquette contenant",
							href=None,
							cellule_id="etiquette_contenant_print_%d" %(c.id),
							onclick="etiquette(this, %d, 'contenant')"%(c.id),
							)
					if request.user.has_perm("stock_labo.panier"):
						if c.date_suppression != None:
							l.add_cellule("<center><img src=\"/static/svg/process-stop.svg\" height=\"24\" /></center>", title=u"Le contenant est supprimé")
						elif c.date_reception == None:
							l.add_cellule("<center><img src=\"/static/svg/process-stop.svg\" height=\"24\" /></center>", title=u"Le contenant n'est pas réceptionné")
						else:
							if c.panier_user == None:
								l.add_cellule("<center><img src=\"/static/svg/format-indent-more.svg\" height=\"24\" alt=\"Ajouter le contenant au panier\"/></center>", title="Ajouter le contenant au panier", href="/django/stock_labo/nomenclature_contenant_panier/%s" %(make_addr_param({"ajouter":"yes", "id_nomenclature":c.nomenclature_lot.nomenclature.id, "id_nomenclature_lot":c.nomenclature_lot.id,"id_contenant":c.id})))
							elif c.panier_user == request.user:
								l.add_cellule("<center><img src=\"/static/svg/format-indent-less.svg\" height=\"24\" alt=\"Supprimer le contenant du panier\"/></center>", title="Supprimer le contenant du panier", href="/django/stock_labo/nomenclature_contenant_panier/%s" %(make_addr_param({"supprimer":"yes", "id_nomenclature":c.nomenclature_lot.nomenclature.id, "id_nomenclature_lot":c.nomenclature_lot.id,"id_contenant":c.id})))
							else:
								l.add_cellule(get_user_param(c.panier_user).initial, title=u"Contenant utilisé par %s %s (%s)" %(c.panier_user.first_name, c.panier_user.last_name, c.panier_user.username))

					list3.add_ligne(l.get_ligne())


			if request.GET.has_key("definition"):

				nom_lot = NomenclatureLot.objects.get(pk=int(request.GET["id_nomenclature_lot"]))

				l = Liste.Ligne()
				l.add_cellule(nom_lot.code, href="/django/stock_labo/nomenclature_lot_edit/%s" %(make_addr_param({"id_nomenclature":nom_lot.nomenclature.id, "id_nomenclature_lot":nom_lot.id})))
				l.add_cellule(nom_lot.f_date_creation(NomenclatureLot._meta.fields[5].format_date_time))
				l.add_cellule("<center><img src=\"/static/svg/system-search.svg\" height=\"24\" alt=\"Etiquette\"/></center>", title="Rechercher contenant", href="/django/stock_labo/nomenclature/%s" %(make_addr_param(rech_def, {"contenant":"yes", "id_nomenclature":lot.nomenclature.id, "id_nomenclature_lot":lot.id})))
				if nom_lot.definition == False:
					l.add_cellule(" ")
				else:
					l.add_cellule("<center><img src=\"/static/svg/system-search.svg\" height=\"24\" alt=\"Etiquette\"/></center>", title=NomenclatureLot._meta.fields[6].nom_long, href="/django/stock_labo/nomenclature/%s" %(make_addr_param(rech_def, {"definition":"yes", "id_nomenclature":lot.nomenclature.id, "id_nomenclature_lot":lot.id})))
				l.add_cellule(
					"<center><img src=\"/static/svg/document-print.svg\" height=\"24\" alt=\"Etiquette\"/></center>",
					title="Impression etiquette contenant",
					href=None,
					cellule_id="etiquette_contenant_print_%d" %(c.id),
					onclick="etiquette(this, %d, 'contenant')"%(c.id),
					)
				l.add_cellule("<center><img src=\"/static/svg/list-add.svg\" height=\"24\" alt=\"Ajouter\"/></center>", title="Nouveau contenant", href="/django/stock_labo/nomenclature_contenant_edit/%s" %(make_addr_param({"id_nomenclature":nom_lot.nomenclature.id, "id_nomenclature_lot":nom_lot.id})))
				list2.add_headers(l.get_ligne())


				ing = NomenclatureLotIngredient.objects.filter(formule=int(request.GET["id_nomenclature_lot"]))

				list3 = Liste(caption="Liste de composition du lot %s de l'article [%s] %s" %(nom_lot.code, nom_lot.nomenclature.code, nom_lot.nomenclature.description), summary=NomenclatureLotIngredient.__doc__)
				l = Liste.Ligne()

				l.add_cellule("<center>S</center>", title="Sauter vers", width="50px")																			#jump
				l.add_cellule(Nomenclature._meta.fields[1].nom_colonne, title=Nomenclature._meta.fields[1].nom_long, width="10%")								#code ingrédient
				l.add_cellule(Nomenclature._meta.fields[2].nom_colonne, title=Nomenclature._meta.fields[2].nom_long)											#nom inqrédient
				l.add_cellule(NomenclatureLotIngredient._meta.fields[3].nom_colonne, title=NomenclatureLotIngredient._meta.fields[3].nom_long, width="10%")		#a doser
				l.add_cellule(NomenclatureLotIngredient._meta.fields[4].nom_colonne, title=NomenclatureLotIngredient._meta.fields[4].nom_long, width="10%")		#dosé
				l.add_cellule(NomenclatureLotIngredient._meta.fields[5].nom_colonne, title=NomenclatureLotIngredient._meta.fields[5].nom_long, width="8%")		#tol+
				l.add_cellule(NomenclatureLotIngredient._meta.fields[6].nom_colonne, title=NomenclatureLotIngredient._meta.fields[6].nom_long, width="8%")		#tol-
				l.add_cellule(NomenclatureLotIngredient._meta.fields[7].nom_colonne, title=NomenclatureLotIngredient._meta.fields[7].nom_long, width="10%")		#validité
				l.add_cellule("<center>Dosages</center>", title="Rechercher des dosages éffectués", width="50px")												#Rechercher
				list3.add_headers(l.get_ligne())
				for i in ing:
					l = Liste.Ligne()
					l.add_cellule("<center><img src=\"/static/svg/edit-redo.svg\" height=\"24\" alt=\"Etiquette\"/></center>", title="Aller dans l'ingrédient", href="/django/stock_labo/nomenclature/%s" %(make_addr_param(rech_def, {"id_nomenclature":i.ingredient.id})))
					l.add_cellule(i.ingredient.code, title="Editer fiche", href="/django/stock_labo/nomenclature_edit/%s" %(make_addr_param({"id_nomenclature":i.ingredient.id})))
					l.add_cellule(i.ingredient.description)
					l.add_cellule(i.get_poids_unit(unit=user_param.unit_masse)["poids_unit"])
					l.add_cellule(i.get_doser_unit(unit=user_param.unit_masse)["poids_unit"])
					l.add_cellule(i.get_tol_pos_unit(unit=user_param.unit_masse)["poids_unit"])
					l.add_cellule(i.get_tol_neg_unit(unit=user_param.unit_masse)["poids_unit"])
					l.add_cellule(i.DOSAGE_VALIDITE[i.valide])
					if i.definition == False:
						l.add_cellule(" ")
					else:
						l.add_cellule("<center><img src=\"/static/svg/system-search.svg\" height=\"24\" alt=\"Etiquette\"/></center>", title=NomenclatureLot._meta.fields[6].nom_long, href="/django/stock_labo/nomenclature/%s" %(make_addr_param(rech_def, {"definition":"yes", "id_nomenclature":i.formule.nomenclature.id, "id_nomenclature_lot":i.formule.id, "id_nomenclature_lot_ingredient":i.id})))

					list3.add_ligne(l.get_ligne())


				if request.GET.has_key("id_nomenclature_lot_ingredient"):

					nom_lot_ing = NomenclatureLotIngredient.objects.get(pk=int(request.GET["id_nomenclature_lot_ingredient"]))
					l = Liste.Ligne()
					l.add_cellule("<center><img src=\"/static/svg/edit-redo.svg\" height=\"24\" alt=\"Etiquette\"/></center>", title="Aller dans l'ingrédient", href="/django/stock_labo/nomenclature/%s" %(make_addr_param(rech_def, {"id_nomenclature":nom_lot_ing.ingredient.id})))
					l.add_cellule(nom_lot_ing.ingredient.code, title="Editer fiche", href="/django/stock_labo/nomenclature_edit/%s" %(make_addr_param({"id_nomenclature":nom_lot_ing.ingredient.id})))
					l.add_cellule(nom_lot_ing.ingredient.description)
					l.add_cellule(nom_lot_ing.get_poids_unit(unit=user_param.unit_masse)["poids_unit"])
					l.add_cellule(nom_lot_ing.get_doser_unit(unit=user_param.unit_masse)["poids_unit"])
					l.add_cellule(nom_lot_ing.get_tol_pos_unit(unit=user_param.unit_masse)["poids_unit"])
					l.add_cellule(nom_lot_ing.get_tol_neg_unit(unit=user_param.unit_masse)["poids_unit"])
					l.add_cellule(nom_lot_ing.DOSAGE_VALIDITE[nom_lot_ing.valide])
					if nom_lot_ing.definition == False:
						l.add_cellule(" ")
					else:
						l.add_cellule("<center><img src=\"/static/svg/system-search.svg\" height=\"24\" alt=\"Etiquette\"/></center>", title="Listes des dosages", href="/django/stock_labo/nomenclature/%s" %(make_addr_param(rech_def, {"definition":"yes", "id_nomenclature":nom_lot_ing.formule.nomenclature.id, "id_nomenclature_lot":nom_lot_ing.formule.id, "id_nomenclature_lot_ingredient":nom_lot_ing.id})))

					list3.add_headers(l.get_ligne())

					dosage = NomenclatureLotIngredientDosage.objects.filter(nomenclature_lot_ingredient=int(request.GET["id_nomenclature_lot_ingredient"]))

					list4 = Liste(caption="Liste des dosages de l'article [%s] %s" %(nom_lot_ing.ingredient.code, nom_lot_ing.ingredient.description), summary=NomenclatureLotIngredientDosage.__doc__)
					l = Liste.Ligne()
					l.add_cellule(NomenclatureLotIngredientDosage._meta.fields[2].nom_colonne, title=NomenclatureLotIngredientDosage._meta.fields[2].nom_long, width="8%")		#dosé
					l.add_cellule(NomenclatureLotIngredientDosage._meta.fields[3].nom_colonne, title=NomenclatureLotIngredientDosage._meta.fields[3].nom_long, width="12%")		#contenant
					l.add_cellule(NomenclatureLotIngredientDosage._meta.fields[4].nom_colonne, title=NomenclatureLotIngredientDosage._meta.fields[4].nom_long, width="12%")		#lot
					l.add_cellule(NomenclatureLotIngredientDosage._meta.fields[5].nom_colonne, title=NomenclatureLotIngredientDosage._meta.fields[5].nom_long, width="12%")		#PID
					l.add_cellule("PID", title="Login opérateur", width="8%")																									#login
					l.add_cellule(NomenclatureLotIngredientDosage._meta.fields[7].nom_colonne, title=NomenclatureLotIngredientDosage._meta.fields[7].nom_long, width="20%")		#date dosage
					list4.add_headers(l.get_ligne())
					for i in dosage:
						l = Liste.Ligne()
						l.add_cellule(i.get_doser_unit(unit=user_param.unit_masse)["poids_unit"])
						l.add_cellule(i.contenant_code)
						l.add_cellule(i.lot)
						l.add_cellule(i.responsable_login)
						if i.responsable == False:
							l.add_cellule("?")
						else:
							l.add_cellule(i.responsable)
						l.add_cellule(i.date_dosage)

						list4.add_ligne(l.get_ligne())

	if list4 != None:
		return render(request, "stock_labo_nomenclature_liste_quadruple.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "recherche": recherche, "list1" : list1.get_liste(), "list2" : list2.get_liste(), "list3" : list3.get_liste(), "list4" : list4.get_liste(), "bouton" : bouton.get_boutons()})
	elif list3 != None:
		return render(request, "stock_labo_nomenclature_liste_triple.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "recherche": recherche, "list1" : list1.get_liste(), "list2" : list2.get_liste(), "list3" : list3.get_liste(), "bouton" : bouton.get_boutons()})
	elif list2 != None:
		return render(request, "stock_labo_nomenclature_liste_double.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "recherche": recherche, "list1" : list1.get_liste(), "list2" : list2.get_liste(), "bouton" : bouton.get_boutons()})
	else:
		return render(request, "stock_labo_nomenclature_liste.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "recherche": recherche, "list" : list1.get_liste(), "bouton" : bouton.get_boutons()})

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def nomenclature_edit(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Article", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Article", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Article", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))

	onglet = Onglets(request.user)
	onglet.set_actif_by_id(0)

	defaut = {}
	info = {}

	if len(request.GET) > 0 and request.GET.has_key("id_nomenclature"):
		if request.GET.has_key("annuler"):
			return HttpResponseRedirect("/django/stock_labo/nomenclature/")
		elif request.GET.has_key("dupliquer") or request.GET["id_nomenclature"] == "":
			form = NomenclatureForm(request.GET)
			if form.is_valid() and request.GET["code"].find(" ") == -1:
				n = form.save(commit=True)
#				n.date_creation = datetime.date.today()
				n.save()
				log = django_models.LogEntry()
				log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
				log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
				log.content_type = ContentType.objects.get(app_label="stock_labo", model="Nomenclature".lower())	#Le type de contenu (ContentType) de l’objet modifié.
				log.object_id = n.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
				log.object_repr = unicode(n)																		#La représentation repr() de l’objet après sa modification.
				log.action_flag = django_models.ADDITION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
				log.change_message = "nomenclature_edit"															#Description de la modification
				log.save()
				return HttpResponseRedirect("/django/stock_labo/nomenclature/")
			else:
				if request.GET["code"].find(" ") != -1:
					info.update({"erreur": "Le code article ne doit pas contenir d'espace"})
				print_etiquette = "/#/"
				return render(request, "stock_labo_nomenclature_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "modif" : form.data["id_nomenclature"], "info" : info, "print_etiquette" : print_etiquette, "print_id" : 0 })
		elif request.GET.has_key("valider") and request.GET["id_nomenclature"] != "":
			ing = Nomenclature.objects.get(pk=int(request.GET["id_nomenclature"]))
			form = NomenclatureForm(request.GET, instance=ing)
			if form.is_valid() and request.GET["code"].find(" ") == -1:
				i = form.save(commit=True)
				log = django_models.LogEntry()
				log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
				log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
				log.content_type = ContentType.objects.get(app_label="stock_labo", model="Nomenclature".lower())	#Le type de contenu (ContentType) de l’objet modifié.
				log.object_id = i.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
				log.object_repr = unicode(i)																		#La représentation repr() de l’objet après sa modification.
				log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
				log.change_message = "nomenclature_edit"															#Description de la modification
				log.save()

				return HttpResponseRedirect("/django/stock_labo/nomenclature/%s" %(make_addr_param({"id_nomenclature":request.GET["id_nomenclature"]})))
			else:
				if request.GET["code"].find(" ") != -1:
					info.update({"erreur": "Le code article ne doit pas contenir d'espace"})
				print_etiquette = "/django/stock_labo/nomenclature_etiquette_print/%s" %(make_addr_param({"id_nomenclature":defaut["id_nomenclature"]}))
				return render(request, "stock_labo_nomenclature_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "modif" : form.data["id_nomenclature"], "info" : info, "print_etiquette" : print_etiquette, "print_id" : request.GET["id_nomenclature"] })
		elif request.GET.has_key("supprimer"):
			ing = Nomenclature.objects.get(pk=int(request.GET["id_nomenclature"]))
			log = django_models.LogEntry()
			log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
			log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
			log.content_type = ContentType.objects.get(app_label="stock_labo", model="Nomenclature".lower())	#Le type de contenu (ContentType) de l’objet modifié.
			log.object_id = ing.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
			log.object_repr = unicode(ing)																		#La représentation repr() de l’objet après sa modification.
			log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
			log.change_message = "nomenclature_edit : suppression"												#Description de la modification
			log.save()
			ing.suppression(request.user)
			return HttpResponseRedirect("/django/stock_labo/nomenclature/")
		else:
			ing = Nomenclature.objects.get(pk=int(request.GET["id_nomenclature"]))
			defaut.update({"id_nomenclature" : request.GET["id_nomenclature"]})
			form = NomenclatureForm(instance=ing, initial=defaut)
			print_etiquette = "/django/stock_labo/nomenclature_etiquette_print/%s" %(make_addr_param({"id_nomenclature":defaut["id_nomenclature"]}))
			return render(request, "stock_labo_nomenclature_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "modif" : ing.id, "print_etiquette" : print_etiquette, "print_id" : request.GET["id_nomenclature"] })


	defaut.update({"reception_site" : user_param.site_perso.id})
	defaut.update({"reception_entrepot" : user_param.entrepot_perso.id})
	defaut.update({"reception_magasin" : user_param.magasin_perso.id})
	defaut.update({"reception_emplacement" : user_param.emplacement_perso})
	form = NomenclatureForm(initial=defaut)
	if defaut.has_key("id_nomenclature"):
		print_etiquette = "/django/stock_labo/nomenclature_etiquette_print/%s" %(make_addr_param({"id_nomenclature":defaut["id_nomenclature"]}))
		return render(request, "stock_labo_nomenclature_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "print_etiquette" : print_etiquette, "print_id" : request.GET["id_nomenclature"] })
	else:
		print_etiquette = "/#/"
		return render(request, "stock_labo_nomenclature_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "print_etiquette" : print_etiquette, "print_id" : 0 })

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def nomenclature_edit2(request):
	"""
	Nouveau Concentré
	"""
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Article", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Article", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Article", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))

	emp = [(p.id, p.nom_court()) for p in SiteEntrepotMagasin.objects.all()]
	emp.insert(0, (99, "Empl. perso : %s" %(user_param.magasin_perso.description)))

	onglet = Onglets(request.user)
	onglet.set_actif_by_id(0)
	step = 0
	defaut = {}
	nomenclature = None
	nomenclature_lot = None
	info = {}

	def set_read_only(f, d):
		for k in ("nomenclature_type", "nomenclature_code", "nomenclature_description", "nomenclature_commentaire", "nomenclature_lot_poids_reference", "nomenclature_lot_commentaire", "nomenclature_lot_projet", "nomenclature_lot_client", "nomenclature_lot_client_ka"):
			if d.has_key(k) and d[k] != None and d[k] != "":
					f.fields[k].widget.attrs["readonly"] = True
		return f

	if len(request.GET) > 0:
		if request.GET.has_key("annuler"):
			return HttpResponseRedirect("/django/stock_labo/nomenclature/")
		if request.GET.has_key("recherche") and request.GET.has_key("nomenclature_code"):
			nomenclature = Nomenclature.objects.filter(code=request.GET["nomenclature_code"])
			defaut.update({"contenant_provenance_site":user_param.site_perso.id})
			site_entrepot_magasin = SiteEntrepotMagasin.objects.filter(site=user_param.site_perso.id, entrepot=user_param.entrepot_perso.id, magasin=user_param.magasin_perso.id)
			if len(site_entrepot_magasin) == 1:
				defaut.update({"nomenclature_site_entrepot_magasin":site_entrepot_magasin[0].id})
			if len(nomenclature) == 1:
				defaut.update({"nomenclature_type":nomenclature[0].nomenclature_type.id})
				defaut.update({"nomenclature_code":nomenclature[0].code})
				defaut.update({"nomenclature_description":nomenclature[0].description})
				defaut.update({"nomenclature_commentaire":nomenclature[0].commentaire})
				defaut.update({"nomenclature_duree_validite":nomenclature[0].duree_validite})
				nomenclature_lot = nomenclature[0].get_nomenclature_lot()
				nomenclature_lot.len = len(nomenclature_lot) + 1
				if len(nomenclature_lot) > 0:
					step = 1
				else:
					defaut.update({"nomenclature_lot_code":datetime.datetime.now().strftime("%Y%m%d%H%M%S")})
					defaut.update({"contenant_date_creation":datetime.datetime.now().strftime("%d/%m/%Y")})
					step = 2
			else:
				step = 3
				defaut.update({"nomenclature_code":request.GET["nomenclature_code"]})
				defaut.update({"contenant_date_creation":datetime.datetime.now().strftime("%d/%m/%Y")})
				defaut.update({"nomenclature_lot_code":datetime.datetime.now().strftime("%Y%m%d%H%M%S")})
				if request.GET.has_key("nomenclature_duree_validite") and request.GET["nomenclature_duree_validite"] != "":
					defaut.update({"nomenclature_duree_validite":request.GET["nomenclature_duree_validite"]})
				else:
					defaut.update({"nomenclature_duree_validite":settings_default.DUREE_VALIDITE_COUP})

			form = NomenclatureForm2(initial=defaut)
			form = set_read_only(form, defaut)
			form.fields["nomenclature_site_entrepot_magasin"].choices = emp
			form.fields["nomenclature_site_entrepot_magasin"].initial = 99
			if step == 1:
				form.fields["nomenclature_lot_poids_reference"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_type"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_description"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_commentaire"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_site_entrepot_magasin"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_duree_validite"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_lot_code"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_lot_commentaire"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_lot_projet"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_lot_client"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_lot_client_ka"].widget = django_forms.HiddenInput()
				form.fields["contenant_date_creation"].widget = django_forms.HiddenInput()
				form.fields["contenant_provenance_site"].widget = django_forms.HiddenInput()
				form.fields["contenant_type1"].widget = django_forms.HiddenInput()
				form.fields["contenant_nombre1"].widget = django_forms.HiddenInput()
				form.fields["contenant_type2"].widget = django_forms.HiddenInput()
				form.fields["contenant_nombre2"].widget = django_forms.HiddenInput()
				form.fields["contenant_type3"].widget = django_forms.HiddenInput()
				form.fields["contenant_nombre3"].widget = django_forms.HiddenInput()
				return render(request, "stock_labo_nomenclature_edit2.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "step": step, "nomenclature_lot" : nomenclature_lot})
			if step == 2:
				return render(request, "stock_labo_nomenclature_edit2.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "step": step})
			if step == 3:
				return render(request, "stock_labo_nomenclature_edit2.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "step": step})
		elif request.GET.has_key("nouveau") and request.GET.has_key("nomenclature_code"):
			nomenclature = Nomenclature.objects.filter(code=request.GET["nomenclature_code"])
			defaut.update({"contenant_provenance_site":user_param.site_perso.id})
			site_entrepot_magasin = SiteEntrepotMagasin.objects.filter(site=user_param.site_perso.id, entrepot=user_param.entrepot_perso.id, magasin=user_param.magasin_perso.id)
			if len(site_entrepot_magasin) == 1:
				defaut.update({"nomenclature_site_entrepot_magasin":site_entrepot_magasin[0].id})
			if len(nomenclature) == 1:
				defaut.update({"nomenclature_type":nomenclature[0].nomenclature_type.id})
				defaut.update({"nomenclature_code":nomenclature[0].code})
				defaut.update({"nomenclature_description":nomenclature[0].description})
				defaut.update({"nomenclature_commentaire":nomenclature[0].commentaire})
				defaut.update({"nomenclature_duree_validite":nomenclature[0].duree_validite})
				defaut.update({"nomenclature_lot_code":datetime.datetime.now().strftime("%Y%m%d%H%M%S")})
				defaut.update({"contenant_date_creation":datetime.datetime.now().strftime("%d/%m/%Y")})

			step = 2
			form = NomenclatureForm2(initial=defaut)
			form = set_read_only(form, defaut)
			form.fields["nomenclature_site_entrepot_magasin"].choices = emp
			form.fields["nomenclature_site_entrepot_magasin"].initial = 99
			return render(request, "stock_labo_nomenclature_edit2.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "step": step})
		elif request.GET.has_key("lot") and request.GET.has_key("nomenclature_code"):
			nomenclature = Nomenclature.objects.filter(code=request.GET["nomenclature_code"])
			defaut.update({"contenant_provenance_site":user_param.site_perso.id})
			site_entrepot_magasin = SiteEntrepotMagasin.objects.filter(site=user_param.site_perso.id, entrepot=user_param.entrepot_perso.id, magasin=user_param.magasin_perso.id)
			if len(site_entrepot_magasin) == 1:
				defaut.update({"nomenclature_site_entrepot_magasin":site_entrepot_magasin[0].id})
			if len(nomenclature) == 1:
				defaut.update({"nomenclature_type":nomenclature[0].nomenclature_type.id})
				defaut.update({"nomenclature_code":nomenclature[0].code})
				defaut.update({"nomenclature_description":nomenclature[0].description})
				defaut.update({"nomenclature_commentaire":nomenclature[0].commentaire})
				defaut.update({"nomenclature_duree_validite":nomenclature[0].duree_validite})
				defaut.update({"contenant_date_creation":datetime.datetime.now().strftime("%d/%m/%Y")})
				nomenclature_lot = nomenclature[0].get_nomenclature_lot()
				lot = nomenclature_lot.filter(code=request.GET["lot"])
				defaut.update({"nomenclature_lot_code": lot[0].code})
				defaut.update({"nomenclature_lot_commentaire": lot[0].commentaire})
				defaut.update({"nomenclature_lot_projet": lot[0].projet})
				defaut.update({"nomenclature_lot_client": lot[0].client})
				defaut.update({"nomenclature_lot_client_ka": lot[0].client_ka})

			step = 2
			form = NomenclatureForm2(initial=defaut)
			form = set_read_only(form, defaut)
			form.fields["nomenclature_site_entrepot_magasin"].choices = emp
			form.fields["nomenclature_site_entrepot_magasin"].initial = 99
			return render(request, "stock_labo_nomenclature_edit2.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "step": step})
		elif request.GET.has_key("valider"):
			step = 3
			if request.GET["nomenclature_code"].find(" ") != -1:
				info.update({"erreur": "Le code article ne doit pas contenir d'espace"})
				form = NomenclatureForm2(initial=request.GET)
				form = set_read_only(form, request.GET)
				form.fields["nomenclature_site_entrepot_magasin"].choices = emp
				form.fields["nomenclature_site_entrepot_magasin"].initial = 99
				return render(request, "stock_labo_nomenclature_edit2.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "step": step, "info" : info})

			n_type = NomenclatureType.objects.get(pk=int(request.GET["nomenclature_type"]))
			log = django_models.LogEntry()
			try:
				nomenclature = n_type.add_nomenclature(code=request.GET["nomenclature_code"], update=False)
				if request.GET["contenant_date_creation"] != "":
					nomenclature.date_creation = datetime.datetime.strptime(request.GET["contenant_date_creation"], "%d/%m/%Y")
				if request.GET["nomenclature_duree_validite"] != "":
					nomenclature.duree_validite = int(request.GET["nomenclature_duree_validite"])
				log.change_message = "nomenclature_edit2"															#Description de la modification
				log.action_flag = django_models.ADDITION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
			except NomenclatureExistant as i:
				nomenclature = i.args[0]
				if nomenclature.date_suppression == None:
					log.change_message = "nomenclature_edit2"															#Description de la modification
				else:
					nomenclature.date_suppression = None
					log.change_message = "nomenclature_edit2 (réssuscite)"															#Description de la modification
				log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
			finally:
				if request.GET["nomenclature_description"] != "":
					if nomenclature.description == None or nomenclature.description == "":
						nomenclature.description = request.GET["nomenclature_description"]
				if request.GET["nomenclature_commentaire"] != "":
					if nomenclature.commentaire == None or nomenclature.commentaire == "":
						nomenclature.commentaire = request.GET["nomenclature_commentaire"]
				if int(request.GET["nomenclature_site_entrepot_magasin"]) == 99:
					if nomenclature.reception_site.id == 1:
						nomenclature.reception_site = user_param.site_perso
					if nomenclature.reception_entrepot.id == 1:
						nomenclature.reception_entrepot = user_param.entrepot_perso
					if nomenclature.reception_magasin.id == 1:
						nomenclature.reception_magasin = user_param.magasin_perso
				else:
					site_entrepot_magasin = SiteEntrepotMagasin.objects.filter(pk=int(request.GET["nomenclature_site_entrepot_magasin"]))
					if len(site_entrepot_magasin) == 1:
						if nomenclature.reception_site.id == 1:
							nomenclature.reception_site = site_entrepot_magasin[0].site
						if nomenclature.reception_entrepot.id == 1:
							nomenclature.reception_entrepot = site_entrepot_magasin[0].entrepot
						if nomenclature.reception_magasin.id == 1:
							nomenclature.reception_magasin = site_entrepot_magasin[0].magasin
				nomenclature.save()
				log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
				log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
				log.content_type = ContentType.objects.get(app_label="stock_labo", model="Nomenclature".lower())	#Le type de contenu (ContentType) de l’objet modifié.
				log.object_id = nomenclature.id																		#La représentation textuelle de la clé primaire de l’objet modifié.
				log.object_repr = unicode(nomenclature)																#La représentation repr() de l’objet après sa modification.
				log.save()


			log = django_models.LogEntry()
			try:
				lot = nomenclature.add_lot(code=request.GET["nomenclature_lot_code"], responsable_creation=request.user, update=False)
			except NomenclatureLotExistant as i:
				lot = i.args[0]
				if lot.date_suppression == None:
					log.change_message = "nomenclature_edit2"															#Description de la modification
				else:
					lot.date_suppression = None
					log.change_message = "nomenclature_edit2 (réssuscite)"															#Description de la modification
				log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
				lot.commentaire = request.GET["nomenclature_lot_commentaire"]
				lot.save()
			else:
				if request.GET["contenant_date_creation"] != "":
					lot.date_creation = datetime.datetime.strptime(request.GET["contenant_date_creation"],"%d/%m/%Y")
					if request.GET["nomenclature_duree_validite"] != "":
						lot.date_fin_validite = lot.fin_validite(duree=int(request.GET["nomenclature_duree_validite"]))
					else:
						lot.date_fin_validite = lot.fin_validite()
				lot.commentaire = request.GET["nomenclature_lot_commentaire"]
				if request.GET["nomenclature_lot_projet"] != None:
					lot.projet = request.GET["nomenclature_lot_projet"]
					lot.client = lot.get_client()
					lot.client_ka = lot.get_client_ka()
				try:
					lot.poids_reference = float(request.GET["nomenclature_lot_poids_reference"].replace(",","."))
				except ValueError:
					pass
				lot.save()
				lot.nomenclature_lot_stat()
				log.action_flag = django_models.ADDITION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
				log.change_message = "nomenclature_edit2"															#Description de la modification
			finally:
				log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
				log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
				log.content_type = ContentType.objects.get(app_label="stock_labo", model="NomenclatureLot".lower())	#Le type de contenu (ContentType) de l’objet modifié.
				log.object_id = lot.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
				log.object_repr = unicode(lot)																		#La représentation repr() de l’objet après sa modification.
				log.save()

			def creation_contenant(nombre, c_type):
				c = 0
				while c < nombre:
					cont = lot.add_contenant(responsable_creation=request.user, type_contenant=ContenantType(pk=c_type))
					cont.provenance_site = StockSite.objects.get(pk=int(request.GET["contenant_provenance_site"]))
					if request.GET["contenant_date_creation"] != "":
						cont.date_reception = datetime.datetime.strptime(request.GET["contenant_date_creation"],"%d/%m/%Y")
						cont.date_creation = datetime.datetime.strptime(request.GET["contenant_date_creation"],"%d/%m/%Y")
					else:
						cont.date_reception = datetime.date.today()
						cont.date_creation = datetime.date.today()
					if request.GET["nomenclature_duree_validite"] != "":
						cont.date_fin_validite = cont.fin_validite(int(request.GET["nomenclature_duree_validite"]))
					else:
						cont.date_fin_validite = cont.fin_validite()
					if int(request.GET["nomenclature_site_entrepot_magasin"]) == 99:
						cont.actuel_site = user_param.site_perso
						cont.actuel_entrepot = user_param.entrepot_perso
						cont.actuel_magasin = user_param.magasin_perso
						cont.stock_site = user_param.site_perso
						cont.stock_entrepot = user_param.entrepot_perso
						cont.stock_magasin = user_param.magasin_perso
					else:
						site_entrepot_magasin = SiteEntrepotMagasin.objects.filter(pk=int(request.GET["nomenclature_site_entrepot_magasin"]))
						if len(site_entrepot_magasin) == 1:
							cont.actuel_site = site_entrepot_magasin[0].site
							cont.actuel_entrepot = site_entrepot_magasin[0].entrepot
							cont.actuel_magasin = site_entrepot_magasin[0].magasin
							cont.stock_site = site_entrepot_magasin[0].site
							cont.stock_entrepot = site_entrepot_magasin[0].entrepot
							cont.stock_magasin = site_entrepot_magasin[0].magasin
					cont.save()
					log = django_models.LogEntry()
					log.action_time = datetime.datetime.now()														#La date et l’heure de l’action.
					log.user = request.user																			#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
					log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())	#Le type de contenu (ContentType) de l’objet modifié.
					log.object_id = cont.id																			#La représentation textuelle de la clé primaire de l’objet modifié.
					log.object_repr = unicode(cont)																	#La représentation repr() de l’objet après sa modification.
					log.action_flag = django_models.ADDITION 														#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
					log.change_message = "nomenclature_edit2"														#Description de la modification
					log.save()
					printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_contenant_imprimante.id)
					imp = Impression.objects.get(pk=user_param.etiquette_contenant.id)
					imp_d = ImpressionDetail.objects.filter(impression=imp)

					etiquette_print(printer, imp=imp, imp_d=imp_d, **{"user_param":user_param, "obj":cont})

					cont.contenant_stat()

					c += 1

			try:
				c_nbr = int(request.GET["contenant_nombre1"])
				c_type = int(request.GET["contenant_type1"])
			except ValueError:
				pass
			else:
				creation_contenant(c_nbr, c_type)

			try:
				c_nbr = int(request.GET["contenant_nombre2"])
				c_type = int(request.GET["contenant_type2"])
			except ValueError:
				pass
			else:
				creation_contenant(c_nbr, c_type)

			try:
				c_nbr = int(request.GET["contenant_nombre3"])
				c_type = int(request.GET["contenant_type3"])
			except ValueError:
				pass
			else:
				creation_contenant(c_nbr, c_type)



			return HttpResponseRedirect("/django/stock_labo/nomenclature/%s" %(make_addr_param({"id_nomenclature":nomenclature.id, "id_nomenclature_lot":lot.id,"contenant" : "yes"})))

	form = NomenclatureForm2()
	form.fields["nomenclature_site_entrepot_magasin"].choices = emp
	form.fields["nomenclature_site_entrepot_magasin"].initial = 99

	form.fields["nomenclature_lot_poids_reference"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_type"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_description"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_commentaire"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_site_entrepot_magasin"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_duree_validite"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_lot_code"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_lot_commentaire"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_lot_projet"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_lot_client"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_lot_client_ka"].widget = django_forms.HiddenInput()
	form.fields["contenant_date_creation"].widget = django_forms.HiddenInput()
	form.fields["contenant_provenance_site"].widget = django_forms.HiddenInput()
	form.fields["contenant_type1"].widget = django_forms.HiddenInput()
	form.fields["contenant_nombre1"].widget = django_forms.HiddenInput()
	form.fields["contenant_type2"].widget = django_forms.HiddenInput()
	form.fields["contenant_nombre2"].widget = django_forms.HiddenInput()
	form.fields["contenant_type3"].widget = django_forms.HiddenInput()
	form.fields["contenant_nombre3"].widget = django_forms.HiddenInput()
	return render(request, "stock_labo_nomenclature_edit2.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "step": step})

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def nomenclature_edit3(request):
	"""
	Nouvelle série/coupage
	"""
	user_param = UserPreference.objects.get(user=request.user)
	if request.GET.has_key("nomenclature_code"):
		if str(request.user.username) == "":
			header = Headers(page="Série/Coupage", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
		elif request.user.first_name == "" and request.user.last_name == "":
			header = Headers(page="Série/Coupage", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
		else:
			header = Headers(page="Série/Coupage", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		if str(request.user.username) == "":
			header = Headers(page="Série/Coupage", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
		elif request.user.first_name == "" and request.user.last_name == "":
			header = Headers(page="Série/Coupage", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
		else:
			header = Headers(page="Série/Coupage", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))

	onglet = Onglets(request.user)
	onglet.set_actif_by_id(0)
	defaut = {}
	nomenclature = None
	nomenclature_lot = None
	info = {}

	if len(request.GET) > 0:
		try:
			defaut.update({"nomenclature_type": int(request.GET["nomenclature_type"])})
		except ValueError:
			defaut.update({"nomenclature_type": None})
		defaut.update({"nomenclature_code": request.GET["nomenclature_code"]})
		defaut.update({"nomenclature_description": request.GET["nomenclature_description"]})
		defaut.update({"nomenclature_commentaire": request.GET["nomenclature_commentaire"]})
		try:
			defaut.update({"nomenclature_duree_validite": int(request.GET["nomenclature_duree_validite"])})
		except ValueError:
			defaut.update({"nomenclature_duree_validite": None})
		try:
			defaut.update({"nomenclature_lot_poids_reference": float(request.GET["nomenclature_lot_poids_reference"].replace(",","."))})
		except ValueError:
			defaut.update({"nomenclature_lot_poids_reference": None})
		defaut.update({"nomenclature_lot_code": request.GET["nomenclature_lot_code"]})
		defaut.update({"nomenclature_lot_commentaire": request.GET["nomenclature_lot_commentaire"]})
		defaut.update({"nomenclature_lot_projet": request.GET["nomenclature_lot_projet"]})
		defaut.update({"nomenclature_lot_client": request.GET["nomenclature_lot_client"]})
		defaut.update({"nomenclature_lot_client_ka": request.GET["nomenclature_lot_client_ka"]})
		try:
			defaut.update({"nomenclature_lot_roxane_manuel": int(request.GET["nomenclature_lot_roxane_manuel"])})
		except ValueError:
			defaut.update({"nomenclature_lot_roxane_manuel": None})
		try:
			defaut.update({"nomenclature_site_entrepot_magasin": int(request.GET["nomenclature_site_entrepot_magasin"])})
		except ValueError:
			defaut.update({"nomenclature_site_entrepot_magasin": None})
		if request.GET["contenant_date_creation"] != "":
#			try:
			defaut.update({"contenant_date_creation": datetime.datetime.strptime(request.GET["contenant_date_creation"],"%d/%m/%Y")})
#			except ValueError:
#				defaut.update({"contenant_date_creation": datetime.date.today()})
		else:
			defaut.update({"contenant_date_creation": datetime.date.today()})
		try:
			defaut.update({"contenant_provenance_site": int(request.GET["contenant_provenance_site"])})
		except ValueError:
			defaut.update({"contenant_provenance_site": None})
		try:
			defaut.update({"contenant_type1": int(request.GET["contenant_type1"])})
		except ValueError:
			defaut.update({"contenant_type1": None})
		try:
			defaut.update({"contenant_nombre1": int(request.GET["contenant_nombre1"])})
		except ValueError:
			defaut.update({"contenant_nombre1": 0})
		try:
			defaut.update({"contenant_type2": int(request.GET["contenant_type2"])})
		except ValueError:
			defaut.update({"contenant_type2": None})
		try:
			defaut.update({"contenant_nombre2": int(request.GET["contenant_nombre2"])})
		except ValueError:
			defaut.update({"contenant_nombre2": 0})
		if request.GET.has_key("annuler"):
			return HttpResponseRedirect("/django/stock_labo/nomenclature/")
		elif request.GET.has_key("print"):
			if request.GET["nomenclature_code"].find(" ") == -1:
				def print_etiquette(nombre, c_type):
					c = 0
					while c < nombre:
						n_type = NomenclatureType.objects.get(
							pk = defaut["nomenclature_type"],
							)

						n = Nomenclature(
							code = defaut["nomenclature_code"],
							description = defaut["nomenclature_description"],
							commentaire = defaut["nomenclature_commentaire"],
							nomenclature_type = n_type,
							reception_site = user_param.site_perso,
							reception_entrepot = user_param.entrepot_perso,
							reception_magasin = user_param.magasin_perso,
							reception_emplacement = user_param.emplacement_perso,
							date_creation = defaut["contenant_date_creation"],
							date_suppression = None,
							duree_validite = defaut["nomenclature_duree_validite"],
							)

						n_lot = NomenclatureLot(
							code = defaut["nomenclature_lot_code"],
							nomenclature = n,
							date_creation = defaut["contenant_date_creation"],
							date_suppression = None,
							definition = False,
							commentaire = defaut["nomenclature_lot_commentaire"],
							projet = defaut["nomenclature_lot_projet"],
							poids_reference = defaut["nomenclature_lot_poids_reference"],
							nbr_ligne_manuel = defaut["nomenclature_lot_roxane_manuel"],
							responsable_creation = request.user,
							)
						n_lot.date_fin_validite = n_lot.fin_validite(),
						n_lot.client = n_lot.get_client(),
						n_lot.client_ka = n_lot.get_client_ka(),

						cont_type = ContenantType.objects.get(
							pk = c_type,
							)

						site_p = StockSite.objects.get(
							pk = defaut["contenant_provenance_site"],
							)

						cont = Contenant(
							code = "NO-REF",
							nomenclature_lot = n_lot,
							type_contenant = cont_type,
							actuel_site = user_param.site_perso,
							actuel_entrepot = user_param.entrepot_perso,
							actuel_magasin = user_param.magasin_perso,
							actuel_emplacement = user_param.emplacement_perso,
							stock_site = user_param.site_perso,
							stock_entrepot = user_param.entrepot_perso,
							stock_magasin = user_param.magasin_perso,
							stock_emplacement = user_param.emplacement_perso,
							tare = cont_type.tare,
							poids = defaut["nomenclature_lot_poids_reference"],
							date_creation = defaut["contenant_date_creation"],
							date_reception = defaut["contenant_date_creation"],
							date_suppression = None,
							date_fin_validite = None,
							seuil_alarme = None,
							panier_user = request.user,
							provenance_site = site_p,
							responsable_suppression = None,
							responsable_mouvement = None,
							responsable_creation = request.user,
							)
						cont.date_fin_validite = cont.fin_validite()

						printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_contenant_imprimante.id)
						imp = Impression.objects.get(pk=user_param.etiquette_contenant.id)
						imp_d = ImpressionDetail.objects.filter(impression=imp)

						etiquette_print(printer, imp=imp, imp_d=imp_d, **{"user_param":user_param, "obj":cont})

						cont.contenant_stat()
						
						c += 1
				if defaut["contenant_nombre1"] != 0 and defaut["contenant_type1"] != None:
					print_etiquette(defaut["contenant_nombre1"], defaut["contenant_type1"])
				if defaut["contenant_nombre2"] != 0 and defaut["contenant_type2"] != None:
					print_etiquette(defaut["contenant_nombre2"], defaut["contenant_type2"])
				if defaut["contenant_nombre1"]+defaut["contenant_nombre2"] > 1:
					info.update({"info": "%d étiquettes imprimées" %(defaut["contenant_nombre1"]+defaut["contenant_nombre2"])})
				else:
					info.update({"info": "%d étiquette imprimée" %(defaut["contenant_nombre1"]+defaut["contenant_nombre2"])})
			else:
				info.update({"erreur": "Le code article ne doit pas contenir d'espace"})
		elif request.GET.has_key("recherche"):
			if request.GET["nomenclature_code_barre"] != None and request.GET["nomenclature_code_barre"] != "" and len(request.GET["nomenclature_code_barre"]) == 10:
				try:
					cont = Contenant.objects.get(code=request.GET["nomenclature_code_barre"])
				except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
					info.update({"erreur": "Aucune correspondance trouvée pour le code barre %s" %(request.GET["nomenclature_code_barre"])})
					defaut["nomenclature_code"] = ""
					defaut["nomenclature_description"] = ""
					defaut["nomenclature_commentaire"] = ""
					defaut["nomenclature_lot_commentaire"] = ""
					defaut["nomenclature_lot_projet"] = ""
					defaut["nomenclature_lot_client"] = ""
					defaut["nomenclature_lot_client_ka"] = ""
				else:
					defaut["nomenclature_code"] = cont.nomenclature_lot.nomenclature.code
					defaut["nomenclature_description"] = cont.nomenclature_lot.nomenclature.description
					defaut["nomenclature_commentaire"] = cont.nomenclature_lot.nomenclature.commentaire
					defaut["nomenclature_lot_commentaire"] = cont.nomenclature_lot.commentaire
					defaut["nomenclature_lot_client"] = cont.nomenclature_lot.client
					defaut["nomenclature_lot_client_ka"] = cont.nomenclature_lot.client_ka
					defaut["nomenclature_lot_projet"] = cont.nomenclature_lot.projet
					defaut["nomenclature_lot_poids_reference"] = cont.nomenclature_lot.poids_reference
					defaut["nomenclature_lot_roxane_manuel"] = cont.nomenclature_lot.nbr_ligne_manuel

			else:
				n = Nomenclature.objects.filter(code=defaut["nomenclature_code"])
				if len(n) >= 1:
					last = len(n) -1
					defaut["nomenclature_code"] = n[last].code
					defaut["nomenclature_description"] = n[last].description
					defaut["nomenclature_commentaire"] = n[last].commentaire
					lot = n[last].get_nomenclature_lot()
					if len(lot) >= 1:
						last = len(lot) -1
						defaut["nomenclature_lot_commentaire"] = lot[last].commentaire
						defaut["nomenclature_lot_projet"] = lot[last].projet
						defaut["nomenclature_lot_client"] = lot[last].client
						defaut["nomenclature_lot_client_ka"] = lot[last].client_ka
						defaut["nomenclature_lot_roxane_manuel"] = lot[last].nbr_ligne_manuel
					else:
						defaut["nomenclature_lot_commentaire"] = ""
						defaut["nomenclature_lot_projet"] = ""
						defaut["nomenclature_lot_client"] = ""
						defaut["nomenclature_lot_client_ka"] = ""
				else:
					info.update({"erreur": "Aucune correspondance trouvée pour le code %s" %(defaut["nomenclature_code"])})
					defaut["nomenclature_code"] = ""
					defaut["nomenclature_description"] = ""
					defaut["nomenclature_commentaire"] = ""
					defaut["nomenclature_lot_commentaire"] = ""
					defaut["nomenclature_lot_projet"] = ""
					defaut["nomenclature_lot_client"] = ""
					defaut["nomenclature_lot_client_ka"] = ""
		elif request.GET.has_key("valider"):
			if request.GET["nomenclature_code"].find(" ") == -1:
				def creation_contenant(nombre, c_type):
					c = 0
					while c < nombre:
						cont = lot.add_contenant(responsable_creation=request.user, type_contenant=ContenantType(pk=c_type))
						cont.provenance_site = StockSite.objects.get(pk=defaut["contenant_provenance_site"])
						cont.date_reception = defaut["contenant_date_creation"]
						cont.date_creation = defaut["contenant_date_creation"]
						cont.date_fin_validite = cont.fin_validite(defaut["nomenclature_duree_validite"])
						if defaut["nomenclature_site_entrepot_magasin"] == 99:
							nomenclature.reception_magasin = user_param.magasin_perso
							cont.actuel_site = user_param.site_perso
							cont.actuel_entrepot = user_param.entrepot_perso
							cont.actuel_magasin = user_param.magasin_perso
							cont.stock_site = user_param.site_perso
							cont.stock_entrepot = user_param.entrepot_perso
							cont.stock_magasin = user_param.magasin_perso
						else:
							site_entrepot_magasin = SiteEntrepotMagasin.objects.filter(pk=defaut["nomenclature_site_entrepot_magasin"])
							if len(site_entrepot_magasin) == 1:
								cont.actuel_site = site_entrepot_magasin[0].site
								cont.actuel_entrepot = site_entrepot_magasin[0].entrepot
								cont.actuel_magasin = site_entrepot_magasin[0].magasin
								cont.stock_site = site_entrepot_magasin[0].site
								cont.stock_entrepot = site_entrepot_magasin[0].entrepot
								cont.stock_magasin = site_entrepot_magasin[0].magasin
						cont.save()
						log = django_models.LogEntry()
						log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
						log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
						log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())		#Le type de contenu (ContentType) de l’objet modifié.
						log.object_id = cont.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
						log.object_repr = unicode(cont)																		#La représentation repr() de l’objet après sa modification.
						log.action_flag = django_models.ADDITION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
						log.change_message = "nomenclature_edit3"															#Description de la modification
						log.save()
						printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_contenant_imprimante.id)
						imp = Impression.objects.get(pk=user_param.etiquette_contenant.id)
						imp_d = ImpressionDetail.objects.filter(impression=imp)

						etiquette_print(printer, imp=imp, imp_d=imp_d, **{"user_param":user_param, "obj":cont})

						cont.contenant_stat()

						c += 1

				n_type = NomenclatureType.objects.get(pk=defaut["nomenclature_type"])

				log = django_models.LogEntry()
				try:
					nomenclature = n_type.add_nomenclature(code=defaut["nomenclature_code"], update=False)
					log.change_message = "nomenclature_edit3"															#Description de la modification
					log.action_flag = django_models.ADDITION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
				except NomenclatureExistant as i:
					nomenclature = i.args[0]
					if nomenclature.date_suppression == None:
						log.change_message = "nomenclature_edit3"															#Description de la modification
					else:
						nomenclature.date_suppression = None
						log.change_message = "nomenclature_edit3 (réssuscite)"															#Description de la modification
					log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
				else:
					nomenclature.duree_validite = defaut["nomenclature_duree_validite"]
					nomenclature.date_creation = defaut["contenant_date_creation"]
				finally:
					if defaut["nomenclature_description"] != "":
						if nomenclature.description == None or nomenclature.description == "":
							nomenclature.description = defaut["nomenclature_description"]
					if defaut["nomenclature_commentaire"] != "":
						if nomenclature.commentaire == None or nomenclature.commentaire == "":
							nomenclature.commentaire = defaut["nomenclature_commentaire"]
					if defaut["nomenclature_site_entrepot_magasin"] == 99:
						if nomenclature.reception_site.id == 1:
							nomenclature.reception_site = user_param.site_perso
						if nomenclature.reception_entrepot.id == 1:
							nomenclature.reception_entrepot = user_param.entrepot_perso
						if nomenclature.reception_magasin.id == 1:
							nomenclature.reception_magasin = user_param.magasin_perso
					else:
						site_entrepot_magasin = SiteEntrepotMagasin.objects.filter(pk=defaut["nomenclature_site_entrepot_magasin"])
						if len(site_entrepot_magasin) == 1:
							if nomenclature.reception_site.id == 1:
								nomenclature.reception_site = site_entrepot_magasin[0].site
							if nomenclature.reception_entrepot.id == 1:
								nomenclature.reception_entrepot = site_entrepot_magasin[0].entrepot
							if nomenclature.reception_magasin.id == 1:
								nomenclature.reception_magasin = site_entrepot_magasin[0].magasin
					nomenclature.save()
					log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
					log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
					log.content_type = ContentType.objects.get(app_label="stock_labo", model="Nomenclature".lower())	#Le type de contenu (ContentType) de l’objet modifié.
					log.object_id = nomenclature.id																		#La représentation textuelle de la clé primaire de l’objet modifié.
					log.object_repr = unicode(nomenclature)																#La représentation repr() de l’objet après sa modification.
					log.save()
				log = django_models.LogEntry()
				try:
					lot = nomenclature.add_lot(code=defaut["nomenclature_lot_code"], responsable_creation=request.user, update=False)
					log.change_message = "nomenclature_edit3"																#Description de la modification
					log.action_flag = django_models.ADDITION 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
				except NomenclatureLotExistant as i:
					lot = i.args[0]
					if lot.date_suppression == None:
						log.change_message = "nomenclature_edit3"																#Description de la modification
					else:
						lot.date_suppression = None
						log.change_message = "nomenclature_edit3 (réssuscite)"																#Description de la modification
					log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
					lot.save()
				else:
					if defaut["contenant_date_creation"] != "":
						lot.date_creation = defaut["contenant_date_creation"]
						lot.date_fin_validite = lot.fin_validite(duree=defaut["nomenclature_duree_validite"])
					if defaut["nomenclature_lot_poids_reference"] != None:
						if lot.poids_reference == None or lot.poids_reference == "":
							lot.poids_reference = defaut["nomenclature_lot_poids_reference"]
					lot.nbr_ligne_manuel = defaut["nomenclature_lot_roxane_manuel"]
					if defaut["nomenclature_lot_projet"] != None:
						lot.projet = defaut["nomenclature_lot_projet"]
						lot.client = lot.get_client()
						lot.client_ka = lot.get_client_ka()
					lot.save()
					lot.nomenclature_lot_stat()
				finally:
					lot.commentaire = defaut["nomenclature_lot_commentaire"]
					log.action_time = datetime.datetime.now()																#La date et l’heure de l’action.
					log.user = request.user																					#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
					log.content_type = ContentType.objects.get(app_label="stock_labo", model="NomenclatureLot".lower())		#Le type de contenu (ContentType) de l’objet modifié.
					log.object_id = lot.id																					#La représentation textuelle de la clé primaire de l’objet modifié.
					log.object_repr = unicode(lot)																			#La représentation repr() de l’objet après sa modification.
					log.save()

				if defaut["contenant_nombre1"] != 0 and defaut["contenant_type1"] != None:
					creation_contenant(defaut["contenant_nombre1"], defaut["contenant_type1"])

				if defaut["contenant_nombre2"] != 0 and defaut["contenant_type2"] != None:
					creation_contenant(defaut["contenant_nombre2"], defaut["contenant_type2"])
				info.update({"info": "%d contenant créés pour l'article %s" %(defaut["contenant_nombre1"]+defaut["contenant_nombre2"], defaut["nomenclature_code"])})
			else:
				info.update({"erreur": "Le code article ne doit pas contenir d'espace"})

#		if defaut["nomenclature_code"] != None and defaut["nomenclature_code"] != "":
#			header.header["page"]= "Coup : %s" %(defaut["nomenclature_code"])
		if defaut["nomenclature_description"] != None and defaut["nomenclature_description"] != "":
			header.header["page"]= defaut["nomenclature_description"]
		defaut.update({"contenant_date_creation": defaut["contenant_date_creation"].strftime("%d/%m/%Y")})
		form = NomenclatureForm3(initial=defaut)
		emp = [(p.id, p.nom_court()) for p in SiteEntrepotMagasin.objects.all()]
		emp.insert(0, (99, "Empl. perso : %s" %(user_param.magasin_perso.description)))
		form.fields["nomenclature_site_entrepot_magasin"].choices = emp
		form.fields["nomenclature_site_entrepot_magasin"].initial = defaut["nomenclature_site_entrepot_magasin"]
		return render(request, "stock_labo_nomenclature_edit3.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "info": info})

	defaut.update({"nomenclature_duree_validite": settings_default.DUREE_VALIDITE_COUP})
	defaut.update({"contenant_provenance_site": user_param.site_perso.id})
	defaut.update({"nomenclature_lot_code": datetime.datetime.now().strftime("%Y%m%d%H%M%S")})
	defaut.update({"contenant_date_creation": datetime.date.today().strftime("%d/%m/%Y")})
	form = NomenclatureForm3(initial=defaut)
	emp = [(p.id, p.nom_court()) for p in SiteEntrepotMagasin.objects.all()]
	emp.insert(0, (99, "Empl. perso : %s" %(user_param.magasin_perso.description)))
	form.fields["nomenclature_site_entrepot_magasin"].choices = emp
	form.fields["nomenclature_site_entrepot_magasin"].initial = 99
	form.fields["nomenclature_type"].initial = NomenclatureType.objects.get(code="COUP").id
	return render(request, "stock_labo_nomenclature_edit3.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "info": info})

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def nomenclature_edit4(request):
	"""
	Nouveau Concentré Roxane
	"""
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Article", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Article", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Article", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))

	user_param = UserPreference.objects.get(user=request.user)
	emp = [(p.id, p.nom_court()) for p in SiteEntrepotMagasin.objects.all()]
	emp.insert(0, (99, "Empl. perso : %s" %(user_param.magasin_perso.description)))

	onglet = Onglets(request.user)
	onglet.set_actif_by_id(0)
	step = 0
	defaut = {}
	info = {}
	nomenclature = None
	nomenclature_lot = None
	def set_read_only(f, d):
		for k in ("nomenclature_type", "nomenclature_code", "nomenclature_description", "nomenclature_commentaire", "nomenclature_lot_poids_reference", "nomenclature_lot_commentaire", "nomenclature_lot_projet"):
			if d.has_key(k) and d[k] != None and d[k] != "":
					f.fields[k].widget.attrs["readonly"] = True
		return f

	if len(request.GET) > 0:
		if request.GET.has_key("annuler"):
			return HttpResponseRedirect("/django/stock_labo/nomenclature/")
		if request.GET.has_key("recherche") and request.GET.has_key("nomenclature_code"):
			cut = request.GET["nomenclature_code"].find("/")
			#if cut == -1:
			#	formule = decode_roxane_export(r"/mnt/par-srv-files/lab-assis/export/", request.GET["nomenclature_code"], ".ROX", r"\r\n")
			#else:
			#	formule = decode_roxane_export(r"/mnt/par-srv-files/lab-assis/export/", request.GET["nomenclature_code"][:cut], ".ROX", r"\r\n")
			if cut == -1:
				formule = decode_roxane_export_new(r"/mnt/par-srv-sql/out/", request.GET["nomenclature_code"], ".txt", r"\r\n")
			else:
				formule = decode_roxane_export_new(r"/mnt/par-srv-sql/out/", request.GET["nomenclature_code"][:cut], ".txt", r"\r\n")
			if formule == None:
				step = 0
			else:
				step = 1
				defaut.update({"nomenclature_code": formule["entete"]["code_formule"]})
#				defaut.update({"nomenclature_commentaire": "Formule roxane n° %s" %(formule["entete"]["manager"])})
				defaut.update({"nomenclature_lot_roxane": formule["entete"]["manager"]})
				defaut.update({"contenant_date_creation": formule["entete"]["date_demande"].strftime("%d/%m/%Y")})
				defaut.update({"nomenclature_lot_code": formule["entete"]["batch"]})
				defaut.update({"nomenclature_lot_poids_reference": formule["entete"]["total"]})
				defaut.update({"nomenclature_lot_roxane_robot": formule["becher"]["last"]["dosage_station"]["robot"]})
				defaut.update({"nomenclature_lot_roxane_manuel": formule["becher"]["last"]["dosage_station"]["manuel"]})
				defaut.update({"nomenclature_duree_validite": settings_default.DUREE_VALIDITE_COUP})
				defaut.update({"contenant_provenance_site":user_param.site_perso.id})
				info_oracle = get_batch_info(formule["entete"]["batch"])
				if len(info_oracle) == 1:
					defaut.update({"nomenclature_description": info_oracle[0]["DESCRIPTION"]})
					defaut.update({"nomenclature_lot_projet": info_oracle[0]["PROJET"]})
					defaut.update({"nomenclature_lot_client": info_oracle[0]["CLIENT"]})
					defaut.update({"nomenclature_lot_client_ka": info_oracle[0]["CLIENT_KA"]})


			form = NomenclatureForm4(initial=defaut)
			form.fields["nomenclature_type"].initial = NomenclatureType.objects.get(code="ROX").id
			form.fields["nomenclature_site_entrepot_magasin"].choices = emp
			form.fields["nomenclature_site_entrepot_magasin"].initial = 99
			nbr_contenant_form = NbrContenantForm()
			if step == 0:
				info.update({"erreur": "Fichier Roxane introuvable"})
				form.fields["nomenclature_lot_poids_reference"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_type"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_description"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_commentaire"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_site_entrepot_magasin"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_duree_validite"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_lot_code"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_lot_commentaire"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_lot_projet"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_lot_client"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_lot_client_ka"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_lot_roxane"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_lot_roxane_robot"].widget = django_forms.HiddenInput()
				form.fields["nomenclature_lot_roxane_manuel"].widget = django_forms.HiddenInput()
				form.fields["contenant_date_creation"].widget = django_forms.HiddenInput()
				form.fields["contenant_provenance_site"].widget = django_forms.HiddenInput()
			return render(request, "stock_labo_nomenclature_edit4.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "nbr_contenant_form" : nbr_contenant_form, "step": step, "info" : info})
		elif request.GET.has_key("valider"):
			step = 1
			if request.GET["nomenclature_code"].find(" ") != -1:
				info.update({"erreur": "Le code article ne doit pas contenir d'espace"})
				form = NomenclatureForm4(initial=request.GET)
				form.fields["nomenclature_type"].initial = NomenclatureType.objects.get(code="ROX").id
				form.fields["nomenclature_site_entrepot_magasin"].choices = emp
				form.fields["nomenclature_site_entrepot_magasin"].initial = 99
				nbr_contenant_form = NbrContenantForm()
				return render(request, "stock_labo_nomenclature_edit4.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "nbr_contenant_form" : nbr_contenant_form, "step": step, "info" : info})
			else:
				step = 2
				n_type = NomenclatureType.objects.get(pk=int(request.GET["nomenclature_type"]))
				log = django_models.LogEntry()
				try:
					nomenclature = n_type.add_nomenclature(code=request.GET["nomenclature_code"], update=False)
					if request.GET["contenant_date_creation"] != "":
						nomenclature.date_creation = datetime.datetime.strptime(request.GET["contenant_date_creation"], "%d/%m/%Y")
					if request.GET["nomenclature_duree_validite"] != "":
						nomenclature.duree_validite = int(request.GET["nomenclature_duree_validite"])
					log.change_message = "nomenclature_edit4"															#Description de la modification
					log.action_flag = django_models.ADDITION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
				except NomenclatureExistant as i:
					nomenclature = i.args[0]
					if nomenclature.date_suppression == None:
						log.change_message = "nomenclature_edit4"															#Description de la modification
					else:
						nomenclature.date_suppression = None
						log.change_message = "nomenclature_edit4 (réssuscite)"															#Description de la modification
					log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.

				if request.GET["nomenclature_description"] != "":
					if nomenclature.description == None or nomenclature.description == "":
						nomenclature.description = request.GET["nomenclature_description"]
				if request.GET["nomenclature_commentaire"] != "":
					if nomenclature.commentaire == None or nomenclature.commentaire == "":
						nomenclature.commentaire = request.GET["nomenclature_commentaire"]
				if int(request.GET["nomenclature_site_entrepot_magasin"]) == 99:
					if nomenclature.reception_site.id == 1:
						nomenclature.reception_site = user_param.site_perso
					if nomenclature.reception_entrepot.id == 1:
						nomenclature.reception_entrepot = user_param.entrepot_perso
					if nomenclature.reception_magasin.id == 1:
						nomenclature.reception_magasin = user_param.magasin_perso
				else:
					site_entrepot_magasin = SiteEntrepotMagasin.objects.filter(pk=int(request.GET["nomenclature_site_entrepot_magasin"]))
					if len(site_entrepot_magasin) == 1:
						if nomenclature.reception_site.id == 1:
							nomenclature.reception_site = site_entrepot_magasin[0].site
						if nomenclature.reception_entrepot.id == 1:
							nomenclature.reception_entrepot = site_entrepot_magasin[0].entrepot
						if nomenclature.reception_magasin.id == 1:
							nomenclature.reception_magasin = site_entrepot_magasin[0].magasin
				nomenclature.save()
				log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
				log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
				log.content_type = ContentType.objects.get(app_label="stock_labo", model="Nomenclature".lower())	#Le type de contenu (ContentType) de l’objet modifié.
				log.object_id = nomenclature.id																		#La représentation textuelle de la clé primaire de l’objet modifié.
				log.object_repr = unicode(nomenclature)																#La représentation repr() de l’objet après sa modification.
				log.save()


				log = django_models.LogEntry()
				try:
					lot = nomenclature.add_lot(code=request.GET["nomenclature_lot_code"], responsable_creation=request.user, update=False)
					log.action_flag = django_models.ADDITION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
					log.change_message = "nomenclature_edit4"															#Description de la modification
				except NomenclatureLotExistant as i:
					lot = i.args[0]
					if lot.date_suppression == None:
						log.change_message = "nomenclature_edit4"												#Description de la modification
					else:
						lot.date_suppression = None
						log.change_message = "nomenclature_edit4 (réssuscite)"												#Description de la modification
					log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
					lot.commentaire = request.GET["nomenclature_lot_commentaire"]
				else:
					if request.GET["contenant_date_creation"] != "":
						lot.date_creation = datetime.datetime.strptime(request.GET["contenant_date_creation"],"%d/%m/%Y")
						if request.GET["nomenclature_duree_validite"] != "":
							lot.date_fin_validite = lot.fin_validite(duree=int(request.GET["nomenclature_duree_validite"]))
						else:
							lot.date_fin_validite = lot.fin_validite()
					lot.commentaire = request.GET["nomenclature_lot_commentaire"]
					#if request.GET["nomenclature_lot_projet"] != None:
						#lot.projet = request.GET["nomenclature_lot_projet"]
						#lot.client = lot.get_client()
						#lot.client_ka = lot.get_client_ka()
					lot.num_roxane = request.GET["nomenclature_lot_roxane"]
					lot.nbr_ligne_robot = int(request.GET["nomenclature_lot_roxane_robot"])
					lot.nbr_ligne_manuel = int(request.GET["nomenclature_lot_roxane_manuel"])
					lot.poids_reference = float(request.GET["nomenclature_lot_poids_reference"].replace(",","."))
					lot.save()
					lot.nomenclature_lot_stat()
				finally:
					log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
					log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
					log.content_type = ContentType.objects.get(app_label="stock_labo", model="NomenclatureLot".lower())	#Le type de contenu (ContentType) de l’objet modifié.
					log.object_id = lot.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
					log.object_repr = unicode(lot)																		#La représentation repr() de l’objet après sa modification.
					log.save()

				def creation_contenant(nombre, c_type):
					c = 0
					while c < nombre:
						cont = lot.add_contenant(responsable_creation=request.user, type_contenant=ContenantType(pk=c_type))
						cont.provenance_site = StockSite.objects.get(pk=int(request.GET["contenant_provenance_site"]))
						if request.GET["contenant_date_creation"] != "":
							cont.date_reception = datetime.datetime.strptime(request.GET["contenant_date_creation"],"%d/%m/%Y")
							cont.date_creation = datetime.datetime.strptime(request.GET["contenant_date_creation"],"%d/%m/%Y")
						else:
							cont.date_reception = datetime.date.today()
							cont.date_creation = datetime.date.today()
						if request.GET["nomenclature_duree_validite"] != "":
							cont.date_fin_validite = cont.fin_validite(int(request.GET["nomenclature_duree_validite"]))
						else:
							cont.date_fin_validite = cont.fin_validite()
						if int(request.GET["nomenclature_site_entrepot_magasin"]) == 99:
							cont.actuel_site = user_param.site_perso
							cont.actuel_entrepot = user_param.entrepot_perso
							cont.actuel_magasin = user_param.magasin_perso
							cont.stock_site = user_param.site_perso
							cont.stock_entrepot = user_param.entrepot_perso
							cont.stock_magasin = user_param.magasin_perso
						else:
							site_entrepot_magasin = SiteEntrepotMagasin.objects.filter(pk=int(request.GET["nomenclature_site_entrepot_magasin"]))
							if len(site_entrepot_magasin) == 1:
								cont.actuel_site = site_entrepot_magasin[0].site
								cont.actuel_entrepot = site_entrepot_magasin[0].entrepot
								cont.actuel_magasin = site_entrepot_magasin[0].magasin
								cont.stock_site = site_entrepot_magasin[0].site
								cont.stock_entrepot = site_entrepot_magasin[0].entrepot
								cont.stock_magasin = site_entrepot_magasin[0].magasin
						cont.save()
						log = django_models.LogEntry()
						log.action_time = datetime.datetime.now()														#La date et l’heure de l’action.
						log.user = request.user																			#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
						log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())	#Le type de contenu (ContentType) de l’objet modifié.
						log.object_id = cont.id																			#La représentation textuelle de la clé primaire de l’objet modifié.
						log.object_repr = unicode(cont)																	#La représentation repr() de l’objet après sa modification.
						log.action_flag = django_models.ADDITION 														#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
						log.change_message = "nomenclature_edit4"														#Description de la modification
						log.save()
						printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_contenant_imprimante.id)
						imp = Impression.objects.get(pk=user_param.etiquette_contenant.id)
						imp_d = ImpressionDetail.objects.filter(impression=imp)

						etiquette_print(printer, imp=imp, imp_d=imp_d, **{"user_param":user_param, "obj":cont})

						cont.contenant_stat()

						c += 1

				try:
					c_nbr = int(request.GET["contenant_nombre1"])
					c_type = int(request.GET["contenant_type1"])
				except ValueError:
					pass
				else:
					creation_contenant(c_nbr, c_type)

				try:
					c_nbr = int(request.GET["contenant_nombre2"])
					c_type = int(request.GET["contenant_type2"])
				except ValueError:
					pass
				else:
					creation_contenant(c_nbr, c_type)


				return HttpResponseRedirect("/django/stock_labo/nomenclature/%s" %(make_addr_param({"id_nomenclature":nomenclature.id, "id_nomenclature_lot":lot.id,"contenant" : "yes"})))

	form = NomenclatureForm4()
	form.fields["nomenclature_site_entrepot_magasin"].choices = emp
	form.fields["nomenclature_site_entrepot_magasin"].initial = 99

	form.fields["nomenclature_lot_poids_reference"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_type"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_description"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_commentaire"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_site_entrepot_magasin"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_duree_validite"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_lot_code"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_lot_commentaire"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_lot_projet"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_lot_client"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_lot_client_ka"].widget = django_forms.HiddenInput()
	form.fields["nomenclature_lot_roxane"].widget = django_forms.HiddenInput()
	form.fields["contenant_date_creation"].widget = django_forms.HiddenInput()
	form.fields["contenant_provenance_site"].widget = django_forms.HiddenInput()
	return render(request, "stock_labo_nomenclature_edit4.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "step": step})

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def nomenclature_edit5(request):
	"""
	Nouveau Concentré Roxane ou Serie/Coupage
	"""
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Article", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Article", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Article", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))

	user_param = UserPreference.objects.get(user=request.user)
	emp = [(p.id, p.nom_court()) for p in SiteEntrepotMagasin.objects.all()]
	emp.insert(0, (99, "Empl. perso : %s" %(user_param.magasin_perso.description)))

	onglet = Onglets(request.user)
	onglet.set_actif_by_id(0)
	step = 0
	defaut = {}
	info = {}
	nomenclature = None
	nomenclature_lot = None

	if len(request.GET) > 0:
		if request.GET.has_key("annuler"):
			return HttpResponseRedirect("/django/stock_labo/nomenclature/")
		elif request.GET.has_key("nomenclature"):
			return HttpResponseRedirect("/django/stock_labo/nomenclature_edit2/%s" %(make_addr_param({"nomenclature_code":request.GET["code"], "recherche":"Recherche article-lot"})))
		elif request.GET.has_key("roxane"):
			return HttpResponseRedirect("/django/stock_labo/nomenclature_edit4/%s" %(make_addr_param({"nomenclature_code":request.GET["code"], "recherche":"Recherche fichier Roxane"})))

	form = RechercheFichierArticleForm()
	return render(request, "stock_labo_nomenclature_edit5.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "step": step})

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def nomenclature_lot_edit(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Article", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Article", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Article", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))
	onglet = Onglets(request.user)
	onglet.set_actif_by_id(0)
	if len(request.GET) > 0:
		if request.GET.has_key("annuler"):
			return HttpResponseRedirect("/django/stock_labo/nomenclature/")
		elif request.GET.has_key("valider") or request.GET.has_key("dupliquer"):
			if request.GET["id_nomenclature_lot"] == "" or request.GET.has_key("dupliquer"):
				list_lot = NomenclatureLot.objects.filter(nomenclature=request.GET["id_nomenclature"]).filter(code=request.GET["code"])
				form = NomenclatureLotForm(request.GET)
				if form.is_valid() and len(list_lot) == 0:
					n_lot = form.save(commit=True)
					n_lot.client = n_lot.get_client()
					n_lot.client_ka = n_lot.get_client_ka()
					n_lot.responsable_creation = request.user
					n_lot.save()
					n_lot.nomenclature_lot_stat()
					log = django_models.LogEntry()
					log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
					log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
					log.content_type = ContentType.objects.get(app_label="stock_labo", model="NomenclatureLot".lower())	#Le type de contenu (ContentType) de l’objet modifié.
					log.object_id = n_lot.id																			#La représentation textuelle de la clé primaire de l’objet modifié.
					log.object_repr = unicode(n_lot)																	#La représentation repr() de l’objet après sa modification.
					log.action_flag = django_models.ADDITION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
					log.change_message = "nomenclature_lot_edit"														#Description de la modification
					log.save()
					return HttpResponseRedirect("/django/stock_labo/nomenclature/%s" %(make_addr_param({"id_nomenclature":request.GET["id_nomenclature"]})))
				else:
					print_etiquette = "/#/"
					return render(request, "stock_labo_nomenclature_lot_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "print_etiquette" : print_etiquette, "print_id" : None})
			else:
				lot = NomenclatureLot.objects.get(pk=int(request.GET["id_nomenclature_lot"]))
				form = NomenclatureLotForm(request.GET, instance=lot)
				if form.is_valid():
					n_lot = form.save(commit=True)
					n_lot.client = n_lot.get_client()
					n_lot.client_ka = n_lot.get_client_ka()
					n_lot.save()
					log = django_models.LogEntry()
					log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
					log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
					log.content_type = ContentType.objects.get(app_label="stock_labo", model="NomenclatureLot".lower())	#Le type de contenu (ContentType) de l’objet modifié.
					log.object_id = n_lot.id																			#La représentation textuelle de la clé primaire de l’objet modifié.
					log.object_repr = unicode(n_lot)																	#La représentation repr() de l’objet après sa modification.
					log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
					log.change_message = "nomenclature_lot_edit"														#Description de la modification
					log.save()
					return HttpResponseRedirect("/django/stock_labo/nomenclature/%s" %(make_addr_param({"id_nomenclature":request.GET["id_nomenclature"]})))
				else:
					form_info = NomenclatureLotInfoForm()
					print_etiquette = "/django/stock_labo/nomenclature_lot_etiquette_print/%s" %(make_addr_param({"id_nomenclature":defaut["id_nomenclature"], "id_nomenclature_lot":defaut["id_nomenclature_lot"]}))
					return render(request, "stock_labo_nomenclature_lot_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "form_info" : form_info, "print_etiquette" : print_etiquette, "print_id" : lot.id})
		elif request.GET.has_key("supprimer"):
			if request.GET["id_nomenclature_lot"] != "":
				lot = NomenclatureLot.objects.get(pk=int(request.GET["id_nomenclature_lot"]))
				log = django_models.LogEntry()
				log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
				log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
				log.content_type = ContentType.objects.get(app_label="stock_labo", model="NomenclatureLot".lower())	#Le type de contenu (ContentType) de l’objet modifié.
				log.object_id = lot.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
				log.object_repr = unicode(lot)																		#La représentation repr() de l’objet après sa modification.
				log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
				log.change_message = "nomenclature_lot_edit : suppression"											#Description de la modification
				log.save()
				lot.suppression(request.user)
				lot.suppression_parent(request.user)
			return HttpResponseRedirect("/django/stock_labo/nomenclature/%s" %(make_addr_param({"id_nomenclature":request.GET["id_nomenclature"]})))
		else:
			defaut = {}
			lot = None
			if request.GET.has_key("id_nomenclature"):
				defaut.update({"id_nomenclature" : request.GET["id_nomenclature"]})
				defaut.update({"nomenclature" : request.GET["id_nomenclature"]})
				ing = Nomenclature.objects.get(pk=int(request.GET["id_nomenclature"]))
				nomenclature_d = unicode(ing)
			if request.GET.has_key("id_nomenclature_lot"):
				lot = NomenclatureLot.objects.get(pk=int(request.GET["id_nomenclature_lot"]))
				defaut.update({"commentaire" : lot.commentaire})
				defaut.update({"projet" : lot.projet})
				defaut.update({"client" : lot.client})
				defaut.update({"client_ka" : lot.client_ka})
				defaut.update({"id_nomenclature_lot" : request.GET["id_nomenclature_lot"]})
				form = NomenclatureLotForm(instance=lot, initial=defaut)
			else:
				defaut.update({"date_fin_validite" : datetime.date.today() + datetime.timedelta(ing.duree_validite)})
				form = NomenclatureLotForm(initial=defaut)
#			print_etiquette = "/django/stock_labo/nomenclature_lot_etiquette_print/%s" %(make_addr_param({"id_nomenclature":defaut["id_nomenclature"], "id_nomenclature_lot":defaut["id_nomenclature_lot"]}))
			if defaut.has_key("id_nomenclature_lot"):
				print_etiquette = "/django/stock_labo/nomenclature_lot_etiquette_print/%s" %(make_addr_param({"id_nomenclature":defaut["id_nomenclature"], "id_nomenclature_lot":defaut["id_nomenclature_lot"]}))
				print_id = defaut["id_nomenclature_lot"]
			else:
				print_etiquette = "/#/"
				print_id = None
			return render(request, "stock_labo_nomenclature_lot_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "nomenclature_d" : nomenclature_d, "form" : form, "print_etiquette" : print_etiquette, "print_id" : print_id})

		#form = NomenclatureLotForm()
		#if defaut.has_key("id_nomenclature_lot"):
		#	print_etiquette = "/django/stock_labo/nomenclature_lot_etiquette_print/%s" %(make_addr_param({"id_nomenclature_lot":defaut["id_nomenclature_lot"], "print_id" : defaut["id_nomenclature_lot"]}))
		#else:
		#	print_etiquette = "/#/"
		#return render(request, "stock_labo_nomenclature_lot_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "print_etiquette" : print_etiquette, "print_id" : None})

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def nomenclature_contenant_edit(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Article", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Article", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Article", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))
	onglet = Onglets(request.user)
	onglet.set_actif_by_id(0)
	info = {}
	if len(request.GET) > 0:
		if request.GET.has_key("annuler"):
			return HttpResponseRedirect("/django/stock_labo/nomenclature/")
		elif request.GET.has_key("valider") or request.GET.has_key("nouveau"):
			code_barre = None
			if request.GET["id_contenant"] == "" or request.GET.has_key("nouveau"):
				form = ContenantForm(request.GET)
				if form.is_valid():
					cont = form.save()
					if cont.date_fin_validite == None:
						cont.date_fin_validite = cont.fin_validite()
					cont.code = "2%0.9d" %(cont.id)
#					if cont.tare == None:
#						cont.tare = cont.type_contenant.tare
					cont.date_creation = datetime.date.today()
					cont.save()
					cont.contenant_stat()
					log = django_models.LogEntry()
					log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
					log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
					log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())		#Le type de contenu (ContentType) de l’objet modifié.
					log.object_id = cont.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
					log.object_repr = unicode(cont)																		#La représentation repr() de l’objet après sa modification.
					log.action_flag = django_models.ADDITION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
					log.change_message = "nomenclature_contenant_edit"													#Description de la modification
					log.save()
					if request.GET["id_nomenclature_lot"] == "":
						return
#						return HttpResponseRedirect("/django/stock_labo/nomenclature/")
					else:
						return HttpResponseRedirect("/django/stock_labo/nomenclature/%s" %(make_addr_param({"contenant":"yes", "id_nomenclature":request.GET["id_nomenclature"], "id_nomenclature_lot":request.GET["id_nomenclature_lot"]})))
				else:
					info.update({"projet" : cont.nomenclature_lot.projet})
					return render(request, "stock_labo_nomenclature_contenant_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "code_barre" : code_barre, "info" : info, "print_contenant_id" : None})
			else:
				code_barre = request.GET["id_contenant"]
				cont = Contenant.objects.get(pk=int(request.GET["id_contenant"]))
				form = ContenantForm(request.GET, instance=cont)
				if form.is_valid():
					cont = form.save(commit=True)
					if cont.date_fin_validite == None:
						cont.date_fin_validite = cont.fin_validite()
					cont.save()
					log = django_models.LogEntry()
					log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
					log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
					log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())		#Le type de contenu (ContentType) de l’objet modifié.
					log.object_id = cont.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
					log.object_repr = unicode(cont)																		#La représentation repr() de l’objet après sa modification.
					log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
					log.change_message = "nomenclature_contenant_edit"													#Description de la modification
					log.save()
					return HttpResponseRedirect("/django/stock_labo/nomenclature/%s" %(make_addr_param({"contenant":"yes", "id_nomenclature":request.GET["id_nomenclature"], "id_nomenclature_lot":request.GET["id_nomenclature_lot"]})))
				else:
					info.update({"projet" : cont.nomenclature_lot.projet})
					return render(request, "stock_labo_nomenclature_contenant_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form, "code_barre" : code_barre, "info" : info, "print_contenant_id" : cont.id})
		elif request.GET.has_key("supprimer"):
			cont = Contenant.objects.get(pk=int(request.GET["id_contenant"]))
			log = django_models.LogEntry()
			log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
			log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
			log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())		#Le type de contenu (ContentType) de l’objet modifié.
			log.object_id = cont.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
			log.object_repr = unicode(cont)																		#La représentation repr() de l’objet après sa modification.
			log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
			log.change_message = "nomenclature_contenant_edit : suppression"									#Description de la modification
			log.save()
			cont.suppression(request.user)
			cont.suppression_parent(request.user)
			return HttpResponseRedirect("/django/stock_labo/nomenclature/%s" %(make_addr_param({"contenant":"yes", "id_nomenclature":request.GET["id_nomenclature"], "id_nomenclature_lot":request.GET["id_nomenclature_lot"]})))
		elif request.GET.has_key("print_contenant"):
			printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_contenant_imprimante.id)
			imp = Impression.objects.get(pk=user_param.etiquette_contenant.id)
			imp_d = ImpressionDetail.objects.filter(impression=imp)
			obj = Contenant.objects.get(pk=request.GET["id_contenant"])
			return etiquette_print(printer, imp=imp, imp_d=imp_d, **{"user_param":user_param, "obj":obj, "return_url":"/django/stock_labo/nomenclature/%s" %(make_addr_param({"contenant":"yes", "id_nomenclature":request.GET["id_nomenclature"], "id_nomenclature_lot":request.GET["id_nomenclature_lot"]}))})
		elif request.GET.has_key("print_emplacement"):
			printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_emplacement_imprimante.id)
			imp = Impression.objects.get(pk=user_param.etiquette_emplacement.id)
			imp_d = ImpressionDetail.objects.filter(impression=imp)
			obj = Contenant.objects.get(pk=request.GET["id_contenant"])
			return etiquette_print(printer, imp=imp, imp_d=imp_d, **{"user_param":user_param, "obj":obj, "return_url":"/django/stock_labo/nomenclature/%s" %(make_addr_param({"contenant":"yes", "id_nomenclature":request.GET["id_nomenclature"], "id_nomenclature_lot":request.GET["id_nomenclature_lot"]}))})
		elif request.GET.has_key("dupliquer"):
			defaut = {}
			code_barre = None
			nomenclature_d = None
			nomenclature_lot_d = None
			info.update({"erreur": "Nouveau Contenant"})
			defaut.update({"code" : "0000000000"})
			defaut.update({"date_reception" : datetime.date.today()})
			defaut.update({"id_nomenclature" : request.GET["id_nomenclature"]})
			defaut.update({"id_nomenclature_lot" : request.GET["id_nomenclature_lot"]})
			defaut.update({"nomenclature_lot" : request.GET["id_nomenclature_lot"]})
			defaut.update({"actuel_site" : user_param.site_perso.id})
			defaut.update({"actuel_entrepot" : user_param.entrepot_perso.id})
			defaut.update({"actuel_magasin" : user_param.magasin_perso.id})
			defaut.update({"actuel_emplacement" : user_param.emplacement_perso})
			defaut.update({"stock_site" : user_param.site_perso.id})
			defaut.update({"stock_entrepot" : user_param.entrepot_perso.id})
			defaut.update({"stock_magasin" : user_param.magasin_perso.id})
			defaut.update({"stock_emplacement" : user_param.emplacement_perso})
			defaut.update({"stock_emplacement" : user_param.emplacement_perso})
			defaut.update({"provenance_site" : user_param.site_perso.id})
			lot = NomenclatureLot.objects.get(pk=int(request.GET["id_nomenclature_lot"]))
			defaut.update({"date_fin_validite" : lot.date_fin_validite})
			nomenclature_lot_d = lot.code
			nomenclature_d = lot.nomenclature.__unicode__()
			info.update({"projet" : lot.projet})
			form = ContenantForm(initial=defaut)
			return render(request, "stock_labo_nomenclature_contenant_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "nomenclature_d" : nomenclature_d, "nomenclature_lot_d" : nomenclature_lot_d, "form" : form, "code_barre" : code_barre, "info" : info, "print_contenant_id" : None})
		else:
			defaut = {}
			code_barre = None
			cont = None
			nomenclature_d = None
			nomenclature_lot_d = None
			if request.GET.has_key("id_contenant"):
				cont = Contenant.objects.get(pk=int(request.GET["id_contenant"]))
				defaut.update({"id_nomenclature" : request.GET["id_nomenclature"]})
				defaut.update({"id_nomenclature_lot" : request.GET["id_nomenclature_lot"]})
				defaut.update({"id_contenant" : request.GET["id_contenant"]})
				code_barre = cont.code
				nomenclature_lot_d = cont.nomenclature_lot.code
				nomenclature_d = cont.nomenclature_lot.nomenclature.__unicode__()
				info.update({"projet" : cont.nomenclature_lot.projet})
				form = ContenantForm(instance=cont, initial=defaut)
			elif request.GET.has_key("id_nomenclature_lot"):
				defaut.update({"code" : "0000000000"})
				defaut.update({"date_reception" : datetime.date.today()})
				defaut.update({"id_nomenclature" : request.GET["id_nomenclature"]})
				defaut.update({"id_nomenclature_lot" : request.GET["id_nomenclature_lot"]})
				defaut.update({"nomenclature_lot" : request.GET["id_nomenclature_lot"]})
				defaut.update({"actuel_site" : user_param.site_perso.id})
				defaut.update({"actuel_entrepot" : user_param.entrepot_perso.id})
				defaut.update({"actuel_magasin" : user_param.magasin_perso.id})
				defaut.update({"actuel_emplacement" : user_param.emplacement_perso})
				defaut.update({"stock_site" : user_param.site_perso.id})
				defaut.update({"stock_entrepot" : user_param.entrepot_perso.id})
				defaut.update({"stock_magasin" : user_param.magasin_perso.id})
				defaut.update({"stock_emplacement" : user_param.emplacement_perso})
				defaut.update({"stock_emplacement" : user_param.emplacement_perso})
				defaut.update({"provenance_site" : user_param.site_perso.id})
				lot = NomenclatureLot.objects.get(pk=int(request.GET["id_nomenclature_lot"]))
				defaut.update({"date_fin_validite" : lot.date_fin_validite})
				nomenclature_lot_d = lot.code
				nomenclature_d = lot.nomenclature.__unicode__()
				info.update({"projet" : lot.projet})
				form = ContenantForm(initial=defaut)
			if cont == None:
				print_contenant_id = None
			else:
				print_contenant_id = cont.id
			return render(request, "stock_labo_nomenclature_contenant_edit.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "nomenclature_d" : nomenclature_d, "nomenclature_lot_d" : nomenclature_lot_d, "form" : form, "code_barre" : code_barre, "info" : info, "print_contenant_id" : print_contenant_id})

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def nomenclature_contenant_panier(request):
	if request.GET.has_key("id_contenant"):
		user_param = UserPreference.objects.get(user=request.user)
		ing = Contenant.objects.get(pk=int(request.GET["id_contenant"]))
		if request.GET.has_key("ajouter"):
			ing.panier_user = request.user
		if request.GET.has_key("supprimer"):
			ing.panier_user = None
		ing.save()
	return HttpResponseRedirect("/django/stock_labo/nomenclature/%s" %(make_addr_param({"contenant":"yes", "id_nomenclature":request.GET["id_nomenclature"], "id_nomenclature_lot":request.GET["id_nomenclature_lot"]})))

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def nomenclature_etiquette_print(request):
	user_param = UserPreference.objects.get(user=request.user)
	printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_nomenclature_imprimante.id)
	imp = Impression.objects.get(pk=user_param.etiquette_nomenclature.id)
	imp_d = ImpressionDetail.objects.filter(impression=imp)
	obj = Nomenclature.objects.get(pk=request.GET["id_nomenclature"])
	return etiquette_print(printer, imp, imp_d, **{"user_param":user_param, "obj":obj, "return_url":"/django/stock_labo/nomenclature/%s" %(make_addr_param({"id_nomenclature":request.GET["id_nomenclature"]}))})

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def nomenclature_lot_etiquette_print(request):
	user_param = UserPreference.objects.get(user=request.user)
	printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_lot_imprimante.id)
	imp = Impression.objects.get(pk=user_param.etiquette_lot.id)
	imp_d = ImpressionDetail.objects.filter(impression=imp)
	obj = NomenclatureLot.objects.get(pk=request.GET["id_nomenclature_lot"])
	return etiquette_print(printer, imp=imp, imp_d=imp_d, **{"user_param":user_param, "obj":obj, "return_url":"/django/stock_labo/nomenclature/%s" %(make_addr_param({"contenant":"yes", "id_nomenclature":request.GET["id_nomenclature"], "id_nomenclature_lot":request.GET["id_nomenclature_lot"]}))})

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def nomenclature_contenant_etiquette_print(request):
	user_param = UserPreference.objects.get(user=request.user)
	printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_contenant_imprimante.id)
	imp = Impression.objects.get(pk=user_param.etiquette_contenant.id)
	imp_d = ImpressionDetail.objects.filter(impression=imp)
	obj = Contenant.objects.get(pk=request.GET["id_contenant"])
	return etiquette_print(printer, imp=imp, imp_d=imp_d, **{"user_param":user_param, "obj":obj, "return_url":"/django/stock_labo/nomenclature/%s" %(make_addr_param({"contenant":"yes", "id_nomenclature":request.GET["id_nomenclature"], "id_nomenclature_lot":request.GET["id_nomenclature_lot"]}))})




