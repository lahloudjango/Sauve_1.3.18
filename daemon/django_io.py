#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pyinotify
import datetime
import time
import posixpath
import traceback
import sys
import os
import signal
import threading
import shutil
import codecs
from django.db import connection

APPS_PATH = "/var/www/django/prod"
#APPS_PATH = "/media/gonteroc/charly/takasago/02003_stock_labo_paris/django/1.0.3"
if __name__ == '__main__':
	sys.path.insert(0, APPS_PATH)
	os.chdir(APPS_PATH)
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
	import django
	django.setup()

import stock_labo.models
from lib_linautom.python import mail
import version

from fonction import print_env, print_ascii, whatisit, multi_file_backups

dossier_import_navette_sap = "/mnt/sto-srv-files/sap/P01/CDENAV/"
dossier_import_solution_vincent = "/mnt/sto-srv-files/sap/P01/CDENAV/solution"
dossier_import_generic = "/mnt/sto-srv-files/sap/P01/CDENAV/generic"
if version.status_developement["data"] == "prod":
	fichier_log = "/var/log/django_io_prod.log"
else:
	fichier_log = "/var/log/django_io_dev.log"


#dossier_import_navette_sap = "/tmp/django"
#dossier_import_solution_vincent = "/tmp/django/solution"
#dossier_import_generic = "/tmp/django/generic"
#fichier_log = "/tmp/django_io.log"

#Affichage des log sur la console
console = False
#console = True


class DossierInconnu(Exception):
	"""
	Le dossier est inconnu
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		print_ascii(__doc__)
class ImportationErreur(Exception):
	"""
	Le thread d'importation à généré une erreur
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		print_ascii(__doc__)
class KillTread(Exception):
	"""
	Le thread d'importation à généré une erreur
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

def test_print(i):
	if i.wd == 1:
		print_ascii("Importation " + i)
		whatisit(i.wd)
	else:
		log_print("rien n'a faire, événement d'un dossier fils wd : %d" %(i.wd), i)

def gestion_importation_sap(event):
	try:
		if event.wd == 1:
			if event.name.endswith(".csv") or event.name.endswith(".CSV"):
				log_print("Importation " + event.pathname)
				err = stock_labo.models.import_navette_sap(emplacement=event.pathname, nom="", extension="", fin_de_ligne="\r\n")
				if err == "":
					multi_file_backups(event.path+"/backup/", event.name[:-4]+".ok")
					shutil.move(event.pathname, event.path+"/backup/"+event.name[:-4]+".ok")
				else:
					multi_file_backups(event.path+"/error/", event.name[:-4]+".err")
					multi_file_backups(event.path+"/error/", event.name[:-4]+".log")
					shutil.move(event.pathname, event.path+"/error/"+event.name[:-4]+".err")
					ferr = codecs.open(event.path+"/error/"+event.name[:-4]+".log", "w", encoding="utf-8")
					ferr.writelines(err)
					ferr.close()

					mail_corps = "Le fichier %s a provoqué une erreur : \n\n" %(event.name)
					ferr = codecs.open(event.path+"/error/"+event.name[:-4]+".err", "r", encoding="utf-8")
					mail_corps += ferr.readline()
					ferr.close()
					mail_corps += "\n\n"
					mail_corps = "Le fichier %s a provoqué une erreur : \n\n" %(event.name)
					ferr = codecs.open(event.path+"/error/"+event.name[:-4]+".log", "r", encoding="utf-8")
					mail_corps += ferr.readline()
					ferr.close()
					m = mail.Mail(mail_corps)
					m.from_("Application_stockparis@takasago.com")
					m.reply_to("charly.gontero@linautom.fr")
					#m.to(["charly.gontero@linautom.fr","yanick_soufflet@takasago.com"])
					m.to(["charly.gontero@linautom.fr","TEPL-IT@takasago.com"])
					if version.status_developement["data"] == "prod":
						m.subject("Stock Labo Paris, Erreur importation fichier navette SAP")
					else:
						m.subject("Ne pas tenir compte de cette email, je fait des tests sur le serveur, charly")
					#m.send("smtp.laposte.net", "charly.gontero@laposte.net", "charly.gontero", "1Addyson")
					m.send(smtp="par-srv-cas01.eu.takasago.com", expediteur="Application_stockparis@takasago.com", user=None , password=None, starttls=False)
				connection_db_ouverte = True
			else:
				shutil.move(event.pathname, event.path+"/error/"+event.name)
				log_print("rien n'a faire, le fichier n'a pas la bonne extention : %s" %(event.name))
		else:
			log_print("rien n'a faire, événement d'un dossier fils wd : %d" %(event.wd))
	except:
		tb = traceback.format_exc()
		log_print("!!!!! ERREUR !!!!!")
		log_print(tb)
		log_print("!!!!! ERREUR !!!!!\n\n")
		raise ImportationErreur

def gestion_importation_vincent(event):
	try:
		if event.wd == 1:
			if event.name.endswith(".csv") or event.name.endswith(".CSV"):
				log_print("Importation " + event.pathname)
				err = stock_labo.models.import_solution_vincent(emplacement=event.pathname, nom="", extension="", fin_de_ligne="\r\n")
				if err == "":
					shutil.move(event.pathname, event.path+"/backup/"+event.name[:-4]+".ok")
				else:
					shutil.move(event.pathname, event.path+"/error/"+event.name[:-4]+".err")
					ferr = codecs.open(event.path+"/error/"+event.name[:-4]+".log", "w", encoding="utf-8")
					ferr.writelines(err)
					ferr.close()

					mail_corps = "Le fichier %s a provoqué une erreur : \n\n" %(event.name)
					ferr = codecs.open(event.path+"/error/"+event.name[:-4]+".err", "r", encoding="utf-8")
					mail_corps += ferr.readline()
					ferr.close()
					mail_corps += "\n\n"
					mail_corps = "Le fichier %s a provoqué une erreur : \n\n" %(event.name)
					ferr = codecs.open(event.path+"/error/"+event.name[:-4]+".log", "r", encoding="utf-8")
					mail_corps += ferr.readline()
					ferr.close()
					m = mail.Mail(mail_corps)
					m.from_("Application_stockparis@takasago.com")
					m.reply_to("charly.gontero@linautom.fr")
					#m.to(["charly.gontero@linautom.fr","yanick_soufflet@takasago.com"])
					m.to(["charly.gontero@linautom.fr","TEPL-IT@takasago.com"])
					if version.status_developement["data"] == "prod":
						m.subject("Stock Labo Paris, Erreur importation fichier solution vincent")
					else:
						m.subject("Ne pas tenir compte de cette email, je fait des tests sur le serveur, charly")
					#m.send("smtp.laposte.net", "charly.gontero@laposte.net", "charly.gontero", "1Addyson")
					m.send(smtp="par-srv-cas01.eu.takasago.com", expediteur="Application_stockparis@takasago.com", user=None , password=None, starttls=False)
				connection_db_ouverte = True
			else:
				shutil.move(event.pathname, event.path+"/error/"+event.name)
				log_print("rien n'a faire, le fichier n'a pas la bonne extention : %s" %(event.name))
		else:
			log_print("rien n'a faire, événement d'un dossier fils wd : %d" %(event.wd))
	except:
		tb = traceback.format_exc()
		log_print("!!!!! ERREUR !!!!!")
		log_print(tb)
		log_print("!!!!! ERREUR !!!!!\n\n")
		raise ImportationErreur

def gestion_importation_generic(event):
	try:
		if event.wd == 1:
			if event.name.endswith(".csv") or event.name.endswith(".CSV"):
				log_print("Importation " + event.pathname)
				err = stock_labo.models.import_generic(emplacement=event.pathname, nom="", extension="", fin_de_ligne="\r\n")
				if err == "":
					shutil.move(event.pathname, event.path+"/backup/"+event.name[:-4]+".ok")
				else:
					shutil.move(event.pathname, event.path+"/error/"+event.name[:-4]+".err")
					ferr = codecs.open(event.path+"/error/"+event.name[:-4]+".log", "w", encoding="utf-8")
					ferr.writelines(err)
					ferr.close()

					mail_corps = "Le fichier %s a provoqué une erreur : \n\n" %(event.name)
					ferr = codecs.open(event.path+"/error/"+event.name[:-4]+".err", "r", encoding="utf-8")
					mail_corps += ferr.readline()
					ferr.close()
					mail_corps += "\n\n"
					mail_corps = "Le fichier %s a provoqué une erreur : \n\n" %(event.name)
					ferr = codecs.open(event.path+"/error/"+event.name[:-4]+".log", "r", encoding="utf-8")
					mail_corps += ferr.readline()
					ferr.close()
					m = mail.Mail(mail_corps)
					m.from_("Application_stockparis@takasago.com")
					m.reply_to("charly.gontero@linautom.fr")
					#m.to(["charly.gontero@linautom.fr","yanick_soufflet@takasago.com"])
					m.to(["charly.gontero@linautom.fr","TEPL-IT@takasago.com"])
					if version.status_developement["data"] == "prod":
						m.subject("Stock Labo Paris, Erreur importation fichier générique")
					else:
						m.subject("Ne pas tenir compte de cette email, je fait des tests sur le serveur, charly")
					#m.send("smtp.laposte.net", "charly.gontero@laposte.net", "charly.gontero", "1Addyson")
					m.send(smtp="par-srv-cas01.eu.takasago.com", expediteur="Application_stockparis@takasago.com", user=None , password=None, starttls=False)
				connection_db_ouverte = True
			else:
				shutil.move(event.pathname, event.path+"/error/"+event.name)
				log_print("rien n'a faire, le fichier n'a pas la bonne extention : %s" %(event.name))
		else:
			log_print("rien n'a faire, événement d'un dossier fils wd : %d" %(event.wd))
	except:
		tb = traceback.format_exc()
		log_print("!!!!! ERREUR !!!!!")
		log_print(tb)
		log_print("!!!!! ERREUR !!!!!\n\n")
		raise ImportationErreur

class EventHandlerModel(pyinotify.ProcessEvent):
	"""
	Class model avec tout les evenement"
	"""
	def process_IN_ACCESS(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_ATTRIB(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_CLOSE_NOWRITE(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_CLOSE_WRITE(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_CREATE(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_DELETE(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_DELETE_SELF(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_DONT_FOLLOW(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_EXCL_UNLINK(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_IGNORED(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_ISDIR(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_MASK_ADD(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_MODIFY(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_MOVED_FROM(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_MOVED_TO(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_MOVE_SELF(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_ONESHOT(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_ONLYDIR(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_OPEN(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_Q_OVERFLOW(self, event):
		log_print("Event:", datetime.datetime.now(), event)

	def process_IN_UNMOUNT(self, event):
		log_print("Event:", datetime.datetime.now(), event)


class EventHandlerImport(EventHandlerModel):
	"""
	On redéfini la class model pour ajouter l'appel de fonction sur les événements retenu
	"""
	def __init__(self, fonction):
		self.fonction = fonction

	def process_IN_CLOSE_WRITE(self, event):
		log_print("Event:", event)
		self.fonction(event)
	def process_IN_MOVED_TO(self, event):
		log_print("Event:", event)
		self.fonction(event)


class ImportThreadTest(threading.Thread):
	"""
	Class de test de gestion multi-tread
	"""
	def __init__(self, nom, dossier, fonction):
		threading.Thread.__init__(self)
		self.nom = nom
		self._stopevent = threading.Event()

	def run(self):
		i = 0
		while not self._stopevent.isSet():
			log_print(self.nom, i)
			i += 1
			self._stopevent.wait(2.0)

	def stop(self):
		self._stopevent.set()


class ImportThread(threading.Thread):
	"""
	Class de definissant les tread d'importation
	"""
	def __init__(self, nom, dossier, fonction):
		threading.Thread.__init__(self)
		self.nom = nom
		self.stop_notifer_loop = False
		self.exception = None
		if posixpath.exists(dossier):
			if not(posixpath.exists(dossier + "/backup")):
				os.mkdir(dossier + "/backup")
			if not(posixpath.exists(dossier + "/error")):
				os.mkdir(dossier + "/error")
			self.dossier = dossier
		else:
			log_print("Dossier dossier_import_navette_sap : %s inconnu" %(dossier_import_navette_sap))
			raise DossierInconnu()
		# watch manager
#		self.flag_on = pyinotify.ALL_EVENTS
		self.flag_on = pyinotify.IN_CLOSE_WRITE|pyinotify.IN_MOVED_TO
		self.wm = pyinotify.WatchManager()
		self.wdd = self.wm.add_watch(self.dossier, self.flag_on, rec=True)

		# event handler
		log_print("importation %s démarré" %(self.nom))
		self.eh = EventHandlerImport(fonction)

		# notifier
		self.notifier = pyinotify.Notifier(self.wm, self.eh)

	def run(self):
		try:
			self.notifier.loop(callback=self.stop_notifer)
		except:
			self.exception = sys.exc_info()
	def stop_notifer(self, context):
		return self.stop_notifer_loop

	def stop_loop(self):
		log_print("stop_notifer_loop")
		self.stop_notifer_loop = True
		log_print("rm_watch")
		self.wm.rm_watch(self.wdd.values())
		time.sleep(1)
		self.exception = KillTread

	def wait_for_exc_info(self):
		return self.__status_queue.get()

	def join_with_exception(self):
		if self.exception == None:
			return None
		else:
			log_print(self.exception)
			raise ImportationErreur

def arret_importation(imp_dic):
	"""
	Fonction d'arrêt des tread d'importation
	"""
	for i in imp_dic.keys():
		log_print("Thread importation %s arrête en cours" %(imp_dic[i]["nom"]))
		log_print("stop_loop")
		imp_dic[i]["thread"].stop_loop()
		log_print("join")
		imp_dic[i]["thread"].join()
		log_print("Thread importation %s arrêté" %(imp_dic[i]["nom"]))


def sig_iterrupt(signal, frame):
	"""
	Gestionnaire d'interruption
	"""
	log_print("Arrêt des thread d'importation")
#	arret_importation(frame.f_locals["imp"])
#	time.sleep(1)
#	log_print("Importation stoppée")
#	whatisit(frame.f_locals["sig"])
	frame.f_locals["sig"]["stop"] = True
#	whatisit(frame.f_locals["sig"])
	log_print("Arret en cours")

class MyEvent(object):
	dir=False 
	mask=0x8 
	maskname="IN_CLOSE_WRITE"
	name=""
	path=""
	pathname=""
	wd=1

def main():
	signal.signal(signal.SIGINT, sig_iterrupt)
	connection_db_ouverte = False
	try:
		imp = {}
		i = {}
		imp.update({"sap" : i})
		i.update({"nom": "Navette SAP"})
		i.update({"dossier": dossier_import_navette_sap})
		i.update({"fonction": gestion_importation_sap})
		i.update({"thread": ImportThread(nom=imp["sap"]["nom"], dossier=imp["sap"]["dossier"], fonction=imp["sap"]["fonction"])})
		imp["sap"]["thread"].start()

		i = {}
		imp.update({"vincent" : i})
		i.update({"nom": "Solution Vincent"})
		i.update({"dossier": dossier_import_solution_vincent})
		i.update({"fonction": gestion_importation_vincent})
		i.update({"thread": ImportThread(nom=imp["vincent"]["nom"], dossier=imp["vincent"]["dossier"], fonction=imp["vincent"]["fonction"])})
		imp["vincent"]["thread"].start()

		i = {}
		imp.update({"generic" : i})
		i.update({"nom": "Fichier generic"})
		i.update({"dossier": dossier_import_generic})
		i.update({"fonction": gestion_importation_generic})
		i.update({"thread": ImportThread(nom=imp["generic"]["nom"], dossier=imp["generic"]["dossier"], fonction=imp["generic"]["fonction"])})
		imp["generic"]["thread"].start()

		sig = {}
		sig.update({"stop": False})


		while sig["stop"] == False:
			for i in imp.keys():
				imp[i]["thread"].join_with_exception()
				list_fichier = os.listdir(imp[i]["dossier"])
				if len(list_fichier) > 2:
					for f in list_fichier:
						print_ascii(f)
						if os.path.isfile(os.path.join(imp[i]["dossier"],f)):
							log_print(":-( Fichier sans signal dans %s: %s" %(imp[i]["nom"], f))
							e = MyEvent()
							e.name=f
							e.path=imp[i]["dossier"]
							e.pathname=os.path.join(imp[i]["dossier"],f)
							imp[i]["fonction"](e)
							connection_db_ouverte = True
							time.sleep(2)
#							break
			if connection_db_ouverte == True:
				log_print("Fermeture de la connection sur la base de donnée")
				connection.close()
				connection_db_ouverte = False
			time.sleep(300)
		connection.close()
		arret_importation(imp)


	except:
		tb = traceback.format_exc()
		log_print("!!!!! ERREUR !!!!!")
		log_print(tb)
		log_print("!!!!! ERREUR !!!!!\n\n")
		log_print("Erreur => arrêt deamon")

		mail_corps = "Le daemon d'importation des fichier à craché\nToutes les importations sont stoppé\n\n"
		mail_corps = "Consulter les log : tail -n30 /var/log/django_io.log \n"
		mail_corps = "Arrêter le daemon totalement : /var/www/django/prod/daemon/django_io.bash force-stop \n\n"
		mail_corps = "Redemmarrer le daemon : /var/www/django/prod/daemon/django_io.bash start \n"
		mail_corps = " : \n"

		mail_corps += tb
		m = mail.Mail(mail_corps)
		m.from_("Application_stockparis@takasago.com")
		m.reply_to("charly.gontero@linautom.fr")
		#m.to(["charly.gontero@linautom.fr","yanick_soufflet@takasago.com"])
		m.to(["charly.gontero@linautom.fr","TEPL-IT@takasago.com"])
		if version.status_developement["data"] == "prod":
			m.subject("Stock Labo Paris, Erreur importation de fichier")
		else:
			m.subject("Ne pas tenir compte de cette email, je fait des tests sur le serveur, charly")
		#m.send("smtp.laposte.net", "charly.gontero@laposte.net", "charly.gontero", "1Addyson")
		m.send(smtp="par-srv-cas01.eu.takasago.com", expediteur="Application_stockparis@takasago.com", user=None , password=None, starttls=False)

		arret_importation(imp)

	log_print("Deamon stoppé")
	exit(0)


if __name__ == '__main__':

	main()


