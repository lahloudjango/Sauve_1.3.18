# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from fonction import *
from stock_labo.models import *

@login_required(login_url=r"/django/user/login/", redirect_field_name="redirect")
def ajax_etiquette(request):
	try:
		user_param = UserPreference.objects.get(user=request.user)
		if request.GET["type_etiquette"] == "contenant":
			printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_contenant_imprimante.id)
			imp = Impression.objects.get(pk=user_param.etiquette_contenant.id)
			obj = Contenant.objects.get(pk=request.GET["id"])
		elif request.GET["type_etiquette"] == "nomenclature_lot":
			printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_lot_imprimante.id)
			imp = Impression.objects.get(pk=user_param.etiquette_lot.id)
			obj = NomenclatureLot.objects.get(pk=request.GET["id"])
		elif request.GET["type_etiquette"] == "nomenclature":
			printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_nomenclature_imprimante.id)
			imp = Impression.objects.get(pk=user_param.etiquette_nomenclature.id)
			obj = Nomenclature.objects.get(pk=request.GET["id"])
		#elif request.GET["type_etiquette"] == "login":
		#	printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_login_imprimante.id)
		#	imp = Impression.objects.get(pk=user_param.etiquette_login.id)
		#				obj = Nomenclature.objects.get(pk=request.GET["id"])
		elif request.GET["type_etiquette"] == "emplacement":
			printer = ImpressionImprimante.objects.get(pk=user_param.etiquette_emplacement_imprimante.id)
			imp = Impression.objects.get(pk=user_param.etiquette_emplacement.id)
			obj = Contenant.objects.get(pk=request.GET["id_contenant"])
		else:
			return HttpResponse(json.dumps({"status" : "erreur", "cellule_id" : request.GET["cellule_id"], "info" : "type_etiquette inconnu"}), content_type="application/json")


		imp_d = ImpressionDetail.objects.filter(impression=imp)
		etiquette_print(printer, imp, imp_d, **{"user_param":user_param, "obj":obj })
		time.sleep(2)
		return HttpResponse(json.dumps({"status" : "ok", "cellule_id" : request.GET["cellule_id"]}), content_type="application/json")
	except:
		return HttpResponse(json.dumps({"status" : "erreur", "cellule_id" : request.GET["cellule_id"]}), content_type="application/json")




