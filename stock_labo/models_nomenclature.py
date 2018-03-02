# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import MyFields
#from django.contrib.admin.widgets import AdminDateWidget
import traceback

#from lib_linautom.python import oracle
from settings_oracle import *

import models_contenant
import models_stock
import models_user

from fonction import *

import django.core.exceptions
import django.db
#except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
#except django.db.IntegrityError:


# MOMENCLATURE : INGREDIENT / FORMULE / ESSAI / ARTICLE

class Interdit(Exception):
	"""
	L'action est interdite sur cette élément
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")
class NomenclatureLotIngredientMultipleErreur(Exception):
	"""
	Cette ingrédient existe déjà pour ce lot
	Activé le parametre "somme" pour faire une somme automatique avec des ingrédients multiple
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")
class NomenclatureLotExistant(Exception):
	"""
	Ce lot existe déjà
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")
class NomenclatureLotMultipleErreur(Exception):
	"""
	Erreur, Plusieurs lot avec le même code !!!!
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")
class NomenclatureExistant(Exception):
	"""
	Cette nomenclature existe déjà
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")
class NomenclatureMultipleErreur(Exception):
	"""
	Erreur, Plusieurs nomenclature existe avec ce code
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")
class NomenclatureLotIngredientExistant(Exception):
	"""
	Cette ingrédient pour cette nomenclature existe déjà
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")
class NomenclatureLotIngredientMultipleErreur(Exception):
	"""
	Erreur, Plusieurs fois cette ingrédient pour cette nomenclature existe
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")
class NomenclatureTypeExistant(Exception):
	"""
	Cette nomenclature_type existe déjà
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")
class NomenclatureTypeMultipleErreur(Exception):
	"""
	Erreur, Plusieurs nomenclature_type existe avec ce code
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")
class NomenclatureLotDestruction(Exception):
	"""
	Destruction impossible, La nomenclature est utilisé par un lot, une formule
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")
class NomenclatureLotIngredientDosageDestructionInterdit(Exception):
	"""
	Destruction d'une ligne seul interdite
	"""
	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
	def __str__(self):
		return self.__doc__.encode("ascii", "replace")
class OracleClient(models.Model):
	"""
	Copie de la table oracle client
	"""
	projet = MyFields.CharField(max_length=30, blank=True, default=None, null=True)
	client = MyFields.CharField(max_length=30, blank=True, default=None, null=True)
	client_ka = MyFields.CharField(max_length=100, blank=True, default=None, null=True)
	def __unicode__(self):
		return "[%s] %s" %(self.projet, self.client)
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")

class NomenclatureLotStat(models.Model):
	"""
	Table de statistique de suivie des lots
	"""
	class Meta:
		ordering = ["code"]
	code = MyFields.CharField(max_length=30, blank=True, default=None, null=True)

	nomenclature_code = MyFields.CharField(max_length=30, blank=True, default=None, null=True)
	nomenclature_description = MyFields.CharField(max_length=100, blank=True, default=None, null=True)
	nomenclature_type_code = models.CharField(max_length=30, blank=True, default=None, null=True)

	date_creation = MyFields.DateField(blank=True, default=None, null=True)
	client = MyFields.CharField(max_length=50, blank=True, default=None, null=True)
	client_ka = MyFields.CharField(max_length=50, blank=True, default=None, null=True)
	projet = MyFields.CharField(max_length=50, blank=True, default=None, null=True)
	poids_reference = MyFields.FloatField(blank=True, default=None, null=True)
	num_roxane = MyFields.CharField(max_length=12, blank=True, default=None, null=True)
	nbr_ligne_robot = MyFields.IntegerField(blank=True, default=None, null=True)
	nbr_ligne_manuel = MyFields.IntegerField(blank=True, default=None, null=True)
	responsable_creation_login = MyFields.CharField(max_length=30, blank=True, default=None, null=True)
	def __unicode__(self):
		return "[%s] %s" %(self.code, self.nomenclature_code)
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")

class NomenclatureType(models.Model):
	"""
	Type de nomenclature
	"""
	code = models.CharField(max_length=30, unique=True, verbose_name="Code")
	code.nom_colonne = "Type MP"
	code.nom_long = "Type d'ingrédient/article"
	description = models.CharField(max_length=100, verbose_name="Description")
	description.nom_colonne = "Description"
	description.nom_long = "Nom du type d'ingrédient"
	def destruction_test(self, user):
		"""
		L'enfant sucidaire interroge sont parent pour savoir s'il est le seul enfant
		Si le parent n'a qu'un enfant alors l'enfant tue sont parent
		( => le parent mort : pas d'enfant )
		destruction_test retourne le plus grand...parent qui peut être détruit
		"""
		return None
	def destruction(self, user):
		for l in self.get_nomenclature():
			l.destruction(user)
		log_auto(user=user, obj=self, flag="d", info="self.destruction(%s)" %(self))
		self.delete()
	def get_nomenclature(self, supp=None):
		if supp == True:
			return Nomenclature.objects.filter(nomenclature_type=self.id).filter(date_suppression__isnull=False)
		if supp == False:
			return Nomenclature.objects.filter(nomenclature_type=self.id).filter(date_suppression__isnull=True)
		else:
			return Nomenclature.objects.filter(nomenclature_type=self.id)
	def add_nomenclature(self, code, description="", commentaire="", date_creation=None, update=True, insert=True):
		"""
		Ajoute une nouvelle nomentclature de ce type
		"""
		if date_creation == None:
			date_creation = datetime.date.today()

		n = Nomenclature.objects.filter(code=code)
		if len(n) == 0:
			if insert == True:
				n = Nomenclature(nomenclature_type=self, code=code, description=description, commentaire=commentaire, date_creation=date_creation)
				n.save()
				return n
			else:
				return None
		elif len(n) == 1:
			if update == True:
				if description != "":
					n[0].description=description
				if commentaire != "":
					n[0].commentaire=commentaire
				n[0].date_suppression=None
				n[0].save()
			raise NomenclatureExistant(n[0])
		else:
			raise NomenclatureMultipleErreur(n)
	def __unicode__(self):
		return "[%s] %s" %(self.code, self.description)
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")
	class Meta:
		ordering = ["code"]

class Nomenclature(models.Model):
	"""
	Liste des Articles/Formules/Essais/Ingrédients
	"""
	code = MyFields.CharField(max_length=30, unique=True, verbose_name="Code")
	code.nom_colonne = "Code"
	code.nom_long = "Code de la Formule/essai/matière première (30c)"
	description = MyFields.CharField(max_length=100, blank=True, default="", verbose_name="Description")
	description.nom_colonne = "Description"
	description.nom_long = "Nom de la Formule/essai/matière première (100c)"
	commentaire = MyFields.TextField(max_length=255, blank=True, default="", verbose_name="Commentaire")
	commentaire.nom_colonne = "C"
	commentaire.nom_long = "Commentaire (255c)"
	nomenclature_type = models.ForeignKey(NomenclatureType, verbose_name="Type")
	reception_site = models.ForeignKey(models_stock.StockSite, verbose_name="Site de stockage par défaut", default=1)
	reception_entrepot = models.ForeignKey(models_stock.StockEntrepot, verbose_name="Stock de stockage par défaut", default=1)
	reception_magasin = models.ForeignKey(models_stock.StockMagasin, verbose_name="Magasin de stockage par défaut", default=1)
	reception_emplacement = MyFields.CharField(max_length=30, blank=True, default="", verbose_name="Emplacement de stockage par défaut")
	reception_emplacement.nom_colonne = "Emplacement"
	reception_emplacement.nom_long = "Emplacement de stockage (30c)"
	date_creation = MyFields.DateField(default=None, blank=True, null=True, verbose_name="Date de Création")
	date_creation.nom_colonne = "Création"
	date_creation.nom_long = "Date de Création"
	date_creation.format_date_time = "%d/%m/%Y"
	date_suppression = MyFields.DateField(blank=True, default=None, null=True, verbose_name="Date de destruction")
	date_suppression.nom_colonne = "Date destruction"
	date_suppression.nom_long = "Date de destruction du contenant"
	date_suppression.format_date_time = "%d/%m/%Y"
	duree_validite = MyFields.IntegerField(default=settings_default.DUREE_VALIDITE_MP, verbose_name="Durée de validité")
	duree_validite.nom_colonne = "Validité"
	duree_validite.nom_long = "Durée de validité par défaut en jours"
	collection = MyFields.BooleanField(default=False, verbose_name="Collection", help_text="Article en collection")
	collection.nom_colonne = "Col"
	collection.nom_long = "Article en collection"
	date_collection = MyFields.DateField(default=None, blank=True, null=True, verbose_name="Date collection")
	date_collection.nom_colonne = "Collection"
	date_collection.nom_long = "Date de changement de statut de collection"
	date_collection.format_date_time = "%d/%m/%Y"
	date_flash_point = MyFields.DateField(default=None, blank=True, null=True, verbose_name="Date Flash")
	date_flash_point.nom_colonne = "Date flash"
	date_flash_point.nom_long = "Date de point éclair"
	date_flash_point.format_date_time = "%d/%m/%Y"
	flash_point = MyFields.FloatField(blank=True, default=None, null=True, verbose_name="Flash", help_text="°C")
	flash_point.nom_colonne = "Flash"
	flash_point.nom_long = "Point éclair"
	responsable_flash_point = models.ForeignKey(User, related_name="nomenclature_responsable_fp", blank=True, default=None, null=True, verbose_name="Responsable Flash")
	def set_validite(self, val, user):
		log_auto(user=user, obj=self, flag="c", info="set_validité")
		self.duree_validite = val
		self.date_suppression = None
		self.save()
		lot = self.get_nomenclature_lot(supp=False)
		for l in lot:
			log_auto(user=user, obj=l, flag="c", info="set_validité")
			l.date_fin_validite = l.fin_validite()
			l.save()
			cont = l.get_nomenclature_lot_contenant(supp=False)
			for c in cont:
				log_auto(user=user, obj=c, flag="c", info="set_validité")
				c.date_fin_validite = c.fin_validite()
				c.save()
	def set_collection(self, user):
		if self.collection == False:
			log_auto(user=user, obj=self, flag="c", info="set_collection")
			self.duree_validite = settings_default.DUREE_VALIDITE_COL
			self.date_collection = datetime.date.today()
			self.collection = True
			self.date_suppression = None
			self.save()
			lots = self.get_nomenclature_lot()
			for lot in lots:
				val = lot.fin_validite()
				if val != lot.date_fin_validite:
					log_auto(user=user, obj=lot, flag="c", info="set_collection")
					lot.date_fin_validite = lot.fin_validite()
					lot.save()
				cont = lot.get_nomenclature_lot_contenant()
				for c in cont:
					if c.date_reception != None:
						val = c.fin_validite()
						if val != c.date_fin_validite:
							log_auto(user=user, obj=c, flag="c", info="set_collection")
							c.date_fin_validite = c.fin_validite()
							c.save()
	def reset_collection(self, user):
		if self.collection == True:
			log_auto(user=user, obj=self, flag="c", info="reset_collection")
			self.duree_validite = settings_default.DUREE_VALIDITE_COUP
			self.date_collection = datetime.date.today()
			self.collection = False
			self.save()
			lots = self.get_nomenclature_lot()
			for lot in lots:
				val = lot.fin_validite()
				if val != lot.date_fin_validite:
					log_auto(user=user, obj=lot, flag="c", info="reset_collection")
					lot.date_fin_validite = lot.fin_validite()
					lot.save()
				cont = lot.get_nomenclature_lot_contenant()
				for c in cont:
					if c.date_reception != None:
						val = c.fin_validite()
						if val != c.date_fin_validite:
							log_auto(user=user, obj=c, flag="c", info="reset_collection")
							c.date_fin_validite = c.fin_validite()
							c.save()
	def set_poids_unit(self, poids, unit):
		if type(unit) == type("string"):
			unit = models_user.UnitMasse.objects.get(code=unit)
		poids = {}
		self.poids_reference = poids*unit.facteur
		self.save()
		return
	def description_split(self, len_max):
		return split_string(self.description, len_max)
	def commentaire_split(self, len_max):
		return split_string(self.commentaire, len_max)
	def actuel_emplacement_code(self):
		return "%s-%s-%s-%s" %(self.reception_site.code, self.reception_entrepot.code, self.reception_magasin.code, self.reception_emplacement)
	def actuel_emplacement_cb(self):
		return "003:%s:%s:%s:%s" %(self.reception_site.code, self.reception_entrepot.code, self.reception_magasin.code, self.reception_emplacement)
	def actuel_emplacement_nom(self):
		return "%s - %s - %s - %s" %(self.reception_site.description, self.reception_entrepot.description, self.reception_magasin.description, self.reception_emplacement)
	def actuel_emplacement_nom_court(self):
		return "%s - %s" %(self.reception_entrepot.description, self.reception_magasin.description)
	def get_nomenclature_lot(self, supp=None):
		if supp == True:
			return NomenclatureLot.objects.filter(nomenclature_id=self.id).filter(date_suppression__isnull=False)
		if supp == False:
			return NomenclatureLot.objects.filter(nomenclature_id=self.id).filter(date_suppression__isnull=True)
		else:
			return NomenclatureLot.objects.filter(nomenclature_id=self.id)
	def add_lot(self, code, responsable_creation, date_creation=None, date_fin_validite=None, update=True, insert=True):
		"""
		Ajoute un lot pour cette nomenclature
		"""
		if date_creation == None:
			date_creation = datetime.date.today()
		if date_fin_validite == None:
			date_fin_validite=date_creation + datetime.timedelta(days = self.duree_validite)
		lot = NomenclatureLot.objects.filter(nomenclature=self.id).filter(code=code)
		if len(lot) == 0:
			if insert == True:
				lot = NomenclatureLot(nomenclature=self, code=code, responsable_creation=responsable_creation, date_creation=date_creation, date_fin_validite=date_fin_validite)
				lot.save()
				return lot
			else:
				return None
		elif len(lot) == 1:
			if update == True:
				lot[0].date_suppression=None
				lot[0].save()
			raise NomenclatureLotExistant(lot[0])
		else:
			raise NomenclatureLotMultipleErreur(lot)
	def suppression(self, user):
		print_ascii("Suppression : %s" %(unicode(self)))
		n_lot = NomenclatureLot.objects.filter(nomenclature=self.id, date_suppression__isnull=True)
		for i in n_lot:
			i.suppression(user)
		self.date_suppression = datetime.date.today()
		self.save()
		log = django_models.LogEntry()
		log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
		log.user = user																						#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
		log.content_type = ContentType.objects.get(app_label="stock_labo", model="Nomenclature".lower())	#Le type de contenu (ContentType) de l’objet modifié.
		log.object_id = self.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
		log.object_repr = self.__unicode__()																#La représentation repr() de l’objet après sa modification.
		log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
		log.change_message = "self.suppression()"															#Description de la modification
		log.save()
		return
	def suppression_parent(self, user):
		print_ascii("Suppression parent check %s" %(unicode(self)))
		return
	def get_nomenclature_lot(self, supp=None):
		if supp == True:
			return NomenclatureLot.objects.filter(nomenclature_id=self.id).filter(date_suppression__isnull=False)
		if supp == False:
			return NomenclatureLot.objects.filter(nomenclature_id=self.id).filter(date_suppression__isnull=True)
		else:
			return NomenclatureLot.objects.filter(nomenclature_id=self.id)
	def destruction_test(self, user):
		"""
		L'enfant sucidaire interroge sont parent pour savoir s'il est le seul enfant
		Si le parent n'a qu'un enfant alors l'enfant tue sont parent
		( => le parent mort : pas d'enfant )
		destruction_test retourne le plus grand...parent qui peut être détruit
		"""
		a = None
		# self peux être détruit ?
		if self.collection == True:
			a = None
		elif self.duree_validite == settings_default.DUREE_VALIDITE_MP:
			if self.get_nomenclature_lot().count() == 1:
				a = self
			else:
				a = None
		elif self.duree_validite == settings_default.DUREE_VALIDITE_COUP:
			if self.get_nomenclature_lot().count() == 1:
				a = self
			else:
				a = None
		else:
			a = None
		# le parent de self peut être détruit ?
		if a == self:
			q = self.nomenclature_type.destruction_test(user)
			if q == None:
				return a
			else:
				return q
		else:
			return None
	def destruction(self, user):
		for l in self.get_nomenclature_lot():
			l.destruction(user)
		log_auto(user=user, obj=self, flag="d", info="self.destruction(%s)" %(self))
		self.delete()
	def f_date_creation(self, f):
		if self.date_creation == None:
			return "??"
		elif self.date_creation == "":
			return "???"
		elif self.date_creation.year < 1900:
			return "Oh!!!"
		else:
			return self.date_creation.strftime(f)
	def f_date_suppression(self, f):
		if self.date_suppression == None:
			return "??"
		elif self.date_suppression == "":
			return "???"
		elif self.date_suppression.year < 1900:
			return "Oh!!!"
		else:
			return self.date_suppression.strftime(f)
	def __unicode__(self):
		return "Article [%s]-%s type %s" %(self.code, self.description, self.nomenclature_type)
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")
	class Meta:
		ordering = ["code"]

class NomenclatureLot(models.Model): #Lot de fabrication
	"""
	Liste des lot des Articles/Formules/Essais/Ingrédients
	"""
	code = MyFields.CharField(max_length=30, verbose_name="Lot")
	code.nom_colonne = "Lot"
	code.nom_long = "Lot de la Formule/essai/matière première (30c)"
	nomenclature = models.ForeignKey(Nomenclature, verbose_name="Article")
	date_creation = MyFields.DateField(default=None, blank=True, null=True, verbose_name="Date de fabrication")
	date_creation.nom_colonne = "Fabrication"
	date_creation.nom_long = "Date de fabrication"
	date_creation.format_date_time = "%d/%m/%Y"
	date_fin_validite = MyFields.DateField(blank=True, default=None, null=True, verbose_name="Fin de validité")
	date_fin_validite.nom_colonne = "Fin de validité"
	date_fin_validite.nom_long = "Date de fin de validité du lot"
	date_fin_validite.format_date_time = "%d/%m/%Y"
	date_suppression = MyFields.DateField(blank=True, default=None, null=True, verbose_name="Date de destruction")
	date_suppression.nom_colonne = "Date destruction"
	date_suppression.nom_long = "Date de destruction du lot"
	date_suppression.format_date_time = "%d/%m/%Y"
	definition = MyFields.BooleanField(default=False, verbose_name="Composition disponible", help_text="Mise à jour automatique")
	definition.nom_colonne = "Def"
	definition.nom_long = "Liste de composition"
	commentaire = MyFields.TextField(max_length=255, blank=True, default="", verbose_name="Commentaire")
	commentaire.nom_colonne = "C"
	commentaire.nom_long = "Commentaire (255c)"
	client = MyFields.CharField(max_length=50, blank=True, default="", verbose_name="Nom du client")
	client.nom_colonne = "Client"
	client.nom_long = "Nom du client"
	client_ka = MyFields.CharField(max_length=50, blank=True, default="", verbose_name="Nom du client KA")
	client_ka.nom_colonne = "Client KA"
	client_ka.nom_long = "Nom du client KA"
	projet = MyFields.CharField(max_length=50, blank=True, default="", verbose_name="N° de projet")
	projet.nom_colonne = "Projet"
	projet.nom_long = "N° de projet (100c)"
	poids_reference = MyFields.FloatField(blank=True, default=None, null=True, verbose_name="Quantité de référence", help_text="g")
	poids_reference.nom_colonne = "Référence"
	poids_reference.nom_long = "Quantité de référence"
	num_roxane = MyFields.CharField(max_length=12, blank=True, default="", verbose_name="N° Roxane")
	num_roxane.nom_colonne = "N° roxane"
	num_roxane.nom_long = "N° de fabrication roxane"
	nbr_ligne_robot = MyFields.IntegerField(blank=True, default=None, null=True, verbose_name="Nbr Roxane")
	nbr_ligne_robot.nom_colonne = "Nbr Roxane"
	nbr_ligne_robot.nom_long = "Nombre de lignes produitent par roxane"
	nbr_ligne_manuel = MyFields.IntegerField(blank=True, default=None, null=True, verbose_name="Nbr Manuel")
	nbr_ligne_manuel.nom_colonne = "Nbr Manuel"
	nbr_ligne_manuel.nom_long = "Nombre de lignes produitent en manuel"
	responsable_creation = models.ForeignKey(User, related_name="responsable_c", blank=True, default=None, null=True, verbose_name="Responsable creation")
	date_flash_point = MyFields.DateField(default=None, blank=True, null=True, verbose_name="Date Flash")
	date_flash_point.nom_colonne = "Date flash"
	date_flash_point.nom_long = "Date de point éclair"
	date_flash_point.format_date_time = "%d/%m/%Y"
	flash_point = MyFields.FloatField(blank=True, default=None, null=True, verbose_name="Flash", help_text="°C")
	flash_point.nom_colonne = "Flash"
	flash_point.nom_long = "Point éclair"
	responsable_flash_point = models.ForeignKey(User, related_name="nomenclature_lot_responsable_fp", blank=True, default=None, null=True, verbose_name="Responsable Flash")
	def get_poids_reference_unit(self, unit=None):
		if unit == None:
			unit = models_user.UnitMasse.objects.get(code="g")
		if type(unit) == type("string"):
			unit = models_user.UnitMasse.objects.get(code=unit)
		poids = {}
		if self.poids_reference == None:
			poids.update({"poids":None})
			poids.update({"unit":unit.code})
			poids.update({"poids_unit":"??"})
		else:
			poids.update({"poids":self.poids_reference/unit.facteur})
			poids.update({"unit":unit.code})
			poids.update({"poids_unit":"%.3f%s" %(self.poids_reference/unit.facteur, unit.code)})
		return poids
	def get_nomenclature_lot_ingredient(self):
		return NomenclatureLotIngredient.objects.filter(nomenclature_lot_id=self.id)
	def get_nomenclature_lot_contenant(self, supp=None):
		if supp == True:
			return models_contenant.Contenant.objects.filter(nomenclature_lot_id=self.id).filter(date_suppression__isnull=False)
		if supp == False:
			return models_contenant.Contenant.objects.filter(nomenclature_lot_id=self.id).filter(date_suppression__isnull=True)
		else:
			return models_contenant.Contenant.objects.filter(nomenclature_lot_id=self.id)
	def add_contenant(self, responsable_creation, type_contenant=None, date_creation=None, date_fin_validite=None, code=None):
		"""
		Ajoute un nouveau contenant pour ce lot
		"""
		if date_creation == None:
			date_creation = datetime.date.today()
		if type_contenant == None:
			type_contenant = models_contenant.ContenantType(pk=1)
		if date_fin_validite == None:
			date_fin_validite = self.date_fin_validite
		cont = models_contenant.Contenant.objects.filter(code=code)
		if len(cont) == 0:
			cont = models_contenant.Contenant(nomenclature_lot=self, type_contenant=type_contenant, code=code, date_creation=date_creation, date_fin_validite=date_fin_validite, responsable_creation=responsable_creation)
			cont.save()
			if cont.code == None or cont.code == "":
				cont.code = "2%0.9d" %(cont.id)
				cont.save()
#				cont.contenant_stat()
			return cont
		if len(cont) == 1:
			raise models_contenant.ContenantExistant(cont[0])
		else:
			raise models_contenant.ContenantMultipleErreur(cont)
	def add_ingredient(self, ingredient, poids, tol_pos=None, tol_neg=None, somme=False):
		"""
		Ajoute un nouvelle ingrédient pour ce lot
		"""
		ing = NomenclatureLotIngredient.objects.filter(formule=self.id).filter(ingredient=ingredient.id)
		if len(ing) == 0:
			ing = NomenclatureLotIngredient(formule=self, ingredient=ingredient, poids=poids, tol_pos=tol_pos, tol_neg=tol_neg)
			ing.save()
			self.definition = True
			self.save()
			return ing
		elif len(ing) == 1:
			if somme == False:
				raise NomenclatureLotIngredientExistant(ing[0])
			else:
				ing[0].poids += poids
				ing[0].tol_pos += tol_pos
				ing[0].tol_neg += tol_neg
				ing[0].save()
				self.definition = True
				self.save()
				return ing[0]
		else:
			raise NomenclatureLotIngredientMultipleErreur(ing)
	def get_client(self):
		if self.projet != None and self.projet != "":
			oracle_client = get_oracle_info(projet = self.projet, limit = 25, exact=True)
			if len(oracle_client) == 0:
				return "??"
			if len(oracle_client) == 1:
				return oracle_client[0]["CLIENT"]
			else:
				return "???"
		else:
			return ""
	def get_client_ka(self):
		if self.projet != None and self.projet != "":
			oracle_client = get_oracle_info(projet = self.projet, limit = 25, exact=True)
			if len(oracle_client) == 0:
				return "??"
			if len(oracle_client) == 1:
				return oracle_client[0]["CLIENT_KA"]
			else:
				return "???"
		else:
			return ""
	def duree_validite(self):
		return self.date_fin_validite - self.date_creation
	def fin_validite(self, duree=None):
		if self.nomenclature.duree_validite == None:
			return None
		else:
			if duree == None:
				return self.date_creation + datetime.timedelta(days = self.nomenclature.duree_validite)
			else:
				return self.date_creation + datetime.timedelta(days = duree)
	def suppression(self, user):
		"""
		Supprime moi et mes enfants
		"""
		print_ascii("Suppression : %s" %(unicode(self)))
		cont = models_contenant.Contenant.objects.filter(nomenclature_lot=self.id, date_suppression__isnull=True)
		for c in cont:
			c.suppression(user)
		self.date_suppression = datetime.date.today()
		self.save()
		log = django_models.LogEntry()
		log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
		log.user = user																						#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
		log.content_type = ContentType.objects.get(app_label="stock_labo", model="NomenclatureLot".lower())	#Le type de contenu (ContentType) de l’objet modifié.
		log.object_id = self.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
		log.object_repr = self.__unicode__()																		#La représentation repr() de l’objet après sa modification.
		log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
		log.change_message = "self.suppression()"															#Description de la modification
		log.save()
		return
	def suppression_parent(self, user):
		"""
		Supprime mes parents
		"""
		print_ascii("Suppression check parent de %s" %(unicode(self)))
		lot = self.nomenclature.get_nomenclature_lot(supp=False)
		if len(lot) == 0:
			print_ascii("Suppression : %s" %(unicode(self.nomenclature)))
			self.nomenclature.date_suppression = datetime.date.today()
			self.nomenclature.save()
			self.nomenclature.suppression_parent(user)
			log = django_models.LogEntry()
			log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
			log.user = user																						#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
			log.content_type = ContentType.objects.get(app_label="stock_labo", model="Nomenclature".lower())	#Le type de contenu (ContentType) de l’objet modifié.
			log.object_id = self.nomenclature.id																#La représentation textuelle de la clé primaire de l’objet modifié.
			log.object_repr = self.nomenclature.__unicode__()																#La représentation repr() de l’objet après sa modification.
			log.action_flag = django_models.CHANGE 																#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
			log.change_message = "self.suppression_parent()"													#Description de la modification
			log.save()
		return
	def destruction_ing(self, user):
		"""
		Destruction des ing d'un lot
		"""
		#print_ascii("Destruction ingrédient de : %s" %(unicode(self.__unicode__())))
		ing = NomenclatureLotIngredient.objects.filter(ingredient=self.id)
		for l in ing:
			ing_d = NomenclatureLotIngredientDosage.objects.filter(nomenclature_lot_ingredient=l.id)
			for d in ing_d:
				print_ascii("Destruction : %s" %(unicode(d)))
				log = django_models.LogEntry()
				log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
				log.user = user																						#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
				log.content_type = ContentType.objects.get(app_label="stock_labo", model="NomenclatureLotIngredient".lower())		#Le type de contenu (ContentType) de l’objet modifié.
				log.object_id = d.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
				log.object_repr = d.__unicode__()																	#La représentation repr() de l’objet après sa modification.
				log.action_flag = django_models.DELETION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
				log.change_message = "self.destruction_ing(%s)" %(d)												#Description de la modification
				log.save()
				d.delete()
			print_ascii("Destruction : %s" %(unicode(l)))
			log = django_models.LogEntry()
			log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
			log.user = user																						#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
			log.content_type = ContentType.objects.get(app_label="stock_labo", model="NomenclatureLotIngredientDosage".lower())		#Le type de contenu (ContentType) de l’objet modifié.
			log.object_id = l.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
			log.object_repr = l.__unicode__()																	#La représentation repr() de l’objet après sa modification.
			log.action_flag = django_models.DELETION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
			log.change_message = "self.destruction_ing(%s)"	%(l)												#Description de la modification
			log.save()
			l.delete()
		return
	def destruction_test(self, user):
		"""
		L'enfant sucidaire interroge sont parent pour savoir s'il est le seul enfant
		Si le parent n'a qu'un enfant alors l'enfant tue sont parent
		( => le parent mort : pas d'enfant )
		destruction_test retourne le plus grand...parent qui peut être détruit
		"""
		a = None
		# self peux être détruit ?
		if self.get_nomenclature_lot_contenant().count() == 1:
			a = self
		else:
			a = None
		# le parent de self peut être détruit ?
		if a == self:
			q = self.nomenclature.destruction_test(user)
			if q == None:
				return a
			else:
				return q
		else:
			return None
	def destruction(self, user):
		for l in self.get_nomenclature_lot_contenant():
			l.destruction(user)
		self.destruction_ing(user)
		log_auto(user=user, obj=self, flag="d", info="self.destruction(%s)" %(self))
		self.delete()
	def f_date_creation(self, f):
		if self.date_creation == None:
			return "??"
		elif self.date_creation == "":
			return "???"
		elif self.date_creation.year < 1900:
			return "Oh!!!"
		else:
			return self.date_creation.strftime(f)
	def f_date_fin_validite(self, f):
		if self.date_fin_validite == None:
			return "??"
		elif self.date_fin_validite == "":
			return "???"
		elif self.date_fin_validite.year < 1900:
			return "Oh!!!"
		else:
			return self.date_fin_validite.strftime(f)
	def f_date_suppression(self, f):
		if self.date_suppression == None:
			return "??"
		elif self.date_suppression == "":
			return "???"
		elif self.date_suppression.year < 1900:
			return "Oh!!!"
		else:
			return self.date_suppression.strftime(f)
	def nomenclature_lot_stat(self):
		"""
		Crée le lot dans la table nomenclaturelotstat
		"""
		lot_stat = NomenclatureLotStat()
		lot_stat.code = self.code 

		lot_stat.nomenclature_code = self.nomenclature.code
		lot_stat.nomenclature_description = self.nomenclature.description
		lot_stat.nomenclature_type_code = self.nomenclature.nomenclature_type.code

		lot_stat.date_creation = self.date_creation
		lot_stat.client = self.client
		lot_stat.client_ka = self.client_ka
		lot_stat.projet = self.projet
		lot_stat.poids_reference = self.poids_reference
		lot_stat.num_roxane = self.num_roxane
		lot_stat.nbr_ligne_robot = self.nbr_ligne_robot
		lot_stat.nbr_ligne_manuel = self.nbr_ligne_manuel
		if self.responsable_creation == None:
			lot_stat.responsable_creation_login = "??"
		else:
			lot_stat.responsable_creation_login = self.responsable_creation.username
		lot_stat.save()
	def __unicode__(self):
		return "Lot %s de %s" %(self.code, self.nomenclature)
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")
	class Meta:
		ordering = ["date_creation"]

class NomenclatureLotIngredient(models.Model): #INGREDIENT
	"""
		Liste des article des lot des Nomenclature/Formule/Ingrédients
	"""
	DOSAGE_VALIDITE = {
		0: "Non dosé",
		1: "Tolérence !!!!",
		10: "Sous-Dosé",
		20: "Dosage OK",
		30: "Sur-Dosé",
		}
	formule = models.ForeignKey(NomenclatureLot, verbose_name="Formule")
	ingredient = models.ForeignKey(Nomenclature, verbose_name="Ingrédient")
	poids = MyFields.FloatField(verbose_name="Poids à doser", default=0, help_text="g")
	poids.nom_colonne = "A doser"
	poids.nom_long = "Poids à doser"
	doser = MyFields.FloatField(verbose_name="Poids dosé", default=0, help_text="g")
	doser.nom_colonne = "Dosé"
	doser.nom_long = "Poids dosé"
	tol_pos = MyFields.FloatField(verbose_name="Tolérence positive", blank=True, default=None, null=True, help_text="g")
	tol_pos.nom_colonne = "Tol. Pos."
	tol_pos.nom_long = "Tolérence positive du dosage"
	tol_neg = MyFields.FloatField(verbose_name="Tolérence negative", blank=True, default=None, null=True, help_text="g")
	tol_neg.nom_colonne = "Tol. Neg."
	tol_neg.nom_long = "Tolérence négative du dosage"
	valide = MyFields.IntegerField(choices=DOSAGE_VALIDITE.items(), default=0, verbose_name="Execution du dosage")
	valide.nom_colonne = "Validité"
	valide.nom_long = str(DOSAGE_VALIDITE)
	definition = MyFields.BooleanField(default=False, verbose_name="Dosage disponible", help_text="Mise à jour automatique")
	definition.nom_colonne = "Def"
	definition.nom_long = "Liste des dosage"
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
	def get_doser_unit(self, unit=None):
		if unit == None:
			unit = models_user.UnitMasse.objects.get(code="g")
		if type(unit) == type("string"):
			unit = models_user.UnitMasse.objects.get(code=unit)
		poids = {}
		if self.doser == None:
			poids.update({"poids":None})
			poids.update({"unit":unit.code})
			poids.update({"poids_unit":"??"})
		else:
			poids.update({"poids":self.doser/unit.facteur})
			poids.update({"unit":unit.code})
			poids.update({"poids_unit":"%.3f%s" %(self.doser/unit.facteur, unit.code)})
		return poids
	def get_tol_pos_unit(self, unit=None):
		if unit == None:
			unit = models_user.UnitMasse.objects.get(code="g")
		if type(unit) == type("string"):
			unit = models_user.UnitMasse.objects.get(code=unit)
		poids = {}
		if self.tol_pos == None:
			poids.update({"poids":None})
			poids.update({"unit":unit.code})
			poids.update({"poids_unit":"??"})
		else:
			poids.update({"poids":self.tol_pos/unit.facteur})
			poids.update({"unit":unit.code})
			poids.update({"poids_unit":"%.3f%s" %(self.tol_pos/unit.facteur, unit.code)})
		return poids
	def get_tol_neg_unit(self, unit=None):
		if unit == None:
			unit = models_user.UnitMasse.objects.get(code="g")
		if type(unit) == type("string"):
			unit = models_user.UnitMasse.objects.get(code=unit)
		poids = {}
		if self.tol_neg == None:
			poids.update({"poids":None})
			poids.update({"unit":unit.code})
			poids.update({"poids_unit":"??"})
		else:
			poids.update({"poids":self.tol_neg/unit.facteur})
			poids.update({"unit":unit.code})
			poids.update({"poids_unit":"%.3f%s" %(self.tol_neg/unit.facteur, unit.code)})
		return poids
	def get_nomenclature_lot_ingredient_dosage(self):
		return NomenclatureLotIngredientDosage.objects.filter(pk=self.id)
	def add_dosage(self, doser, contenant_code=None, lot=None, responsable_login=None, responsable_id=None, date_dosage=None):
		"""
		Ajoute un dosage por cette ingrédient
			faire le controle de toléance ajouster le flag valide
		"""
		if date_dosage == None:
			date_dosage = datetime.datetime.now()
		if doser == 0.0:
			return None
		else:
			dosage = NomenclatureLotIngredientDosage(nomenclature_lot_ingredient=self, doser=doser, lot=lot, contenant_code=contenant_code, responsable_login=responsable_login, responsable=responsable_id, date_dosage=date_dosage)
			dosage.save()
			self.doser += doser
			if self.tol_pos != None and self.tol_neg != None:
				if self.doser > self.poids + self.tol_pos:
					self.valide = 30
				elif self.doser < self.poids + self.tol_neg:
					self.valide = 10
				else:
					self.valide = 20
			else:
				self.valide = 1
			self.definition = True
			self.save()
		return dosage

	def substitution(self):
		"""
		La substitution entraine la gérération d'un nouveau lot avec la substitution
			blog.pk == 1
			blog.pk = None
			blog.save() => blog.pk == 2
			copie des ingnédient dans le nouveau lot
			déplacement des dosage dans le nouveau lot
		"""
		print_ascii("Pas de Suppression : %s" %(unicode(self)))
	def suppression(self, user):
		"""
		On ne supprime jamais un ingrédient, on le sbstitue
		"""
		print_ascii("Pas de Suppression : %s" %(unicode(self)))
		raise Interdit()
	#def destruction_parent(self, user):
	#	"""
	#	Destruction d'un dosage interdit !!!!
	#	"""
	#	print_ascii("Destruction : %s" %(unicode(self)))
	#	raise NomenclatureLotIngredientDosageDestructionInterdit()
	#	return
	#def destruction(self, user):
	#	"""
	#	Si l'ingredient ne contient plus d'ingrédient, RAZ du flag definition
	#	"""
	#	print_ascii("Destruction : %s" %(unicode(self)))
	#	raise NomenclatureLotIngredientDosageDestructionInterdit()
	#	return
	def __unicode__(self):
		return "[%s - %s] - %.3fg/%.3fg : %s" %(self.formule, self.ingredient, self.doser, self.poids, self.DOSAGE_VALIDITE[self.valide])
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")
	class Meta:
		ordering = ["ingredient"]

class NomenclatureLotIngredientDosage(models.Model): #DOSAGE
	"""
		Liste des dosages des article des lots des Nomenclature
	"""
	nomenclature_lot_ingredient = models.ForeignKey(NomenclatureLotIngredient, verbose_name="Dosage de l'article")
	doser = MyFields.FloatField(verbose_name="Poids dosé", default=0, help_text="g")
	doser.nom_colonne = "Dosé"
	doser.nom_long = "Dosage partiel"
	contenant_code = MyFields.CharField(max_length=30, blank=True, default=None, null=True, verbose_name="Code Contenant Utilisé pour le dosage")
	contenant_code.nom_colonne = "Contenant"
	contenant_code.nom_long = "Contenant utilisé pour le dosage (30c)"
	lot = MyFields.CharField(max_length=30, blank=True, default=None, null=True, verbose_name="Code Lot Utilisé pour le dosage")
	lot.nom_colonne = "Lot"
	lot.nom_long = "Lot utilisé pour le dosage"
	responsable_login = MyFields.CharField(max_length=30, blank=True, default=None, null=True, verbose_name="Responsable de pesée")
	responsable_login.nom_colonne = "Opérateur"
	responsable_login.nom_long = "Nom de l'opérateur pour ce dosage (30c)"
	responsable = models.ForeignKey(User, blank=True, default=None, null=True, verbose_name="Utilisateur")
	date_dosage = MyFields.DateTimeField(blank=False, default=None, null=False, help_text="YYYY-MM-DD HH:MM:SS", verbose_name="Date de Dosage")
	date_dosage.nom_colonne = "Date dosage"
	date_dosage.nom_long = "Date de réalisation du dosage"
	date_dosage.format_date_time = "%d/%m/%Y %H-%M-%S"
	def get_doser_unit(self, unit=None):
		if unit == None:
			unit = models_user.UnitMasse.objects.get(code="g")
		if type(unit) == type("string"):
			unit = models_user.UnitMasse.objects.get(code=unit)
		poids = {}
		if self.doser == None:
			poids.update({"poids":None})
			poids.update({"unit":unit.code})
			poids.update({"poids_unit":"??"})
		else:
			poids.update({"poids":self.doser/unit.facteur})
			poids.update({"unit":unit.code})
			poids.update({"poids_unit":"%.3f%s" %(self.doser/unit.facteur, unit.code)})
		return poids
	def suppression(self, user):
		"""
		suppression d'un dosage interdit !!!!!
		"""
		print_ascii("Pas de Suppression : %s" %(unicode(self)))
		raise Interdit()
	#def destruction_parent(self, user):
	#	"""
	#	Destruction d'un dosage interdit !!!!
	#	"""
	#	print_ascii("Destruction : %s" %(unicode(self)))
	#	raise NomenclatureLotIngredientDosageDestructionInterdit()
	#	return
	def destruction(self, user):
		"""
		Destruction d'un dosage interdit !!!!
		"""
		print_ascii("Destruction : %s" %(unicode(self)))
		raise NomenclatureLotIngredientDosageDestructionInterdit()
		return
	def f_date_dosage(self, f):
		if self.date_dosage == None:
			return "??"
		elif self.date_dosage == "":
			return "???"
		elif self.date_dosage.year < 1900:
			return "Oh!!!"
		else:
			return self.date_dosage.strftime(f)
	def __unicode__(self):
		return "[%s]-%.3fg/%.3fg" %(self.nomenclature_lot_ingredient, self.doser, self.nomenclature_lot_ingredient.poids)
	def __str__(self):
		return self.__unicode__().encode("ascii", "replace")
	class Meta:
		ordering = ["nomenclature_lot_ingredient"]


