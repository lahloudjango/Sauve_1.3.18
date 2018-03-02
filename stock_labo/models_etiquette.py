# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import MyFields
#from django.contrib.admin.widgets import AdminDateWidget
import datetime

from lib_linautom.python import etiquette


IMPRESSION_ZPL_ORIENTATION = etiquette.Print.IMPRESSION_ZPL_ORIENTATION
IMPRESSION_DETAIL_TYPE = etiquette.Print.IMPRESSION_DETAIL_TYPE
IMPRESSION_FORMAT = etiquette.Print.IMPRESSION_FORMAT
IMPRESSION_POLICE = etiquette.Print.IMPRESSION_POLICE






class ImpressionImprimanteParam(models.Model):
	"""
	Liste de parametrage imprimante
	"""
	description = models.CharField(max_length=100)
	def __unicode__(self):
		return "%s" %(self.description)
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")
	class Meta:
		ordering = ["description"]

class ImpressionImprimanteParamDetail(models.Model):
	"""
	Detail liste de parametrage imprimante
	"""
	description = MyFields.CharField(verbose_name="nom du champs", max_length=100, blank=True, default="")
	impression_imprimante_param = models.ForeignKey(ImpressionImprimanteParam)
	champ_data = MyFields.CharField(verbose_name="code imprimante", max_length=100, blank=True, default=None, null=True)
	def __unicode__(self):
		return "%s(%s)" %(self.description, self.impression_imprimante_param.description)
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")
	class Meta:
		ordering = ["impression_imprimante_param"]

class Impression(models.Model):
	"""
	Liste des models d'etiquette ( mise en pages )
	"""
	description = models.CharField(max_length=100)
	etiquette_format = models.IntegerField(choices=IMPRESSION_FORMAT.items(), verbose_name="Format de l'impression")
	imp_auto = models.BooleanField(default=False, verbose_name="Impression automatique", help_text="Impression sans apperçu")
	def __unicode__(self):
		if self.imp_auto:
			return "%s - %s - imp. auto" %(self.description, IMPRESSION_FORMAT[self.etiquette_format])
		else:
			return "%s - %s - aperçu av. imp." %(self.description, IMPRESSION_FORMAT[self.etiquette_format])
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")
	class Meta:
		ordering = ["description"]

class ImpressionImprimante(models.Model):
	"""
	Liste des imprimantes
	"""
	description = models.CharField(max_length=100)
	largeur = models.IntegerField(verbose_name="Largeur de l'étiquette/page", default="210", help_text="mm")
	longueur = models.IntegerField(verbose_name="Longueur de l'étiquette/page", default="297", help_text="mm")
	resolution = models.IntegerField(verbose_name="Résolution de l'imprimante (Zebra)", default="300", help_text="dpi")
	imprimante_port = models.CharField(max_length=100, blank=True, default=None, null=True, help_text="Inutile pour les format PDF")
	param_pre_impression = models.ForeignKey(ImpressionImprimanteParam, related_name="param_pre_impression")
	param_post_impression = models.ForeignKey(ImpressionImprimanteParam, related_name="param_prost_impression")
	def __unicode__(self):
		return "%s - %s" %(self.description, self.imprimante_port)
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")
	class Meta:
		ordering = ["description"]

class ImpressionDetail(models.Model):
	"""
	Detail de mise en pages des etiquettes
	"""
	description = MyFields.CharField(verbose_name="nom du champs", max_length=100, blank=True, default="")
	description.nom_colonne = None
	description.nom_long = None
	impression = models.ForeignKey(Impression)
	impression_detail_type = MyFields.IntegerField(verbose_name="Type de champ", default="1", choices=IMPRESSION_DETAIL_TYPE.items(), help_text="???")
	impression_detail_type.nom_colonne = None
	impression_detail_type.nom_long = None
	champ_data = MyFields.CharField(verbose_name="Donnée à imprimer", max_length=100, blank=True, default=None, null=True)
	champ_data.nom_colonne = None
	champ_data.nom_long = None
	pos_x = MyFields.IntegerField(verbose_name="Position en X", blank=True, default=None, null=True)
	pos_x.nom_colonne = None
	pos_x.nom_long = None
	pos_y = MyFields.IntegerField(verbose_name="Position Y", blank=True, default=None, null=True)
	pos_y.nom_colonne = None
	pos_y.nom_long = None
	police = MyFields.IntegerField(verbose_name="Police d'écriture", choices=IMPRESSION_POLICE.items(), blank=True, default=None, null=True)
	police.nom_colonne = None
	police.nom_long = None
	orientation = MyFields.IntegerField(verbose_name="Orientation du text", blank=True, default=None, null=True)
	orientation.nom_colonne = None
	orientation.nom_long = None
	param1 = MyFields.CharField(verbose_name="Parametre 1", max_length=30, blank=True, default=None, null=True)
	param1.nom_colonne = None
	param1.nom_long = None
	param2 = MyFields.CharField(verbose_name="Parametre 2", max_length=30, blank=True, default=None, null=True)
	param2.nom_colonne = None
	param2.nom_long = None
	couleur = MyFields.CharField(verbose_name="Couleur RVB + Alignement", help_text="0,0,0,L => 255,255,255,R", max_length=30, blank=True, default=None, null=True)
	couleur.nom_colonne = None
	couleur.nom_long = None
	def __unicode__(self):
		return "[%s] %s" %(self.impression, self.description)
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")
	class Meta:
		ordering = ["impression", "description"]








