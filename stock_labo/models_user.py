# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import MyFields
#from django.contrib.admin.widgets import AdminDateWidget
import datetime

from django.contrib.auth.models import User
import models_stock
import models_etiquette
import models_nomenclature

# USER


class UnitMasse(models.Model):
	"""
		Table des unités et des facteur de correspondante
		g : Gramme : 1
		kg : Kilo gramme : 0.001
		mg : Milli gramme : 1000
	"""
	code = models.CharField(max_length=30, unique=True, verbose_name="Code de l'unité")
	code.nom_colonne = "Code"
	code.nom_long = "Code de l'unité"
	description = models.CharField(max_length=100, verbose_name="Description")
	description.nom_colonne = "Description"
	description.nom_long = "Description de l'unitée d'affichage"
	facteur = models.FloatField(verbose_name="Facteur de convertion", help_text="Example: g  : Gramme : 1\
         kg : Kilogramme : 0.001\
         mg : Milligramme : 1000")
	facteur.nom_colonne = "Facteur"
	facteur.nom_long = "Facteur de conversion du gramme vers cette nouvelle unité"
	def __unicode__(self):
		return "[%s] %s : %.3f" %(self.code, self.description, self.facteur)
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")
	class Meta:
		ordering = ["facteur"]

class UserPreference(models.Model):
	"""
		Préférence utilisateur
	"""
	user = models.OneToOneField(User, verbose_name="Login Utilisateur")
	initial = models.CharField(max_length=5, blank=True, default="", verbose_name="Initial de la personne")
	initial.nom_colonne = "Initial"
	initial.nom_long = "Initial de la personne (5c)"
	unit_masse = models.ForeignKey(UnitMasse, verbose_name="Unité", default=1)
	site_perso = models.ForeignKey(models_stock.StockSite, verbose_name="Site personel par défaut", default=1)
	entrepot_perso = models.ForeignKey(models_stock.StockEntrepot, verbose_name="Stock personel par défaut", default=1)
	magasin_perso = models.ForeignKey(models_stock.StockMagasin, verbose_name="Magasin personel par défaut", default=1)
	emplacement_perso = models.CharField(max_length=30, blank=True, default="", verbose_name="Emplacement personel par défaut")
	emplacement_perso.nom_colonne = "Emplacement"
	emplacement_perso.nom_long = "Emplacement personel par défaut"
	etiquette_contenant = models.ForeignKey(models_etiquette.Impression, related_name="etiquette_contenant", verbose_name="Etiquette contenant", default=1)
	etiquette_contenant_imprimante = models.ForeignKey(models_etiquette.ImpressionImprimante, related_name="imprimante_etiquette_contenant", verbose_name="Imprimante étiquette contenant", default=1)
	etiquette_lot = models.ForeignKey(models_etiquette.Impression, related_name="etiquette_lot", verbose_name="Etiquette lot", default=1)
	etiquette_lot_imprimante = models.ForeignKey(models_etiquette.ImpressionImprimante, related_name="imprimante_etiquette_lot", verbose_name="Imprimante étiquette lot", default=1)
	etiquette_nomenclature = models.ForeignKey(models_etiquette.Impression, related_name="etiquette_nomenclature", verbose_name="Etiquette article", default=1)
	etiquette_nomenclature_imprimante = models.ForeignKey(models_etiquette.ImpressionImprimante, related_name="imprimante_etiquette_nomenclature", verbose_name="Imprimante étiquette nomenclature", default=1)
	etiquette_login = models.ForeignKey(models_etiquette.Impression, related_name="etiquette_login", verbose_name="Etiquette login", default=1)
	etiquette_login_imprimante = models.ForeignKey(models_etiquette.ImpressionImprimante, related_name="imprimante_etiquette_login", verbose_name="Imprimante étiquette login", default=1)
	etiquette_emplacement = models.ForeignKey(models_etiquette.Impression, related_name="etiquette_emplacement", verbose_name="Etiquette emplacement", default=1)
	etiquette_emplacement_imprimante = models.ForeignKey(models_etiquette.ImpressionImprimante, related_name="imprimante_etiquette_emplacement", verbose_name="Imprimante étiquette emplacement", default=1)
	etiquette_emplacement_machine_flash = models.ForeignKey(models_etiquette.Impression, related_name="etiquette_emplacement_machine_flash", verbose_name="Etiquette emplacement machine flash", default=1)
	etiquette_emplacement_machine_flash_imprimante = models.ForeignKey(models_etiquette.ImpressionImprimante, related_name="imprimante_etiquette_emplacement_machine_flash", verbose_name="Imprimante étiquette emplacement machine flash", default=1)
	def __unicode__(self):
		return "%s" %(unicode(self.user))
	def __str__(self):
		return ("[%s] %s-%s-%s-%s" %(unicode(self.user), self.site_perso.code, self.entrepot_perso.code, self.magasin_perso.code, self.emplacement_perso)).encode("ascii", "replace")
	class Meta:
		ordering = ["user"]

