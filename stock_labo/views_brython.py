# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from fonction import *
from models import *
from forms import *

@login_required(login_url="/django/utilisateur/login/", redirect_field_name="redirect")
def brython(request):
	user_param = UserPreference.objects.get(user=request.user)
	if str(request.user.username) == "":
		header = Headers(page="Sample Lab", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	elif request.user.first_name == "" and request.user.last_name == "":
		header = Headers(page="Sample Lab", user="%s" %(request.user), panier=len(Contenant.objects.filter(panier_user=request.user)))
	else:
		header = Headers(page="Sample Lab", user="%s-%s_%s" %(request.user.username, request.user.first_name, request.user.last_name[:1]), panier=len(Contenant.objects.filter(panier_user=request.user)))
	onglet = Onglets(request.user)
#	onglet.set_actif_by_id(8)

#	bouton = Boutons()
#	bouton.add_bouton("Panier dans<br/>le stock<br/>personnel", title="Créer un nouvel ingrédient", href="#")
#	bouton.add_bouton("Ranger<br/>le panier<br/>en stock", title="Importer un fichier", href="#")


	return render(request, "stock_labo_brython.html", {"header": header.get_headers(), "onglet" : onglet.get_onglets(), "brython" : True})



#from dajaxice.decorators import dajaxice_register
import json

def ajax_brython(request):
	print "ajax_brython", request.GET["projet"], request.GET["client"], request.GET["client_ka"]

	data = {}
	data.update({"client" : "Hello"})
	return HttpResponse(json.dumps(data), content_type = "application/json")



#from django_websocket import require_websocket
#@require_websocket
#def sample_lab_ws(request):
#    message = request.websocket.wait()
#    request.websocket.send(message)


#from django.http import HttpResponse
#from django_websocket import accept_websocket
#def modify_message(message):
#    return message.lower()
#@accept_websocket
#def sample_lab_ws(request):
#	print dir(request.websocket)
#	if not request.is_websocket():
#		message = request.GET['message']
#		message = modify_message(message)
#		return HttpResponse(message)
#	else:
#		for message in request.websocket:
#			message = modify_message(message)
#			request.websocket.send(message)
