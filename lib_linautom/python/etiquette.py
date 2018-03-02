# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Module d'enrobage d'impression des étiquettes en PDF et ZPL
"""
import codecs

__author__ = "Charly GONTERO"
__date__ = "2016-01-20 14:44:57"
__version__ = 2.1
__credits__ = """
 *  print.py
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

class DestinationErreur(Exception):
	"""
	Destination incorrect
	"""
	def __init__(self, *args, **kwargs):
		pass

class TypeImpressionErreur(Exception):
	"""
	Type impression inconnu
	"""
	def __init__(self, *args, **kwargs):
		pass

class TypeImpressionDetailErreur(Exception):
	"""
	Type impression detail inconnu
	"""
	def __init__(self, *args, **kwargs):
		pass

class TypeImpressionDetailImcompatible(Exception):
	"""
	Type impression detail imcompatible avec le type_impression
	"""
	def __init__(self, *args, **kwargs):
		pass

class PoliceInconnu(Exception):
	"""
	La police d'écriture est inconnu
	"""
	def __init__(self, *args, **kwargs):
		pass

class Print(object):
	"""
	Enrobage de etiquette_pdf et etiquette_zpl pour un appel commun
	"""
	IMPRESSION_ZPL_ORIENTATION = {
		0   : "N",
		90  : "R",
		180 : "I",
		270 : "B",
		}
	IMPRESSION_DETAIL_TYPE = {
		1  : "Data",			# Le champ data est remplacé par sa valeur correspondante avant l'ecriture de la ligne
		2  : "Text libre",		# text libre
		3  : "Image",			# lien vers une image
		11 : "Carre",			# carre
		12 : "Cercle",			# cercle
		13 : "Ligne",			# ligne
		21 : "Modèle",			# lien vers le model html
		}
	IMPRESSION_FORMAT = {
		1 : "ZPL",				# Impression imprimante ZPL
		2 : "PDF",				# Retour PDF
		3 : "HTML2PDF",			# Retour PDF, construction HTML
		}
	IMPRESSION_POLICE = {
		1  : "Plein Text",		# Impression Text
		11 : "Code 39",			# Impression Code 39
		12 : "Code 128",		# Impression Code 128
		13 : "Code QR",			# Impression Code QR
		14 : "Code Datamatrix",	# Impression Code Datamatrix
		}

	def __init__(self, type_impression, largeur_page, longueur_page, destination, resolution):
		"""
		l"origine de la mise en page est le coins en bas à gauche
		port :
			socket : impression direct (socket://printer:port)
			lp : impression sur une file d'impression lp://printer/fichier
			file : enregistrement fichier file://fichier
		"""
		self.type_impression = type_impression
		self.largeur_page = largeur_page
		self.longueur_page = longueur_page
		self.resolution = resolution
		self.zpl_factor_res = resolution/25.4
		d = destination.split("://")
		self.printer = None
		self.fichier = None
		self.protocol = d[0]
		if self.protocol == "socket":
			p = d[1].split(":")
			self.printer = p[0]
			self.port = int(p[1])
		elif self.protocol == "lp":
			self.printer = d[1][:d[1].find(":")]
			self.fichier = d[1][d[1].find(":")+1:]
		elif self.protocol == "file":
			self.fichier = d[1]
		else:
			raise DestinationErreur

		if self.type_impression == 1: # ZPL
			import etiquette_zpl
			self.etiquette = etiquette_zpl.Zpl()
			self.etiquette.standard_header()
			self.etiquette.codepage("MS")
		elif self.type_impression == 2: # PDF
			import etiquette_pdf
			if self.fichier == None:
				import random
				rand = str(int(random.random()*1000000))
				self.fichier = "/tmp/label_%s.pdf" %(rand)
			self.fichier.replace("%s", rand)
			orient = 0
			if largeur_page > longueur_page:
				orient = 1
			self.etiquette = etiquette_pdf.EtiquettePDF(self.fichier, pagesize_mm=(self.largeur_page,self.longueur_page), orientation=orient)
		elif self.type_impression == 3: # HTML2PDF
			raise TypeImpressionErreur
		else:
			raise TypeImpressionErreur

	def add_ligne(self, impression_detail_type, champ_data, pos_x, pos_y, police, orientation, param1, param2, couleur):
		"""
		ajoute une ligne d'information
		"""
		if self.type_impression == 1: # ZPL
			if impression_detail_type == 1 or impression_detail_type == 2: 	# Data / Text
				if police == 1: 	# Text simple
					if self.IMPRESSION_ZPL_ORIENTATION.has_key(orientation):
						self.etiquette.police(hauteur=int(param1*self.zpl_factor_res), largeur=int(param2*self.zpl_factor_res), police=0, orientation=self.IMPRESSION_ZPL_ORIENTATION[orientation])
					else:
						self.etiquette.police(hauteur=int(param1*self.zpl_factor_res), largeur=int(param2*self.zpl_factor_res), police=0, orientation="N")
					self.etiquette.impression_text(position_x=int(pos_x*self.zpl_factor_res), position_y=int(pos_y*self.zpl_factor_res), text=champ_data, origine="B")
				elif police == 11:	# Code 39
					self.etiquette.barre_code_format(barre=float(param2)*(self.resolution/1000.0), narrow="3.0", height="3.0")
					if self.IMPRESSION_ZPL_ORIENTATION.has_key(orientation):
						self.etiquette.code_39(hauteur=int(param1*self.zpl_factor_res), orientation=self.IMPRESSION_ZPL_ORIENTATION[orientation], legende_b="N", legende_h="N", mode="Y")
					else:
						self.etiquette.code_39(hauteur=int(param1*self.zpl_factor_res), orientation="N", legende_b="N", legende_h="N", mode="Y")
					self.etiquette.impression_text(position_x=int(pos_x*self.zpl_factor_res), position_y=int(pos_y*self.zpl_factor_res), text=champ_data, origine="B")
				elif police == 12:	# Code 128
					self.etiquette.barre_code_format(barre=float(param2)*(self.resolution/1000.0), narrow="3.0", height="3.0")
					if self.IMPRESSION_ZPL_ORIENTATION.has_key(orientation):
						self.etiquette.code_128(hauteur=int(param1*self.zpl_factor_res), orientation=self.IMPRESSION_ZPL_ORIENTATION[orientation], legende_b="Y", legende_h="N", ucc="N", mode="A")
					else:
						self.etiquette.code_128(hauteur=int(param1*self.zpl_factor_res), orientation="N", legende_b="Y", legende_h="N", ucc="N", mode="A")
					self.etiquette.impression_text(position_x=int(pos_x*self.zpl_factor_res), position_y=int(pos_y*self.zpl_factor_res), text=champ_data, origine="B")
				elif police == 13:	# Code QR
					if self.IMPRESSION_ZPL_ORIENTATION.has_key(orientation):
						self.etiquette.code_qr(orientation=self.IMPRESSION_ZPL_ORIENTATION[orientation], model=1, factor=int(float(param1)*(self.resolution/1000.0)))
					else:
						self.etiquette.code_qr(orientation="N", model=2, factor=int(float(param1)*(self.resolution/1000.0)))
					self.etiquette.impression_text(position_x=int(pos_x*self.zpl_factor_res), position_y=int(pos_y*self.zpl_factor_res), text=self.etiquette.code_qr_text_format(text=champ_data, dencity="M", data_type="M", mode="A"), origine="B")
				elif police == 14:	# Code Datamatrix
					if self.IMPRESSION_ZPL_ORIENTATION.has_key(orientation):
						self.etiquette.code_datamatrix(orientation=self.IMPRESSION_ZPL_ORIENTATION[orientation], pixel=float(param2)*(self.resolution/1000.0), qualite=200, colonne=param1, ligne=param1, data_type=6, escape="_")
					else:
						self.etiquette.code_datamatrix(orientation="N", pixel=float(param2)*(self.resolution/1000.0), qualite=200, colonne=param1, ligne=param1, data_type=6, escape="_")
					self.etiquette.impression_text(position_x=int(pos_x*self.zpl_factor_res), position_y=int(pos_y*self.zpl_factor_res), text=champ_data, origine="B")
				else:
					raise PoliceInconnu
			elif impression_detail_type == 3:	# Image
				raise TypeImpressionDetailImcompatible
			elif impression_detail_type == 11:	# Carré
				carre(self, position_x=int(pos_x*self.zpl_factor_res), position_y=int(pos_y*self.zpl_factor_res), h=int(param1*self.zpl_factor_res), l=int(param2*self.zpl_factor_res) , largeur=champ_data, couleur="B", rayon=0, origine="B")
			elif impression_detail_type == 12:	# Cercle
				cercle(self, position_x=int(pos_x*self.zpl_factor_res), position_y=int(pos_y*self.zpl_factor_res), diametre=int(param1*self.zpl_factor_res), largeur=champ_data, couleur="B", origine="B")
			elif impression_detail_type == 13:	# Ligne
				if pos_x<0 or pos_y<0:
					orient = "R"
				else:
					orient = "L"
				ligne(self, position_x=abs(int(pos_x*self.zpl_factor_res)), position_y=abs(int(pos_y*self.zpl_factor_res)), h=int(param1*self.zpl_factor_res), l=int(param2*self.zpl_factor_res), largeur=champ_data, couleur="B", orientation=orient, origine="B")
			elif impression_detail_type == 21:	# Modèle
				raise TypeImpressionDetailImcompatible
			else:
				raise TypeImpressionDetailErreur
		elif self.type_impression == 2: # PDF
			if impression_detail_type == 1 or impression_detail_type == 2: 	# Data Text
				if police == 1: 	# Text simple
					if orientation != 0:
						self.etiquette.save_state()
						self.etiquette.orientation(orientation)
					aligne = "L"
					if couleur != None and couleur != "":
						color = couleur.split(",")
						if len(color) >= 3:
							self.etiquette.font_color(int(color[0]), int(color[1]), int(color[2]))
						else:
							self.etiquette.font_color(0,0,0)
						if len(color) >= 4 and color[3] in ("L", "R", "C"):
							aligne = color[3]
					else:
						self.etiquette.font_color(0,0,0)
					self.etiquette.font_size("Courier", param1)
					self.etiquette.impression_text(x=pos_x, y=pos_y, t=champ_data, alignement=aligne)
					if orientation != 0:
						self.etiquette.restore_state()
				elif police == 11:	# Code 39
					raise TypeImpressionDetailImcompatible
				elif police == 12:	# Code 128
					if orientation != 0:
						self.etiquette.save_state()
						self.etiquette.orientation(orientation)
					self.etiquette.print_code_128(x=pos_x, y=pos_y, text=champ_data, hauteur=param1, largeur=param2/10.0, font_size=1, human_readable=1)
					if orientation != 0:
						self.etiquette.restore_state()
				elif police == 13:	# Code QR
					if orientation != 0:
						self.etiquette.save_state()
						self.etiquette.orientation(orientation)
					self.etiquette.print_code_qr(x=pos_x, y=pos_y, text=champ_data, taille=param1)
					if orientation != 0:
						self.etiquette.restore_state()
				elif police == 14:	# Code Datamatrix
					raise TypeImpressionDetailImcompatible
				else:
					raise PoliceInconnu
			elif impression_detail_type == 3:	# Image
				if champ_data.lower().endswith(".svg"):
					self.etiquette.print_svg_file(x=pos_x, y=pos_y, facteur_x=param1/100.0, facteur_y=param2/100.0, image_file=champ_data)
				else:
					self.etiquette.print_image_file(x=pos_x, y=pos_y, len_x=param1, len_y=param2, image_file=champ_data)
			elif impression_detail_type == 11:	# Carré
				if couleur != None and couleur != "":
					color = couleur.split(",")
					if len(color) >= 3:
						self.etiquette.back_ground_color(int(color[0]), int(color[1]), int(color[2]))
					else:
						self.etiquette.back_ground_color(0,0,0)
				else:
					self.etiquette.back_ground_color(0,0,0)
				self.etiquette.carre(x=pos_x, y=pos_y, len_x=param1-pos_x, len_y=param2-pos_y, fond=0, bordure=1)
			elif impression_detail_type == 12:	# Cercle
				if couleur != None and couleur != "":
					color = couleur.split(",")
					if len(color) >= 3:
						self.etiquette.back_ground_color(int(color[0]), int(color[1]), int(color[2]))
					else:
						self.etiquette.back_ground_color(0,0,0)
				else:
					self.etiquette.back_ground_color(0,0,0)
				self.etiquette.cercle(cen_x=pos_x, cen_y=pos_y, r=param1, fond=0, bordure=1)
			elif impression_detail_type == 13:	# Ligne
				if couleur != None and couleur != "":
					color = couleur.split(",")
					if len(color) >= 3:
						self.etiquette.back_ground_color(int(color[0]), int(color[1]), int(color[2]))
					else:
						self.etiquette.back_ground_color(0,0,0)
				else:
					self.etiquette.back_ground_color(0,0,0)
				self.etiquette.ligne(x=pos_x, y=pos_y, len_x=param1, len_y=param2)
			elif impression_detail_type == 21:	# Modèle
				raise TypeImpressionDetailErreur
			else:
				raise TypeImpressionDetailErreur
		elif self.type_impression == 3: # HTML2PDF
			if impression_detail_type == 1 or impression_detail_type == 2: 	# Data Text
				raise TypeImpressionDetailImcompatible
			elif impression_detail_type == 3:	# Image
				raise TypeImpressionDetailImcompatible
			elif impression_detail_type == 11:	# Carré
				raise TypeImpressionDetailImcompatible
			elif impression_detail_type == 12:	# Cercle
				raise TypeImpressionDetailImcompatible
			elif impression_detail_type == 13:	# Ligne
				raise TypeImpressionDetailImcompatible
			elif impression_detail_type == 21:	# Modèle
				raise TypeImpressionDetailImcompatible
			else:
				raise TypeImpressionDetailErreur
		else:
			raise TypeImpressionErreur

	def new_page(self):
		"""
		Création d'une nouvelle page
		"""
		if self.type_impression == 1: # ZPL
			self.etiquette.standard_footer()
			self.etiquette.standard_header()
		elif self.type_impression == 2: # PDF
			self.etiquette.page_next()
		elif self.type_impression == 3: # HTML2PDF
			raise TypeImpressionErreur
		else:
			raise TypeImpressionErreur

	def end_page(self):
		"""
		Fin de page
		"""
		if self.type_impression == 1: # ZPL
			self.etiquette.standard_footer()
		elif self.type_impression == 2: # PDF
			self.etiquette.page_next()
		elif self.type_impression == 3: # HTML2PDF
			raise TypeImpressionErreur
		else:
			raise TypeImpressionErreur

	def return_page(self):
		"""
		Création d'une nouvelle page
		"""
		if self.type_impression == 1: # ZPL
			return self.etiquette.etiquette
		elif self.type_impression == 2: # PDF
			pass
		elif self.type_impression == 3: # HTML2PDF
			raise TypeImpressionErreur
		else:
			raise TypeImpressionErreur

	def _save_file():
		"""
		Création d'une nouvelle page
		"""
		if self.type_impression == 1: # ZPL
			f = codecs.open(self.fichier, "w", encoding="utf-8")
			f.write(self.etiquette.etiquette)
			f.close()
		elif self.type_impression == 2: # PDF
			self.etiquette.save()
		elif self.type_impression == 3: # HTML2PDF
			raise TypeImpressionErreur
		else:
			raise TypeImpressionErreur

	def print_page(self):
		"""
		Création d'une nouvelle page
		"""
		if self.protocol == "socket":
			import socket
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((self.printer, self.port))
			sock.send(self.etiquette.etiquette.encode("850"))
			sock.close()
		elif self.protocol == "lp":
			self._save_file()
			import cups
			conn = cups.Connection ()
			id_job = conn.printFile(self.printer, self.fichier, self.fichier)
			conn.close()
		elif self.protocol == "file":
			self._save_file()
		else:
			raise DestinationErreur

	def get_page(self):
		if self.type_impression == 1: # ZPL
			return self.etiquette.etiquette
		elif self.type_impression == 2: # PDF
			return self.etiquette.get_pdf()
		elif self.type_impression == 3: # HTML2PDF
			raise TypeImpressionErreur
		else:
			raise TypeImpressionErreur


if __name__ == "__main__":


	e = Print(type_impression=2, largeur_page=50, longueur_page=35, destination="file://print_etiquette.pdf", resolution=600)

	e.add_ligne(impression_detail_type=11, champ_data="Charly", pos_x=2, pos_y=2, police=1, orientation=0, param1=48, param2=33, couleur="0,0,0,L")
	e.add_ligne(impression_detail_type=13, champ_data="Charly", pos_x=15, pos_y=2, police=1, orientation=0, param1=15, param2=33, couleur="0,0,0,L")
	e.add_ligne(impression_detail_type=1, champ_data="Charly", pos_x=16, pos_y=28, police=1, orientation=0, param1=10, param2=0, couleur="0,0,0,L")
	e.add_ligne(impression_detail_type=1, champ_data="GONTERO", pos_x=16, pos_y=25, police=1, orientation=0, param1=10, param2=0, couleur="0,0,0,L")
	e.add_ligne(impression_detail_type=1, champ_data="1000123478", pos_x=5, pos_y=-14, police=12, orientation=90, param1=28, param2=8, couleur="0,0,0,L")
	e.add_ligne(impression_detail_type=1, champ_data="1000123478", pos_x=32, pos_y=3, police=1, orientation=0, param1=15, param2=0, couleur="255,0,0,C")

	e.add_ligne(impression_detail_type=1, champ_data="40 Impasse de Chappet;01170 CROZET;FRANCE", pos_x=20, pos_y=12, police=13, orientation=0, param1=10, param2=0, couleur="")

	e.add_ligne(impression_detail_type=3, champ_data="/media/gonteroc/charly/charly/dev/git_tools_robots/static/logo_vectored.svg", pos_x=35, pos_y=26, police=0, orientation=0, param1=10, param2=10, couleur="")


	e.new_page()

	e.print_page()







