# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#import pyinotify
#import signal
#import threading
#import shutil
#import posixpath
#import time
from django.utils import timezone
import datetime
import sys
import os
import codecs
import traceback
#import openpyxl
import types

	
APPS_PATH = "/var/www/django/prod"
if __name__ == '__main__':
	sys.path.insert(0, APPS_PATH)
	os.chdir(APPS_PATH)
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
	import django
	django.setup()

#print sys.path
import version
#print version.status_developement

from stock_labo.models import Nomenclature, NomenclatureType
from lib_linautom.python import mail
from django.contrib.auth.models import Permission, User
from django.conf import settings
#from lib_linautom.python import mysql
#from lib_linautom.python import oracle
from settings_oracle import *

from fonction import print_env, print_ascii, whatisit, log_auto

if version.status_developement["data"] == "prod":
	fichier_log = "/var/log/django_collection_prod.log"
else:
	fichier_log = "/var/log/django_collection_dev.log"


#Affichage des log sur la console
console = False
console = True

class DossierInconnu(Exception):
	"""
	Le dossier est inconnu
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		print_ascii(__doc__)

def log_print(*text):
	"""
	Fonction de login automatique
	"""
	f_log = codecs.open(fichier_log, "a", encoding="utf-8")
	d = datetime.datetime.now().strftime("%a, %Y-%m-%d %X ")
	for t in text:
		if console == True:
			print_ascii(t)
		l = d + unicode(t) + "\n"
		f_log.writelines(l)
	f_log.close()


def get_collection():
	if version.status_developement["oracle"] == "onet_test" or version.status_developement["oracle"] == "onet_prod":
		o=oracle.Oracle()
		param_oracle = version.status_developement["oracle"]
		o.open(**DATABASES_ORACLE[param_oracle])
		querry = "SELECT PERFUMERCODE FROM PT_COLLECTIONS_DISTINCT"
		oracle_client = o.execute(querry)
		o.close()
		code_collection = [c["PERFUMERCODE"] for c in oracle_client]
		return code_collection
	else:
		log_print("!!!!!!!!!!  param oracle inconnu !!!!!!!!!!")
		raise ValueError("!!!!!!!!!!  param oracle inconnu !!!!!!!!!!")

def check_collection():
	user = User.objects.get(username="script")
	ing = Nomenclature.objects.all()
	col_plus = 0
	col_moins = 0
	log = []
	for i in ing:
		if i.code in code_collection:
			if i.collection == False:
				log.append("%18s : Collection" %(i.code))
				col_plus += 1
			i.set_collection(user)
		else:
			if i.collection == True:
				log.append("%18s : PAS collection" %(i.code))
				col_moins += 1
			i.reset_collection(user)
	log_print(*log)
	log_print("Article ENTREE en collection : %d" %(col_plus))
	log_print("Article SORTIE de collection : %d" %(col_moins))
	return



if __name__ == '__main__':
	user = User.objects.get(username="script")


	code_collection = get_collection()
	log_print("Nombre d'article collection : %d" %(len(code_collection)))
	check_collection()
	log = []
	a = 0
	n_type = NomenclatureType.objects.get(code="C")
	for c in code_collection:
		n = Nomenclature.objects.filter(code=c)
		if n.count() == 0:
			z = n_type.add_nomenclature(code=c, date_creation=datetime.date.today(), update=True, insert=True)
			log_auto(user, z, "a", "django_collection")
			z.set_collection(user)
			log.append("%s : Article inconnu" %(c))
			a += 1
	log_print(*log)
	log_print("Nombre d'article collection inconnu : %d" %(a))


	pass


