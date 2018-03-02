# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from fonction import *
from models import *
from forms import *

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def param_utilisateur(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Utilisateur", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Utilisateur", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Utilisateur", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))
	onglet = Onglets(request.user)
	onglet.set_actif_by_id(5)

	default = {}
	user = request.user

	try:
		user_param = UserPreference.objects.get(user__id=user.id)
		default.update({"username" : user.username})
		default.update({"email" : user.email})
		default.update({"first_name" : user.first_name})
		default.update({"last_name" : user.last_name})

		try:
			default.update({"unit_masse" : user_param.unit_masse.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.unit_masse.id incorrect !!!!")
		try:
			default.update({"site_perso" : user_param.site_perso.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.site_perso.id incorrect !!!!")
		try:
			default.update({"entrepot_perso" : user_param.entrepot_perso.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.entrepot_perso.id incorrect !!!!")
		try:
			default.update({"magasin_perso" : user_param.magasin_perso.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.magasin_perso.id incorrect !!!!")
		try:
			default.update({"emplacement_perso" : user_param.emplacement_perso})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.emplacement_perso.id incorrect !!!!")
		try:
			default.update({"etiquette_contenant" : user_param.etiquette_contenant.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.etiquette_contenant.id incorrect !!!!")
		try:
			default.update({"etiquette_contenant_imprimante" : user_param.etiquette_contenant_imprimante.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.etiquette_contenant_imprimante.id incorrect !!!!")
		try:
			default.update({"etiquette_lot" : user_param.etiquette_lot.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.etiquette_lot.id incorrect !!!!")
		try:
			default.update({"etiquette_lot_imprimante" : user_param.etiquette_lot_imprimante.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.etiquette_lot_imprimante.id incorrect !!!!")
		try:
			default.update({"etiquette_nomenclature" : user_param.etiquette_nomenclature.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.etiquette_nomenclature.id incorrect !!!!")
		try:
			default.update({"etiquette_nomenclature_imprimante" : user_param.etiquette_nomenclature_imprimante.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.etiquette_nomenclature_imprimante.id incorrect !!!!")
		try:
			default.update({"etiquette_login" : user_param.etiquette_login.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.etiquette_login.id incorrect !!!!")
		try:
			default.update({"etiquette_login_imprimante" : user_param.etiquette_login_imprimante.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.etiquette_login_imprimante.id incorrect !!!!")
		try:
			default.update({"etiquette_emplacement" : user_param.etiquette_emplacement.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.etiquette_emplacement.id incorrect !!!!")
		try:
			default.update({"etiquette_emplacement_imprimante" : user_param.etiquette_emplacement_imprimante.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.etiquette_emplacement_imprimante.id incorrect !!!!")
		try:
			default.update({"etiquette_emplacement_machine_flash" : user_param.etiquette_emplacement_machine_flash.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.etiquette_emplacement_machine_flash.id incorrect !!!!")
		try:
			default.update({"etiquette_emplacement_machine_flash_imprimante" : user_param.etiquette_emplacement_machine_flash_imprimante.id})
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			print_ascii("user_param.etiquette_emplacement_machine_flash_imprimante.id incorrect !!!!")
	except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
		user_param = UserPreference(user=user)
		user_param.save()

	if len(request.GET) > 0:
		if request.GET.has_key("annuler"):
			return HttpResponseRedirect("/django/stock_labo/nomenclature/")
		elif request.GET.has_key("valider"):
			default.update({"email" : request.GET["email"]}	)
			default.update({"first_name" : request.GET["first_name"]})
			default.update({"last_name" : request.GET["last_name"]})

			default.update({"unit_masse" : int(request.GET["unit_masse"])})
			default.update({"site_perso" : int(request.GET["site_perso"])})
			default.update({"entrepot_perso" : int(request.GET["entrepot_perso"])})
			default.update({"magasin_perso" : int(request.GET["magasin_perso"])})
			default.update({"emplacement_perso" : request.GET["emplacement_perso"]})
			default.update({"etiquette_contenant" : int(request.GET["etiquette_contenant"])})
			default.update({"etiquette_contenant_imprimante" : int(request.GET["etiquette_contenant_imprimante"])})
			default.update({"etiquette_lot" : int(request.GET["etiquette_lot"])})
			default.update({"etiquette_lot_imprimante" : int(request.GET["etiquette_lot_imprimante"])})
			default.update({"etiquette_nomenclature" : int(request.GET["etiquette_nomenclature"])})
			default.update({"etiquette_nomenclature_imprimante" : int(request.GET["etiquette_nomenclature_imprimante"])})
			default.update({"etiquette_login" : int(request.GET["etiquette_login"])})
			default.update({"etiquette_login_imprimante" : int(request.GET["etiquette_login_imprimante"])})
			default.update({"etiquette_emplacement" : int(request.GET["etiquette_emplacement"])})
			default.update({"etiquette_emplacement_imprimante" : int(request.GET["etiquette_emplacement_imprimante"])})
			default.update({"etiquette_emplacement_machine_flash" : int(request.GET["etiquette_emplacement_machine_flash"])})
			default.update({"etiquette_emplacement_machine_flash_imprimante" : int(request.GET["etiquette_emplacement_machine_flash_imprimante"])})
			default.update({"password" : request.GET["password"]})

			form = UserParamChangeForm(default)
			if form.is_valid():
				user.email = default["email"]
				user.first_name = default["first_name"]
				user.last_name = default["last_name"]
				user_param.unit_masse = UnitMasse.objects.get(id=default["unit_masse"])
				user_param.site_perso = StockSite.objects.get(id=default["site_perso"])
				user_param.entrepot_perso = StockEntrepot.objects.get(id=default["entrepot_perso"])
				user_param.magasin_perso = StockMagasin.objects.get(id=default["magasin_perso"])
				user_param.emplacement_perso = default["emplacement_perso"]
				user_param.etiquette_contenant = Impression.objects.get(id=default["etiquette_contenant"])
				user_param.etiquette_contenant_imprimante = ImpressionImprimante.objects.get(id=default["etiquette_contenant_imprimante"])
				user_param.etiquette_lot = Impression.objects.get(id=default["etiquette_lot"])
				user_param.etiquette_lot_imprimante = ImpressionImprimante.objects.get(id=default["etiquette_lot_imprimante"])
				user_param.etiquette_nomenclature = Impression.objects.get(id=default["etiquette_nomenclature"])
				user_param.etiquette_nomenclature_imprimante = ImpressionImprimante.objects.get(id=default["etiquette_nomenclature_imprimante"])
				user_param.etiquette_login = Impression.objects.get(id=default["etiquette_login"])
				user_param.etiquette_login_imprimante = ImpressionImprimante.objects.get(id=default["etiquette_login_imprimante"])
				user_param.etiquette_emplacement = Impression.objects.get(id=default["etiquette_emplacement"])
				user_param.etiquette_emplacement_imprimante = ImpressionImprimante.objects.get(id=default["etiquette_emplacement_imprimante"])
				user_param.etiquette_emplacement_machine_flash = Impression.objects.get(id=default["etiquette_emplacement_machine_flash"])
				user_param.etiquette_emplacement_machine_flash_imprimante = ImpressionImprimante.objects.get(id=default["etiquette_emplacement_machine_flash_imprimante"])

				user.save()
				user_param.save()

				log = django_models.LogEntry()
				log.action_time = datetime.datetime.now()											#La date et l’heure de l’action.
				log.user = request.user																#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
				log.content_type = ContentType.objects.get(app_label="auth", model="user".lower())	#Le type de contenu (ContentType) de l’objet modifié.
				log.object_id = user.id																#La représentation textuelle de la clé primaire de l’objet modifié.
				log.object_repr = unicode(user)														#La représentation repr() de l’objet après sa modification.
				log.action_flag = django_models.CHANGE 													#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
				log.change_message = "param_utilisateur"											#Description de la modification
				log.save()
				log = django_models.LogEntry()
				log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
				log.user = request.user																				#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
				log.content_type = ContentType.objects.get(app_label="stock_labo", model="UserPreference".lower())	#Le type de contenu (ContentType) de l’objet modifié.
				log.object_id = user_param.id																		#La représentation textuelle de la clé primaire de l’objet modifié.
				log.object_repr = unicode(user_param)																#La représentation repr() de l’objet après sa modification.
				log.action_flag = django_models.CHANGE 																	#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
				log.change_message = "param_utilisateur"															#Description de la modification
				log.save()
				return HttpResponseRedirect("/django/stock_labo/nomenclature/")

		elif request.GET.has_key("print_login"):
			printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_login_imprimante.id)
			imp = Impression.objects.get(pk=user_param.etiquette_login.id)
			imp_d = ImpressionDetail.objects.filter(impression=imp)
			class ObjClass(object):
				def init(self):
					self.code_cb = ":".join(("001", user_param.user.username, request.GET["password"]))
			obj = ObjClass()
			obj.init()
			return etiquette_print(printer, imp=imp, imp_d=imp_d, **{"user_param":user_param, "obj":obj, "return_url":"/django/stock_labo/param_utilisateur/"})


	form = UserParamChangeForm(default)
	return render(request, "stock_labo_param_utilisateur.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "form" : form})
