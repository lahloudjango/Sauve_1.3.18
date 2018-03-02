# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

import MyFields
#from django.contrib.admin.widgets import AdminDateWidget
import traceback

import models_contenant
import models_stock
from models_nomenclature import *
import settings_default

from fonction import *

import django.core.exceptions
import django.db
#except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
#except django.db.IntegrityError:


def add_nomenclature_type(code, description):
	"""
		Ajout d'un nouveau type de contenant
		Si le contenant existe déja, l'objet nomenclature_type correspondant est retourné
		Si le type n'existe pas, le type est créer et l'objet nomenclature_type correspondant est retourné
	"""
	n_type = NomenclatureType.objects.filter(code=code)
	if len(n_type) == 0:
		n_type = NomenclatureType(code=code, description=description)
		n_type.save()
		return n_type
	if len(n_type) == 1:
		raise NomenclatureTypeExistant(n_type[0])
	else:
		raise NomenclatureTypeMultipleErreur(n_type)

def import_generic(emplacement, nom, extension, fin_de_ligne="\n"):
	"""
	import generique de fichier

	Correspondance classe de champs fichier csv et objet base de données
		NomenclatureType = article_type
		Nomenclature = article
		NomenclatureLot = article_lot
		NomenclatureLotIngredient = article_lot_ing
		NomenclatureLotIngredientDosage = article_lot_ing_dos

		ContenantType = contenant_type
		Contenant = contenant

		StockSite = stock_site
		StockEntrepot = stock_entrepot
		StockMagasin = stock_magazin

	le classe d'objet doivent être dans cette ordre dans les colonnes
		"article_type" : None,
		"article" : None,
		"article_lot" : None,
		"article_lot_ing" : None,
		"article_lot_ing_dos" : None,
		"contenant_type" : None,
		"stock_site" : None,
		"stock_entrepot" : None,
		"stock_magazin" : None,
		"contenant" : None,


	"""

	f = codecs.open(emplacement+nom+extension, "r", encoding="utf-8")
	fichier_import = f.read().split(fin_de_ligne)
	f.close()

	h = fichier_import.pop(0)
	hh = h.split(";")
	head = []
	erreur = ""

	for hhh in hh:
		head.append({"obj":hhh.split(".")[0],"champ":hhh.split(".")[1]})
	linge = []
	l = 0 # n° de ligne du fichier
	c = 0 # n° de colonne du fichier
	while l < len(fichier_import):
		if len(fichier_import[l]) == 0:
			l += 1
			continue
		try:
			objs = {
				"article_type" : None,
				"article" : None,
				"article_lot" : None,
				"article_lot_ing" : None,
				"article_lot_ing_dos" : None,
				"contenant_type" : None,
				"stock_site" : None,
				"stock_entrepot" : None,
				"stock_magazin" : None,
				"contenant" : None,
				}
			ligne = fichier_import[l].split(";")
			print_ascii(ligne)
			c = 0
			while c < len(ligne):
				valeur = None
				if head[c]["champ"] == "code":
					valeur = ligne[c]
				else:
					try:
						valeur = int(ligne[c])
					except:
						try:
							valeur = float(ligne[c])
						except:
							valeur = ligne[c]
				if head[c]["obj"] == "article_type":
					try:
						objs[head[c]["obj"]] = NomenclatureType.objects.get(**{head[c]["champ"]:valeur})
					except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
						objs[head[c]["obj"]] = NomenclatureType(**{head[c]["champ"]:valeur})
						objs[head[c]["obj"]].save()
					cc = c + 1
					while cc < len(ligne) and head[cc]["obj"] == head[c]["obj"]:
						try:
							v = int(ligne[cc])
						except:
							try:
								v = float(ligne[cc])
							except:
								v = ligne[cc]
						setattr(objs[head[c]["obj"]], head[cc]["champ"], v)
						cc += 1
					objs[head[c]["obj"]].save()
					c = cc
				elif head[c]["obj"] == "article":
					try:
						objs[head[c]["obj"]] = objs["article_type"].add_nomenclature(**{head[c]["champ"]:valeur})
					except NomenclatureExistant as i:
						objs[head[c]["obj"]] = i.args[0]
					cc = c + 1
					while cc < len(ligne) and head[cc]["obj"] == head[c]["obj"]:
						try:
							v = int(ligne[cc])
						except:
							try:
								v = float(ligne[cc])
							except:
								v = ligne[cc]
						setattr(objs[head[c]["obj"]], head[cc]["champ"], v)
						cc += 1
					objs[head[c]["obj"]].save()
					c = cc
				elif head[c]["obj"] == "article_lot":
					try:
						objs[head[c]["obj"]] = objs["article"].add_lot(**{head[c]["champ"]:valeur})
					except NomenclatureLotExistant as i:
						objs[head[c]["obj"]] = i.args[0]
					cc = c + 1
					while cc < len(ligne) and head[cc]["obj"] == head[c]["obj"]:
						try:
							v = int(ligne[cc])
						except:
							try:
								v = float(ligne[cc])
							except:
								v = ligne[cc]
						setattr(objs[head[c]["obj"]], head[cc]["champ"], v)
						cc += 1
					objs[head[c]["obj"]].save()
					c = cc
	#			elif head[c]["obj"] == "article_lot_ing":
	#			elif head[c]["obj"] == "article_lot_ing_dos":
	#			elif head[c]["obj"] == "contenant_type":
	#			elif head[c]["obj"] == "stock_site":
	#			elif head[c]["obj"] == "stock_entrepot":
	#			elif head[c]["obj"] == "stock_magazin":
	#			elif head[c]["obj"] == "contenant":



				else:
					print_ascii("!!!!!!!!!L'OBJECT N'EST PAS RECONNU!!!!!!!!!")
					c += 1

		except:
#			print_ascii("Fichier : %s:%d : %s" %(nom+extension, l, ligne))
#			print_ascii(traceback.format_exc())
			erreur += "Fichier : %s:%d : %s" %(nom+extension, l, ligne)
			erreur += str(traceback.format_exc())
			erreur += "-"*80
			erreur += "\n"
			erreur += dump_env(locals())
			erreur += "\n"

#		bloquage de test
#		if l == 0:
#			break

		l += 1

	return erreur

def import_navette_sap(emplacement, nom, extension, fin_de_ligne="\n"):
	"""
	import des fichier de navette SAP
		0: Type de matière
		1: Code Corporate
		2: Désignation article
		3: Type de conditionnement
		4: Poids net ( en g )
		5: Numéro de lot
		6: Date de fin de validité (YYYYMMDD)
		7: Numéro d'unité de stock

	"""
	print_ascii("import_navette_sap : " + emplacement+nom+extension)
	f = codecs.open(emplacement+nom+extension, "r", encoding="utf-8")
	fichier_import = f.read().split(fin_de_ligne)
	f.close()

	erreur = ""
	h = fichier_import.pop(0)
	head = h.split(";")
	#print_ascii(head)
	l = 0
	c = 0
	while l < len(fichier_import):
		if len(fichier_import[l]) == 0:
			l += 1
			continue
		ligne = fichier_import[l].split(";")
		if ligne[0] in ("RAWM", "BASE", "FINI"):
			try:
				ligne = fichier_import[l].split(";")
				objs = {}
				objs.update({"article_type_code" : "MP"})
				objs.update({"article_type_description" : "???"})
				objs.update({"article_code" : ligne[1]})
				objs.update({"article_description" : ligne[2]})
				objs.update({"article_lot_code" : ligne[5]})
				objs.update({"article_contenant_poids" : float(ligne[4])})
				try:
					objs.update({"article_contenant_type" : models_contenant.ContenantType.objects.get(code=ligne[3])})
				except django.core.exceptions.ObjectDoesNotExist, django.core.exceptions.DoesNotExist:
					objs.update({"article_contenant_type" : models_contenant.ContenantType.objects.get(code="??")})
				objs.update({"article_contenant_code" : ligne[7]})
				objs.update({"fin_validite" : ligne[6]})

				try:
					n_type = add_nomenclature_type(objs["article_type_code"], objs["article_type_description"])
				except NomenclatureTypeExistant as i:
					n_type = i.args[0]
				try:
					n = n_type.add_nomenclature(code=objs["article_code"], description=objs["article_description"])
				except NomenclatureExistant as i:
					n = i.args[0]
				else:
					log = django_models.LogEntry()
					log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
					log.user = User.objects.get(username="script")														#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
					log.content_type = ContentType.objects.get_for_model(n)												#Le type de contenu (ContentType) de l’objet modifié.
					log.object_id = n.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
					log.object_repr = unicode(n)																		#La représentation repr() de l’objet après sa modification.
					log.action_flag = django_models.ADDITION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
					log.change_message = "import_navette_sap"															#Description de la modification
					log.save()

				try:
					lot = n.add_lot(code=objs["article_lot_code"], responsable_creation=User.objects.get(username="script"), date_fin_validite=datetime.datetime.strptime(objs["fin_validite"],"%Y%m%d"))
				except NomenclatureLotExistant as i:
					lot = i.args[0]
				else:
					log = django_models.LogEntry()
					log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
					log.user = User.objects.get(username="script")														#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
					log.content_type = ContentType.objects.get_for_model(lot)											#Le type de contenu (ContentType) de l’objet modifié.
					log.object_id = lot.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
					log.object_repr = unicode(lot)																		#La représentation repr() de l’objet après sa modification.
					log.action_flag = django_models.ADDITION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
					log.change_message = "import_navette_sap"															#Description de la modification
					log.save()

				try:
					cont = lot.add_contenant(responsable_creation=User.objects.get(username="script"), code=objs["article_contenant_code"])
				except models_contenant.ContenantExistant as i:
					cont = i.args[0]
					print_ascii(unicode(cont) + " existe déjà")
				else:
					cont.provenance_site = models_stock.StockSite.objects.get(code="STO")
					cont.poids = objs["article_contenant_poids"]
					cont.tare = cont.type_contenant.tare
					cont.type_contenant = objs["article_contenant_type"]
					cont.save()
					log = django_models.LogEntry()
					log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
					log.user = User.objects.get(username="script")														#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
					log.content_type = ContentType.objects.get_for_model(cont)											#Le type de contenu (ContentType) de l’objet modifié.
					log.object_id = cont.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
					log.object_repr = unicode(cont)																		#La représentation repr() de l’objet après sa modification.
					log.action_flag = django_models.ADDITION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
					log.change_message = "import_navette_sap"															#Description de la modification
					log.save()
					print_ascii(unicode(cont) + " nouveau")

			except:
	#			print_ascii("Fichier : %s:%d : %s" %(nom+extension, l, ligne))
	#			print_ascii(traceback.format_exc())
				erreur += "Fichier : %s:%d : %s" %(nom+extension, l, ligne)
				erreur += str(traceback.format_exc())
				erreur += "\n"
				erreur += dump_env(locals())
				erreur += "-"*80
				erreur += "\n"
		else:
			print_ascii("ligne de code ligne inconnu : " + fichier_import[l])

#		bloquage de test
#		if l == 0:
#			break

		l += 1
	return erreur

def import_solution_vincent(emplacement, nom, extension, fin_de_ligne="\n"):
	"""
	import des fichier des solution dénéré depuis le fichier exel de vincent
	"""
	print_ascii("import_solution_vincent : " + emplacement+nom+extension)

	f = codecs.open(emplacement+nom+extension, "r", encoding="latin_1")
	fichier_import = f.read().split(fin_de_ligne)
	f.close()

	erreur = ""
	h = fichier_import.pop(0)
	head = h.split(",")
#	print_ascii(head)
	l = 0
	while l < len(fichier_import):
		if len(fichier_import[l]) == 0:
			l += 1
			continue
		ligne = fichier_import[l].split(",")
#		print_ascii(ligne)

		try:

			try:
				n_type = add_nomenclature_type("MP", "Matière première")
			except NomenclatureTypeExistant as i:
				n_type = i.args[0]

			try:
				code = "%06d" %(int(ligne[5]))
			except:
				code = ligne[5]
			try:
				pure = n_type.add_nomenclature(code=code)
			except NomenclatureExistant as i:
				pure = i.args[0]
			else:
				log = django_models.LogEntry()
				log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
				log.user = User.objects.get(username="script")														#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
				log.content_type = ContentType.objects.get_for_model(pure)											#Le type de contenu (ContentType) de l’objet modifié.
				log.object_id = pure.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
				log.object_repr = unicode(pure)																		#La représentation repr() de l’objet après sa modification.
				log.action_flag = django_models.ADDITION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
				log.change_message = "import_solution_vincent pure"															#Description de la modification
				log.save()

			try:
				code = "%06d" %(int(ligne[7]))
			except:
				code = ligne[7]
			try:
				solvant = n_type.add_nomenclature(code=code)
			except NomenclatureExistant as i:
				solvant = i.args[0]
			else:
				log = django_models.LogEntry()
				log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
				log.user = User.objects.get(username="script")														#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
				log.content_type = ContentType.objects.get_for_model(solvant)										#Le type de contenu (ContentType) de l’objet modifié.
				log.object_id = solvant.id																			#La représentation textuelle de la clé primaire de l’objet modifié.
				log.object_repr = unicode(solvant)																	#La représentation repr() de l’objet après sa modification.
				log.action_flag = django_models.ADDITION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
				log.change_message = "import_solution_vincent solvant"												#Description de la modification
				log.save()

			ps = int((float(ligne[6].replace(",", ".")) / float(ligne[4].replace(",", ".")))*100)
			objs = {}
			objs.update({"article_type_code" : "S"})
			objs.update({"article_type_description" : "Solution"})
			objs.update({"article_code" : ligne[1]})
			objs.update({"article_commentaire" : "%s%s%d%s%s" %(pure.code, "@", ps, "%", solvant.code)})
			objs.update({"article_description" : "%s%s%d%s%s" %(pure.description, "@", ps, "%", solvant.description)})
#			if ligne[2].startswith("SOL"):
#				objs.update({"article_code" : ligne[1]})
#				objs.update({"article_description" : "%s%s%d%s%s" %(pure.code, "@", ps, "%", solvant.code)})
#				objs.update({"article_commentaire" : "%s%s%d%s%s" %(pure.description, "@", ps, "%", solvant.description)})
#			else:
#				objs.update({"article_code" : ligne[1]})
#				objs.update({"article_description" : "%s%s%d%s%s" %(pure.code, "@", ps, "%", solvant.code)})
#				objs.update({"article_commentaire" : "%s%s%d%s%s" %(pure.description, "@", ps, "%", solvant.description)})
			objs.update({"article_lot_code" : ligne[20]})
			objs.update({"contenant_code" : ligne[21]})
			objs.update({"pure_poids" : float(ligne[6].replace(",", "."))})
			objs.update({"solvant_poids" : float(ligne[8].replace(",", "."))})
			objs.update({"pure_dose" : float(ligne[13].replace(",", "."))})
			objs.update({"solvant_dose" : float(ligne[17].replace(",", "."))})
			objs.update({"responsable_login" : ligne[19]})

			try:
				n_type = add_nomenclature_type(objs["article_type_code"], objs["article_type_description"])
			except NomenclatureTypeExistant as i:
				n_type = i.args[0]
			try:
				n = n_type.add_nomenclature(code=objs["article_code"], description=objs["article_description"][:100], commentaire=objs["article_commentaire"])
			except NomenclatureExistant as i:
				n = i.args[0]
			else:
				log = django_models.LogEntry()
				log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
				log.user = User.objects.get(username="script")														#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
				log.content_type = ContentType.objects.get_for_model(n)												#Le type de contenu (ContentType) de l’objet modifié.
				log.object_id = n.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
				log.object_repr = unicode(n)																		#La représentation repr() de l’objet après sa modification.
				log.action_flag = django_models.ADDITION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
				log.change_message = "import_solution_vincent solution"												#Description de la modification
				log.save()

			try:
				lot = n.add_lot(code=objs["article_lot_code"], responsable_creation=User.objects.get(username="script"))
			except NomenclatureLotExistant as i:
				lot = i.args[0]
				print_ascii(unicode(lot) + " existe déjà")
			else:
				log = django_models.LogEntry()
				log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
				log.user = User.objects.get(username="script")														#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
				log.content_type = ContentType.objects.get_for_model(lot)											#Le type de contenu (ContentType) de l’objet modifié.
				log.object_id = lot.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
				log.object_repr = unicode(lot)																		#La représentation repr() de l’objet après sa modification.
				log.action_flag = django_models.ADDITION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
				log.change_message = "import_solution_vincent"														#Description de la modification
				log.save()
			try:
				cont = lot.add_contenant(responsable_creation=User.objects.get(username="script"), code=objs["contenant_code"])
			except models_contenant.ContenantExistant as i:
				cont = i.args[0]
				print_ascii(unicode(cont) + " existe déjà")
			else:
				log = django_models.LogEntry()
				log.action_time = datetime.datetime.now()															#La date et l’heure de l’action.
				log.user = User.objects.get(username="script")														#L’utilisateur (une instance AUTH_USER_MODEL) qui a procédé à l’action.
				log.content_type = ContentType.objects.get_for_model(cont)											#Le type de contenu (ContentType) de l’objet modifié.
				log.object_id = cont.id																				#La représentation textuelle de la clé primaire de l’objet modifié.
				log.object_repr = unicode(cont)																		#La représentation repr() de l’objet après sa modification.
				log.action_flag = django_models.ADDITION 															#Le type de l’action journalisée : ADDITION, CHANGE, DELETION.
				log.change_message = "import_solution_vincent solvant"												#Description de la modification
				log.save()
				poids = float(ligne[4].replace(",", "."))
				cont.type_contenant = cont.chois_type_contenant(poids)
				cont.poids = poids
				cont.tare = cont.type_contenant.tare
				cont.provenance_site = models_stock.StockSite.objects.get(code="STO")
				cont.save()


			try:
				ing = lot.add_ingredient(ingredient=pure, poids=objs["pure_poids"])
				dosage = ing.add_dosage(doser=objs["pure_dose"], responsable_login=objs["responsable_login"])
			except NomenclatureLotIngredientExistant as i:
				ing = i.args[0]
	#			dosage = ing.add_dosage(doser=float(ligne[13].replace(",", ".")), responsable_login=ligne[19])

			try:
				ing = lot.add_ingredient(ingredient=solvant, poids=objs["solvant_poids"])
				dosage = ing.add_dosage(doser=objs["solvant_dose"], responsable_login=objs["responsable_login"])
			except NomenclatureLotIngredientExistant as i:
				ing = i.args[0]
	#			dosage = ing.add_dosage(doser=float(ligne[17].replace(",", ".")), responsable_login=ligne[19])
		except:
#			print_ascii("Fichier : %s:%d : %s" %(nom+extension, l, ligne))
#			print_ascii(traceback.format_exc())
			erreur += "Fichier : %s:%d : %s" %(nom+extension, l, ligne)
			erreur += str(traceback.format_exc())
			erreur += "\n"
			erreur += dump_env(locals())
			erreur += "-"*80
			erreur += "\n"

#		bloquage de test
#		if l == 0:
#			break

		l += 1

	return erreur

def decode_roxane_export_new(emplacement, nom, extension, fin_de_ligne="\n"):
	"""
	Creation/ mise a jour d'une nomentclature en suivant un fichier d'export roxane nouvelle formule
	"""
	try:
		f = codecs.open(emplacement+nom+extension, "r", encoding="iso-8859-1")
	except IOError:
		try:
			f = codecs.open("%s%s/%s%s" %(emplacement, datetime.date.today().year, nom, extension), "r", encoding="iso-8859-1")
		except IOError:
			return None

	entete = {}
	ing = []
	becher = {}
	dosage_station = {"robot" : 0, "manuel": 0}
	fichier_formule = f.read().split("\r\n")
	f.close()
	UNITE_MASSE = {
		"mg" : 0.001,
		"g" : 1.0,
		"kg" : 1000.0,
	}
	ligne = fichier_formule.pop(0).split("|")
	#print_ascii(ligne)

	#0  N° de batch client
	#1  N° Compo-Manager local
	#2  Code formule
	#3  Date demande
	#4  Date validation
	#5  Quantité totale du batch
	#6  unité
	#7  Demandeur
	#8  Destinataire
	#9  Etat de l'O.F.
	#	R : Refusé
	#	T : Terminé
	entete.update({"batch" : ligne[0]})
	entete.update({"manager" : ligne[1]})
	entete.update({"code_formule" : ligne[2]})
	entete.update({"date_demande" : datetime.datetime.strptime(ligne[3].strip(),"%Y%m%d")})
	entete.update({"date_validation" : datetime.datetime.strptime(ligne[4].strip(),"%Y%m%d")})
	entete.update({"total" : float(ligne[5].replace(",", "."))*UNITE_MASSE[ligne[6]]})
	entete.update({"demandeur" : ligne[7]})
	entete.update({"destinataire" : ligne[8]})
	entete.update({"status" : ligne[9]})


	for l in fichier_formule:
		if len(l) == 0:
			continue
		ligne = l.split("|")
		#print_ascii(ligne)
		ll = {}
		# 001015|2|400|10|0|mg|<||2|1||201702221556|1
		#0  Code matière
		#1  Code ligne
		#2  Quantité demandée
		#3  Tolérance utilisée
		#4  Quantité de matière prélevée
		#5  unité
		#6  Statut du prélèvement
		#   > : Sur dosage Accepté
		#   < : Sous dosage accepté
		#   S : Sous dosage accepté
		#   >X: Dépassement refusé
		#   T : Terminé
		#   A : A faire
		#   ? : Problème
		#7  Numéro de lot
		#8  Numéro de ressource ayant prélevé le lot 1:robot, !=1 :manuel
		#9  Numéro de sous OF ( N° de becher )
		#10 Code opérateur ayant prélevé le lot
		#11 Date et heure du prélèvement
		#12 Temps de prélèvement en secondes
		ll.update({"code_ing" : ligne[0]})
		ll.update({"type_dosage" : ligne[1]})
		try:
			ll.update({"poids" : float(ligne[2].replace(",", "."))*UNITE_MASSE[ligne[5]]})
		except ValueError:
			ll.update({"poids" : None})
		try:
			ll.update({"tolérance" : float(ligne[3].replace(",", "."))*UNITE_MASSE[ligne[5]]})
		except ValueError:
			ll.update({"tolérance" : None})
		try:
			ll.update({"dosee" : float(ligne[4].replace(",", "."))*UNITE_MASSE[ligne[5]]})
		except ValueError:
			ll.update({"dosee" : None})
		ll.update({"statut" : ligne[6]})
		ll.update({"lot" : ligne[7]})
		ll.update({"station" : ligne[8]})
		ll.update({"code_operateur" : ligne[10]})
		try:
			ll.update({"date" : datetime.datetime.strptime(ligne[11],"%Y%m%d%H%M")})
		except ValueError:
			ll.update({"date" : None})
		try:
			ll.update({"temps" : int(ligne[12])})
		except ValueError:
			ll.update({"temps" : None})

		if becher.has_key(ligne[9]):
			becher[ligne[9]]["ing"].append(ll)
		else:
			becher.update({ ligne[9] : {} })
			becher[ligne[9]].update({ "ing" : [] })
			becher[ligne[9]]["ing"].append(ll)
			becher[ligne[9]].update({ "dosage_station" : {} })
			becher[ligne[9]]["dosage_station"].update({ "robot" : 0 })
			becher[ligne[9]]["dosage_station"].update({ "manuel" : 0 })
			becher.update({ "last" : becher[ligne[9]] })

		if becher[ligne[9]]["dosage_station"].has_key(ll["station"]):
			becher[ligne[9]]["dosage_station"][ll["station"]] += 1
		else:
			becher[ligne[9]]["dosage_station"].update({ll["station"]: 1})
		if ll["station"] == "1" or ll["station"] == 1:
			becher[ligne[9]]["dosage_station"]["robot"] += 1
		else:
			becher[ligne[9]]["dosage_station"]["manuel"] += 1


	for k in ["manager", "code_formule", "date_demande", "date_validation", "total", "demandeur", "destinataire", "status"]:
		print_ascii("%s : %s" %(k, entete[k]))
	for b in ["1", "2", "3", "4", "5", "6", "last"]:
		if becher.has_key(b):
			print_ascii("	Becher : %s" %(b))
			print_ascii("	Nbr ing : %s" %(len(becher[b]["ing"])))
			for s in becher[b]["dosage_station"].keys():
				print_ascii("		%s : %s" %(s, becher[b]["dosage_station"][s]))

	return {"entete": entete, "becher" : becher }

def decode_roxane_export(emplacement, nom, extension, fin_de_ligne="\n"):
	"""
	Creation/ mise a jour d'une nomentclature en suivant un fichier d'export roxane
	"""
	try:
		f = codecs.open(emplacement+nom+extension, "r", encoding="iso-8859-1")
	except IOError:
		try:
			f = codecs.open("%s%s/%s%s" %(emplacement, datetime.date.today().year, nom, extension), "r", encoding="iso-8859-1")
		except IOError:
			return None

	fichier_formule = f.read().split(fin_de_ligne)
	f.close()

	poids_total = float(fichier_formule[0][84:96])
	formule =None
	lot =None
	nbr_ligne = 0
	entete = {}
	ing = []
	dosage_station = {}
	IMPORT_ROXANE_EXPORT_STATUS = {
		"10": "Ok",
		"11": "Refusé",
		"12": "Refusé et à refaire",
		}
	for ligne in fichier_formule:
		if len(ligne) == 0:
			continue
		if ligne.startswith("A"):
			entete.update({"type_ligne" : ligne[0]}) 					# (1 car.) (A = ligne d'entête)
			entete.update({"type_ordre" : ligne[1:3]}) 					# (2 car.) (par défaut '04'=fabrication)
			entete.update({"batch" : ligne[3:23].strip()}) 				# (20 car.)
			entete.update({"manager" : ligne[23:43].strip()}) 			# (20 car.)
			entete.update({"code_formule" : ligne[43:63].strip()}) 		# (20 car.)
			entete.update({"date_demande" : datetime.datetime.strptime(ligne[63:73].strip(),"%Y/%m/%d")}) 		# (10 car.) format AAAA/MM/JJ
			entete.update({"date_validation" : datetime.datetime.strptime(ligne[73:83].strip(),"%Y/%m/%d")}) 	# (10 car.) format AAAA/MM/JJ
			entete.update({"total" : float(ligne[83:96].strip())}) 		# (13 car.) exprimée en grammes format 999999999.999 (Le séparateur décimal étant le point)
			entete.update({"demandeur" : ligne[96:106].strip()}) 		# (10 car.)
			entete.update({"destinataire" : ligne[106:116].strip()}) 	# (10 car.)
			entete.update({"status" : ligne[116:118]}) 					# (2 car.)	'10' = OK, '11' = Refusé,  ‘12’ = Refusé et à refaire

		if ligne.startswith("B"): #1 ligne pour chaque numéro de lot de matière, chaque ligne commençant par le 
			print_ascii("%d.." %(nbr_ligne))
			ll = {}

			ll.update({"type_ligne" : ligne[0]}) 					# (1 car.) (A = ligne d'entête)
			ll.update({"type_dosage" : ligne[1:3]}) 				# (2 car.) (valeur par défaut '01' = pesée)
			ll.update({"code_ing" : ligne[3:23].strip()}) 			# (20 car.)
			ll.update({"poids" : float(ligne[23:36].strip())}) 			# (13 car.) exprimée en grammes 
			ll.update({"tolérance" : float(ligne[36:49].strip())}) 		# (13 car.) exprimée en grammes 
			ll.update({"dosee" : float(ligne[49:62].strip())}) 			# (13 car.) exprimée en grammes 
			ll.update({"statut" : ligne[62:63]}) 					# (1 car.)		'A',’<’ ou ‘I’ = Sous-pesée		'T' = pesée correcte	'@' = dépassement accepté	'>' = dépassement refusé
			ll.update({"lot" : ligne[63:83].strip()}) 				# (20 car.)
			ll.update({"quantite_lot" : float(ligne[83:96].strip())}) 		# (13 car.) exprimée en grammes
			ll.update({"station" : ligne[96:98].strip()}) 			# (2 car.)
			ll.update({"code_operateur" : ligne[98:103].strip()}) 	# (5 car)
			ll.update({"date" : datetime.datetime.strptime(ligne[103:121].strip(),"%Y/%m/%d%H:%M:%S")}) 			# (10 car.) format AAAA/MM/JJ + (8 car.) format HH:MM:SS
			ll.update({"temps" : int(ligne[121:125].strip())}) 			# (4 car.) exprimé en secondes et uniquement pour la partie automatisée pour toutes les quantités le format est ‘999999999.999’ et le séparateur décimal est le point.

			if dosage_station.has_key(ll["station"]):
				dosage_station[ll["station"]] += 1
			else:
				dosage_station.update({ll["station"]: 1})
			if ll["station"] == "1" or ll["station"] == 1:
				dosage_station["robot"] += 1
			else:
				dosage_station["manuel"] += 1

			ing.append(ll)

		if ligne.startswith("C"):
			entete.update({"nbr_ligne" : int(ligne[1:11])}) 			# (2 car.) (par défaut '04'=fabrication)
			entete.update({"nbr_ligne_fichier" : len(ing)}) 			# (2 car.) (par défaut '04'=fabrication)


	return {"entete": entete, "ing": ing, "dosage_station": dosage_station}

def import_status_collection(emplacement, nom, extension, fin_de_ligne="\n"):
	"""
	importation status collection pour les articles
	Entête de colonne
	article_type.code
	article.code
	article.description
	article.commentaire
	article.collection
	"""
	import time
	data = csv_dic(emplacement+nom+extension, fin_de_ligne="\n", encoding="utf-8", separateur=";")
	for d in data:
		try:
			article_type = add_nomenclature_type(d["article_type.code"], "")
		except NomenclatureTypeExistant as i:
			article_type = i.args[0]
		try:
			article = article_type.add_nomenclature(d["article.code"], update=False, insert=True)
		except NomenclatureExistant as i:
			article = i.args[0]
			log_auto(user=User.objects.get(username="script"), obj=article, flag="c", info="import_status_collection")
			if article.description == "":
				article.description = d["article.description"]
			if article.commentaire == "":
				article.commentaire = d["article.commentaire"]
			article.duree_validite = settings_default.DUREE_VALIDITE_COL
			article.collection = True
			article.date_suppression = None
			article.save()
			lots = article.get_nomenclature_lot()
			for lot in lots:
				val = lot.fin_validite()
				if val != lot.date_fin_validite:
					log_auto(user=User.objects.get(username="script"), obj=lot, flag="c", info="import_status_collection")
					lot.date_fin_validite = lot.fin_validite()
					lot.save()
				cont = lot.get_nomenclature_lot_contenant()
				for c in cont:
					if c.date_reception != None:
						val = c.fin_validite()
						if val != c.date_fin_validite:
							log_auto(user=User.objects.get(username="script"), obj=c, flag="c", info="import_status_collection")
							c.date_fin_validite = c.fin_validite()
							c.save()
		else:
			log_auto(user=User.objects.get(username="script"), obj=article, flag="a", info="import_status_collection")
			article.description = d["article.description"]
			article.commentaire = d["article.commentaire"]
			article.duree_validite = settings_default.DUREE_VALIDITE_COL
			article.collection = True
			article.save()
		#count += 1
		#if count > 50:
			#break

def import_duree_validite(emplacement, nom, extension, fin_de_ligne="\n"):
	"""
	importation status collection pour les articles
	Entête de colonne
	article_type.code
	article.code
	article.description
	article.duree_validite
	"""
	import time
	user = User.objects.get(username="script")
	count = 0
	data = csv_dic(emplacement+nom+extension, fin_de_ligne="\n", encoding="utf-8", separateur=";")
	for d in data:
		try:
			article_type = add_nomenclature_type(d["article_type.code"], "")
		except NomenclatureTypeExistant as i:
			article_type = i.args[0]
		try:
			article = article_type.add_nomenclature(d["article.code"], update=False, insert=True)
		except NomenclatureExistant as i:
			article = i.args[0]
			print "Article existe : ", article
			log_auto(user=user, obj=article, flag="c", info="import_duree_validite")
			article.set_validite(int(d["article.duree_validite"]), user)
		else:
			print "Articje n'existe pas : ", article
			log_auto(user=User.objects.get(username="script"), obj=article, flag="a", info="import_duree_validite")
			article.description = d["article.description"]
			article.duree_validite = int(d["article.duree_validite"])
			article.save()
		#count += 1
		#if count > 10:
		#	break

def import_article(emplacement, nom, extension, fin_de_ligne="\n"):
	"""
	importation status collection pour les articles
	Entête de colonne
	article_type.code
	article.code
	article.description
	"""
	import time
	user = User.objects.get(username="script")
	count = 0
	data = csv_dic(emplacement+nom+extension, fin_de_ligne="\n", encoding="utf-8", separateur=";")
	for d in data:
		try:
			article_type = add_nomenclature_type(d["article_type.code"], "")
		except NomenclatureTypeExistant as i:
			article_type = i.args[0]
		try:
			article = article_type.add_nomenclature(d["article.code"], update=False, insert=True)
		except NomenclatureExistant as i:
			article = i.args[0]
			print "Article existe : ", article
			log_auto(user=user, obj=article, flag="c", info="import_article")
			article.description = d["article.description"]
			article.save()
		else:
			print "Articje n'existe pas : ", article
			log_auto(user=User.objects.get(username="script"), obj=article, flag="a", info="import_article")
			article.description = d["article.description"]
			article.save()
		#count += 1
		#if count > 10:
		#	break



def add_momenclature_ingredient_contexa(self, emplacement, nom, extension, fin_de_ligne="\n"):
	"""
	Creation/ mise a jour d'une nomentclature en suivant un fichier d'export roxane
	"""
	f = codecs.open(emplacement+nom+extension, "r", encoding="utf-8")
	fichier_formule = f.read().split(fin_de_ligne)
	f.close()

	entete = fichier_formule.pop(0).split("\t")
	colonne = {}
	num = 0
	for c in entete:
		colonne.update({c.replace("\"", ""):num})
		num += 1

	num = 1
	for ligne in fichier_formule:
		if len(ligne) == 0:
			continue
		l = ligne.split("\t")
		print_ascii("%d %s" %(num, l[colonne["codeingredient"]].replace("\"", "")))
		num += 1
		if l[colonne["codeingredient"]].replace("\"", "").startswith("---"):
			continue
		ing = self.add_nomenclature(code=l[colonne["codeingredient"]].replace("\"", ""), description=l[colonne["nomingredient"]].replace("\"", ""), commentaire="")
		if l[colonne["numlot"]].replace("\"", "") == "":
			continue
		try:
			lot = ing.add_lot(code=l[colonne["numlot"]].replace("\"", ""), responsable_creation=User.objects.get(username="script"), description="", commentaire="")
		except NomenclatureLotExistant as i:
			lot = i.args[0]
		if l[colonne["codecontainer"]].replace("\"", "") == "":
			continue
		type_contenant = models_contenant.ContenantType.objects.get(code="??")
		stock_site = models_stock.StockSite.objects.get(code="??")
		stock_entrepot = models_stock.StockEntrepot.objects.get(code="??")
		stock_magasin = models_stock.StockMagasin.objects.get(code="??")
		cont = lot.add_contenant(responsable_creation=User.objects.get(username="script"), type_contenant=type_contenant, stock_site=stock_site, stock_entrepot=stock_entrepot, stock_magasin=stock_magasin, code=l[colonne["codecontainer"]].replace("\"", ""), date_creation=datetime.date.today())

def add_momenclature_roxane_import(self, emplacement, nom, extension):
	"""
	Creation d'une nomentclature en suivant un fichier d'import roxane
	"""


