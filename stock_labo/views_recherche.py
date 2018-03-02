# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from fonction import *
from models import *
from forms import *

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def recherche(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Contenant", user="%s" %(request.user), panier=Contenant.objects.filter(panier_user=request.user).count())
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Contenant", user="%s" %(request.user), panier=Contenant.objects.filter(panier_user=request.user).count())
	else:
		header = Headers(page="Contenant", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=Contenant.objects.filter(panier_user=request.user).count())
	onglet = Onglets(request.user)
	onglet.set_actif_by_id(1)
	list1 = None
	list2 = None
	list3 = None
	list4 = None
	info = {}
	bouton = Boutons()
#	bouton.add_bouton("Nouvel <br/>Article", title="Créer un nouvel ingrédient", href="/django/stock_labo/nomenclature_edit/")

	rech_def = {}
	if request.GET.has_key("limit_du"):
		rech_def.update({"limit_du":int(request.GET["limit_du"])})
	else:
		rech_def.update({"limit_du":0})
	if request.GET.has_key("limit_au"):
		rech_def.update({"limit_au":int(request.GET["limit_au"])})
	else:
		rech_def.update({"limit_au":100})
	if request.GET.has_key("suivant_stock") or request.GET.has_key("suivant_global"):
		pas = rech_def["limit_au"] - rech_def["limit_du"]
		rech_def["limit_au"] += pas
		rech_def["limit_du"] += pas
	if request.GET.has_key("recherche_stock") or request.GET.has_key("recherche_global"):
		pas = rech_def["limit_au"] - rech_def["limit_du"]
		rech_def["limit_au"] = pas
		rech_def["limit_du"] = 0
	if request.GET.has_key("unite_stock"):
		rech_def.update({"unite_stock":request.GET["unite_stock"]})
	if request.GET.has_key("code"):
		rech_def.update({"code":request.GET["code"]})
	if request.GET.has_key("description"):
		rech_def.update({"description":request.GET["description"]})
	if request.GET.has_key("lot"):
		rech_def.update({"lot":request.GET["lot"]})
	if request.GET.has_key("type_nomenclature"):
		rech_def.update({"type_nomenclature":request.GET["type_nomenclature"]})
	if request.GET.has_key("type_contenant"):
		rech_def.update({"type_contenant":request.GET["type_contenant"]})
	if request.GET.has_key("date_du"):
		rech_def.update({"date_du":request.GET["date_du"]})
	if request.GET.has_key("date_au"):
		rech_def.update({"date_au":request.GET["date_au"]})
	if request.GET.has_key("sup"):
		rech_def.update({"sup":request.GET["sup"]})
	if request.GET.has_key("collection"):
		rech_def.update({"collection":request.GET["collection"]})
	if request.GET.has_key("commentaire"):
		rech_def.update({"commentaire":request.GET["commentaire"]})
	recherche = RechercheContenantForm(initial=rech_def)

	if len(request.GET) > 0:
		if request.GET.has_key("recherche_flash"):
			fp_hist = []
			try:
				if request.GET["unite_stock"] != "":
					fp_hist = get_flash_point(contenant_code=request.GET["unite_stock"])
				elif request.GET["lot"] != "":
					fp_hist = get_flash_point(nomenclature_lot_code=request.GET["lot"])
				elif request.GET["code"] != "":
					fp_hist = get_flash_point(nomenclature_code=request.GET["code"])
				elif request.GET["description"] != "":
					fp_hist = get_flash_point(nomenclature_description=request.GET["description"])
			except FlashPointInconnu:
				info.update({"erreur" : "Aucun point éclair connu"})

			if len(fp_hist) > 0:
				"""
				Liste des flash point
				"""

				nouvelle_liste = Table(caption="Points éclair", summary="Point éclair", style="width:100%;", entete=False, table_class="list_table")

				l = Table.Ligne(ligne_class="list_thead")
				l.add_cellule("Code", title="Code Article", style=None, cellule_class="list_thead_th")
				l.add_cellule("Article", title="Description article", style=None, cellule_class="list_thead_th")
				l.add_cellule("Lot", title="Code lot", style=None, cellule_class="list_thead_th")
				l.add_cellule("Date", title="Date d'enregistrement du point éclare", style=None, cellule_class="list_thead_th")
				l.add_cellule("Flash", title="Point éclare", style=None, cellule_class="list_thead_th")
				l.add_cellule("Resp.", title="Responçable point éclair", style=None, cellule_class="list_thead_th")
				nouvelle_liste.add_headers(l.get_ligne())

				nouvelle_liste.liste.update({"n_ligne_total" : fp_hist.count()})

				for c in fp_hist:
					l = Table.Ligne(style="line-height: 180%;")
					l.add_cellule(c.nomenclature_code)
					l.add_cellule(c.nomenclature_description)
					l.add_cellule(c.nomenclature_lot_code)
					l.add_cellule(c.date_flash_point)
					l.add_cellule(c.flash_point)
					l.add_cellule(c.responsable_flash_point_login)
					l.ligne["ligne_class"] == None 
					for c in l.ligne["cellules"]:
						c["cellule_class"] = "list_body_td"
					nouvelle_liste.add_ligne(l.get_ligne(), class_paire="list_body_tr_p", class_impaire="list_body_tr_i")

				list1 = nouvelle_liste







				return render(request, "stock_labo_contenant_liste.html", {
					"header": header.get_headers(),
					"onglet" : onglet.get_onglets(),
					"recherche": recherche,
					"list" : list1.get_liste(),
					"info" : info})






		else:
			lieu_recherche = []
			lieu_recherche.append({"designation" : "Recherche dans le stock perso", "site" : user_param.site_perso.id, "entrepot" : user_param.entrepot_perso.id, "magasin" : user_param.magasin_perso.id})
			lieu_recherche.append({"designation" : "Recherche dans le stock proche", "site" : user_param.site_perso.id, "entrepot" : user_param.entrepot_perso.id})
			lieu_recherche.append({"designation" : "Recherche dans le stockage commun", "magasin.type" : "20"})
			if request.GET.has_key("recherche_global") or request.GET.has_key("suivant_global"):
				lieu_recherche.append({"designation" : "Recherche global"})
			list1 = Liste(caption=Contenant.__doc__, summary=Contenant.__doc__)

			rech = 0
			cont = []
			c = []
			while rech < len(lieu_recherche):
				info.update({"info":lieu_recherche[rech]["designation"]})

				if rech_def.has_key("sup"):
					c = Contenant.objects.filter(date_suppression__isnull=False).order_by("date_fin_validite")
				else:
					c = Contenant.objects.filter(date_suppression__isnull=True).order_by("date_fin_validite")
					if lieu_recherche[rech].has_key("site"):
						c = c.filter(actuel_site__id=lieu_recherche[rech]["site"])
					if lieu_recherche[rech].has_key("entrepot"):
						c = c.filter(actuel_entrepot__id=lieu_recherche[rech]["entrepot"])
					if lieu_recherche[rech].has_key("magasin"):
						c = c.filter(actuel_magasin__id=lieu_recherche[rech]["magasin"])
					if lieu_recherche[rech].has_key("magasin.type"):
						c = c.filter(actuel_magasin__stock_magasin_type__lt=lieu_recherche[rech]["magasin.type"])

				list1.liste["n_ligne_total"] = c.count()

				if rech_def.has_key("unite_stock") and rech_def["unite_stock"] != "":
					c = c.filter(code__icontains=rech_def["unite_stock"])

				if rech_def.has_key("code") and rech_def["code"] != "":
					c = c.filter(nomenclature_lot__nomenclature__code__icontains=rech_def["code"])

				if rech_def.has_key("description") and rech_def["description"] != "":
					c = c.filter(nomenclature_lot__nomenclature__description__icontains=rech_def["description"])

				if rech_def.has_key("lot") and rech_def["lot"] != "":
					c = c.filter(nomenclature_lot__code__icontains=rech_def["lot"])

				if rech_def.has_key("type_nomenclature") and rech_def["type_nomenclature"] != "":
					c = c.filter(nomenclature_lot__nomenclature__nomenclature_type__code__icontains=rech_def["type_nomenclature"])

				if rech_def.has_key("type_contenant") and rech_def["type_contenant"] != "":
					c = c.filter(type_contenant__code__icontains=rech_def["type_contenant"])

				if rech_def.has_key("date_du") and rech_def["date_du"] != "":
					c = c.filter(date_creation__gte=rech_def["date_du"])

				if rech_def.has_key("date_au") and rech_def["date_au"] != "":
					c = c.filter(commentaire__lte=rech_def["date_au"])

				if rech_def.has_key("commentaire") and rech_def["commentaire"] != "":
					c = c.filter(nomenclature_lot__nomenclature__commentaire__icontains=rech_def["commentaire"])

				if rech_def.has_key("collection"):
					c = c.filter(nomenclature_lot__nomenclature__collection=True)

				cont += c
				rech += 1

			i = 0
			cont_id = []
			while i < len(cont):
				if cont[i].id in cont_id:
					cont.pop(i)
					continue
				else:
					cont_id.append(cont[i].id)
					i += 1

			list1.liste.update({"n_ligne_affiche" : len(cont)})
			if len(cont) == 0:
				info.update({"erreur":"Aucun contenant disponible pour cette recherche"})
			cont = cont[rech_def["limit_du"]:rech_def["limit_au"]]
			list1.liste.update({"n_ligne_limit" : len(cont)})

			l = Liste.Ligne()
			l.add_cellule("Code barre", title=Contenant._meta.fields[1].nom_long, width="100px")										#code barre
			l.add_cellule("code article", title=Nomenclature._meta.fields[1].nom_long, width="120px")									#code MP
			l.add_cellule(Nomenclature._meta.fields[2].nom_colonne, title=Nomenclature._meta.fields[2].nom_long)						#description
			l.add_cellule("<center>C</center>", title="Commentaire", width="50px")														#commantaire
			l.add_cellule("Type", title=NomenclatureType._meta.fields[1].nom_long, width="50px")										#type
			l.add_cellule("contenant", title=ContenantType._meta.fields[1].nom_long, width="80px")										#type_contenant
	#		l.add_cellule(StockSite._meta.fields[1].nom_colonne, title=StockSite._meta.fields[1].nom_long, width="8%")					#stock_site
			l.add_cellule(StockEntrepot._meta.fields[1].nom_colonne, title=StockEntrepot._meta.fields[1].nom_long, width="8%")			#stock_entrepot
			l.add_cellule(StockMagasin._meta.fields[1].nom_colonne, title=StockMagasin._meta.fields[1].nom_long, width="8%")			#stock_magasin
	#		l.add_cellule(Contenant._meta.fields[14].nom_colonne, title=Contenant._meta.fields[14].nom_long, width="8%")				#date_creation
			l.add_cellule(Contenant._meta.fields[15].nom_colonne, title=Contenant._meta.fields[15].nom_long, width="8%")				#date_reception
			l.add_cellule(Contenant._meta.fields[17].nom_colonne, title=Contenant._meta.fields[17].nom_long, width="8%")				#date_fin_validite
			l.add_cellule("<center>Col</center>", title=Nomenclature._meta.fields[12].nom_long, width="50px")			#collection
			l.add_cellule("<center>Imp. É</center>", title="Imprimer une nouvelle etiquette", width="80px")								#Etiquette
			if request.user.has_perm("stock_labo.panier"):
				l.add_cellule("<center>Panier</center>", title="Ajouter/Supprimer du panier", width="80px")									#Panier
			l.add_cellule("<center>Der. M.</center>", title="Responsable du dernier mouvement", width="80px")							#mouvement
			list1.add_headers(l.get_ligne())
			for c in cont:
				l = Liste.Ligne()
				l.add_cellule(c.code, href="/django/stock_labo/nomenclature_contenant_edit/%s" %(make_addr_param({"id_nomenclature":c.nomenclature_lot.nomenclature.id, "id_nomenclature_lot":c.nomenclature_lot.id,"id_contenant":c.id})))
				l.add_cellule(c.nomenclature_lot.nomenclature.code)
				l.add_cellule(c.nomenclature_lot.nomenclature.description)
				if c.nomenclature_lot.nomenclature.commentaire == "" or c.nomenclature_lot.nomenclature.commentaire == None:
					l.add_cellule(" ")
				else:
					l.add_cellule("<center><img src=\"/static/svg/format-justify-fill.svg\" height=\"24\" alt=\"Commentaire\"/></center>", title=c.nomenclature_lot.nomenclature.commentaire)
				l.add_cellule(c.nomenclature_lot.nomenclature.nomenclature_type.code, title=c.nomenclature_lot.nomenclature.nomenclature_type.code)
				l.add_cellule(c.type_contenant.code, title=c.type_contenant.description)
	#			l.add_cellule(c.actuel_site.code, title=c.stock_site.description)
				l.add_cellule(c.actuel_entrepot.description, title=c.stock_entrepot.description)
				l.add_cellule(c.actuel_magasin.description, title=format_list_param_user(get_site_entrepot_magasin_users(site=c.actuel_site, entrepot=c.actuel_entrepot, magasin=c.actuel_magasin)))
	#			l.add_cellule(c.f_date_creation(Contenant._meta.fields[14].format_date_time))
				l.add_cellule(c.f_date_reception(Contenant._meta.fields[15].format_date_time))
				l.add_cellule(c.f_date_fin_validite(Contenant._meta.fields[17].format_date_time))
				if c.nomenclature_lot.nomenclature.collection == True:
					l.add_cellule("<center>X</center>")
				else:
					l.add_cellule(" ")
				if c.date_suppression != None:
					l.add_cellule("<center><img src=\"/static/svg/process-stop.svg\" height=\"24\" /></center>", title=u"Le contenant est supprimé")
				else:
					l.add_cellule(
						"<center><img src=\"/static/svg/document-print.svg\" height=\"24\" alt=\"Etiquette\"/></center>",
						title="Impression etiquette contenant",
						href=None,
						cellule_id="etiquette_print_%d" %(c.id),
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
						else:
							if get_user_param(c.panier_user) == None:
		#							c.panier_user = None
		#							c.save()
								l.add_cellule("<center>???</center>", title=u"Contenant utilisé par inconnu %s %s (%s)" %(c.panier_user.first_name, c.panier_user.last_name, c.panier_user.username))
							else:
								if c.panier_user == request.user:
									l.add_cellule("<center><img src=\"/static/svg/format-indent-less.svg\" height=\"24\" alt=\"Supprimer le contenant du panier\"/></center>", title="Supprimer le contenant du panier", href="/django/stock_labo/nomenclature_contenant_panier/%s" %(make_addr_param({"supprimer":"yes", "id_nomenclature":c.nomenclature_lot.nomenclature.id, "id_nomenclature_lot":c.nomenclature_lot.id,"id_contenant":c.id})))
								else:
									l.add_cellule(get_user_param(c.panier_user).initial, title=u"Contenant utilisé par %s %s (%s)" %(c.panier_user.first_name, c.panier_user.last_name, c.panier_user.username))
				if c.responsable_mouvement == None:
					l.add_cellule("<center>--</center>", title="Pas de mouvement enregistré")
				else:
					l.add_cellule("<center>%s</center>" %(get_user_param(c.responsable_mouvement).initial), title=u"Contenant déplacé par %s %s (%s)" %(c.responsable_mouvement.first_name, c.responsable_mouvement.last_name, c.responsable_mouvement.username))

				list1.add_ligne(l.get_ligne())



			if list4 != None:
				return render(request, "stock_labo_contenant_liste.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "recherche": recherche, "list1" : list1.get_liste(), "list2" : list2.get_liste(), "list3" : list3.get_liste(), "list4" : list4.get_liste(), "bouton" : bouton.get_boutons()})
			elif list3 != None:
				return render(request, "stock_labo_contenant_liste.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "recherche": recherche, "list1" : list1.get_liste(), "list2" : list2.get_liste(), "list3" : list3.get_liste(), "bouton" : bouton.get_boutons()})
			elif list2 != None:
				return render(request, "stock_labo_contenant_liste.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "recherche": recherche, "list1" : list1.get_liste(), "list2" : list2.get_liste(), "bouton" : bouton.get_boutons()})
			else:
		#		return render(request, "stock_labo_contenant_liste.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "recherche": recherche, "list" : list1.get_liste(), "bouton" : bouton.get_boutons()})
				return render(request, "stock_labo_contenant_liste.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "recherche": recherche, "list" : list1.get_liste(), "info" : info})

	return render(request, "stock_labo_contenant_liste.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "recherche": recherche, "info" : info})


@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def recherche_contenant_etiquette_print(request):
	user_param = UserPreference.objects.get(user=request.user)
	printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_contenant_imprimante.id)
	imp = Impression.objects.get(pk=user_param.etiquette_contenant.id)
	imp_d = ImpressionDetail.objects.filter(impression=imp)
	obj = Contenant.objects.get(pk=request.GET["id_contenant"])
	return etiquette_print(printer, imp=imp, imp_d=imp_d, **{"user_param":user_param, "obj":obj, "return_url":"/django/stock_labo/recherche/"})

