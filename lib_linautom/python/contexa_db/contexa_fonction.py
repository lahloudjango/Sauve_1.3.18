#-*- coding: utf-8 -*-
"""
Module de manipulation des base de donnée contexa
"""
from __future__ import unicode_literals

import time

__author__ = "Charly GONTERO"
__date__ = "2016-01-20 14:44:57"
__version__ = 1.1
__credits__ = """
 *  contexa_fonction.py
 *
 *  Copyright 2011 Charly GONTERO
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 *  MA 02110-1301, USA.
"""

VERSION = __version__
def version():
	return __version__

def compo_test(mysql, list_seringues, model, mysql_default_db, max_ingredient_formule, max_poids_formule, auto_print_cb = False, nom_formule = "TEST"):
	"""Création de formule de test suivant un model est ume liste d'ingrédienbt
	list_seringues = [
					{"robot" : 1, "tete" : 1, "module" : 1, "seringue" : 2},
					{"robot" : 1, "tete" : 1, "module" : 1, "seringue" : 3},
					]
	model = [
			{"mode_dosage" : 1, "poids" : 5000},
			{"mode_dosage" : 1, "poids" : 100},
			{"mode_dosage" : 1, "poids" : 60},
			{"mode_dosage" : 1, "poids" : 1000},
			{"mode_dosage" : 1, "poids" : 80},
			{"mode_dosage" : 1, "poids" : 200},
			{"mode_dosage" : 1, "poids" : 15000},
			{"mode_dosage" : 1, "poids" : 100},
			]
	auto_print_cb = 1  : impression auto des eiquettes des formules créer

	max_ingredient_formule
		1 : cré des formules de type calibration avec une seul seringue par formule
		> 1 : donnes le nombre max d'ingredient dans la formule
	max_poids_formule : limite le nombre d'ingrédients dans une formule au poids max autorisé

	"""

	string_date_du_jour = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())







	num_formule = 0
	nbr_ingredient_formule = max_ingredient_formule
	poidstotal = max_poids_formule
	id_formule = 0
	g = 0
	#-------------------------------------------------
	for seringue in list_seringues:
	#------------------------------------------------- Recherche de l'IDingredient
		IDseringue = ((seringue["module"]-1)*250)+seringue["seringue"]
		print "IDseringue", IDseringue
		sql_querry = "SELECT IDingredient FROM `%s`.`co%s_paramseringue` " %(mysql_default_db, seringue["robot"])
		sql_querry = sql_querry + "WHERE `IDseringue`= %s" %(IDseringue)
		IDingredient = mysql.execute(sql_querry)
		print "IDingredient", IDingredient
		if IDingredient[0]["IDingredient"] == 0:
			continue
		if nbr_ingredient_formule >= max_ingredient_formule or poidstotal >= max_poids_formule:
			g = 0
			poidstotal = 0
			num_formule = num_formule + 1
			nbr_ingredient_formule = 0

			print nbr_ingredient_formule, max_ingredient_formule
			if max_ingredient_formule == 1:


				sql_querry = "SELECT codeingredient, nomingredient, emplacement FROM %s.ingredients " %(mysql_default_db)
				sql_querry = sql_querry + "WHERE `IDingredient`= %s" %(IDingredient[0]["IDingredient"])
				detail_ingredient = mysql.execute(sql_querry)
				print "detail_ingredient", detail_ingredient

				sql_querry = "INSERT INTO `%s`.`formules` SET" %(mysql_default_db)

				nomformule = "%s" %(detail_ingredient[0]["nomingredient"])
				if len(nomformule) >= 100:
					nomformule = nomformule[:99]
				sql_querry = sql_querry + " `nomformule`= \"%s\"" %(nomformule)

				detailformule = "CAL R%s T%s M%s S%s" %(seringue["robot"],seringue["tete"], seringue["module"],seringue["seringue"])
				if len(detailformule) >= 30:
					detailformule = detailformule[:29]
				sql_querry = sql_querry + ",`detailformule`= \"%s\"" %(detailformule)

				detailformule2 = "Code : %s - Empl :  %s" %(detail_ingredient[0]["codeingredient"], detail_ingredient[0]["emplacement"])
				if len(detailformule2) >= 30:
					detailformule2 = detailformule2[:29]
				sql_querry = sql_querry + ",`detailformule2`= \"%s\"" %(detailformule2)

				detailformule3 = "%s" %(detail_ingredient[0]["nomingredient"])
				if len(detailformule3) >= 30:
					detailformule3 = detailformule3[:29]
				sql_querry = sql_querry + ",`detailformule3`= \"%s\"" %(detailformule3)

				codeformule = "CAL%s" %(detail_ingredient[0]["codeingredient"])
				if len(codeformule) >= 30:
					codeformule = codeformule[0:29]
				sql_querry = sql_querry + ",`codeformule`= \"%s\"" %(codeformule)





				sql_querry = sql_querry + ",`nomresponsable`= \"Calibreur\""
				sql_querry = sql_querry + ",`heurecreation`= \"%s\"" %(string_date_du_jour)
				sql_querry = sql_querry + ",`modecreation`= 2"
				sql_querry = sql_querry + ",`statusformule`= 1"
	#			sql_querry = sql_querry + ",`IDrecipient`= 1"
				sql_querry = sql_querry + ",`typecompo`= 1"
			else:
				sql_querry = "INSERT INTO `%s`.`formules` SET" %(mysql_default_db)
				nomformule = "Test n %s" %(num_formule)
				if len(nomformule) > 100:
					nomformule = nomformule[0:99]
				sql_querry = sql_querry + " `nomformule`= \"%s\"" %(nomformule)

				detailformule = "%s" %(nom_formule)
				if len(detailformule) > 30:
					detailformule = detailformule[0:29]
				sql_querry = sql_querry + ",`detailformule`= \"%s\"" %(detailformule)

				codeformule = "%s%s" %(nom_formule.upper()[:20],num_formule)
				if len(codeformule) > 30:
					codeformule = codeformule[0:29]
				sql_querry = sql_querry + ",`codeformule`= \"%s\"" %(codeformule)

				sql_querry = sql_querry + ",`nomresponsable`= \"Testeur\""
				sql_querry = sql_querry + ",`heurecreation`= \"%s\"" %(string_date_du_jour)
				sql_querry = sql_querry + ",`modecreation`= 2"
				sql_querry = sql_querry + ",`statusformule`= 1"
	#			sql_querry = sql_querry + ",`IDrecipient`= 1"
				sql_querry = sql_querry + ",`typecompo`= 1"
			print "sql_querry", sql_querry
			mysql.execute(sql_querry)

	#------------------------------------------------- Recuperation de l'id_formule
			sql_querry = "SELECT LAST_INSERT_ID()"
			id_formule = mysql.execute(sql_querry)
			print "id_formule", id_formule

			#------------------------------------------------- Impression code barres
			if auto_print_cb != False:
				sql_querry = "INSERT INTO `%s`.`sf_printspooler` SET" %(mysql_default_db)
				sql_querry = sql_querry + " `id_formule`='%s'" %(id_formule[0]["LAST_INSERT_ID()"])
				sql_querry = sql_querry + ",`dateprod`='%s'" %(string_date_du_jour)
				sql_querry = sql_querry + ",`type`=1"
				sql_querry = sql_querry + ",`source`='%s'" %(seringue["robot"])
				mysql.execute(sql_querry)



	#------------------------------------------------- Creation des dosages
		for dosage in model:
			nbr_ingredient_formule = nbr_ingredient_formule + 1
			poidstotal = poidstotal + dosage["poids"]
			sql_querry = "INSERT INTO `%s`.`ingredientsformule` SET" %(mysql_default_db)
			sql_querry = sql_querry + " `id_formule`='%s'" %(id_formule[0]["LAST_INSERT_ID()"])
			sql_querry = sql_querry + ",`IDingredient`='%s'" %(IDingredient[0]["IDingredient"])
			sql_querry = sql_querry + ",`poids`='%s'" %(dosage["poids"])
			sql_querry = sql_querry + ",`modedosage`='%s'" %(dosage["mode_dosage"])
			sql_querry = sql_querry + ",`tete`=%s" %(seringue["tete"])
			sql_querry = sql_querry + ",`module`='%s'" %(seringue["module"])
			sql_querry = sql_querry + ",`seringue`='%s'" %(seringue["seringue"])
			sql_querry = sql_querry + ",`modechoisi`='%s'" %(dosage["mode_dosage"])
			sql_querry = sql_querry + ",`groupe`='%s'" %(g)
			sql_querry = sql_querry + ",`parts`='%s'" %(dosage["poids"])
			sql_querry = sql_querry + ",`RobotNumber`='%s'" %(seringue["robot"])
			sql_querry = sql_querry + ",`numerolot`=''"
			sql_querry = sql_querry + ",`emplacement`=''"
			mysql.execute(sql_querry)

			g = g + 1














class OrdreContexor(object):
	"""
	Definition des ordre contexor
	"""

	def __init__(self):
		pass

	def point_haut(self):
		ordre = []
		ordre.append(1)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def set_vitesse(self):
		ordre = []
		ordre.append(2)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def move_table(self, position = 10000):
		ordre = []
		ordre.append(3)
		ordre.append(position)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def speed_pos(self):
		ordre = []
		ordre.append(4)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def speed_neg(self):
		ordre = []
		ordre.append(5)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def speed_stop(self):
		ordre = []
		ordre.append(6)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def pompage(self, nbr=1, pause=1000):
		ordre = []
		ordre.append(7)
		ordre.append(nbr)
		ordre.append(pause)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def ferme_vannes(self):
		ordre = []
		ordre.append(8)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def ferme_une_vanne(self, vanne):
		ordre = []
		ordre.append(9)
		ordre.append(vanne)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def ouvre_une_vanne(self, vanne):
		ordre = []
		ordre.append(10)
		ordre.append(vanne)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def ouvre_une_tete(self, vanne):
		ordre = []
		ordre.append(11)
		ordre.append(vanne)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def ferme_une_tete(self, vanne):
		ordre = []
		ordre.append(12)
		ordre.append(vanne)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def ouvre_plus_vannes(self, premiere, nbr):
		ordre = []
		ordre.append(13)
		ordre.append(premiere)
		ordre.append(nbr)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def freme_plus_vannes(self, premiere, nbr):
		ordre = []
		ordre.append(14)
		ordre.append(premiere)
		ordre.append(nbr)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def ferme_plus_tete(self):
		ordre = []
		ordre.append(15)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def ouvre_plus_tete(self):
		ordre = []
		ordre.append(16)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def purge(self, nbr=1):
		ordre = []
		ordre.append(17)
		ordre.append(nbr)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def compteur1(self, nbr=1, point=1):
		ordre = []
		ordre.append(18)
		ordre.append(nbr)
		ordre.append(point)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def compteur2(self, nbr=1, point=1):
		ordre = []
		ordre.append(19)
		ordre.append(nbr)
		ordre.append(point)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def compteur3(self, nbr=1, point=1):
		ordre = []
		ordre.append(20)
		ordre.append(nbr)
		ordre.append(point)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def tempo1(self, temp_ms=1000):
		ordre = []
		ordre.append(21)
		ordre.append(temp_ms)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def tempo2(self, temp_ms=1000):
		ordre = []
		ordre.append(22)
		ordre.append(temp_ms)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		ordre.append(0)
		return ordre

	def insert_group(self, mysql, mysql_db, robot, nom_group, responsable="Le purgeur", date=None, add_proup_number=True):
		mysql_shema_commande = "co%s_commande" %(robot)
		if date == None:
			datecreation = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		else:
			datecreation = time.strftime("%Y-%m-%d %H:%M:%S", date)

		querry = "INSERT INTO `%s`.`%s` SET `nomcommande` = \"%s\", `nomresponsable` = \"%s\", `datecreation` = \"%s\"" %(mysql_default_db, mysql_shema_commande, nom_group, responsable, datecreation)
		mysql.execute(querry)
		querry = "SELECT LAST_INSERT_ID()"
		idcommande = mysql.execute(querry)
		if add_proup_number == True:
			nom_group += " ID %s" %(str(idcommande[0]["LAST_INSERT_ID()"]))
			querry = "UPDATE `%s`.`%s` SET `nomcommande` = \"%s\" WHERE IDcommande = %d" %(mysql_default_db, mysql_shema_commande, nomcommande, idcommande[0]["LAST_INSERT_ID()"])
			mysql.execute(querry)
		return idcommande[0]["LAST_INSERT_ID()"]

	def insert_ordre(self, mysql, mysql_db, robot, id_group, list_param):
		mysql_shema_detail_commande = "co%s_detailcommande" %(robot)
		querry = "INSERT INTO `%s`.`%s` SET `IDcommande` = %d, `commandenum` = %d, `param_1` = %d, `param_2` = %d, `param_3` = %d, `param_4` = %d, `param_5` = %d" %(mysql_default_db, mysql_shema_detail_commande, id_group, list_param[0], list_param[1], list_param[2], list_param[3], list_param[4], list_param[5])
		mysql.execute(querry)

	def insert_ordre_list(self, mysql, mysql_db, robot, id_group, fonction, list_vanne):
		for v in list_vanne:
			incert_ordre(mysql, mysql_db, robot, id_group , fonction(v))




#def ordre_groupe(mysql, mysql_db, robot, nom_group, model, list_vanne):

#	print robot
#	print nom_group
#	print model
#	print list_vanne
#	print len(list_vanne)

#	nomresponsable = "Le purgeur"
#	datecreation = string_date_du_jour
#	querry = "INSERT INTO `%s`.`%s` SET `nomcommande` = \"%s\", `nomresponsable` = \"%s\", `datecreation` = \"%s\"" %(mysql_default_db, mysql_shema_commande, nomcommande, nomresponsable, datecreation)
#	mysql.execute(querry)
#	querry = "SELECT LAST_INSERT_ID()"
#	idcommande = mysql.execute(querry)
#	nomcommande += str(idcommande[0]["LAST_INSERT_ID()"])
#	querry = "UPDATE `%s`.`%s` SET `nomcommande` = \"%s\" WHERE IDcommande = %d" %(mysql_default_db, mysql_shema_commande, nomcommande, idcommande[0]["LAST_INSERT_ID()"])
#	mysql.execute(querry)
#
#
#	com = OrdreContexor.move_table(10000)
#	querry = "INSERT INTO `%s`.`%s` SET `IDcommande` = %d, `commandenum` = %d, `param_1` = %d, `param_2` = %d, `param_3` = %d, `param_4` = %d, `param_5` = %d" %(mysql_default_db, mysql_shema_detail_commande, idcommande[0]["LAST_INSERT_ID()"], com[0], com[1], com[2], com[3], com[4], com[5])
#	mysql.execute(querry)
#	#com = OrdreContexor.point_haut()
#	#querry = "INSERT INTO `%s`.`%s` SET `IDcommande` = %d, `commandenum` = %d, `param_1` = %d, `param_2` = %d, `param_3` = %d, `param_4` = %d, `param_5` = %d" %(mysql_default_db, mysql_shema_detail_commande, idcommande[0]["LAST_INSERT_ID()"], com[0], com[1], com[2], com[3], com[4], com[5])
#	#mysql.execute(querry)
#
#	for v in sorted(list_vanne):
#		com = OrdreContexor.ouvre_une_vanne(v)
#		querry = "INSERT INTO `%s`.`%s` SET `IDcommande` = %d, `commandenum` = %d, `param_1` = %d, `param_2` = %d, `param_3` = %d, `param_4` = %d, `param_5` = %d" %(mysql_default_db, mysql_shema_detail_commande, idcommande[0]["LAST_INSERT_ID()"], com[0], com[1], com[2], com[3], com[4], com[5])
#		mysql.execute(querry)
#
#	com = OrdreContexor.move_table(2500000)
#	querry = "INSERT INTO `%s`.`%s` SET `IDcommande` = %d, `commandenum` = %d, `param_1` = %d, `param_2` = %d, `param_3` = %d, `param_4` = %d, `param_5` = %d" %(mysql_default_db, mysql_shema_detail_commande, idcommande[0]["LAST_INSERT_ID()"], com[0], com[1], com[2], com[3], com[4], com[5])
#	mysql.execute(querry)
#	com = OrdreContexor.point_haut()
#	querry = "INSERT INTO `%s`.`%s` SET `IDcommande` = %d, `commandenum` = %d, `param_1` = %d, `param_2` = %d, `param_3` = %d, `param_4` = %d, `param_5` = %d" %(mysql_default_db, mysql_shema_detail_commande, idcommande[0]["LAST_INSERT_ID()"], com[0], com[1], com[2], com[3], com[4], com[5])
#	mysql.execute(querry)
#
#	for v in sorted(list_vanne):
#		com = OrdreContexor.ferme_une_vanne(v)
#		querry = "INSERT INTO `%s`.`%s` SET `IDcommande` = %d, `commandenum` = %d, `param_1` = %d, `param_2` = %d, `param_3` = %d, `param_4` = %d, `param_5` = %d" %(mysql_default_db, mysql_shema_detail_commande, idcommande[0]["LAST_INSERT_ID()"], com[0], com[1], com[2], com[3], com[4], com[5])
#		mysql.execute(querry)
#
#	#com = OrdreContexor.pompage(nbr=1, pause=5000)
#	#querry = "INSERT INTO `%s`.`%s` SET `IDcommande` = %d, `commandenum` = %d, `param_1` = %d, `param_2` = %d, `param_3` = %d, `param_4` = %d, `param_5` = %d" %(mysql_default_db, mysql_shema_detail_commande, idcommande[0]["LAST_INSERT_ID()"], com[0], com[1], com[2], com[3], com[4], com[5])
#	#mysql.execute(querry)
#
#	com = OrdreContexor.compteur1(nbr = 3, point = 1)
#	querry = "INSERT INTO `%s`.`%s` SET `IDcommande` = %d, `commandenum` = %d, `param_1` = %d, `param_2` = %d, `param_3` = %d, `param_4` = %d, `param_5` = %d" %(mysql_default_db, mysql_shema_detail_commande, idcommande[0]["LAST_INSERT_ID()"], com[0], com[1], com[2], com[3], com[4], com[5])
#	mysql.execute(querry)


