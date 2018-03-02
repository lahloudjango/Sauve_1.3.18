# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Module de gestion des pistolets code barres et du décodage de code barres
"""

import datetime

__author__ = "Charly GONTERO"
__date__ = "2017-03-29 13:48:00"
__version__ = 1.6
__credits__ = """
 *  scancb.py
 *
 *  Copyright 2011 Charly GONTERO
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 *  MA 02110-1301, USA.
"""

VERSION = __version__
def version():
	return __version__


class Scan(object):
	"""
		Class de gestion des lecteurs codes barres et décodage des codes barres
		Si le lecteur CB est en émulation keyboard ; ne pas utilisé les fonctions open, scan, close
	"""
#	import serial

	TYPE_FORMAT_CB = {
		"contexa": {
			"desc": "Code barres CONTEXA",
			"format": {
					"01": "code barres ingrédient avec code ingrédient ( Sans Déstockage )",
					"02": "code barres ingrédient avec ID ingrédient ( Avec Déstockage )",
					"11": "Ingrédient Dans Table ingrédientlot ( EP )",
					"12": "code barres tuyaux",
					"50": "code barres Base Commune",
					"51": "code barres Dilution",
					"52": "code barres Coeur",
					"53": "code barres Sous-formule",
					"54": "code barres Formule de Base",
					"55": "code barres Compo Test",
					"56": "code barres Compo Purge",
					"57": "code barres Split Sous-formule",

					"80": "Login contexa",
					"81": "Tare",
					"82": "code barres spéciaux",
						}
					},
		"linautom": {
			"desc": "Code barres LINAUTOM",
			"format": {
				"001": "Code barres de login automatique",
				"002": "Code barres de selection balance",
				"003": "Code barres emplacement : code emplacement =  003:site_id:entrepot_id:magasin_id:emplacement",
				"004": "Code barres de selection type de contenant",
				"005": "Code barres emplacement id"
						}
					},
		"firmenich": {
			"desc": "Code barres FIRMENICH",
			"format": {
				"class1d":"Contenant CLASS (GVA)",
				"sap1d":"Code barres SAP lineaire",
				"class2d":"Code barres CLASS",
				"class2d_ghs":"Code barres CLASS GHS ( avec pictogramme )",
				"sap2d":"Code barres SAP datamatrix",
						}
					},
	}

	def __init__(self):
		"""
			Définition/Initialisation des données de base
			Pour le décodage des CB contexa définir mysql et mysql_db
		"""
		print "init Scan"
		self.mysql = None
		self.mysql_db = None
		self.periode_default = datetime.timedelta(days = 30)
		self.cb = {
						"type":None,
						"descript":None,
						"format":None,
						"fonction":None,
						}

	def open(self,port, baudrate, parity, stopbits, bytesize):
		"""
			Ouvre le port RS232 pour la lecture CB
		"""
		self.rs = self.serial.Serial(port=port, baudrate=baudrate, parity=parity, stopbits=stopbits, bytesize=bytesize)
		self.rs.open()

	def close(self):
		"""
			Ferme le port RS232 pour la lecture CB
		"""
		self.rs.close()

	def scan(self):
		"""
			Déclanche l"écoute sur le port RS232 et retourne le CB
		"""
		cb = ""
		while cb[-1:] != "\n":
			self.cb["cb_string"] += self.rs.read(1)

	def bell(self):
		"""
			Caractaire faisant sonner le clavier - le lecteur CB
		"""
		self.rs.write("\a")

	def format_cb(self, cb):
		"""
			Format les CB contexa : remplace le \r par un :
			Fait le découpage du code barres sur le : de séparation des champs
		"""
		self.cb["cb_string"] = cb.replace("\r", ":")
		self.cb["cb_list"] = self.cb["cb_string"].split(":")

	def decode_cb(self):
		"""
			réalise tous les décodages CB et rempli la structure CB
			self.cb["cb_string"] doit être initialisé et format executée avec le CB
			Utilisez par la suite format_cb pour la mise en forme
		"""
		if self.decode_cb_speciaux():
			print "TYPE:%s ; FORMAT:%s => %s ; DESCRIPTION:%s" %(self.cb["type"], self.cb["format"], self.cb["fonction"], self.cb["descript"])
			return True
		if self.decode_cb_linautom():
			print "TYPE:%s ; FORMAT:%s => %s ; DESCRIPTION:%s" %(self.cb["type"], self.cb["format"], self.cb["fonction"], self.cb["descript"])
			return True
		if self.decode_cb_contexa():
			print "TYPE:%s ; FORMAT:%s => %s ; DESCRIPTION:%s" %(self.cb["type"], self.cb["format"], self.cb["fonction"], self.cb["descript"])
			return True
		if self.decode_cb_firmenich():
			print "TYPE:%s ; FORMAT:%s => %s ; DESCRIPTION:%s" %(self.cb["type"], self.cb["format"], self.cb["fonction"], self.cb["descript"])
			return True
		return False

	def decode_cb_speciaux(self):
		"""
			réalise le décodage du CB et rempli la structure CB
			self.cb["cb_string"] doit être initialisé avec le CB
			Utilisez par la suite format_cb pour la mise en forme
			Fonction annulation : #ANNULE ; n ;0
			Fonction validation : #VALIDE ; #OK ; o ;1
			Fonction reset : #RESET
		"""
		if self.cb["cb_list"][0] == "#ANNULE":
			self.cb.update({"type":"linautom"})
			self.cb.update({"descript":"code barres fonction"})
			self.cb.update({"format":"fonction"})
			self.cb.update({"fonction": "annule"})
			return True
		if self.cb["cb_list"][0] == "#OK" or self.cb["cb_list"][0] == "#VALIDE":
			self.cb.update({"type":"linautom"})
			self.cb.update({"descript":"code barres fonction"})
			self.cb.update({"format":"fonction"})
			self.cb.update({"fonction": "ok"})
			return True
		if self.cb["cb_list"][0] == "#RESET":
			self.cb.update({"type":"linautom"})
			self.cb.update({"descript":"code barres fonction"})
			self.cb.update({"format":"fonction"})
			self.cb.update({"fonction": "reset"})
			return True
		if self.cb["cb_list"][0] == "#MENU":
			self.cb.update({"type":"linautom"})
			self.cb.update({"descript":"code barres fonction"})
			self.cb.update({"format":"fonction"})
			self.cb.update({"fonction": "menu"})
			return True
		if self.cb["cb_list"][0] == "#TARE":
			self.cb.update({"type":"linautom"})
			self.cb.update({"descript":"code barres fonction"})
			self.cb.update({"format":"fonction"})
			self.cb.update({"fonction": "tare"})
			return True
		if self.cb["cb_list"][0] == "#REAPPRO":
			self.cb.update({"type":"linautom"})
			self.cb.update({"descript":"code barres fonction"})
			self.cb.update({"format":"fonction"})
			self.cb.update({"fonction": "reappro"})
			return True
		return False

	def decode_cb_contexa(self):
		"""
			réalise le décodage des CB contexa
			self.cb["cb_string"] doit être initialisé avec le CB
			Utilisez par la suite format_cb pour la mise en forme
			01: code barres ingrédient avec code ingrédient
			02: code barres ingrédient avec ID ingrédient
			12: code barres tuyaux
			51: -> 56: code barres formule
		"""
		if self.cb["cb_list"][0] == "01":
			self.cb.update({"type":"contexa"})
			self.cb.update({"format":self.cb["cb_list"][0]})
			self.cb.update({"descript":self.TYPE_FORMAT_CB["contexa"]["format"][self.cb["cb_list"][0]]})
			self.cb.update({"code_ingredient":self.cb["cb_list"][1]})
			if len(self.cb["cb_list"]) > 1:
				self.cb.update({"lot":self.cb["cb_list"][2]})
				self.cb.update({"fin_validite": datetime.datetime.strptime(self.cb["cb_list"][3], "%d-%m-%Y")})
			return True
		elif self.cb["cb_list"][0] == "02":
			self.cb.update({"type":"contexa"})
			self.cb.update({"format":self.cb["cb_list"][0]})
			self.cb.update({"descript":self.TYPE_FORMAT_CB["contexa"]["format"][self.cb["cb_list"][0]]})
			self.cb.update({"id_ingredient":int(self.cb["cb_list"][1])})
			return True
		elif self.cb["cb_list"][0] == "12":
			self.cb.update({"type":"contexa"})
			self.cb.update({"format":self.cb["cb_list"][0]})
			self.cb.update({"descript":self.TYPE_FORMAT_CB["contexa"]["format"][self.cb["cb_list"][0]]})
			self.cb.update({"id_ingredient":int(self.cb["cb_list"][1])})
			return True
		elif self.cb["cb_list"][0] in ("50","51","52","53","54","55","56","57"):
			if len(self.cb["cb_list"]) == 2:
				self.cb.update({"type":"contexa"})
				self.cb.update({"format":self.cb["cb_list"][0]})
				self.cb.update({"descript":self.TYPE_FORMAT_CB["contexa"]["format"][self.cb["cb_list"][0]]})
				self.cb.update({"code_type_formule":self.cb["cb_list"][0]})
				self.cb.update({"id_formule":int(self.cb["cb_list"][1])})
			else:
				self.cb.update({"type":"contexa"})
				self.cb.update({"format":self.cb["cb_list"][0]})
				self.cb.update({"descript":self.TYPE_FORMAT_CB["contexa"]["format"][self.cb["cb_list"][0]]})
				self.cb.update({"code_type_formule":self.cb["cb_list"][0]})
				self.cb.update({"code_formule":self.cb["cb_list"][1]})
				self.cb.update({"lot":self.cb["cb_list"][2]})
				try:
					self.cb.update({"id_formule": int(self.cb["cb_list"][2])})
				except ValueError:
					try:
						self.cb.update({"id_formule": int(self.cb["cb_list"][2][2:])})
					except ValueError:
						try:
							self.cb.update({"id_formule": int(self.cb["cb_list"][2][2:-4])})
						except ValueError:
							self.cb.update({"id_formule": None})
				self.cb.update({"fin_validite": datetime.datetime.strptime(self.cb["cb_list"][3], "%d-%m-%Y")})
			return True
		elif self.cb["cb_list"][0] == "82:":
			self.cb.update({"type":"contexa"})
			self.cb.update({"format":self.cb["cb_list"][0]})
			self.cb.update({"descript":self.TYPE_FORMAT_CB["contexa"]["format"][self.cb["cb_list"][0]]})
			self.cb.update({"action":self.cb["cb_list"][0]})
			self.cb.update({"param2":self.cb["cb_list"][1][:2]})
			self.cb.update({"param1":self.cb["cb_list"][1][3:4]})
			self.cb.update({"code_action":self.cb["cb_list"][1][5:6]})
			self.cb.update({"element":self.cb["cb_list"][1][7:8]})
			return True
		return False

	def decode_cb_firmenich(self):
		"""
			Décodage des CB firmenich
			self.cb["cb_string"] doit être initialisé avec le CB
			Utilisez par la suite format_cb pour la mise en forme
		"""
		if len(self.cb["cb_list"]) == 1:
			if self.cb["cb_list"][0][:3] == "GVA":
				self.cb.update({"type":"firmenich"})
				self.cb.update({"descript":"Contenant CLASS (GVA )"})
				self.cb.update({"format":"class1d"})
				self.cb.update({"lot":self.cb["cb_list"][0]})
				return True
			else:
				self.cb.update({"type":"firmenich"})
				self.cb.update({"descript":"code barres SAP lineaire"})
				self.cb.update({"format":"sap1d"})
				self.cb.update({"lot":self.cb["cb_list"][0].replace("\t", "/")})
				return True
		elif len(self.cb["cb_list"]) == 3:
			self.cb.update({"type":"firmenich"})
			self.cb.update({"descript":"code barres SAP lineaire"})
			self.cb.update({"format":"sap2d"})
			self.cb.update({"lot": "/".join(self.cb["cb_list"])})
			return True
		elif len(self.cb["cb_list"]) == 4:
			self.cb.update({"type":"firmenich"})
			self.cb.update({"descript":"code barres CLASS"})
			self.cb.update({"format":"class2d_ghs"})
			self.cb.update({"code_ingredient":self.cb["cb_list"][0]})
			self.cb.update({"lot":self.cb["cb_list"][1]})
			self.cb.update({"contenant":self.cb["cb_list"][3]})
			self.cb.update({"fin_validite":datetime.datetime.strptime(self.cb["cb_list"][2],"%d%b%Y")})
			return True
		elif len(self.cb["cb_list"]) == 5:
			try:
				self.cb.update({"fin_validite":datetime.datetime.strptime(self.cb["cb_list"][2],"%d%b%Y")})
			except ValueError:
				try:	
					self.cb.update({"debut_validite":datetime.datetime.strptime(self.cb["cb_list"][2],"%Y/%m/%d")})
				except ValueError:
					pass
				else:
					self.cb.update({"type":"firmenich"})
					self.cb.update({"descript":"code barres SAP datamatrix"})
					self.cb.update({"format":"sap2d"})
					self.cb.update({"code_ingredient":self.cb["cb_list"][0]})
					self.cb.update({"lot":self.cb["cb_list"][1]})
					self.cb.update({"contenant":self.cb["cb_list"][3]})
					return True
			else:
				self.cb.update({"type":"firmenich"})
				self.cb.update({"descript":"code barres CLASS"})
				self.cb.update({"format":"class2d"})
				self.cb.update({"code_ingredient":self.cb["cb_list"][0]})
				self.cb.update({"lot":self.cb["cb_list"][1]})
				self.cb.update({"contenant":self.cb["cb_list"][3]})
				return True
		return False

	def decode_cb_linautom(self):
		"""
			réalise le décodage des CB linautom ( qrcode )
			self.cb["cb_string"] doit être initialisé avec le CB
			Utilisez par la suite format_cb pour la mise en forme
		"""
		if self.cb["cb_list"][0] == "001":
			self.cb.update({"type" : "linautom"})
			self.cb.update({"format" : self.cb["cb_list"][0]})
			self.cb.update({"descript" : self.TYPE_FORMAT_CB["linautom"]["format"][self.cb["cb_list"][0]]})
			self.cb.update({"user" : self.cb["cb_list"][1]})
			self.cb.update({"pass" : self.cb["cb_list"][2]})
			return True
		if self.cb["cb_list"][0] == "002":
			self.cb.update({"type" : "linautom"})
			self.cb.update({"format" : self.cb["cb_list"][0]})
			self.cb.update({"descript" : self.TYPE_FORMAT_CB["linautom"]["format"][self.cb["cb_list"][0]]})
			self.cb.update({"protocol" : ""})
			self.cb.update({"port" : ""})
			self.cb.update({"baudrate" : ""})
			self.cb.update({"parity" : ""})
			self.cb.update({"stopbits" : ""})
			self.cb.update({"bytesize" : ""})
			self.cb.update({"fin_de_ligne" : ""})

			self.cb.update({"protocol" : self.cb["cb_list"][1]})
			if len(self.cb["cb_list"]) >= 3:
				if self.cb["cb_list"][2].startswith("/dev"):
					self.cb.update({"port" : self.cb["cb_list"][2]})
					if len(self.cb["cb_list"]) >= 4:
						self.cb.update({"baudrate" : self.cb["cb_list"][3]})
					if len(self.cb["cb_list"]) >= 5:
						self.cb.update({"parity" : self.cb["cb_list"][4]})
					if len(self.cb["cb_list"]) >= 6:
						self.cb.update({"stopbits" : self.cb["cb_list"][5]})
					if len(self.cb["cb_list"]) >= 7:
						self.cb.update({"bytesize" : self.cb["cb_list"][6]})
					if len(self.cb["cb_list"]) >= 8:
						self.cb.update({"fin_de_ligne" : self.cb["cb_list"][7]})
				else:
					if len(self.cb["cb_list"]) >= 4:
						self.cb.update({"port" : ":".join((self.cb["cb_list"][2],self.cb["cb_list"][3]))})
					if len(self.cb["cb_list"]) >= 5:
						self.cb.update({"baudrate" : self.cb["cb_list"][4]})
					if len(self.cb["cb_list"]) >= 6:
						self.cb.update({"parity" : self.cb["cb_list"][5]})
					if len(self.cb["cb_list"]) >= 7:
						self.cb.update({"stopbits" : self.cb["cb_list"][6]})
					if len(self.cb["cb_list"]) >= 8:
						self.cb.update({"bytesize" : self.cb["cb_list"][7]})
					if len(self.cb["cb_list"]) >= 9:
						self.cb.update({"fin_de_ligne" : self.cb["cb_list"][8]})
			return True
		if self.cb["cb_list"][0] == "003":
			self.cb.update({"type":"linautom"})
			self.cb.update({"format":self.cb["cb_list"][0]})
			self.cb.update({"descript":self.TYPE_FORMAT_CB["linautom"]["format"][self.cb["cb_list"][0]]})
			self.cb.update({"site":self.cb["cb_list"][1]})
			self.cb.update({"entrepot":self.cb["cb_list"][2]})
			self.cb.update({"magasin":self.cb["cb_list"][3]})
			self.cb.update({"emplacement":self.cb["cb_list"][4]})
			return True
		if self.cb["cb_list"][0] == "004":
			self.cb.update({"type":"linautom"})
			self.cb.update({"format":self.cb["cb_list"][0]})
			self.cb.update({"descript":self.TYPE_FORMAT_CB["linautom"]["format"][self.cb["cb_list"][0]]})
			self.cb.update({"contenant_type":self.cb["cb_list"][1]})
			return True
		if self.cb["cb_list"][0] == "005":
			self.cb.update({"type":"linautom"})
			self.cb.update({"format":self.cb["cb_list"][0]})
			self.cb.update({"descript":self.TYPE_FORMAT_CB["linautom"]["format"][self.cb["cb_list"][0]]})
			self.cb.update({"emplacement_id":self.cb["cb_list"][1]})
			return True
		return False



