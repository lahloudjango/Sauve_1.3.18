# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import MyFields
#from django.contrib.admin.widgets import AdminDateWidget 
import datetime

# LOG



class Log(models.Model):
	"""
	log des transaction/movement dans le stock
	"""
	LOG_MODULE = (
			( 0, "Menu principal"),
			( 1, "Sortie ( Stock => Navette )"),
			( 2, "Entrées ( Navette => Stock )"),
			( 3, "Recherche contenant"),
			( 4, "Création contenant"),
			( 5, "Destruction contenant"),
			( 6, "(Ré)Impressions étiquettes"),
			( 7, "Édition d'une fiche contenant"),
			( 8, "Dé-stockage"),
			( 9, "Déplacement"),
			( 99, "Deconnexion/Login"),
			)

	LOG_ACTION = (
			( 11, "Contenant Creation"),
			( 12, "Contenant Suppression"),
			( 13, "Contenant Déplacement"),
			( 14, "Contenant Modification"),

			( 21, "Matière Creation"),
			( 22, "Matière Suppression"),
			( 23, "Matière Modification"),

			( 31, "Nomenclature Creation"),
			( 32, "Nomenclature Suppression"),
			( 33, "Nomenclature Modification"),

			( 41, "Stock Site Creation"),
			( 42, "Stock Site Suppression"),
			( 43, "Stock Site Modification"),

			( 51, "Stock Magasin Creation"),
			( 52, "Stock Magasin Suppression"),
			( 53, "Stock Magasin Modification"),

			( 61, "Etiquette Creation"),
			( 62, "Etiquette Suppression"),
			( 63, "Etiquette Modification"),

			( 71, "Panier Creation"),
			( 72, "Panier Suppression"),
			( 73, "Panier Modification"),

			( 91, "Login"),
			( 92, "Logoff"),
			( 93, "Modification"),
			)

	LOG_LEVEL = (
			( 0, "Panic"),
			( 1, "Correction à la volé avant crache"),
			( 2, "Instabilité"),
			( 3, "Erreur Critique"),
			( 4, "Erreur"),
			( 5, "Alarme"),
			( 6, "Info"),
			( 7, "Info debug"),
			)
	"""
	KERN_EMERG 		"0" 	Emergency messages, system is about to crash or is unstable 							pr_emerg
	KERN_ALERT 		"1" 	Something bad happened and action must be taken immediately 							pr_alert
	KERN_CRIT 		"2" 	A critical condition occurred like a serious hardware/software failure 					pr_crit
	KERN_ERR 		"3" 	An error condition, often used by drivers to indicate difficulties with the hardware 	pr_err
	KERN_WARNING 	"4" 	A warning, meaning nothing serious by itself but might indicate problems 				pr_warning
	KERN_NOTICE 	"5" 	Nothing serious, but notably nevertheless. Often used to report security events. 		pr_notice
	KERN_INFO 		"6" 	Informational message e.g. startup information at driver initialization 				pr_info
	KERN_DEBUG 		"7" 	Debug messages 																			pr_debug, pr_devel if DEBUG is defined 
	"""

	date = models.DateTimeField(default=datetime.datetime.now(), help_text="YYYY-MM-DD HH:MM:SS")
	login = models.CharField(max_length=30)
	login.nom_colonne = None
	login.nom_long = None
	log_level = models.IntegerField(verbose_name="Niveau de log", choices=LOG_LEVEL)
	log_level.nom_colonne = None
	log_level.nom_long = None
	log_action = models.IntegerField(verbose_name="Action", choices=LOG_ACTION)
	log_action.nom_colonne = None
	log_action.om_long = None
	Log_module = models.IntegerField(verbose_name="Module", choices=LOG_MODULE)
	Log_module.nom_colonne = None
	Log_module.nom_long = None
	parametre = models.CharField(max_length=100)
	parametre.nom_colonne = None
	parametre.nom_long = None
	ancienne_valeur = models.CharField(max_length=100)
	ancienne_valeur.nom_colonne = None
	ancienne_valeur.nom_long = None
	nouvelle_valeur = models.CharField(max_length=100)
	nouvelle_valeur.nom_colonne = None
	nouvelle_valeur.nom_long = None
	def __unicode__(self):
		return "[%s]" %(self.date, self.log_action.nom_action)
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")
	def date__dd_mm_yyyy(self):
		return self.date.strftime("%d/%m/%Y %H:%M:%S")
	class Meta:
		ordering = ["id"]

