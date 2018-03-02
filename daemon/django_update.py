# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#import pyinotify
#import signal
#import threading
#import shutil
#import posixpath
#import time
import datetime
import sys
import os
import codecs
import traceback
import openpyxl
import types

APPS_PATH = "/var/www/django/last"
if __name__ == '__main__':
	sys.path.insert(0, APPS_PATH)
	os.chdir(APPS_PATH)
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
	import django
	django.setup()

	
import version
from stock_labo.models import Contenant, ContenantStat, Nomenclature, NomenclatureLot, OracleClient
import django.core.exceptions
from lib_linautom.python import mail
from django.contrib.auth.models import Permission, User
from django.conf import settings
from lib_linautom.python import mysql
from django.db import connection
from lib_linautom.python import oracle
from settings_oracle import *

from fonction import print_env, print_ascii, whatisit

print version


def get_client(projet):
	oc = OracleClient.objects.filter(projet=projet)
	if len(oc) == 0:
		return "??"
	else:
		return oc[0].client

def get_client_ka(projet):
	oc = OracleClient.objects.filter(projet=projet)
	if len(oc) == 0:
		return "??"
	else:
		return oc[0].client_ka


def lot_s():
	lot = NomenclatureLot.objects.all()
	for l in lot:
		if l.projet != None and l.projet != "":
			if l.projet.startswith("EUFR") or l.projet.startswith("16-") or l.projet.startswith("17-"):
				print l, l.projet, l.client , l.client_ka
				if l.client == None or l.client == "" or l.client == "??" or l.client == "???":
					#print l.get_client()
					#l.client = l.get_client()
					print get_client(l.projet)
					l.client = get_client(l.projet)
					l.save()
				if l.client_ka == None or l.client_ka == "" or l.client_ka == "??" or l.client_ka == "???":
					#print l.get_client_ka()
					#l.client_ka = l.get_client_ka()
					print get_client_ka(l.projet)
					l.client_ka = get_client_ka(l.projet)
					l.save()
		l.nomenclature_lot_stat()


def cont_s():
	cont_stat = ContenantStat.objects.all()
	contenant_type = ""
	for cs in cont_stat:
		#print "Contenant : ", cs.contenant_code
		contenant_type = ""
		try:
			c = Contenant.objects.get(code=cs.contenant_code)
		except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
			l = NomenclatureLot.objects.filter(code=cs.nomenclature_lot_code)
			if l.count() > 0:
				print "Le lot existe : ", cs.contenant_code
				if l[l.count()-1].responsable_creation != None:
					cs.contenant_responsable_creation_login = l[l.count()-1].responsable_creation.username
					#cs.save()			
					continue
			else:
				print "Plus d'info sur le contenant : ", cs.contenant_code
				continue
		else:
			#print "Le contenant existe : ", cs.contenant_code
			c.responsable_creation = c.nomenclature_lot.responsable_creation
			if c.responsable_creation != None:
				cs.contenant_responsable_creation_login = c.responsable_creation.username
				c.save()
				cs.save()			

def update_oracle_client():
	cursor = connection.cursor()
	cursor.execute("TRUNCATE TABLE `stock_labo_oracleclient`")

	if version.status_developement["oracle"] == "onet_test" or version.status_developement["oracle"] == "onet_prod":
		o=oracle.Oracle()
		param_oracle = version.status_developement["oracle"]
		o.open(**DATABASES_ORACLE[param_oracle])
		querry = "SELECT CUSTNAME as CLIENT, KA as CLIENT_KA, PROJECTNUMBER as PROJET FROM PROJECTS_CUSTOMERS_KA"
		print querry
		oracle_client = o.execute(querry)
		o.close()
		print len(oracle_client)
		for oc in oracle_client:
			c = OracleClient(projet=oc["PROJET"], client=oc["CLIENT"], client_ka=oc["CLIENT_KA"])
			c.save()
	else:
		log_print("!!!!!!!!!!  param oracle inconnu !!!!!!!!!!")
		raise ValueError("!!!!!!!!!!  param oracle inconnu !!!!!!!!!!")

if __name__ == '__main__':

	update_oracle_client()

	#print get_client("15-00381")
	#print get_client_ka("15-00381")

	lot_s()
	cont_s()





