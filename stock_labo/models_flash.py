# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import MyFields
#from django.contrib.admin.widgets import AdminDateWidget
import traceback

import models_contenant
import models_stock
import models_user
import models_nomenclature

from fonction import *

import django.core.exceptions
import django.db
#except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
#except django.db.IntegrityError:



class FlashPointInconnu(Exception):
	"""
	Aucune valeur de point éclair connu
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")


def get_flash_point(contenant_code=None, nomenclature_code=None, nomenclature_description=None, nomenclature_lot_code=None):
	"""
	Recherche point éclair
	"""
	if contenant_code != None:
		cont = models_contenant.Contenant.objects.filter(code=contenant_code)
		if len(cont) > 0:
			nomenclature_lot_code = cont[0].nomenclature_lot.code

	if nomenclature_lot_code != None:
		fp_hist = FlashPointHist.objects.filter(nomenclature_lot_code__icontains=nomenclature_lot_code)
		if len(fp_hist) > 0:
			return fp_hist
		else:
			raise FlashPointInconnu()
	elif nomenclature_code != None:
		fp_hist = FlashPointHist.objects.filter(nomenclature_code__icontains=nomenclature_code)
		if len(fp_hist) > 0:
			return fp_hist
		else:
			raise FlashPointInconnu()
	elif nomenclature_description != None:
		fp_hist = FlashPointHist.objects.filter(nomenclature_description__icontains=nomenclature_description)
		if len(fp_hist) > 0:
			return fp_hist
		else:
			raise FlashPointInconnu()
	else:
		raise FlashPointInconnu()

def set_flash_point(nomenclature_lot, flash_point, date_flash_point, user):
	"""
	enregiste en point éclair
	"""
	nomenclature_lot.flash_point = flash_point
	nomenclature_lot.date_flash_point = date_flash_point
	nomenclature_lot.responsable_flash_point = user
	nomenclature_lot.save()
	log_auto(user=user, obj=nomenclature_lot, flag="c", info="set_flash_point(%s)" %(nomenclature_lot))
	nomenclature_lot.nomenclature.flash_point = flash_point
	nomenclature_lot.nomenclature.date_flash_point = date_flash_point
	nomenclature_lot.nomenclature.responsable_flash_point = user
	nomenclature_lot.nomenclature.save()
	log_auto(user=user, obj=nomenclature_lot.nomenclature, flag="c", info="set_flash_point(%s)" %(nomenclature_lot.nomenclature))
	fp = FlashPointHist(nomenclature_code=nomenclature_lot.nomenclature.code,
			nomenclature_description=nomenclature_lot.nomenclature.description,
			nomenclature_lot_code=nomenclature_lot.code,
			date_flash_point=date_flash_point,
			flash_point=flash_point,
			responsable_flash_point_login=user.username
			)
	fp.save()
	log_auto(user=user, obj=fp, flag="a", info="set_flash_point(%s)" %(fp))

	nomenclature_lot_code.nom_colonne = "Lot"
	nomenclature_lot_code.nom_long = "Lot de la Formule/essai/matière première (30c)"
	date_flash_point = MyFields.DateField(default=None, blank=True, null=True, verbose_name="Date Flash")
	date_flash_point.nom_colonne = "Date flash"
	date_flash_point.nom_long = "Date de point éclair"
	date_flash_point.format_date_time = "%d/%m/%Y"
	flash_point = MyFields.FloatField(blank=True, default=None, null=True, verbose_name="Flash", help_text="°C")
	flash_point.nom_colonne = "Flash"
	flash_point.nom_long = "Point éclair"
	responsable_flash_point_login = MyFields.CharField(max_length=30, blank=True, default=None, null=True)
	responsable_flash_point_login.nom_colonne = "Responçable"
	responsable_flash_point_login.nom_long = "Responçable enregistrement point éclair"
	def __unicode__(self):
		return "[%s]%s/%s : %2f°C" %(self.nomenclature_code, self.nomenclature_description, self.nomenclature_lot_code, self.flash_point)
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")

class FlashPointHist(models.Model):
	"""
	Historique des flash point
	"""
	nomenclature_code = MyFields.CharField(max_length=30, verbose_name="Code")
	nomenclature_code.nom_colonne = "Code"
	nomenclature_code.nom_long = "Code de la Formule/essai/matière première (30c)"
	nomenclature_description = MyFields.CharField(max_length=100, blank=True, default="", verbose_name="Description")
	nomenclature_description.nom_colonne = "Description"
	nomenclature_description.nom_long = "Nom de la Formule/essai/matière première (100c)"
	nomenclature_lot_code = MyFields.CharField(max_length=30, verbose_name="Lot")
	nomenclature_lot_code.nom_colonne = "Lot"
	nomenclature_lot_code.nom_long = "Lot de la Formule/essai/matière première (30c)"
	date_flash_point = MyFields.DateField(default=None, blank=True, null=True, verbose_name="Date Flash")
	date_flash_point.nom_colonne = "Date flash"
	date_flash_point.nom_long = "Date de point éclaire"
	date_flash_point.format_date_time = "%d/%m/%Y"
	flash_point = MyFields.FloatField(blank=True, default=None, null=True, verbose_name="Flash", help_text="°C")
	flash_point.nom_colonne = "Flash"
	flash_point.nom_long = "Point éclaire"
	responsable_flash_point_login = MyFields.CharField(max_length=30, blank=True, default=None, null=True)
	def __unicode__(self):
		return "[%s]%s/%s : %2f°C" %(self.nomenclature_code, self.nomenclature_description, self.nomenclature_lot_code, self.flash_point)
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")

class FlashPointMachine(models.Model):
	"""
	Emplacement Flash
	"""
	class Meta:
		ordering = ["machine_empl_code"]
	machine_empl_code = MyFields.CharField(max_length=30, verbose_name="Code")
	machine_empl_code.nom_colonne = "Code emplacement flash"
	machine_empl_code.nom_long = "Code emplacement sur machine flach (30c)"
	machine_empl_description = MyFields.CharField(max_length=100, blank=True, default="", verbose_name="Description")
	machine_empl_description.nom_colonne = "Description emplacement machine flash"
	machine_empl_description.nom_long = "Deescription de l'emplacement sur la machime flash (100c)"
	nomenclature_lot = models.ForeignKey(models_nomenclature.NomenclatureLot, blank=True, default=None, null=True, verbose_name="Article/Lot")
	def __unicode__(self):
		if self.nomenclature_lot == None:
			return "[%s]%s : vide" %(self.machine_empl_code, self.machine_empl_description)
		else:
			return "[%s]%s : %s" %(self.machine_empl_code, self.machine_empl_description, self.nomenclature_lot.nomenclature)
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")


















