# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from fonction import *
from models import *
from forms import *

import json


@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def sample_lab(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Sample Lab", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Sample Lab", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Sample Lab", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))
	onglet = Onglets(request.user)
	onglet.set_actif_by_id(8)
	info = {}
	default = {}
	verification = False

#	bouton = Boutons()
#	bouton.add_bouton("Panier dans<br/>le stock<br/>personnel", title="Créer un nouvel ingrédient", href="#")
#	bouton.add_bouton("Ranger<br/>le panier<br/>en stock", title="Importer un fichier", href="#")
	if len(request.GET) > 0:
		if request.GET.has_key("valider"):
			verification = True

			if request.GET["date_realisation"] == None or request.GET["date_realisation"] == "":
				default.update({"date_realisation":datetime.date.today()})
			else:
				try:
					default.update({"date_realisation":datetime.datetime.strptime(request.GET["date_realisation"],"%d/%m/%Y")})
				except:
					info.update({"erreur":"date incorrecte"})
					verification = False
			default.update({"responsable":User.objects.get(pk=request.GET["responsable"])})
			default.update({"nbr_echantillon":int(request.GET["nbr_echantillon"])})
			default.update({"type_demande":int(request.GET["type_demande"])})

			if request.GET["projet"] != None and request.GET["projet"] != "":
				o_info_projet = get_oracle_info(client=request.GET["client"], client_ka=request.GET["client_ka"], projet=request.GET["projet"], group_by="projet", exact=True)
				if len(o_info_projet) == 1:
					default.update({"projet":o_info_projet[0]["PROJET"]})
				elif len(o_info_projet) > 1:
					verification = False
					info.update({"erreur":"Les critères Projet Client ont donnés plus d'un résultat pour le projet"})
				else:
					verification = False
					info.update({"erreur":"Les critères Projet Client ont donnés aucun résultat pour le projet"})
			else:
				default.update({"projet":""})
			if request.GET["client"] != None and request.GET["client"] != "":
				o_info_client = get_oracle_info(client=request.GET["client"], client_ka=request.GET["client_ka"], projet=request.GET["projet"], group_by="client", exact=True)
				if len(o_info_client) == 1:
					default.update({"client":o_info_client[0]["CLIENT"]})
				elif len(o_info_client) > 1:
					verification = False
					info.update({"erreur":"Les critères Projet Client ont donnés plus d'un résultat pour le client"})
				else:
					verification = False
					info.update({"erreur":"Les critères Projet Client ont donnés aucun résultat pour le client"})
			else:
				default.update({"client":""})

			if request.GET["client_ka"] != None and request.GET["client_ka"] != "":
				o_info_client_ka = get_oracle_info(client=request.GET["client"], client_ka=request.GET["client_ka"], projet=request.GET["projet"], group_by="client_ka", exact=True)
				if len(o_info_client_ka) == 1:
					default.update({"client_ka":o_info_client_ka[0]["CLIENT_KA"]})
				elif len(o_info_client_ka) > 1:
					verification = False
					info.update({"erreur":"Les critères Projet Client ont donnés plus d'un résultat pour le client ka"})
				else:
					verification = False
					info.update({"erreur":"Les critères Projet Client ont donnés aucun résultat pour le client ka"})
			else:
				default.update({"client_ka":""})



			if default["responsable"] == "":
				verification = False
			if default["nbr_echantillon"] == "":
				verification = False
			if default["type_demande"] == "":
				verification = False

			if request.GET.has_key("valider") and verification == True:
				sample = SampleLabStat()

				sample.projet = default["projet"]
				sample.client = default["client"]
				sample.client_ka = default["client_ka"]
				sample.date_realisation = default["date_realisation"]
				sample.responsable = default["responsable"]
				sample.nbr_echantillon = default["nbr_echantillon"]
				sample.type_demande = default["type_demande"]
				sample.save()

				info.update({"info":"Enregistrement de %s %s pour %s" %(default["nbr_echantillon"], SampleLabStat.TYPE_DEMANDE[default["type_demande"]], default["client"])})

				default = {}



	if not default.has_key("date_realisation") or default["date_realisation"] == None or default["date_realisation"] == "":
		default.update({"date_realisation":datetime.date.today()})
	if not default.has_key("responsable") or default["responsable"] == None or default["responsable"] == "":
		default.update({"responsable":request.user.id})

	sample_lab_form = SampleLabForm(default)
#	whatisit(sample_lab_form.base_fields["type_demande"])
	#print verification
	return render(request, "stock_labo_sample_lab.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "brython" : None, "form" : sample_lab_form, "info" : info})

def ajax_sample_lab_projet(request):
	data = get_oracle_info(projet = request.GET["projet"], group_by="projet", limit = 25)
	return HttpResponse(json.dumps(data), content_type = "application/json")

def ajax_sample_lab_client(request):
	data = get_oracle_info(client = request.GET["client"], projet = request.GET["projet"], group_by="client", limit = 25)
	return HttpResponse(json.dumps(data), content_type = "application/json")

def ajax_sample_lab_client_ka(request):
	data = get_oracle_info(client = request.GET["client"], client_ka = request.GET["client_ka"], projet = request.GET["projet"], group_by="client_ka", limit = 25)
	return HttpResponse(json.dumps(data), content_type = "application/json")



