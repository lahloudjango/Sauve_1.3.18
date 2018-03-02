# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from fonction import *
from models import *
from forms import *
from django.conf import settings
from lib_linautom.python import mysql


@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def log(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Log", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Log", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Log", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))
	onglet = Onglets(request.user)
	onglet.set_actif_by_id(10)
#	bouton = Boutons()
#	bouton.add_bouton("Panier dans<br/>le stock<br/>personnel", title="Créer un nouvel ingrédient", href="#")
#	bouton.add_bouton("Ranger<br/>le panier<br/>en stock", title="Importer un fichier", href="#")


	rech_def = {}
	if request.GET.has_key("limit_du"):
		rech_def.update({"limit_du":int(request.GET["limit_du"])})
	else:
		rech_def.update({"limit_du":0})
	if request.GET.has_key("limit_au"):
		rech_def.update({"limit_au":int(request.GET["limit_au"])})
	else:
		rech_def.update({"limit_au":100})
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

	if request.GET.has_key("contenant_code"):
		rech_def.update({"contenant_code":request.GET["contenant_code"]})
	if request.GET.has_key("nomenclature_lot_code"):
		rech_def.update({"nomenclature_lot_code":request.GET["nomenclature_lot_code"]})
	if request.GET.has_key("nomenclature_code"):
		rech_def.update({"nomenclature_code":request.GET["nomenclature_code"]})
	if request.GET.has_key("nomenclature_description"):
		rech_def.update({"nomenclature_description":request.GET["nomenclature_description"]})
	recherche_log_form = RechercheLogForm(initial=rech_def)

	if len(request.GET) > 0:
		my=mysql.Mysql()
		my.open(mysql_host=settings.DATABASES["default"]["HOST"], mysql_port=int(settings.DATABASES["default"]["PORT"]), mysql_user=settings.DATABASES["default"]["USER"], mysql_password=settings.DATABASES["default"]["PASSWORD"] )

		querry = """
		SELECT action_time,
			username,
			object_repr,
			action_flag,
			first_name,
			last_name,
			change_message
		FROM %s.django_admin_log
		LEFT JOIN %s.auth_user ON django_admin_log.user_id = auth_user.id
		LEFT JOIN %s.stock_labo_contenant ON django_admin_log.object_id = stock_labo_contenant.id
		LEFT JOIN %s.stock_labo_nomenclaturelot ON stock_labo_contenant.nomenclature_lot_id = stock_labo_nomenclaturelot.id
		LEFT JOIN %s.stock_labo_nomenclature ON stock_labo_nomenclaturelot.nomenclature_id = stock_labo_nomenclature.id
		WHERE content_type_id = 24""" %(settings.DATABASES["default"]["NAME"],
										settings.DATABASES["default"]["NAME"],
										settings.DATABASES["default"]["NAME"],
										settings.DATABASES["default"]["NAME"],
										settings.DATABASES["default"]["NAME"])


		"""
		class LogEntryContenant(models.Model):
			action_time = models.DateTimeField(_('action time'), auto_now=True)
			user = models.ForeignKey(settings.AUTH_USER_MODEL)
			content_type = models.ForeignKey(ContentType, blank=True, null=True)
			object_id = models.TextField(_('object id'), blank=True, null=True)
			object_repr = models.CharField(_('object repr'), max_length=200)
			action_flag = models.PositiveSmallIntegerField(_('action flag'))
			change_message = models.TextField(_('change message'), blank=True)
		"""

		if rech_def.has_key("contenant_code") and rech_def["contenant_code"] != "":
			querry += " and stock_labo_contenant.code LIKE \"%%%s%%\"" %(rech_def["contenant_code"])
		if rech_def.has_key("nomenclature_lot_code") and rech_def["nomenclature_lot_code"] != "":
			querry += " and stock_labo_nomenclaturelot.code LIKE \"%%%s%%\"" %(rech_def["nomenclature_lot_code"])
		if rech_def.has_key("nomenclature_code") and rech_def["nomenclature_code"] != "":
			querry += " and stock_labo_nomenclature.code LIKE \"%%%s%%\"" %(rech_def["nomenclature_code"])
		if rech_def.has_key("nomenclature_description") and rech_def["nomenclature_description"] != "":
			querry += " and stock_labo_nomenclature.description LIKE \"%%%s%%\"" %(rech_def["nomenclature_description"])

		ing = my.execute(querry)
		my.close()

		list1 = Liste(caption="Historique - Log", summary="Historique - Log")

		list1.liste.update({"n_ligne_total" : django_models.LogEntry.objects.all().count()})

		list1.liste.update({"n_ligne_affiche" : len(ing)})
		ing = ing[rech_def["limit_du"]:rech_def["limit_au"]]
		list1.liste.update({"n_ligne_limit" : len(ing)})

		l = Liste.Ligne()
		l.add_cellule("Date", title="Date de l'action", width="120px")
		l.add_cellule("Utilisateur", title="Origine de l'action", width="80px")
		l.add_cellule("Objet", title="Objet sible de l'action")
		l.add_cellule("Action", width="100px")
		l.add_cellule("Commentaire", width="15%")
		list1.add_headers(l.get_ligne())

		dic_status = {django_models.ADDITION:"Création",django_models.CHANGE:"Modification",django_models.DELETION:"Destruction"}

		for i in ing:
			l = Liste.Ligne()
			l.add_cellule(i["action_time"])
			l.add_cellule(i["username"])
			l.add_cellule(i["object_repr"])
			l.add_cellule(dic_status[i["action_flag"]])
			l.add_cellule(i["change_message"])

			list1.add_ligne(l.get_ligne())

	else:
		list1 = Liste(caption="Historique - Log", summary="Historique - Log")
		list1.liste["p"] = False

	return render(request, "stock_labo_log.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "brython" : False, "recherche_log_form" : recherche_log_form, "list" : list1.get_liste()})

