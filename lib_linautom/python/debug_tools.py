# -*- coding: utf-8 -*-
"""
Outil de dévelopement et de debug
"""
from __future__ import unicode_literals

import codecs
import types
import datetime

__author__ = "Charly GONTERO"
__date__ = "2018-02-22 10:41:55"
__version__ = "1.0.2"
__credits__ = """
 *  debug_tools.py
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

class Csv(object):
	"""
	class de gestion des fichier csv
	"""
	def __init__(self, nom_fichier, separateur=";", fin_de_ligne="\n", encoding="utf-8"):
		self.nom_fichier = nom_fichier
		self.separateur = separateur
		self.fin_de_ligne = fin_de_ligne
		self.encoding = encoding
		self.dic = None
		self.entete = None
		self.s = ""
		self.csv = ""
	def set_as_dic(self, dic):
		"""
		definis une nouvelle liste en donnée de base
		"""
		self.dic = dic
	def get_as_dic(self, ):
		"""
		Donnee les données sous forme de liste de dictionnaire
		"""
		return self.dic
	def set_as_str(self, s):
		"""
		Donne une chaine de caractaire comme source de données
		"""
		self.s = s
		liste_ligne = self.s.split(self.fin_de_ligne)
		h = liste_ligne.pop(0)
		col_liste_nom = h.split(self.separateur)
		self.dic = []
		for lf in liste_ligne:
			if lf == "":
				continue
			ligne = lf.split(self.separateur)
			l = {}
			for colonne in range(0, len(col_liste_nom)):
				l.update({col_liste_nom[colonne]:ligne[colonne]})
			self.dic.append(l)
	def get_as_str(self, entete=None):
		"""
		Donne les données sous forme de chaine de caractaire
		"""
		if len(self.dic) > 0:
			if entete == None:
				self.entete = [ k for k in self.dic[0].keys()] 
			else:
				self.entete = entete
			csv = []
			csv.append( self.separateur.join(self.entete) )
			for r in self.dic:
				csv_ligne = []
				for k in self.entete:
					csv_ligne.append( unicode(r[k]) )
				csv.append( self.separateur.join(csv_ligne) )
			self.csv = self.fin_de_ligne.join(csv)
			return self.csv	
		else:
			return ""
	def write(self, entete=None):
		"""
		Ecriture d'une liste de dic dans un csv
		"""
		self.get_as_str(entete)
		if self.csv != "":
			f = codecs.open(self.nom_fichier, "w", encoding=self.encoding)
			f.write(self.csv)
			f.close()
		else:
			print "rien n'a enregistrer"
	def read(self):
		"""
		Lecture d'un CSV et formation d'une liste de dictionnaire avec les ligne de donnée
		"""
		f = codecs.open(self.nom_fichier, "r", encoding=self.encoding)
		fichier_import = f.read()
		f.close()
		
		if len(fichier_import) > 0:
			self.set_as_str(fichier_import)

def string_as_ascii(text):
	"""
	Convertie l'objet ou la chaine de caractaire en chaine de carractaire ascii
	"""
	if type(text) == types.StringType:
		return text
	elif type(text) == types.UnicodeType:
		return text.encode("ascii", "replace")
	elif type(text) == types.NoneType:
		return None
	else:
		t = str(text)
		if type(t) == types.StringType:
			return t
		else:
			return t.encode("ascii", "replace")

def print_ascii(text):
	print string_as_ascii(text)

def string_as_unicode(text):
	"""
	Convertie l'objet ou la chaine de caractaire en chaine de carractaire unicode
	"""
	if type(text) == types.UnicodeType:
		return text
	elif type(text) == types.StringType:
		return text.decode("ascii", "replace")
	elif type(text) == types.NoneType:
		return None
	else:
		t = unicode(text)
		if type(t) == types.UnicodeType:
			return t
		else:
			return t.decode("ascii", "replace")

def print_unicode(text):
	print string_as_unicode(text)

def dump_env(env):
	"""
	Si env est un dictionnaire, le dictionnaire est présenté en 2 colonnes sinon retourne l'objet
	Retourne un object pour string_as_unicode string_as_ascii 
	"""
	if type(env) == types.DictType:
		l_key = 0
		for v in env.keys():
			if len(v) < l_key:
				l_key = len(v)

		f = "%%%ds : %%s\n" %(l_key+2)
		e = ""
		for v in env.keys():
			if string_as_unicode(v).find("__") < 0:
				e += f %(string_as_unicode(v), string_as_unicode(env[v]))
		return e
	else:
		return e

def whatisit(a):
	print type(a)
	print dir(a)
	print a

def whatisit_full(a):
	print a
	print type(a)
	print dir(a)
	print_ascii(dump_env_as_unicode(a))

class Log(object):
	"""
	class de gestion des log
	"""

	LOG_LEVEL = {
		"NO_LOG" :			-1,
		"EMERG" :			0,
		"ALERT" :			1,
		"CRIT" :			2,
		"ERR" :				3,
		"WARNING" :			4,
		"NOTICE" :			5,
		"INFO" :			6,
		"DEBUG" :			7,
		"DEFAULT" :			5,
		"DEFAULT_PRINT" :	5,
		}
	limit_log = LOG_LEVEL["DEFAULT"]
	limit_print = LOG_LEVEL["DEFAULT_PRINT"]

	def __init__(self, fichier, limit_log="DEFAULT", limit_print="DEFAULT_PRINT"):
		if limit_log not in self.LOG_LEVEL.keys():
			raise ValueError("limit_log incorrect, list : %s" %(self.LOG_LEVEL,keys()))
		else:
			self.limit_log = self.LOG_LEVEL[limit_log]
		if limit_print not in self.LOG_LEVEL.keys():
			raise ValueError("limit_print incorrect, list : %s" %(self.LOG_LEVEL,keys()))
		else:
			self.limit_print = self.LOG_LEVEL[limit_print]

	def write(self, level, *text):
		"""
		Fonction de login automatique
		"""
		d = datetime.datetime.now().strftime("%a, %Y-%m-%d %X ")
		ligne_log = ""
		for t in text:
			l = "%s %s %s" %(d, level, string_as_unicode(t))
			if self.LOG_LEVEL[level] <= limit_print:
				print_ascii(t)

			if self.LOG_LEVEL[level] <= limit_log:
				ligne_log += l + "\n"

		if ligne_log != "":
			f_log = codecs.open(fichier_log, "a", encoding="utf-8")
			f_log.writelines(l)
			f_log.close()


if __name__ == '__main__':

	nom_fichier = "test.csv"
	csv = Csv(nom_fichier, separateur=",", fin_de_ligne="\n", encoding="utf-8")
	csv.read()

	print csv.s
	print csv.dic

	nom_fichier = "test2.csv"

	csv1 = Csv(nom_fichier, separateur=";", fin_de_ligne="\r\n", encoding="utf-8")
	csv1.set_as_dic(csv.get_as_dic())
	csv1.write(["nbr_formule", "moyenne_poids"])


