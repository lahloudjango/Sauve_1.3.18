# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import MyFields
#from django.contrib.admin.widgets import AdminDateWidget

from django.contrib.auth.models import User
import models_stock
import models_nomenclature
import models_user

from fonction import *

class ContenantExistant(Exception):
	"""
	Ce contenant existe déjà
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")
class ContenantMultipleErreur(Exception):
	"""
	Erreur, Plusieurs contenant avec le même code !!!!
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")
class ContenantStatExistant(Exception):
	"""
	Ce contenant existe déjà
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")
class ContenantStatMultipleErreur(Exception):
	"""
	Erreur, Plusieurs contenant avec le même code !!!!
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")
class ContenantStatInconnuErreur(Exception):
	"""
	Erreur, Plusieurs contenant avec le même code !!!!
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")

# CONTENANT



class ContenantStat(models.Model):
	"""
	Table de statistique de suivie des contenants
	"""
	contenant_type_code = MyFields.CharField(max_length=30, blank=True, default=None, null=True)
	contenant_code = MyFields.CharField(max_length=30, blank=True, default=None, null=True)
	contenant_date_creation = MyFields.DateField(default=None)
	contenant_responsable_creation_login = MyFields.CharField(max_length=30, blank=True, default=None, null=True)
	contenant_provenance_site_code = models.CharField(max_length=30, blank=True, default=None, null=True)
	contenant_provenance_site_description = models.CharField(max_length=100, blank=True, default=None, null=True)
	contenant_date_suppression = MyFields.DateField(blank=True, default=None, null=True)
	contenant_responsable_suppression_login = MyFields.CharField(max_length=30, blank=True, default=None, null=True)
	nomenclature_lot_code = MyFields.CharField(max_length=30, blank=True, default=None, null=True)
	nomenclature_lot_client = MyFields.CharField(max_length=50, blank=True, default=None, null=True)
	nomenclature_lot_projet = MyFields.CharField(max_length=50, blank=True, default=None, null=True)
	nomenclature_lot_poids_reference = MyFields.FloatField(blank=True, default=None, null=True)
	nomenclature_code = MyFields.CharField(max_length=30, blank=True, default=None, null=True)
	nomenclature_description = MyFields.CharField(max_length=100, blank=True, default=None, null=True)
	nomenclature_type_code = models.CharField(max_length=30, blank=True, default=None, null=True)
	nomenclature_type_description = models.CharField(max_length=100, blank=True, default=None, null=True)

class ContenantType(models.Model):
	"""
		Liste des types de contenants
	"""
	code = MyFields.CharField(max_length=30, unique=True, verbose_name="Code")
	code.nom_colonne = "Type C"
	code.nom_long = "Code du format de contenant (30c)"
	description = MyFields.CharField(max_length=100, verbose_name="Description")
	description.nom_colonne = "Type C"
	description.nom_long = "Description du type de contenant (100c)"
	capacite = MyFields.FloatField(verbose_name="Capacité du Contenant", help_text="g")
	capacite.nom_colonne = "Capacité"
	capacite.nom_long = "Capacité du type de contenant"
	tare = MyFields.FloatField(verbose_name="Tare", help_text="g")
	tare.nom_colonne = "Tare"
	tare.nom_long = "Poids à vide du contenant avec sont bouchon"
	def get_contenant(self, supp=None):
		if supp == True:
			return Contenant.objects.filter(pk=self.id).filter(date_suppression__isnull=False)
		if supp == False:
			return Contenant.objects.filter(pk=self.id).filter(date_suppression__isnull=True)
		else:
			return Contenant.objects.filter(pk=self.id)
	def __unicode__(self):
		return "%s - %.2fg" %(self.description, self.capacite)
	def __str__(self):
		return ("[%s] %s - %.2fg" %(self.code, self.description, self.capacite)).encode("ascii", "replace")
	class Meta:
		ordering = ["id"]

class Contenant(models.Model):
	"""
		Liste des contenants
	"""
	"""
		Code contenant sur 10 chiffre
		1xxxxxxxxx : Contenant SAP
		2xxxxxxxxx : Contenant Linautom
		3xxxxxxxxx : Solution fichier exel Vincent
		4xxxxxxxxx :
		5xxxxxxxxx :
		6xxxxxxxxx : Contenant Navette SAP
		7xxxxxxxxx :
		8xxxxxxxxx :
		9xxxxxxxxx :
	"""
	code = MyFields.CharField(max_length=30, blank=True, default=None, null=True, unique=True, verbose_name="Code")
	code.nom_colonne = "Code barre"
	code.nom_long = "Code barre du contenant (30c)"
	nomenclature_lot = models.ForeignKey(models_nomenclature.NomenclatureLot, verbose_name="Article/Lot")
	type_contenant = models.ForeignKey(ContenantType, verbose_name="Type de Contenant", default=1)
	actuel_site = models.ForeignKey(models_stock.StockSite, verbose_name="Site actuel", default=1)
	actuel_entrepot = models.ForeignKey(models_stock.StockEntrepot, verbose_name="Entrepôt actuel", default=1)
	actuel_magasin = models.ForeignKey(models_stock.StockMagasin, verbose_name="Magasin actuel", default=1)
	actuel_emplacement = MyFields.CharField(max_length=30, blank=True, default="", verbose_name="Emplacement actuel")
	actuel_emplacement.nom_colonne = "Emplacement"
	actuel_emplacement.nom_long = "Emplacement de stockage (30c)"
	stock_site = models.ForeignKey(models_stock.StockSite, related_name="stock_site", verbose_name="Site de stockage", default=1)
	stock_entrepot = models.ForeignKey(models_stock.StockEntrepot, related_name="stock_entrepot", verbose_name="Entrepôt de stockage", default=1)
	stock_magasin = models.ForeignKey(models_stock.StockMagasin, related_name="stock_magasin", verbose_name="Magasin de stockage", default=1)
	stock_emplacement = MyFields.CharField(max_length=30, blank=True, default="", verbose_name="Emplacement de stockage")
	stock_emplacement.nom_colonne = "Emplacement"
	stock_emplacement.nom_long = "Emplacement de stockage (30c)"
	tare = MyFields.FloatField(blank=True, default=None, null=True, verbose_name="Poids vide du contenant", help_text="g")
	tare.nom_colonne = "Tare"
	tare.nom_long = "Tare réel du contenant vide avec sont bouchon ; la valeur du type de contenant est utilisée si la valeur réel n'est pas disponible"
	poids = MyFields.FloatField(blank=True, default=None, null=True, verbose_name="Quantité de matière", help_text="g")
	poids.nom_colonne = "Poids"
	poids.nom_long = "Poids du contenu"
	date_creation = MyFields.DateField(default=None, verbose_name="Date de création")
	date_creation.nom_colonne = "Date création"
	date_creation.nom_long = "Date de création du contenant manuel ou import automatique"
	date_creation.format_date_time = "%d/%m/%Y"
	date_reception = MyFields.DateField(blank=True, default=None, null=True, verbose_name="Date de réception")
	date_reception.nom_colonne = "Date réception"
	date_reception.nom_long = "Date de réception du contenant"
	date_reception.format_date_time = "%d/%m/%Y"
	date_suppression = MyFields.DateField(blank=True, default=None, null=True, verbose_name="Date de destruction")
	date_suppression.nom_colonne = "Date destruction"
	date_suppression.nom_long = "Date de destruction du contenant"
	date_suppression.format_date_time = "%d/%m/%Y"
	date_fin_validite = MyFields.DateField(blank=True, default=None, null=True, verbose_name="Date de fin de validité")
	date_fin_validite.nom_colonne = "Fin validité"
	date_fin_validite.nom_long = "Date de fin de validité ; la date de validité de la formule/essai est utilisé par défaut"
	date_fin_validite.format_date_time = "%d/%m/%Y"
	seuil_alarme = MyFields.IntegerField(blank=True, default=None, null=True, verbose_name="Alarme réapprovisionnement", help_text="g")
	seuil_alarme.nom_colonne = "Alarme"
	seuil_alarme.nom_long = "Seuil d'alarme de réaprovisionement"
	panier_user = models.ForeignKey(User, verbose_name="Panier utilisateur", related_name="panier_user", blank=True, default=None, null=True)
	provenance_site = models.ForeignKey(models_stock.StockSite, related_name="provenance_site", verbose_name="Site de provenance", default=1)
	#responsable_suppression_login = MyFields.CharField(max_length=30, blank=True, default=None, null=True, verbose_name="Responsable de suppression login")
	#responsable_suppression_login.nom_colonne = "Responsable de suppression"
	#responsable_suppression_login.nom_long = "Nom du responsable de la suppression (30c)"
	responsable_suppression = models.ForeignKey(User, related_name="responsable_suppression", blank=True, default=None, null=True, verbose_name="Responsable de suppression")
	responsable_mouvement = models.ForeignKey(User, related_name="responsable_mouvement", blank=True, default=None, null=True, verbose_name="Responsable dernier mouvement")
	responsable_creation = models.ForeignKey(User, related_name="responsable_creation", blank=True, default=None, null=True, verbose_name="Responsable de création")
	def get_poids_unit(self, unit=None):
		if unit == None:
			unit = models_user.UnitMasse.objects.get(code="g")
		if type(unit) == type("string"):
			unit = models_user.UnitMasse.objects.get(code=unit)
		poids = {}
		if self.poids == None:
			poids.update({"poids":None})
			poids.update({"unit":unit.code})
			poids.update({"poids_unit":"??"})
		else:
			poids.update({"poids":self.poids/unit.facteur})
			poids.update({"unit":unit.code})
			poids.update({"poids_unit":"%.3f%s" %(self.poids/unit.facteur, unit.code)})
		return poids
	def set_poids_unit(self, poids, unit):
		if type(unit) == type("string"):
			unit = models_user.UnitMasse.objects.get(code=unit)
		poids = {}
		self.poids = poids*unit.facteur
		self.save()
		return
	def get_tare_unit(self, unit=None):
		if unit == None:
			unit = models_user.UnitMasse.objects.get(code="g")
		if type(unit) == type("string"):
			unit = models_user.UnitMasse.objects.get(code=unit)
		poids = {}
		if self.tare == None:
			poids.update({"poids":None})
			poids.update({"unit":unit.code})
			poids.update({"poids_unit":"??"})
		else:
			poids.update({"poids":self.tare/unit.facteur})
			poids.update({"unit":unit.code})
			poids.update({"poids_unit":"%.3f%s" %(self.tare/unit.facteur, unit.code)})
		return poids
	def set_tare_unit(self, poids, unit):
		if type(unit) == type("string"):
			unit = models_user.UnitMasse.objects.get(code=unit)
		poids = {}
		self.tare = poids*unit.facteur
		self.save()
		return
	def suppression(self, user):
		"""
		suppression 
			=> la fonction renseigne "date_fin_validite"
			=> la fonction recherche tout les enfant "date_fin_validite"
		"""
		print_ascii("Suppression : %s" %(unicode(self)))
		self.date_suppression = datetime.date.today()
		#self.responsable_suppression_login = user.username
		self.responsable_suppression = user
		self.panier_user = None
		self.save()
		self.contenant_stat(supp=True)
		log = django_models.LogEntry()
		log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
		log.user = user																						#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
		log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())		#Le type de contenu (ContentType) de l’objet modifié.
		log.object_id = self.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
		log.object_repr = self.__unicode__()																#La représentation repr() de l’objet après sa modification.
		log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
		log.change_message = "self.suppression()"															#Description de la modification
		log.save()
		return
	def suppression_parent(self, user):
		"""
		suppression parent
			=> recherche le parent, si le parent n'a pas d'enfants la champs "date_fin_validite"
			=> si le parent n'a pas d'enfant, renseigne le champ "date_fin_validite"
		"""
		print_ascii("Suppression check parent de %s" %(unicode(self)))
		cont = self.nomenclature_lot.get_nomenclature_lot_contenant(supp=False)
		if len(cont) == 0:
			print_ascii("Suppression : %s" %(unicode(self.nomenclature_lot)))
			self.nomenclature_lot.date_suppression = datetime.date.today()
			self.nomenclature_lot.save()
			self.nomenclature_lot.suppression_parent(user)
			log = django_models.LogEntry()
			log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
			log.user = user																						#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
			log.content_type = ContentType.objects.get(app_label="stock_labo", model="NomenclatureLot".lower())	#Le type de contenu (ContentType) de l’objet modifié.
			log.object_id = self.nomenclature_lot.id															#La représentation textuelle de la clé primaire de l’objet modifié.
			log.object_repr = self.nomenclature_lot.__unicode__()												#La représentation repr() de l’objet après sa modification.
			log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
			log.change_message = "self.suppression_parent()"													#Description de la modification
			log.save()
		return
	def destruction_test(self, user):
		"""
		L'enfant sucidaire interroge sont parent pour savoir s'il est le seul enfant
		Si le parent n'a qu'un enfant alors l'enfant tue sont parent
		( => le parent mort : pas d'enfant )
		destruction_test retourne le plus grand...parent qui peut être détruit
		"""
		# self peux être détruit ?
		a = self
		# le parent de self peut être détruit ?
		if a == self:
			q = self.nomenclature_lot.destruction_test(user)
			if q == None:
				return a
			else:
				return q
		else:
			return None
	def destruction(self, user):
		log_auto(user=user, obj=self, flag="d", info="self.destruction(%s)" %(self))
		self.delete()
	#def destruction_parent(self, user):
	#	"""
	#	Destruction des parents
	#	"""
	#	#print_ascii("Destruction check parent de %s" %(unicode(self)))
	#	# Suppresion du contenant pour contenant_stat
	#	self.date_suppression = datetime.date.today()
	#	#self.responsable_suppression_login = user.username
	#	self.responsable_suppression = user
	#	self.panier_user = None
	#	self.save()
	#	self.contenant_stat(supp=True)
	#	if Contenant.objects.filter(nomenclature_lot=self.nomenclature_lot.id).count() <= 1:
	#		if self.nomenclature_lot.destruction_parent(user) == False:
	#			# print_ascii("Destruction : %s" %(unicode(self.nomenclature_lot)))
	#			# self.nomenclature_lot.destruction_ing(user)
	#			log = django_models.LogEntry()
	#			log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
	#			log.user = user																						#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
	#			log.content_type = ContentType.objects.get(app_label="stock_labo", model="NomenclatureLot".lower())	#Le type de contenu (ContentType) de l’objet modifié.
	#			log.object_id = self.nomenclature_lot.id															#La représentation textuelle de la clé primaire de l’objet modifié.
	#			log.object_repr = self.nomenclature_lot.__unicode__()												#La représentation repr() de l’objet après sa modification.
	#			log.action_flag = django_models.DELETION 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
	#			log.change_message = "self.suppression_parent()"													#Description de la modification
	#			log.save()
	#			self.nomenclature_lot.delete()
	#			# print_ascii("Destruction : %s" %(unicode(self.__unicode__())))
	#			log = django_models.LogEntry()
	#			log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
	#			log.user = user																						#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
	#			log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())	#Le type de contenu (ContentType) de l’objet modifié.
	#			log.object_id = self.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
	#			log.object_repr = self.__unicode__()																#La représentation repr() de l’objet après sa modification.
	#			log.action_flag = django_models.DELETION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
	#			log.change_message = "self.destruction_parent()"													#Description de la modification
	#			log.save()
	#			return True
	#		else:
	#			# print_ascii("Destruction : %s" %(unicode(self.__unicode__())))
	#			log = django_models.LogEntry()
	#			log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
	#			log.user = user																						#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
	#			log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())	#Le type de contenu (ContentType) de l’objet modifié.
	#			log.object_id = self.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
	#			log.object_repr = self.__unicode__()																#La représentation repr() de l’objet après sa modification.
	#			log.action_flag = django_models.DELETION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
	#			log.change_message = "self.destruction_parent()"													#Description de la modification
	#			log.save()
	#			return True
	#	else:
	#		# print_ascii("Destruction : %s" %(unicode(self.__unicode__())))
	#		log = django_models.LogEntry()
	#		log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
	#		log.user = user																						#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
	#		log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())	#Le type de contenu (ContentType) de l’objet modifié.
	#		log.object_id = self.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
	#		log.object_repr = self.__unicode__()																#La représentation repr() de l’objet après sa modification.
	#		log.action_flag = django_models.DELETION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
	#		log.change_message = "self.destruction_parent()"													#Description de la modification
	#		log.save()
	#		self.delete()
	#		return True
	#def destruction(self, user):
	#	""" 
	#	Detruit la ligne et détruit les enfants pour éviter les orphelins
	#	Si parent = true => détruit les parent
	#	"""
	#	# Suppresion du contenant pour contenant_stat
	#	self.date_suppression = datetime.date.today()
	#	#self.responsable_suppression_login = user.username
	#	self.responsable_suppression = user
	#	self.panier_user = None
	#	self.save()
	#	self.contenant_stat(supp=True)
	#	log = django_models.LogEntry()
	#	log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
	#	log.user = user																						#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
	#	log.content_type = ContentType.objects.get(app_label="stock_labo", model="Contenant".lower())		#Le type de contenu (ContentType) de l’objet modifié.
	#	log.object_id = self.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
	#	log.object_repr = self.__unicode__()																#La représentation repr() de l’objet après sa modification.
	#	log.action_flag = django_models.DELETION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
	#	log.change_message = "self.destruction()"															#Description de la modification
	#	log.save()
	#	self.delete()
	#	return
	def chois_type_contenant(self, poids):
		c_type = ContenantType.objects.all().order_by("capacite")
		c = c_type[0]
		for cont in c_type:
			if poids <= cont.capacite:
				c = cont
				break
		return c
	def duree_validite(self):
		return self.date_fin_validite - self.date_creation
	def fin_validite(self, duree=None):
		if duree == None:
			if self.nomenclature_lot.nomenclature.duree_validite == None :
				return None
			elif self.nomenclature_lot.nomenclature.nomenclature_type.code == "MP":
				if self.date_reception == None:
					return self.nomenclature_lot.date_fin_validite
				else:
					return self.date_reception + datetime.timedelta(days = self.nomenclature_lot.nomenclature.duree_validite)
			else:
				return self.nomenclature_lot.date_fin_validite
		else:
			return self.date_reception + datetime.timedelta(days = duree)
	def actuel_emplacement_code(self):
		return "%s-%s-%s-%s" %(self.actuel_site.code, self.actuel_entrepot.code, self.actuel_magasin.code, self.actuel_emplacement)
	def stock_emplacement_code(self):
		return "%s-%s-%s-%s" %(self.stock_site.code, self.stock_entrepot.code, self.stock_magasin.code, self.stock_emplacement)
	def actuel_emplacement_cb(self):
		return "003:%s:%s:%s:%s" %(self.actuel_site.code, self.actuel_entrepot.code, self.actuel_magasin.code, self.actuel_emplacement)
	def stock_emplacement_cb(self):
		return "003:%s:%s:%s:%s" %(self.stock_site.code, self.stock_entrepot.code, self.stock_magasin.code, self.stock_emplacement)
	def actuel_emplacement_nom(self):
		return "%s - %s - %s - %s" %(self.actuel_site.description, self.actuel_entrepot.description, self.actuel_magasin.description, self.actuel_emplacement)
	def stock_emplacement_nom(self):
		return "%s - %s - %s - %s" %(self.stock_site.description, self.stock_entrepot.description, self.stock_magasin.description, self.stock_emplacement)
	def actuel_emplacement_nom_court(self):
		return "%s - %s" %(self.actuel_entrepot.description, self.actuel_magasin.description)
	def stock_emplacement_nom_court(self):
		return "%s - %s" %(self.stock_entrepot.description, self.stock_magasin.description)
	def colored_stock(self):
		if self.poids < self.type_contenant.seuil_alarme_mg:
			return "red"
		else:
			return None
	def colored_validite(self):
		if self.date_fin_validite < datetime.date.today():
			return "red"
		else:
			return None
	def f_date_creation(self, f=None):
		if f == None:
			f = Contenant._meta.fields[14].format_date_time
		if self.date_creation == None:
			return "??"
		elif self.date_creation == "":
			return "???"
		elif self.date_creation.year < 1900:
			return "Oh!!!"
		else:
			return self.date_creation.strftime(f)
	def f_date_reception(self, f=None):
		if f == None:
			f = Contenant._meta.fields[15].format_date_time
		if self.date_reception == None:
			return "??"
		elif self.date_reception == "":
			return "???"
		elif self.date_reception.year < 1900:
			return "Oh!!!"
		else:
			return self.date_reception.strftime(f)
	def f_date_suppression(self, f=None):
		if f == None:
			f = Contenant._meta.fields[16].format_date_time
		if self.date_suppression == None:
			return "??"
		elif self.date_suppression == "":
			return "???"
		elif self.date_suppression.year < 1900:
			return "Oh!!!"
		else:
			return self.date_suppression.strftime(f)
	def f_date_fin_validite(self, f=None):
		if f == None:
			f = Contenant._meta.fields[17].format_date_time
		if self.date_fin_validite == None:
			return "??"
		elif self.date_fin_validite == "":
			return "???"
		elif self.date_fin_validite.year < 1900:
			return "Oh!!!"
		else:
			return self.date_fin_validite.strftime(f)
	def contenant_stat(self, supp=False):
		"""
		Crée le contenant dans la table contenantstat
		Une copie de la fonction est utilisé dans le module impression sans enregistrement
		"""
		cont_stat = ContenantStat.objects.filter(contenant_code=self.code)
		if len(cont_stat) == 0 or self.code == "NO-REF":
			cont_stat = ContenantStat(contenant_code=self.code)
			cont_stat.contenant_type_code = self.type_contenant.code
			cont_stat.contenant_date_creation = self.date_creation
			cont_stat.contenant_provenance_site_code = self.provenance_site.code
			cont_stat.contenant_provenance_site_description = self.provenance_site.description
			cont_stat.contenant_date_suppression = self.date_suppression
			cont_stat.nomenclature_lot_code = self.nomenclature_lot.code
			cont_stat.nomenclature_lot_client = self.nomenclature_lot.client
			cont_stat.nomenclature_lot_projet = self.nomenclature_lot.projet
			cont_stat.nomenclature_lot_poids_reference = self.nomenclature_lot.poids_reference
			cont_stat.nomenclature_code = self.nomenclature_lot.nomenclature.code
			cont_stat.nomenclature_description = self.nomenclature_lot.nomenclature.description
			cont_stat.nomenclature_type_code = self.nomenclature_lot.nomenclature.nomenclature_type.code
			cont_stat.nomenclature_type_description = self.nomenclature_lot.nomenclature.nomenclature_type.description
			if self.responsable_suppression != None:
				cont_stat.contenant_responsable_suppression_login = self.responsable_suppression.username
			if self.responsable_creation != None:
				cont_stat.contenant_responsable_creation_login = self.responsable_creation.username
			if supp == True and self.code != "NO-REF":
				cont_stat.contenant_date_suppression = self.date_suppression
				if self.responsable_suppression != None:
					cont_stat.contenant_responsable_suppression_login = self.responsable_suppression.username
			cont_stat.save()
		elif len(cont_stat) == 1:
			if supp == True:
				if self.code != "NO-REF":
					cont_stat[0].contenant_date_suppression = self.date_suppression
					if self.responsable_suppression != None:
						cont_stat[0].contenant_responsable_suppression_login = self.responsable_suppression.username
					cont_stat[0].save()
				else:
					raise ContenantStatInconnuErreur(cont_stat[0])
			else:
				raise ContenantStatExistant(cont_stat[0])
		else:
			raise ContenantStatMultipleErreur(cont_stat)
	def __unicode__(self):
		return "Contenant [%d] %s de %s" %(self.id, self.code, self.nomenclature_lot)
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")
	class Meta:
#		verbose_name = "Contenant"
		ordering = ["id"]




