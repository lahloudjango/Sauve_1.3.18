# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class CharField(models.CharField):
	"""
	Redefinition de models.CharField pour ajouter des propriétées personel
	"""
	nom_colonne = None
	nom_long = None

class TextField(models.TextField):
	"""
	Redefinition de models.CharField pour ajouter des propriétées personel
	"""
	nom_colonne = None
	nom_long = None

class FloatField(models.FloatField):
	"""
	Redefinition de models.CharField pour ajouter des propriétées personel
	"""
	nom_colonne = None
	nom_long = None

class DateTimeField(models.DateTimeField):
	"""
	Redefinition de models.CharField pour ajouter des propriétées personel
	"""
	nom_colonne = None
	nom_long = None
	format_date_time = "%Y-%m-%d %H:%M:%S"

class DateField(models.DateField):
	"""
	Redefinition de models.CharField pour ajouter des propriétées personel
	"""
	nom_colonne = None
	nom_long = None
	format_date_time = "%d/%m/%Y"

class IntegerField(models.IntegerField):
	"""
	Redefinition de models.CharField pour ajouter des propriétées personel
	"""
	nom_colonne = None
	nom_long = None

class BooleanField(models.BooleanField):
	"""
	Redefinition de models.CharField pour ajouter des propriétées personel
	"""
	nom_colonne = None
	nom_long = None


