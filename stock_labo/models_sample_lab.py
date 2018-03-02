# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import MyFields
#from django.contrib.admin.widgets import AdminDateWidget
import datetime

from django.contrib.auth.models import User
import models_stock
import models_nomenclature
import models_user
from django.contrib.admin import models as django_models
from django.contrib.contenttypes.models import ContentType

from fonction import *


class SampleLabStat(models.Model):
	"""
	Table de statistique sample lab
	"""
	#Attention les clefs sont utilisé comme index en base de données
	TYPE_DEMANDE = { 
	"" : "---------",
	1 : "EDT (eau de toilette)",
	2 : "Présentation marketing",
	3 : "Make orders",
	4 : "Solution MP",
	5 : "Oil",
	}

	projet = MyFields.CharField(max_length=50, blank=True, default=None, null=True)
	client = MyFields.CharField(max_length=50, blank=True, default=None, null=True)
	client_ka = MyFields.CharField(max_length=50, blank=True, default=None, null=True)
	date_realisation = MyFields.DateField(blank=False, default=None, null=True)
	responsable = models.ForeignKey(User, blank=False, default=None, null=True, verbose_name="Responsable fabrication")
	nbr_echantillon = MyFields.IntegerField(blank=False, default=None, null=True, verbose_name="Nbr Échantillon")
	type_demande = MyFields.IntegerField(choices=TYPE_DEMANDE.items(), blank=False, default=None, null=True, verbose_name="Type de demande")

	def __unicode__(self):
		return "[%s] %s : %d" %(self.projet, self.client, self.nbr_echantillon)
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")
	class Meta:
		ordering = ["date_realisation"]



