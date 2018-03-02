
#import time
from browser import window, document, html, document, ajax, alert, timer
import json
#from browser import websocket
from jqueryui import jq

idtimer = 1
list_projet = []

def make_addr_param(*args):
	param = {}
	for a in args:
		param.update(a)
	add = "?"
	for p in param:
		add += "%s=%s&" %(p, param[p])
	return add[:-1]


def id_projet_on_input_ajax():
	ba = ajax.ajax()
	ba.bind('complete',id_projet_on_input_on_receipt)
	#ba.open('POST',url,True)
	#ba.set_header('content-type','application/x-www-form-urlencoded')
	#ba.send({'x':0, 'y':1})

	param_get = make_addr_param({"projet" : document["id_projet"].value})
	ba.open("GET", "/django/stock_labo/ajax_sample_lab_projet" + param_get, True)
	ba.set_header("content-type", "application/x-www-form-urlencoded")
	ba.send()

def id_projet_on_input():
	global idtimer
	timer.clear_timeout(idtimer)
	idtimer = timer.set_timeout(id_projet_on_input_ajax, 1500)
	
def id_projet_on_input_on_receipt(reponse):
	global list_projet
	list_projet = json.loads(reponse.text)
	jq['id_projet'].autocomplete(source=list_projet)

document["id_projet"].bind("input", id_projet_on_input)
document["id_projet"].bind("blur", id_projet_on_input_ajax)

#jq["id_date_realisation"].datepicker(showButtonPanel=True)
