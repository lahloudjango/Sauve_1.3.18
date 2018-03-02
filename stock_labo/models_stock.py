# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import MyFields
#from django.contrib.admin.widgets import AdminDateWidget
import datetime


# STOCK

class StockSiteInconnu(Exception):
	"""
	Le site de stockage est inconnu
	"""
	def __init__(self, *args, **kwargs):
		pass
class StockEntrepotInconnu(Exception):
	"""
	L'entrepôt de stockage est inconnu
	"""
	def __init__(self, *args, **kwargs):
		pass
class StockMagasinInconnu(Exception):
	"""
	Le magasin de stockage est inconnu
	"""
	def __init__(self, *args, **kwargs):
		pass

class StockSite(models.Model):
	"""
	Liste des sites de stockage
	"""
	code = models.CharField(max_length=30, unique=True, verbose_name="Code site")
	code.nom_colonne = "Site"
	code.nom_long = "Site de stockage"
	description = models.CharField(max_length=100, verbose_name="Description")
	description.nom_colonne = "Description"
	description.nom_long = "Description du site de stockage"
	def __unicode__(self):
		return "%s" %(self.description)
	def __str__(self):
		return ("[%s] %s" %(self.code, self.description)).encode("ascii", "replace")
	class Meta:
		ordering = ["code"]

class StockEntrepot(models.Model):
	"""
	Liste des entrepôt de stockage
	"""
	code = models.CharField(max_length=30, unique=True, verbose_name="Code site")
	code.nom_colonne = "Stock"
	code.nom_long = "Stockage"
	description = models.CharField(max_length=100, verbose_name="Description")
	description.nom_colonne = "Description"
	description.nom_long = "Description de l'entropot"
	def __unicode__(self):
		return "%s" %(self.description)
	def __str__(self):
		return ("[%s] %s" %(self.code, self.description)).encode("ascii", "replace")
	class Meta:
		ordering = ["code"]

class StockMagasin(models.Model):
	"""
	Liste des sites de stockage
	"""
	# Attention on fait référence à l'emplacement STOCK_MAGASIN_TYPE[3][0] pour la poubelle
	STOCK_MAGASIN_TYPE = (
		(10, "Stockage"),
		(20, "Navette"),
		(30, "Personnel"),
		(100, "Poubelle/Destruction"),
		)

	code = models.CharField(max_length=30, unique=True, verbose_name="Code magasin")
	code.nom_colonne = "Magasin"
	code.nom_long = "Magasin de stockage"
	description = models.CharField(max_length=100, verbose_name="Description")
	description.nom_colonne = "Description"
	description.nom_long = "Description du magasin"
	stock_magasin_type = models.IntegerField(choices=STOCK_MAGASIN_TYPE, default=10, verbose_name="Type de magasin")
	stock_magasin_type.nom_colonne = "Type magasin"
	stock_magasin_type.nom_long = "Type de magasin de stockage"
	def __unicode__(self):
		return "%s" %(self.description)
	def __str__(self):
		return ("[%s] %s" %(self.code, self.description)).encode("ascii", "replace")
	class Meta:
		ordering = ["code"]

class SiteEntrepotMagasin(models.Model):
	"""
	Liste d'association site-entrepot-magasin
	"""
	site = models.ForeignKey(StockSite, verbose_name="Site")
	entrepot = models.ForeignKey(StockEntrepot, verbose_name="Entrepot")
	magasin = models.ForeignKey(StockMagasin, verbose_name="Magasin")
	def nom_court(self):
		return "%s %s" %(self.entrepot.description, self.magasin.description)

	def __unicode__(self):
		return "[%s-%s-%s] %s %s %s" %(self.site.code, self.entrepot.code, self.magasin.code, self.site.description, self.entrepot.description, self.magasin.description)
	def __str__(self):
		return (self.__unicode__()).encode("ascii", "replace")
	class Meta:
		ordering = ["site", "entrepot", "magasin"]

