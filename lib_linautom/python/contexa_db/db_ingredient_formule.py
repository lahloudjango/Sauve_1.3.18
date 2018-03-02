# -*- coding: utf-8 -*-
"""
Fonction spécifique au base de données CONTEXA
Ces fonction sont faite par rétro-ingégnerie, sans le support de contexa
Assurez-vous que ces fonctions soient compatible avec votre basse de donnée avant de les utilisées
"""
from __future__ import unicode_literals

__author__ = "Charly GONTERO"
__date__ = "2016-01-25 17:44:12"
__version__ = 1.0
__credits__ = """
 *  db_ingredient_formule.py
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


V4_3 = {
	"id":						"IDingredientformule",
	"id_formule":				"IDformule",
	"id_ing":					"IDingredient",
	"id_produit":				"produit",
	"id_mode_dosage_erreur":	"modeerreur",
	"id_mode_dosage_prevu":		"modechoisi",
	"id_mode_dosage":			"modedosage",
	"id_status_ing":			"ingrstatus",
	"poids":					"poids",
	"tete":						"tete",
	"module":					"module",
	"seringue":					"seringue",
	"ordre_prod":				"ordreprod",
	"poids_dose_auto":			"poidsdoserauto",
	"lot":						"numerolot",
	"responsable":				"nomresponsable",
	"date_prod":				"heureprod",
	"dosage_groupe":			"groupe",
	"robot_erreur":				"ErreurRobot",
	"robot_number":				"RobotNumber",
	}

V5_0 = {
	"id":						"IDingredientformule",
	"id_formule":				"IDformule",
	"id_ing":					"IDingredient",
	"id_produit":				"produit",
	"id_mode_dosage_erreur":	"modeerreur",
	"id_mode_dosage_prevu":		"modechoisi",
	"id_mode_dosage":			"modedosage",
	"id_status_ing":			"ingrstatus",
	"id_formule_base":			"IDformulebase",
	"id_base_ĉommune":			"IDbasecommune",
	"id_coeur":					"IDcoeur",
	"id_sous_formule":			"IDsousformule",
	"id_split_formule":			"IDformuleSF",
	"id_ing_formule_base":		"IDingredientformulebase",
	"id_formule_coeur":			"IDformulecoeur",
	"robot_number":				"RobotNumber",
	"tete":						"tete",
	"module":					"module",
	"seringue":					"seringue",
	"paquet":					"paquet",
	"dosage_groupe":			"groupe",
	"ordre_prod":				"ordreprod",
	"poids":					"poids",
	"poids_man":				"poidsdoserman",
	"poids_auto":				"poidsdoserauto",
	"poids_bc":					"poidsdosermanbc",
	"poids_co":					"poidsdosermanco",
	"poids_sf":					"poidsdosermansf",
	"poids_increase":			"poidsincrease",
	"tol_abs_pos":				"toldosabspos",
	"tol_abs_neg":				"toldosabsneg",
	"paquet_poids_total":		"poidstotalpaquet",
	"paquet_dose":				"poidspaquetdose",
	"paquet_tol_abs_pos":		"toldosabspospaquet",
	"paguet_tol_abs_neg":		"toldosabsnegpaquet",
	"part":						"parts",
	"part_bc":					"partsbc",
	"part_co":					"partsco",
	"part_sf":					"partssf",
	"lot":						"numerolot",
	"date_validite":			"datevalidite",
	"responsable":				"nomresponsable",
	"date_prod":				"heureprod",
	"robot_erreur":				"ErreurRobot",
	"calibration_status":		"calibrationstatus",
	"calibration_event":		"calibrationevent",
	"erreur_man":				"ErreurManuel",
	"emplacement":				"emplacement",
	"nbr_reajust":				"nbreajustement",
	"substitution":				"substitution",
	"code sf":					"codeSF",
	"nom_sf":					"nomSF",
	"nom_sf_2":					"nomSF2",
	"split":					"split",
	"code_container":			"codecontainer",
	"ing_info":					"infoingrforhist",
	"log_info_1":				"loginfo1",
	"log_info_2":				"loginfo2",
	"log_info_3":				"loginfo3",
	"log_info_4":				"loginfo4",
	"temps_dosage":				"dosingtime",
	"temp_dose":				"temperature",
	}

V5_13 = {
	"id":						"IDingredientformule",
	"id_formule":				"IDformule",
	"id_ing":					"IDingredient",
	"id_produit":				"produit",
	"id_mode_dosage_erreur":	"modeerreur",
	"id_mode_dosage_prevu":		"modechoisi",
	"id_mode_dosage":			"modedosage",
	"id_status_ing":			"ingrstatus",
	"id_formule_base":			"IDformulebase",
	"id_base_ĉommune":			"IDbasecommune",
	"id_coeur":					"IDcoeur",
	"id_sous_formule":			"IDsousformule",
	"id_split_formule":			"IDformuleSF",
	"id_ing_formule_base":		"IDingredientformulebase",
	"id_formule_coeur":			"IDformulecoeur",
	"robot_number":				"RobotNumber",
	"tete":						"tete",
	"module":					"module",
	"seringue":					"seringue",
	"paquet":					"paquet",
	"dosage_groupe":			"groupe",
	"ordre_prod":				"ordreprod",
	"poids":					"poids",
	"poids_man":				"poidsdoserman",
	"poids_auto":				"poidsdoserauto",
	"poids_bc":					"poidsdosermanbc",
	"poids_co":					"poidsdosermanco",
	"poids_sf":					"poidsdosermansf",
	"poids_increase":			"poidsincrease",
	"tol_abs_pos":				"toldosabspos",
	"tol_abs_neg":				"toldosabsneg",
	"paquet_poids_total":		"poidstotalpaquet",
	"paquet_dose":				"poidspaquetdose",
	"paquet_tol_abs_pos":		"toldosabspospaquet",
	"paguet_tol_abs_neg":		"toldosabsnegpaquet",
	"part":						"parts",
	"part_bc":					"partsbc",
	"part_co":					"partsco",
	"part_sf":					"partssf",
	"lot":						"numerolot",
	"date_validite":			"datevalidite",
	"responsable":				"nomresponsable",
	"date_prod":				"heureprod",
	"robot_erreur":				"ErreurRobot",
	"calibration_status":		"calibrationstatus",
	"calibration_event":		"calibrationevent",
	"erreur_man":				"ErreurManuel",
	"emplacement":				"emplacement",
	"nbr_reajust":				"nbreajustement",
	"substitution":				"substitution",
	"code sf":					"codeSF",
	"nom_sf":					"nomSF",
	"nom_sf_2":					"nomSF2",
	"split":					"split",
	"code_container":			"codecontainer",
	"ing_info":					"infoingrforhist",
	"log_info_1":				"loginfo1",
	"log_info_2":				"loginfo2",
	"log_info_3":				"loginfo3",
	"log_info_4":				"loginfo4",
	"temps_dosage":				"dosingtime",
	"temp_dose":				"temperature",
	}

db_ingredient_formule = {"4.3" : V4_3, "5.0" : V5_0, "5.0" : V5_13}

def get_db_ingredient_formule(version, param):
	return db_ingredient_formule[version][param]
