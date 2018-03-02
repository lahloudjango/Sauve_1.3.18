# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Outil pratique utilié avec djangà
"""
import codecs
import types
import datetime
import etiquette

__author__ = "Charly GONTERO"
__date__ = "2017-05-04 09:03:30"
__version__ = 1.0
__credits__ = """
 *  django_tools.py
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


class Table(object):
	""" 
	Construit la structure pour les tables
	"""
	class Ligne(object):
		""" 
		Construit la structure pour une ligne
		"""
		def __init__(self, title=None, href=None, ligne_class=None, style=None, ligne_id=None):
			""" 
			Crée une nouvelle ligne
			"""
			self.ligne = {}
			self.ligne.update({"affiche" : True})
			self.ligne.update({"ligne_class" : ligne_class})
			self.ligne.update({"title" : title})
			self.ligne.update({"style" : style})
			self.ligne.update({"ligne_id" : ligne_id})
			self.ligne.update({"paire" : None})
			self.ligne.update({"cellules" : []})

		def add_cellule(self, label, title=None, href=None, cellule_class=None, style=None, cellule_id=None, colspan=None, rowspan=None, onclick=None):
			""" 
			Ajoute une cellule à la ligne
			"""
			cellule = {}
			cellule.update({"label" : label})
			cellule.update({"href" : href})
			cellule.update({"cellule_class" : cellule_class})
			cellule.update({"title" : title})
			cellule.update({"style" : style})                                                                                                                                
			cellule.update({"cellule_id" : cellule_id})
			cellule.update({"colspan" : colspan})
			cellule.update({"rowspan" : rowspan})
			cellule.update({"onclick" : onclick})
			self.ligne["cellules"].append(cellule)

		def get_ligne(self):
			return self.ligne

	def __init__(self, p=True, caption="", summary="", table_class=None, title=None, style=None, table_id=None, entete=True):
		"""
		Initalise la structure pour les listes
		"""
		self.liste = {}
		self.liste.update({"p" : p})
		self.liste.update({"caption" : caption})
		self.liste.update({"summary" : summary})
		self.liste.update({"table_class" : table_class})
		self.liste.update({"title" : title})
		self.liste.update({"style" : style})
		self.liste.update({"entete" : entete})
		self.liste.update({"table_id" : table_id})
		self.liste.update({"headers" : []})
		self.liste.update({"liste" : []})
		self.liste.update({"footers" : []})
		self.liste.update({"n_ligne_affiche" : 0})
		self.liste.update({"n_ligne_limit" : 0})
		self.liste.update({"n_ligne_total" : 0})
		self.liste.update({"limit_du" : None})
		self.liste.update({"limit_au" : None})

	def add_headers(self, h):
		"""
		défini les entêtes de colonne dans le même format de Ligne
		"""
		self.liste["headers"].append(h)

	def add_ligne(self, ligne, class_paire=None, class_impaire=None):
		"""
		ajoute une ligne à la liste
		"""
		if len(self.liste["liste"])%2 == 0:
			ligne["paire"] = True
		if class_paire != None:
			ligne["ligne_class"] = class_paire
		else:
			ligne["paire"] = False
		if class_impaire != None:
			ligne["ligne_class"] = class_impaire
		self.liste["liste"].append(ligne)

	def add_footers(self, h):
		"""
		défini les pieds de colonne dans le même format de Ligne
		"""
		self.liste["footers"].append(h)

	def get_liste(self):
		return self.liste


def make_addr_param(*args):
	"""
	construit une addresse/parametre URL avec un/des dico de paramettres
	"""
	param = {}
	for a in args:
		param.update(a)
	add = "?"
	for p in param:
		if type(param[p]) == types.UnicodeType:
			add += "%s=%s&" %(str(p), param[p])
		else:
			add += "%s=%s&" %(str(p), str(param[p]))
	return add[:-1]

def split_string(string, len_max):
	"""
	decoupage intéligent d'une chaine de caractaire sur les caractaire : space _ % @
	"""
	separateur = (" ","_","%","@")
	pos = []
	debut = -1
	fin = 0
	ligne = []
	for c in string:
		if c in separateur:
			pos.append((debut+1,fin+1))
			debut = fin
			fin += 1
		else:
			fin += 1
	pos.append((debut+1,fin+1))
	ss = ""
	i = 0
	for p in pos:
		if len(ss) + len(string[p[0]:p[1]]) <= len_max:
			ss += string[p[0]:p[1]]
		elif len(ss) == 0:
			ligne.append(ss)
			ss = ""
		else:
			ligne.append(ss)
			ss = string[p[0]:p[1]]
	ligne.append(ss)
	return ligne

def get_attr_data(objet, arbre):
	"""
	Recupération d'un attribut à partir d'une liste-arbre objet
	A partir d'une chaine de caractaire, retourne les éléments pour reconstruire l'objet
	"""
#	print arbre
	if len(arbre) < 1:
		return "obj err"
	if len(arbre) == 1:
		if arbre[0].endswith("()"):
			o=getattr(objet, arbre[0][:-2])
			return o()
		elif arbre[0].endswith(")"):
			o=getattr(objet, arbre[0][:arbre[0].find("(")])
			p=arbre[0][arbre[0].find('(')+1:-1]
			try:
				p_int = int(p)
				return o(p_int)
			except:
				pass
			return o(eval(p))
		elif arbre[0].startswith("[") and arbre[0].endswith("]"):
			i = eval(arbre[0][1:-1])
			if type(i) == type(2) and i < len(objet):
				return objet[i]
			elif type(i) == type("string"):
				if i in objet.keys():
					return objet[i]
				else:
					return None
			else:
				return "--"
		else:
			return getattr(objet, arbre[0])
	if len(arbre) > 1:
		if arbre[0].endswith("()"):
#			o=getattr(objet, arbre[0][:-2])
#			return get_attr_data(objet=o()[0], arbre=arbre[1:])
			o=getattr(objet, arbre[0][:-2])
			return get_attr_data(objet=o(), arbre=arbre[1:])
		elif arbre[0].endswith(")"):
			o=getattr(objet, arbre[0][:arbre[0].find("(")])
			p=arbre[0][arbre[0].find('(')+1:-1]
			try:
				p_int = int(p)
				return get_attr_data(objet=o(p_int), arbre=arbre[1:])
			except:
				pass
			return get_attr_data(objet=o(eval(p)), arbre=arbre[1:])
		else:
			o=getattr(objet, arbre[0])
			return get_attr_data(objet=o, arbre=arbre[1:])

def get_data(objet, element):
	"""
	Construction de l'arbre objet
	A partir d'une chaine de caractaire, retourne les éléments pour reconstruire l'objet
	"""
	arbre = element.split(".")
	return get_attr_data(objet=objet, arbre=arbre)

class ClassPolymorph(object):
	def addattr(self, name, value):
		self.__setattr__(name, value)

def etiquette_print(printer, imp, imp_d, *args, **element):
	"""
	construction d'une impression à partir d'une liste d'objet de description de l'impression
	"""
	meta = ClassPolymorph()
	meta.addattr("date_print", datetime.datetime.now().strftime("%d/%m/%Y"))
	element.update({"meta": meta})
	e = etiquette.Print(type_impression=imp.etiquette_format, largeur_page=printer.largeur, longueur_page=printer.longueur, destination=printer.imprimante_port, resolution=printer.resolution)
	for ligne in imp_d:
		if ligne.impression_detail_type == 1:
			if ligne.champ_data[:ligne.champ_data.find(".")] in element.keys():
				data = get_data(element[ligne.champ_data[:ligne.champ_data.find(".")]], ligne.champ_data[ligne.champ_data.find(".")+1:])
				e.add_ligne(
							impression_detail_type=ligne.impression_detail_type,
							champ_data=data,
							pos_x=ligne.pos_x,
							pos_y=ligne.pos_y,
							police=ligne.police,
							orientation=ligne.orientation,
							param1=float(ligne.param1),
							param2=float(ligne.param2),
							couleur="0,0,0,L")
			else:
				print_ascii("%s dans %s est incorrecte" %(ligne.champ_data[:ligne.champ_data.find(".")], ligne.champ_data))
				e.add_ligne(impression_detail_type=ligne.impression_detail_type, champ_data="!!OBJ ERR!!", pos_x=ligne.pos_x, pos_y=ligne.pos_y, police=ligne.police, orientation=ligne.orientation, param1=int(ligne.param1), param2=int(ligne.param2), couleur="0,0,0,L")
		else:
			e.add_ligne(impression_detail_type=ligne.impression_detail_type, champ_data=ligne.champ_data, pos_x=ligne.pos_x, pos_y=ligne.pos_y, police=ligne.police, orientation=ligne.orientation, param1=int(ligne.param1), param2=int(ligne.param2), couleur="0,0,0,L")

	e.end_page()
	if imp.imp_auto == True:
		e.print_page()
		if element.has_key("return_url"):
			return HttpResponseRedirect(element["return_url"])
		else:
			return
	else:
		if imp.etiquette_format == 1:
			response = HttpResponse(e.get_page(), content_type="text/txt")
			response["Content-Disposition"] = "attachment; filename=\"etiquette_print_%s.txt\"" %(datetime.datetime.now().strftime("%Y-%m-%d_%H%M"))
			if element.has_key("return_url"):
				return response
			else:
				return e.get_page()
		elif imp.etiquette_format == 2:
			response = HttpResponse(e.get_page(), content_type="application/pdf")
			response["Content-Disposition"] = "attachment; filename=\"etiquette_print_%s.pdf\"" %(datetime.datetime.now().strftime("%Y-%m-%d_%H%M"))
			if element.has_key("return_url"):
				return response
			else:
				return e.get_page()
		elif imp.etiquette_format == 3:
			response = HttpResponse(e.get_page(), content_type="application/pdf")
			response["Content-Disposition"] = "attachment; filename=\"etiquette_print_%s.pdf\"" %(datetime.datetime.now().strftime("%Y-%m-%d_%H%M"))
			if element.has_key("return_url"):
				return response
			else:
				return e.get_page()
		else:
			print_ascii("!!! FORMAT IMPRESSION INCONNU !!!")
			return

def param_as_in_list_int(request_get, dic, element, liste, default=None):
	"param est un int dans une liste"
	if request_get.has_key(element) and request_get[element] != "":
		try:
			ee = int(request_get[element])
		except:
			dic.update({element: default })
			dic.update({"s_"+element: None})
			return False
		else:
			if ee in liste:
				dic.update({element: ee })
				dic.update({"s_"+element: "="})
				return True
			else:
				dic.update({element: default })
				dic.update({"s_"+element: None})
				return False
	else:
		dic.update({element: default })
		dic.update({"s_"+element: None})
		return False
def param_as_in_list_str(request_get, dic, element, liste, default=None):
	"param est un str dans une liste"
	if request_get.has_key(element) and request_get[element] != "":
		if request_get[element] in liste:
			dic.update({element: request_get[element] })
			dic.update({"s_"+element: "="})
			return True
		else:
			dic.update({element: default })
			dic.update({"s_"+element: None})
			return False
	else:
		dic.update({element: default })
		dic.update({"s_"+element: None})
		return False
def param_as_str(request_get, dic, element, default=None):
	"param est un str"
	if request_get.has_key(element) and request_get[element] != "":
		if request_get[element][:2] in (">=", "<="):
			dic.update({element: request_get[element][2:] })
			dic.update({"s_"+element: request_get[element][:2]})
		elif request_get[element][:1] in ("=", ">", "<"):
			dic.update({element: request_get[element][1:] })
			dic.update({"s_"+element: request_get[element][:1]})
		else:
			dic.update({element: request_get[element]})
			dic.update({"s_"+element: None})
		return True
	else:
		dic.update({element: default })
		dic.update({"s_"+element: None})
		return False
def param_as_bool(request_get, dic, element, default=None):
	"param est un bool"
	if request_get.has_key(element):
		if request_get[element] == "on":
			dic.update({element:True})
			dic.update({"s_"+element: "="})
		else:
			dic.update({element:False})
			dic.update({"s_"+element: "="})
	else:
		if len(request_get) == 0:
			dic.update({element:default})
			dic.update({"s_"+element: "="})
		else:
			dic.update({element:False})
			dic.update({"s_"+element: "="})
def param_as_int(request_get, dic, element, default=None):
	"param est un int"
	if request_get.has_key(element) and request_get[element] != "":
		try:
			if request_get[element][:2] in (">=", "<="):
				dic.update({element: int(request_get[element][2:]) })
				dic.update({"s_"+element: request_get[element][:2]})
			elif request_get[element][:1] in ("=", ">", "<"):
				dic.update({element: int(request_get[element][1:]) })
				dic.update({"s_"+element: request_get[element][:1]})
			else:
				dic.update({element: int(request_get[element]) })
				dic.update({"s_"+element: None})
			return True
		except:
			dic.update({element: default })
			dic.update({"s_"+element: None})
			return False
	else:
		dic.update({element: default })
		dic.update({"s_"+element: None})
		return False
def param_as_float(request_get, dic, element, default=None):
	"param est un float"
	if request_get.has_key(element) and request_get[element] != "":
		try:
			if request_get[element][:2] in (">=", "<="):
				dic.update({element: float(request_get[element][2:]) })
				dic.update({"s_"+element: request_get[element][:2]})
			elif request_get[element][:1] in ("=", ">", "<"):
				dic.update({element: float(request_get[element][1:]) })
				dic.update({"s_"+element: request_get[element][:1]})
			else:
				dic.update({element: float(request_get[element]) })
				dic.update({"s_"+element: None})
			return True
		except:
			dic.update({element: default })
			dic.update({"s_"+element: None})
			return False
	else:
		dic.update({element: default })
		dic.update({"s_"+element: None})
		return False
def param_as_date_time(request_get, dic, element, format_date_time, format_date, default=None):
	"param est un datetime"
	if request_get.has_key(element) and request_get[element] != "":
		try:
			if request_get[element][:2] in (">=", "<="):
				dic.update({element: datetime.datetime.strptime(request_get[element][2:], format_date_time) })
				dic.update({"s_"+element: request_get[element][:2]})
			elif request_get[element][:1] in ("=", ">", "<"):
				dic.update({element: datetime.datetime.strptime(request_get[element][1:], format_date_time) })
				dic.update({"s_"+element: request_get[element][:1]})
			else:
				dic.update({element: datetime.datetime.strptime(request_get[element], format_date_time) })
				dic.update({"s_"+element: None})
			return True
		except:
			try:
				if request_get[element][:2] in (">=", "<="):
					dic.update({element: datetime.datetime.strptime(request_get[element][2:], format_date) })
					dic.update({"s_"+element: request_get[element][:2]})
				elif request_get[element][:1] in ("=", ">", "<"):
					dic.update({element: datetime.datetime.strptime(request_get[element][1:], format_date) })
					dic.update({"s_"+element: request_get[element][:1]})
				else:
					dic.update({element: datetime.datetime.strptime(request_get[element], format_date) })
					dic.update({"s_"+element: None})
				return True
			except:
				dic.update({element: default })
				dic.update({"s_"+element: None})
				return False
	else:		
		dic.update({element: default })
		dic.update({"s_"+element: None})
		return False
def param_as_data(request_get, dic, element, clas, default=None):
	"param est un id pour obtenir un oblet"
	if request_get.has_key(element) and request_get[element] != "" and request_get[element] != "0" and request_get[element] != 0:
		try:
			dic.update({element: clas.objects.get(pk=int(request_get[element])) })
			dic.update({"s_"+element: "="})
		except:
			dic.update({element: default })
			dic.update({"s_"+element: None})
	else:
		dic.update({element: default })
		dic.update({"s_"+element: None})

def objet_set_element(objet, dic, element, set_none=False):
	"Enregistre un element s'il n'est pas null"
	if dic[element] != None or set_none == True:
		objet.__setattr__(element, dic[element])

def dic_element_is(dic, element, param, default=None):
	"Réduit un objet a un élément"
	if dic.has_key(element) and dic[element] != None:
		dic.update({element : dic[element].__getattribute__(param) })
	else:
		dic.update({element : default })

def dic_element_as_unicode(dic, element, param=None, default=None):
	"Prends l'element ou le param de l'element, le convertie en unicode et ajoute le filtre"
	if dic.has_key(element) and dic[element] != None:
		if param == None:
			a = dic[element]
		else:
			a = dic[element].__getattribute__(param)
		if type(dic[element]) in ('StringType', 'StringTypes', 'UnicodeType'):
			b = a
		else:
			b = unicode(a)
		if dic.has_key("s_"+element) and dic["s_"+element] != None:
			dic.update({element : dic["s_"+element] + b })
		else:
			dic.update({element : b })
	else:
		dic.update({element : None })
def dic_element_is_str(dic, element, param=None, default=None):
	"Prends l'element ou le param de l'element, le convertie en str et ajoute le filtre"
	if dic.has_key(element) and dic[element] != None:
		if param == None:
			a = dic[element]
		else:
			a = dic[element].__getattribute__(param)
		if type(dic[element]) in ('StringType', 'StringTypes', 'UnicodeType'):
			b = a
		else:
			b = str(a)
		if dic.has_key("s_"+element) and dic["s_"+element] != None:
			dic.update({element : dic["s_"+element] + b })
		else:
			dic.update({element : b })
	else:
		dic.update({element : None })
def dic_element_is_str_date_time(dic, element, format_date_time, default=None):
	"Convertie une date en str suivant un format"
	if dic.has_key(element) and dic[element] != None:
		if dic.has_key("s_"+element) and dic["s_"+element] != None:
			dic.update({ element : dic["s_"+element] + dic[element].strftime(format_date_time) })
		else:
			dic.update({ element : dic[element].strftime(format_date_time) })
	else:
		if default == None:
			dic.update({ element : None })
		else:
			dic.update({ element : default.strftime(format_date_time) })


def get_objet_param(objet, dic, element, default=None):
	"Prend le paramètre d'un objet et le place d'une dic"
	dic.update({element: objet.__getattribute__(element) })
def get_objet_objet_param(objet, dic, element, param, default=None):
	"Prend le paramètre d'un objet d'un objet et le place d'une dic"
	if objet.__getattribute__(element) != None:
		dic.update({element: objet.__getattribute__(element).__getattribute__(param) })
def get_objet_param_is_date_time_str(objet, dic, element, format_date_time, default=None):
	"Prend la date d'un objet et le place d'une dicen str"
	if objet.__getattribute__(element) != None:
		dic.update({element: objet.__getattribute__(element).strftime(format_date_time) })
def check_limit(request_get, dic, nbr_ligne=100):
	if request_get.has_key("limit_du"):
		dic.update({"limit_du":int(request_get["limit_du"])})
	else:
		dic.update({"limit_du":0})
	if request_get.has_key("limit_au"):
		dic.update({"limit_au":int(request_get["limit_au"])})
	else:
		dic.update({"limit_au":nbr_ligne})
	if request_get.has_key("suivant"):
		if dic["limit_au"] <= dic["limit_du"]:
			pas = dic["limit_au"]
			dic["limit_au"] = dic["limit_du"] + pas
		else:
			pas = dic["limit_au"] - dic["limit_du"]
			dic["limit_au"] += pas
			dic["limit_du"] += pas
	if request_get.has_key("recherche"):
		if dic["limit_au"] <= dic["limit_du"]:
			pas = dic["limit_au"]
			dic["limit_au"] = dic["limit_du"] + pas
		else:
			pas = dic["limit_au"] - dic["limit_du"]
			dic["limit_au"] = pas
			dic["limit_du"] = 0
def my_filter(guerry_set, dic, element):
	"Mon filtre perso d'objet"
	if dic.has_key(element) == True and dic[element] != None:
		if dic.has_key("s_"+element) == True:
			if dic["s_"+element] == "=":
				return guerry_set.filter(**{element:dic[element]})
			elif dic["s_"+element] == ">":
				return guerry_set.filter(**{element+"__gt":dic[element]})
			elif dic["s_"+element] == "<":
				return guerry_set.filter(**{element+"__lt":dic[element]})
			elif dic["s_"+element] == ">=":
				return guerry_set.filter(**{element+"__gte":dic[element]})
			elif dic["s_"+element] == "<=":
				return guerry_set.filter(**{element+"__lte":dic[element]})
			elif dic["s_"+element] == None:
				return guerry_set.filter(**{element+"__icontains":dic[element]})
			else:
				raise ValueError("Filtre invalide")
		raise ValueError("Element inconnu")
	return guerry_set


