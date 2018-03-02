# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Class de création d'étiquettes en zpl pour imprimante Zebra

Simulateur à http://labelary.com/
"""

__author__ = "Charly GONTERO"
__date__ = "2016-01-20 14:44:57"
__version__ = 3.2
__credits__ = """
 *  etiquette_zpl.py
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



def whatisit(a):
	print type(a)
	print dir(a)
	print a


class Zpl(object):
	"""
	Class de création d'étiquettes en zpl pour imprimante Zebra
	"""
	def __init__(self):
		"""
		Défini la variable étiquette qui contient le text ZPL de l"etiquette
		"""
		self.etiquette = ""

	def standard_header(self):
		"""
		défini pour une etiquette l"entete standard
		^XA : start
		~JSB : backfeed printing 
		^LH0,0 : position repère
		^FS
		^FR : impression en inserse sur le fond
		"""
		self.etiquette += "^XA\n~JSB\n^LH0,0^FS\n^FR\n"

	def standard_footer(self):
		"""
		défini pour une etiquette la fin standard
		^PR2,2,2 : vitesse d'impression
		^PQ1,0,0,N : Qualité, pause, copie, pause réécriture
		^XZ : END
		"""
		self.etiquette += "^PR2,2,2\n^PQ1,0,0,N\n^XZ\n"

	def codepage(self, codepage="MS"):
		"""
		Valeurs:
			U.S.A. 1 : 									USA1
			U.S.A. 2 : 									USA2
			U.K. : 										UK
			Holland : 									ND
			Denmark/Norway : 							DK
			Sweden/Finland :							SW
			Germany :									DE
			France 1 : 									FR1 / FR
			France 2 : 									FR2
			Italy : 									IT
			Spain : 									SP
			miscellaneous : 							OTHER
			Japan (ASCII with Yen symbol) : 			JP
			IBM Code Page 850 (see page 42) : 			MS
			16-bit (Unicode) encoded scalable fonts* :	UTF16
			Shift-JIS for scalable Japanese fonts** : 	JIS
			EUC-Kanji for scalable fonts : 				EUC
			Unicode (for Unicode-encoded fonts) 		unicode
			8-bit access to Unicode-encoded fonts : 	UTF8
			Code Page 850 : 							850
			Code Page 1250 : 							1250
			Code Page 1251 : 							1251
			Code Page 1253 : 							1253
			Code Page 1254 : 							1254
			Code Page 1255 : 							1255
		"""
		if codepage == "USA1":
			self.etiquette += "^CI0\n"
		elif codepage == "USA2":
			self.etiquette += "^CI1\n"
		elif codepage == "UK":
			self.etiquette += "^CI2\n"
		elif codepage == "ND":
			self.etiquette += "^CI3\n"
		elif codepage == "DK":
			self.etiquette += "^CI4\n"
		elif codepage == "SW":
			self.etiquette += "^CI5\n"
		elif codepage == "DE":
			self.etiquette += "^CI6\n"
		elif codepage == "FR1":
			self.etiquette += "^CI7\n"
		elif codepage == "FR":
			self.etiquette += "^CI7\n"
		elif codepage == "FR2":
			self.etiquette += "^CI8\n"
		elif codepage == "IT":
			self.etiquette += "^CI9\n"
		elif codepage == "SP":
			self.etiquette += "^CI10\n"
		elif codepage == "OTHER":
			self.etiquette += "^CI11\n"
		elif codepage == "JP":
			self.etiquette += "^CI12\n"
		elif codepage == "MS":
			self.etiquette += "^CI13\n"
		elif codepage == "UTF16":
			self.etiquette += "^CI14\n"
		elif codepage == "JIS":
			self.etiquette += "^CI15\n"
		elif codepage == "EUC":
			self.etiquette += "^CI16\n"
		elif codepage == "unicode":
			self.etiquette += "^CI17\n"
		elif codepage == "UTF8":
			self.etiquette += "^CI24\n"
		elif codepage == "850":
			self.etiquette += "^CI13\n"
		elif codepage == "1250":
			self.etiquette += "^CI31\n"
		elif codepage == "1251":
			self.etiquette += "^CI33\n"
		elif codepage == "1253":
			self.etiquette += "^CI34\n"
		elif codepage == "1254":
			self.etiquette += "^CI35\n"
		elif codepage == "1255":
			self.etiquette += "^CI36\n"
		else:
			self.etiquette += "^CI13\n"

	def position_h(self, position_x, position_y):
		"""
		changement de position du curseur par rapport à l"origine (^LL)
		Par defaut l"origine est en haut à gauche de l"étiquette
		"""
		self.etiquette += "^FO%s,%s\n" %(str(position_x),str(position_y))

	def position_b(self, position_x, position_y):
		"""
		changement de position du curseur par rapport à l"origine (^LL)
		Par defaut l"origine est en haut à gauche de l"étiquette
		"""
		self.etiquette += "^FT%s,%s\n" %(str(position_x), str(position_y))

	def police(self, hauteur, largeur, police=0, orientation="N"):
		"""
		définition de la police d"ecriture pour les texts
		police : defaut = 0
			Pour le detail des polices il faut les imprimer directement depuis le menu de l"imprimante"
		orientation :
			N = normal
			R = 90 degrees
			I = inverted 180 degrees
			B = 270 degrees
		""" 
		self.etiquette += "^A%s%s,%s,%s\n" %(str(police), orientation, str(hauteur), str(largeur))

	def impression_text(self, position_x, position_y, text, origine="B"):
		"""
		Impression d"une ligne de text
		"""
		if origine == "B":
			self.position_b(position_x, position_y)
		elif origine == "H":
			self.position_h(position_x, position_y)
		self.etiquette += "^FD%s^FS\n" %(text)

	def commentaire(self, c):
		"""
		Ajoute un commentaire dans le text de l"etiquette
		"""
		self.etiquette += "^FX%s^FS\n" %(c)

	def carre(self, position_x, position_y, h, l , bordure=1, couleur="B", rayon=0, origine="B"):
		"""
		Dessine depuis le coin en haut à gauche de heuteur h et de largeur l vers la droite en bas
		millieu et bord sont la couleur du centre et du bord du carre avec une valeur de 0 -> 32000
		"""
		if origine == "B":
			self.position_b(position_x, position_y)
		elif origine == "H":
			self.position_h(position_x, position_y)
		self.etiquette += "^GB%s,%s,%s,%s,%s^FS\n" %(str(l), str(h), str(bordure), couleur, str(rayon))

	def cercle(self, position_x, position_y, diametre, largeur=1, couleur="B", origine="B"):
		"""
		Dessine un cercle
			couleur du trait 
			B : noir
			W : blanc
		"""
		if origine == "B":
			self.position_b(position_x, position_y)
		elif origine == "H":
			self.position_h(position_x, position_y)
		self.etiquette += "^GC%d,%d,%d^FS\n" %(str(diametre), str(largeur), str(couleur))

	def ligne(self, position_x, position_y, h, l, orientation, largeur=1, couleur="B", origine="B"):
		"""
		Dessine une ligne dans une boite de hauteur h et de largeur l
			couleur du trait 
			B : noir
			W : blanc
		orientation:
			R : carré vers le bas à droite
			L : carré vers le bas à gauche
		"""
		if origine == "B":
			self.position_b(position_x, position_y)
		elif origine == "H":
			self.position_h(position_x, position_y)
		self.etiquette += "^GD%d,%d,%d,%s,%s^FS\n" %(str(l), str(h), str(largeur), couleur, orientation)

	def orientation_text(self, direction="N", espace=0):
		"""
		Defini l"orientation du text horisontal, vertical
		direction
			H : horisontal
			V : vertival
			R : retourné
		"""
		self.etiquette += "^FP%s,%d\n" %(direction, str(espace))

	def barre_code_format(self, barre, narrow="3.0", height="3.0"):
		"""
		Défini la largeur de barre des code barres
		"""
		self.etiquette += "^BY%s,%s,%s\n" %(barre, narrow, height)

	def code_39(self, hauteur, legende_b="Y", legende_h="N", orientation="N", mode="N"):
		"""
		chargement impression "text" en code 39
		orientation
			N = normal
			R = 90 degrees
			I = 180 degrees
			B = 270 degrees
		mode : bit de controle
			Y = oui
			N = non
		"""
		self.etiquette += "^B3%s,%s,%s,%s,%s\n" %(orientation, mode, str(hauteur), legende_b, legende_h)

	def code_128(self, hauteur, legende_b="Y", legende_h="N", orientation="N",  ucc="N", mode="A"):
		"""
		hauteur : hauteur de chaque ligne de données men pixel
		orientation
			N = normal
			R = 90 degrees
			I = 180 degrees
			B = 270 degrees
		mode
			N = no selected mode
			U = UCC Case Mode
			A = Automatic Mode
		"""
		self.etiquette += "^BC%s,%s,%s,%s,%s,%s\n" %(orientation, str(hauteur), legende_b, legende_h, ucc, mode)

	def code_qr_text_format(self, text, dencity="M", data_type="M", mode="A"):
		"""
		dencity
			H = ultra-high reliability level
			Q = high reliability level
			M = standard level
			L = high density level
		mode
			N = numeric
			A = alphanumeric
			Bxxxx = 8-bit byte mode
			K = Kanji
		data_type
			A = Automatic Input (default). Data character string JIS8 unit, Shift JIS. When the input mode is Automatic Input, the binary codes of 0x80 to 0x9F and 0xE0 to 0xFF cannot be set.
			M = Manual Input
		"""
		return "%s%s,%s%s" %(dencity, data_type, mode, text)

	def code_qr(self, orientation="N", model=2, factor=3):
		"""
		Chargement impression "text" code qrcode
		orientation
			N = normal
			R = rotated 90 degrees (clockwise)
			I = inverted 180 degrees
			B = read from bottom up, 270 degrees
		model
			1 = originale
			2 = avancé
		factor
			1 = 150 dpi printers
			2 = 200 dpi printers
			3 = 300 dpi printers
			6 = 600 dpi printers
			...
			10
		"""
		self.etiquette += "^BQ%s,%s,%s\n" %(orientation, str(model), str(factor))

	def code_datamatrix(self, orientation="N", pixel=1, qualite=200, colonne=20, ligne=20, data_type=6, escape="_"):
		"""
		Chargement impression "text" code data matrix
		orientation
			N = normal
			R = rotated 90 degrees (clockwise)
			I = inverted 180 degrees
			B = read from bottom up, 270 degrees
		qualite 0, 50, 80, 100, 140, 200
		colonne 9 à 49
		ligne 9 à 49
		data_type :
			1 = field data is numeric + space (0..9,”) – No \&’’ quality set at 200
			2 = field data is uppercase alphanumeric + space (A..Z,’’) – No \&’’
			3 = field data is uppercase alphanumeric + space, period, comma, dash, and slash (0..9,A..Z,“.-/”)
			4 = field data is upper-case alphanumeric + space (0..9,A..Z,’’) – no \&’’
			5 = field data is full 128 ASCII 7-bit set
			6 = field data is full 256 ISO 8-bit set
			Default Value: 6
		escape ( unix life \ " )
			Default Value: _ (underscore)
			This parameter is used only if quality 200 is specified. It is the
			escape character for embedding special control sequences
			within the field data. See Field Data (^FD) for ^BX usage.
		"""
		self.etiquette += "^BX%s,%s,%s,%s,%s,%s,%s\n" %(orientation, str(pixel), str(qualite), str(colonne), str(ligne), data_type, escape)


if __name__ == "__main__":

	"""
	etiquette = Zpl()
	etiquette.standard_header()
	etiquette.codepage("UTF8")
	etiquette.police(80, 60, police=0, orientation="N")
	etiquette.impression_text(500, 180, "QUITTE")
	etiquette.code_128(hauteur = 150)
	etiquette.impression_text(30, 150, "#QUITTE")
	etiquette.standard_footer()

	etiquette.standard_header()
	etiquette.codepage("UTF8")
	etiquette.police(80, 60, police=0, orientation="N")
	etiquette.impression_text(500, 880, "MODIFIE")
	etiquette.code_128(hauteur = 150)
	etiquette.impression_text(30, 850, "#MODIFIE")
	etiquette.standard_footer()
	"""


	etiquette = Zpl()
	etiquette.standard_header()
	etiquette.codepage("MS")

#	etiquette.police(100, 20, police=0, orientation="N")
#	etiquette.impression_text(20, 20, "002068")

#	etiquette.police(20, 15, police=0, orientation="N")
#	etiquette.impression_text(20, 60, "BUTYL QUINOLINE SEC")

#	etiquette.police(20, 15, police=0, orientation="N")
#	etiquette.impression_text(20, 90, "GIVAUDAN INTERNATIONAL SA")


	etiquette.police(30, 30, police=0, orientation="N")
	etiquette.impression_text(100, 180, "1000827845")

	etiquette.barre_code_format(barre=2, narrow="2.0", height="2.0")

	etiquette.code_128(hauteur=20, legende_b="Y", legende_h="N", orientation="B",  ucc="N", mode="A")
	etiquette.impression_text(50, 200, "1000827845")

#	etiquette.code_datamatrix( orientation="N", pixel=1, qualite=200, colonne=20, ligne=20, data_type=6, escape="_")

	etiquette.code_qr(orientation="N", model=2, factor=3)
	etiquette.impression_text(300, 100, "1000827845")


	etiquette.standard_footer()

	print etiquette.etiquette


	import socket
	TCP_HOST = "172.25.9.152"
	TCP_PORT = 9100

	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, msg:
		print "[ERROR] %s\n" %(msg[1])
		exit(1)

	try:
		sock.connect((TCP_HOST, TCP_PORT))
	except socket.error, msg:
		print "[ERROR] %s\n" %(msg[1])
		exit(2)

#	sock.send("GET %s HTTP/1.0\r\nHost: %s\r\n\r\n" % (etiquette.etiquette, TCP_HOST))
	sock.send(etiquette.etiquette)
	 

	sock.close()
