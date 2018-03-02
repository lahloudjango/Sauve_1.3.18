# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User
from django.contrib.auth.decorators import login_required


import types
import time
import datetime
import codecs
import os

from django.contrib.admin import models as django_models
from django.contrib.contenttypes.models import ContentType
import django.core.exceptions
import django.db

#from lib_linautom.python import oracle
import settings_oracle
import settings_default
import version

from django.core.urlresolvers import reverse

from django import forms as django_forms

from formss import *
from classs import *

from lib_linautom.python.debug_tools import print_ascii, whatisit, dump_env
from lib_linautom.python.django_tools import etiquette_print, make_addr_param, Table, split_string

from stock_labo.models_user import UnitMasse, UserPreference


def get_user_param(user):
	try:
		return UserPreference.objects.get(user=user)
	except django.core.exceptions.ObjectDoesNotExist:
		None

def format_list_param_user(list_param_user):
	list_name = []
	for p in list_param_user:
		list_name.append("[%s] %s %s" %(unicode(p.user.username), unicode(p.user.first_name), unicode(p.user.last_name)))
	return "\n".join(list_name)

def get_site_entrepot_magasin_users(site, entrepot, magasin):
	return UserPreference.objects.filter(site_perso=site, entrepot_perso=entrepot, magasin_perso=magasin)

class OracleParamInconnu(Exception):
	"""
	Paramètre oracle inconnu
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")

def multi_file_backups(dossier, fichier_base):
	fichier = []
	for f in os.listdir(dossier):
		if f.startswith(fichier_base):
			fichier.append(f)
	fichier.sort(reverse=True)
	i = len(fichier)
	extension=".%%0%dd" %(len(str(i)))
	print fichier
	for f in fichier:
		print dossier+f, dossier+fichier_base+extension %(i)
		os.rename(dossier+f, dossier+fichier_base+extension %(i))
		i -= 1                                                                                                                                                           

def get_batch_info(batch):
	"""
	Recherche les info formule roxane
	SELECT
		c.batch_number      AS BATCH_NUMBER,
		c.xinumber          AS CODE,
		trim(c.frmlname)    AS DESCRIPTION,
		c.profilenumber     AS PROJET,
		cust.aliasname      AS CLIENT,
		ka.keyaccountname   AS CLIENT_KA
	FROM pmis_apps.his_frml_comphdr              c
		LEFT JOIN pmis_master.gpmis_projects_cl  p     ON p.projectnumber = c.profilenumber
		LEFT JOIN pmis_master.gpmis_customer_dtl cust  ON cust.custid = p.custid
		LEFT JOIN pmis_master.gpmis_customer     ka    ON ka.keyaccountid = cust.keyaccountid
	WHERE 
		c.batch_number = '20170630085310000105'
		AND rownum < 10
	"""
	if version.status_developement["oracle"] == "onet_test" or version.status_developement["oracle"] == "onet_prod":
		o=oracle.Oracle()
		param_oracle = version.status_developement["oracle"]
		o.open(**DATABASES_ORACLE[param_oracle])
		querry = """
		SELECT
			c.batch_number      AS BATCH_NUMBER,
			c.xinumber          AS CODE,
			trim(c.frmlname)    AS DESCRIPTION,
			c.profilenumber     AS PROJET,
			cust.aliasname      AS CLIENT,
			ka.keyaccountname   AS CLIENT_KA
		FROM pmis_apps.his_frml_comphdr              c
			LEFT JOIN pmis_master.gpmis_projects_cl  p     ON p.projectnumber = c.profilenumber
			LEFT JOIN pmis_master.gpmis_customer_dtl cust  ON cust.custid = p.custid
			LEFT JOIN pmis_master.gpmis_customer     ka    ON ka.keyaccountid = cust.keyaccountid
		WHERE 
			c.batch_number = '%s'
			AND rownum < 10
		""" %(batch)
		print querry
		oracle_batch = o.execute(querry)
		print oracle_batch
		o.close()
		return oracle_batch
	else:
		raise OracleParamInconnu()

def get_oracle_info(client=None, client_ka=None, projet=None, group_by=None, limit=None, exact=False):
	"""
	Recherche du client, client_ka, projet
	client : le nom du client contient
	client_ka : le nom client_ka contient
	projet : le N° de projet contient
	group_by : nom du champ ou l'on veux une entrée unique
	limit : nombre de résultat max
	SELECT 
		c.profilenumber     AS PROJET,
		cust.aliasname      AS CLIENT,
		ka.keyaccountname   AS CLIENT_KA
	FROM pmis_apps.his_frml_comphdr              c
		LEFT JOIN pmis_master.gpmis_projects_cl  p     ON p.projectnumber = c.profilenumber
		LEFT JOIN pmis_master.gpmis_customer_dtl cust  ON cust.custid = p.custid
		LEFT JOIN pmis_master.gpmis_customer     ka    ON ka.keyaccountid = cust.keyaccountid
	WHERE c.profilenumber = '17-11732/1'
		AND rownum < 10
	"""
	where_and = []
	if version.status_developement["oracle"] == "onet_test" or version.status_developement["oracle"] == "onet_prod":
		o=oracle.Oracle()
		param_oracle = version.status_developement["oracle"]
		o.open(**DATABASES_ORACLE[param_oracle])
		querry = "SELECT"
		if group_by == "client":
			if querry != "SELECT":
				querry += ","
		elif group_by == "client_ka":
			if querry != "SELECT":
				querry += ","
			querry += " DISTINCT"
		elif group_by == "projet":
			if querry != "SELECT":
				querry += ","
			querry += " DISTINCT"
		querry += " cust.aliasname as CLIENT"
		querry += ","
		querry += " ka.keyaccountname as CLIENT_KA"
		querry += ","
		querry += " c.profilenumber as PROJET"

		#if group_by != None:
		#	querry += ", SUM(1) as NOMBRE"
		querry += """
		FROM pmis_apps.his_frml_comphdr               c
			LEFT JOIN pmis_master.gpmis_projects_cl   p     ON p.projectnumber = c.profilenumber
			LEFT JOIN pmis_master.gpmis_customer_dtl  cust  ON cust.custid = p.custid
			LEFT JOIN pmis_master.gpmis_customer      ka    ON ka.keyaccountid = cust.keyaccountid
		"""

		if client != None and client != "":
			if exact == True:
				where_and.append("cust.aliasname = \'%s\'" %(client.replace("'","''")))
			else:
				where_and.append("REGEXP_LIKE(cust.aliasname, \'%s\', 'i')" %(client.replace("'","''")))
		if client_ka != None and client_ka != "":
			if exact == True:
				where_and.append("ka.keyaccountname = \'%s\'" %(client_ka.replace("'","''")))
			else:
				where_and.append("REGEXP_LIKE(ka.keyaccountname, \'%s\', 'i')" %(client_ka.replace("'","''")))
		if projet != None and projet != "":
			if exact == True:
				where_and.append("c.profilenumber = \'%s\'" %(projet.replace("'","''")))
			else:
				where_and.append("REGEXP_LIKE(c.profilenumber, \'%s\', 'i')" %(projet.replace("'","''")))


		if len(where_and) > 0:
			querry += " WHERE "
			querry += " AND ".join(where_and)

		#if group_by == "client":
		#	querry += " GROUP BY cust.aliasname"
		#elif group_by == "client_ka":
		#	querry += " GROUP BY ka.keyaccountname"
		#elif group_by == "projet":
		#	querry += " GROUP BY c.profilenumber"

		if limit != None:
			querry = "SELECT * FROM ( %s ) WHERE ROWNUM <= %s" %(querry, limit)

		print querry
		oracle_client = o.execute(querry)
		print oracle_client
		o.close()
		return oracle_client
	else:
		raise OracleParamInconnu()

def csv_dic(nom_fichier, fin_de_ligne="\n", encoding="utf-8", separateur=";"):
	"""
	Lecture d'un dico et formation d'une liste de dictionnaire avec les ligne de donnée
	"""
	f = codecs.open(nom_fichier, "r", encoding=encoding)
	fichier_import = f.read().split(fin_de_ligne)
	f.close()

	col_liste_nom = []

	h = fichier_import.pop(0)
	col_liste_nom = h.split(separateur)
	col_liste_num = range(0, len(col_liste_nom))
	resultat_dict = []
	for lf in fichier_import:
		if lf == "":
			continue
		ligne = lf.split(separateur)
		l = {}
		for colonne in col_liste_num:
			l.update({col_liste_nom[colonne]:ligne[colonne]})
		resultat_dict.append(l)
	return resultat_dict

def log_auto(user, obj, flag, info):
	"""
	Fonction de login
	user : instance user pour l'action
	obj : object affecté par l'action
	falg : c=ADDITION, c=CHANGE, d=DELETION
	info : message text de complément
	"""
	log = django_models.LogEntry()
	log.action_time = datetime.datetime.now()							#La date et l’heure de l’action.
	log.user = user														#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
	log.content_type = ContentType.objects.get_for_model(obj)			#Le type de contenu (ContentType) de l’objet modifié.
	log.object_id = obj.id												#La représentation textuelle de la clé primaire de l’objet modifié.
	log.object_repr = unicode(obj)										#La représentation repr() de l’objet après sa modification.
	if flag == "a":
		log.action_flag = django_models.ADDITION 						#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
	elif flag == "c":
		log.action_flag = django_models.CHANGE 							#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
	elif flag == "d":
		log.action_flag = django_models.DELETION 						#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
	else:
		ValueError("flag must be in a, c, d")
	log.change_message = info											#Description de la modification
	log.save()

class Headers(object):
	"""
	Construit la structure pour l'entête des pages
	"""
	def __init__(self, page, user, panier):
		"""
		Initalise la structure pour l'entête des pages
		"""
		self.header = {}
		self.header.update({"page" : page})
		self.header.update({"site" : "Takasago Paris"})
		self.header.update({"user" : user})
		self.header.update({"panier" : panier})
		self.header.update({"apps" : "Gestionnaire de Stock %s" %(version.status_developement["info"])})
		self.header.update({"date" : time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())})

	def get_headers(self):
		return self.header

class Onglets(object):
	"""
	Construit la structure pour les onglets
	"""
	def __init__(self, user):
		"""
		Initalise la structure pour les onglets
		"""
		self.onglet = []
		o = {}
		o.update({"label" : "Article"})
		o.update({"title" : "Liste des articles (formules-essais-matière première"})
		o.update({"href" : "/django/stock_labo/nomenclature/"})
		o.update({"actif" : False})
		o.update({"visible" : user.has_perm("stock_labo.article")})
		self.onglet.append(o)
		o = {}
		o.update({"label" : "Recherche"})
		o.update({"title" : "Recherche de contenant"})
		o.update({"href" : "/django/stock_labo/recherche/"})
		o.update({"actif" : False})
		o.update({"visible" : user.has_perm("stock_labo.recherche")})
		self.onglet.append(o)
		o = {}
		o.update({"label" : "Mouvement"})
		o.update({"title" : "Déplacement et suppression de contenant"})
		o.update({"href" : "/django/stock_labo/mouvement/"})
		o.update({"actif" : False})
		o.update({"visible" : user.has_perm("stock_labo.mouvement")})
		self.onglet.append(o)
		o = {}
		o.update({"label" : "Panier"})
		o.update({"title" : "Elements du panier"})
		o.update({"href" : "/django/stock_labo/panier/"})
		o.update({"actif" : False})
		o.update({"visible" : user.has_perm("stock_labo.panier")})
		self.onglet.append(o)
		o = {}
		o.update({"label" : "Stock de travail"})
		o.update({"title" : "Elements de mon stock personnel de travail"})
		o.update({"href" : "/django/stock_labo/stock_perso/"})
		o.update({"actif" : False})
		o.update({"visible" : user.has_perm("stock_labo.stock_perso")})
		self.onglet.append(o)
		o = {}
		o.update({"label" : "Mes Paramètres"})
		o.update({"title" : "Praramètre personel"})
		o.update({"href" : "/django/stock_labo/param_utilisateur/"})
		o.update({"actif" : False})
		o.update({"visible" : user.has_perm("stock_labo.param_perso")})
		self.onglet.append(o)
		o = {}
		o.update({"label" : "Import"})
		o.update({"title" : "Importer un fichier de donnée"})
		o.update({"href" : "/django/stock_labo/entree/"})
		o.update({"actif" : False})
		o.update({"visible" : user.has_perm("stock_labo.import")})
		self.onglet.append(o)
		o = {}
		o.update({"label" : "Réception"})
		o.update({"title" : "Réception des contenants"})
		o.update({"href" : "/django/stock_labo/reception/"})
		o.update({"actif" : False})
		o.update({"visible" : user.has_perm("stock_labo.reception")})
		self.onglet.append(o)
		o = {}
		o.update({"label" : "Sample lab"})
		o.update({"title" : "Module d'administration django"})
		o.update({"href" : "/django/stock_labo/sample_lab/"})
		o.update({"actif" : False})
		o.update({"visible" : user.has_perm("stock_labo.sample_lab")})
		self.onglet.append(o)
		o = {}
		o.update({"label" : "Flash"})
		o.update({"title" : "Engregistrement point éclaire"})
		o.update({"href" : "/django/stock_labo/flash/"})
		o.update({"actif" : False})
		o.update({"visible" : user.has_perm("stock_labo.flash")})
		self.onglet.append(o)
		o = {}
		o.update({"label" : "Log"})
		o.update({"title" : "Suivie d'un article, lot, contenant"})
		o.update({"href" : "/django/stock_labo/log/"})
		o.update({"actif" : False})
		o.update({"visible" : user.has_perm("stock_labo.log")})
		self.onglet.append(o)
		o = {}
		o.update({"label" : "Module admin"})
		o.update({"title" : "Module d'administration django"})
		o.update({"href" : "/django/admin/"})
		o.update({"actif" : False})
		o.update({"visible" : user.is_staff})
		self.onglet.append(o)
		o = {}
		o.update({"label" : "<img src=\"/static/svg/system-log-out.svg\" height=\"20\" alt=\"Ajouter\"/>"})
		o.update({"title" : "Déconnexion"})
		o.update({"href" : "/django/utilisateur/logout/"})
		o.update({"actif" : False})
		o.update({"visible" : True})
		self.onglet.append(o)
		o = {}
		o.update({"label" : "<img src=\"/static/svg/go-home.svg\" height=\"20\" alt=\"Ajouter\"/>"})
		o.update({"title" : "Menu principal"})
		o.update({"href" : "/django/"})
		o.update({"actif" : False})
		o.update({"visible" : True})
		self.onglet.append(o)

	def get_onglets(self):
		return self.onglet

	def set_actif_by_id(self, id_onglet):
		"""
		Active un onglet en utilisart son ID
		"""
		i = 0
		while i < len(self.onglet):
			if i == id_onglet:
				self.onglet[i]["actif"] = True
			else:
				self.onglet[i]["actif"] = False
			i += 1

class Liste(object):
	"""
	Construit la structure pour les listes
	"""
	class Ligne(object):
		"""
		Construit la structure pour une ligne
		"""
		def __init__(self):
			"""
			Crée une nouvelle ligne
			"""
			self.ligne = {}
			self.ligne.update({"paire" : None})
			self.ligne.update({"cellules" : []})

		def add_cellule(self, label, title="", href=None, width=None, cellule_id=None, onclick=None, style=None):
			"""
			Ajute une cellule à la ligne
			"""
			cellule = {}
			cellule.update({"label" : label})
			cellule.update({"title" : title})
			cellule.update({"href" : href})
			cellule.update({"width" : width})
			cellule.update({"cellule_id" : cellule_id})
			cellule.update({"onclick" : onclick})
			cellule.update({"style" : style})
			self.ligne["cellules"].append(cellule)

		def get_ligne(self):
			return self.ligne

	def __init__(self, caption="Liste 1", summary= "Liste1", p=True):
		"""
		Initalise la structure pour les listes
		"""
		self.liste = {}
		self.liste.update({"p" : p})
		self.liste.update({"n_ligne_affiche" : 0})
		self.liste.update({"n_ligne_limit" : 0})
		self.liste.update({"n_ligne_total" : 0})
		self.liste.update({"summary" : summary})
		self.liste.update({"caption" : caption})
		self.liste.update({"headers" : []})
		self.liste.update({"liste" : []})

	def add_headers(self, h):
		"""
		défini les entêtes de colonne dans le même format de Ligne
		"""
		self.liste["headers"].append(h)

	def add_ligne(self, ligne):
		"""
		ajoute une ligne à la liste
		"""
		if len(self.liste["liste"])%2 == 0:
			ligne["paire"] = True
		else:
			ligne["paire"] = False
		self.liste["liste"].append(ligne)

	def set_print(self, p=True):
		"""
		Active/Désactive l'affichage
		"""
		self.liste["p"] = p

	def get_liste(self):
		return self.liste

class Boutons(object):
	"""
	Construit la structure pour les Boutons
	"""
	def __init__(self, p=True):
		"""
		Initalise la structure pour les Boutons
		"""
		self.bouton = {}
		self.bouton.update({"p" : p})
		self.bouton.update({"liste" : []})

	def add_bouton(self, label, title="", href="", new_windows=False):
		"""
		Ajoute un nouveau bouton
		"""
		b = {}
		b.update({"label" : label})
		b.update({"title" : title})
		b.update({"href" : href})
		b.update({"new_windows" : new_windows})
		self.bouton["liste"].append(b)

	def set_print(self, p=True):
		"""
		Active/Désactive l'affichage
		"""
		self.bouton["p"] = p

	def get_boutons(self):
		return self.bouton

