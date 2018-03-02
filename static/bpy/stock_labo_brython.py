
#import time
from browser import window, document, html, document, ajax, alert, timer
import json
#from browser import websocket

idtimer = 1

def make_addr_param(*args):
	param = {}
	for a in args:
		param.update(a)
	add = "?"
	for p in param:
		add += "%s=%s&" %(p, param[p])
	return add[:-1]

def on_receipt(reponse):
	r = json.loads(reponse.text)
	document["data2"].value = r["client"]

def on_data1_input():
	global idtimer
	timer.clear_timeout(idtimer)
	idtimer = timer.set_timeout(on_recherche_click, 1500)
	
def on_recherche_click():
	ba = ajax.ajax()
	ba.bind('complete',on_receipt)
	#ba.open('POST',url,True)
	#ba.set_header('content-type','application/x-www-form-urlencoded')
	#ba.send({'x':0, 'y':1})

	param_get = make_addr_param({"projet" : "", "client" : document['data1'].value, "client_ka" : ""})
	ba.open("GET", "/django/stock_labo/brython/ajax_brython/"+param_get, True)
	ba.set_header("content-type", "application/x-www-form-urlencoded")
	ba.send()

document["recherche"].bind("click", on_recherche_click)
document["data1"].bind("blur", on_recherche_click)
document["data1"].bind("input", on_data1_input)
