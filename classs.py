# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from lib_linautom.python import scancb

from fonction import *


class LocalScanCB(scancb.Scan):
	"""
	Redéfinition de la class Scan pour ajouter les fonction local
	"""
	def decode_cb_sap(self):
		if len(self.cb["cb_string"]) == 10 and self.cb["cb_string"][3] != ":":
			self.cb.update({"type":"sap"})
			self.cb.update({"format":"10c"})
			self.cb.update({"descript":"contenant sap"})
			self.cb.update({"contenant":self.cb["cb_string"]})
			return True


	def decode_cb(self):
		"""
		réalise tous les décodages CB et rempli la structure CB
		self.cb["cb_string"] doit être initialisé avec le CB
		Utilisez par la suite format_cb pour la mise en forme
		"""
		if self.decode_cb_sap():
			#print_ascii("TYPE:%s ; FORMAT:%s => %s ; DESCRIPTION:%s" %(self.cb["type"], self.cb["format"], self.cb["fonction"], self.cb["descript"]))
			return True
		elif self.decode_cb_speciaux():
			#print_ascii("TYPE:%s ; FORMAT:%s => %s ; DESCRIPTION:%s" %(self.cb["type"], self.cb["format"], self.cb["fonction"], self.cb["descript"]))
			return True
		elif self.decode_cb_linautom():
			#print_ascii("TYPE:%s ; FORMAT:%s => %s ; DESCRIPTION:%s" %(self.cb["type"], self.cb["format"], self.cb["fonction"], self.cb["descript"]))
			return True
		else:
			print "Décodage impossible de %s" %(self.cb["cb_string"])
			return False

#	def format_cb(self, cb):
#		"""
#			Format les CB contexa : remplace le \r par un ;
#			Suppression du charactaire ">" des pistolets contexa
#		"""
#		if cb[:1] == ">":
#			self.cb["cb_string"] = cb[1:].replace("\r", ";")
#		else:
#			self.cb["cb_string"] = cb.replace("\r", ";")
#		self.cb["cb_list"] = self.cb["cb_string"].split(";")
