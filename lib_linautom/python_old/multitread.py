#-*- coding: utf-8 -*-
from __future__ import unicode_literals

import threading
import time


class TimeOut(Exception):
	def __init__(self, *args, **kwargs):
		pass


class ControledFonction(object):
	"""
	Fonction avec time out
	"""
	def __init__(self, fonction, time, name="Thread Fonction"):
		"""
		fonction : pointeur vers la fonction dont le temps d'execution est controlée
		time : temps max d'execution
		"""
		self.param = {
			"time":time,
			"t_fonction_kill":False,
			"t_time_out_kill":False,
			}
		self.t_fonction = threading.Thread(group=None, target=fonction, name=name, args=("Fonction",), kwargs={})
		self.param.update({"t_fonction":self.t_fonction})

		self.t_time_out = threading.Thread(group=None, target=self.time_out, name="Thread TimeOut", args=("TimeOut",), kwargs={})
		self.param.update({"t_time_out":self.t_time_out})
		
	def time_out(*args, **kwargs):
		"""
		args[0] = <__main__.ControledFonction object +-= self
		"""
		time.sleep(args[0].param["time"])
		if args[0].param["t_time_out_kill"] == True:
			print "time_out : tuée"	
		else:
			args[0].param["t_fonction_kill"] = True
			args[0].param["t_fonction"]._Thread__stop()
#			print "time_out : kill de t_fonction"
			args[0].param["t_fonction"].join()
#			print "time_out : fin de t_fonction"
			print "time_out : FONCTION TUEE %s" %(args[0].param["t_fonction"].name)
	
	def start(self):
		"""
		Déclanche le compte à reboure et l'exécution de la fonction
		"""
		self.t_time_out.start()
		self.t_fonction.start()

	def join(self):
		"""
		s'attache à la fonction qui se termine soit normallement soit en fin de compte à reboure
		"""
		self.param["t_fonction"].join()
		if self.param["t_fonction_kill"] == True:
#			print "join : tuée"
			return -1
		else:
			self.param["t_time_out_kill"] = True
#			print "join : fin de t_fonction"
			self.param["t_time_out"]._Thread__stop()
#			print "join : kill de t_time_out"
			self.param["t_time_out"].join()
#			print "join : fin de t_time_out"
			return 0
 
if __name__ == "__main__":

	def affiche1(param, *args, **kwargs):
		while param["boucle"]<15:
			print "Execution de la fonction 1 boucle %d" %(param["boucle"])
			time.sleep(1)
			param["boucle"]+=1
		print args
		print kwargs

	def affiche2(*args, **kwargs):
		j=0
		while j<15:
			print "Execution de la fonction 2 boucle %d" %(j)
			time.sleep(3)
			j+=1

#	a1 = ControledFonction(affiche1, 20, "F1")
#	a1.start()
#	err = a1.join()
#	if err < 0:
#		print "Fin sur TIMEOUT sur la fonction 1"
#	else:
#		print "Fin normal de la fonction 1"

#	a2 = ControledFonction(affiche2, 20, "F2")
#	a2.start()
#	err = a2.join()
#	if err < 0:
#		print "Fin sur TIMEOUT sur la fonction 2"
#	else:
#		print "Fin normal de la fonction 2"



#	t_fonction = threading.Thread(group=None, target=affiche1, name="Thread Fonction", args=("Fonction",), kwargs={})
#	t_fonction.start()
#	time.sleep(5)

#	t_fonction._Thread__stop()
#	t_fonction.join()

	param = {"boucle":0}
	print param
	t = threading.Thread(group=None, target=affiche1, name="AA", args=(param,), kwargs={})
	t.start()
	t.join(5)
	if t.is_alive():
		t._Thread__stop()
		print param
		print "Thread tuée"
	else:
		print param
		print "Fin normal"
	
	print "stop"
