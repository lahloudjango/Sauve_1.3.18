# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Fonction spécifique au base de données CONTEXA
Ces fonction sont faite par rétro-ingégnerie, sans le support de contexa
Assurez-vous que ces fonctions soient compatible avec votre basse de donnée avant de les utilisées
"""

import datetime

__author__ = "Charly GONTERO"
__date__ = "2015-11-15 19:06:43"
__version__ = 1.3
__credits__ = """
 *  contexa.py
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


def mois_courant():
	date = datetime.datetime.now()
	return date.strftime("%y%m")

def list_mois_recherche_hist(nbr_mois_recherche):
	date = datetime.datetime.now()
	dic_date = {"mois" : date.month, "annee" : date.year}

	nbr_mois = nbr_mois_recherche

	list_mois_hist = []
	while nbr_mois >= 0 :
		list_mois_hist.append("%s%02d" %(str(dic_date["annee"])[-2:], dic_date["mois"]))

		dic_date["mois"] -= 1
		if dic_date["mois"] < 1:
			dic_date["annee"] -= 1
			dic_date["mois"] = 12

		nbr_mois -= 1

	return list_mois_hist


dico_ingredient_formule = {
	"id": "IDingredientformule",
	"id_formule": "IDformule",
	"id_ing": "IDingredient",
	"id_produit": "produit",
	"id_mode_dosage_erreur": "modeerreur",
	"id_mode_dosage_prevu": "modechoisi",
	"id_mode_dosage": "modedosage",
	"id_ing_status": "ingrstatus",
	"poids": "poids",
	"tete": "tete",
	"module": "module",
	"seringue": "seringue",
	"ordre_prod": "ordreprod",
	"poids_dose_auto": "poidsdoserauto",
	"lot": "numerolot",
	"responsable": "nomresponsable",
	"date_prod": "heureprod",
	"dosage_groupe": "groupe",
	"robot_erreur": "ErreurRobot",
	"robot_number": "RobotNumber",
}

dico_formule = {
	"id": "IDformule",
	"id_mode_creation": "modecreation",
	"id_status_formule": "statusformule",
	"id_recipient_type": "IDrecipienttype",
	"id_type_compo": "typecompo",
	"id_recipient": "recipientnum",
	"nom": "nomformule",
	"code": "codeformule",
	"commentaire1": "detailformule",
	"commentaire2": "detailformule2",
	"commentaire3": "detailformule3",
	"responsable": "nomresponsable",
	"date_creation": "heurecreation",
	"date_debut_fab": "heuredebutfabrication",
	"date_fin_fab": "heurefinfabrication",
	"check_prod": "checkprod",
	"temp_dosage": "temperature",
	"tare_pm": "tarepm",
	"duree_fab": "dureefabrication",
	"nbr_retour_table": "retourtable",
	"ordre_prod": "ordreprod",
}

list_mode_creation_formule = [
	"[0] Automatique (fichier)",
	"[1] Manuel en Cours",
	"[2] Manuel Terminer",
	"[3] A Doser Manuellement",
	"[4] Automatique Avec Mode de Dosage (fichier)",
	"[?] Mode de création inconnu",
	]

list_status_formule = [
	"[0] Saisie manuelle",
	"[1] Attente de production Auto",
	"[2] En Production Auto",
	"[3] Attente de Production Manuel",
	"[4] Production Manuel Erreur Récipient",
	"[5] 0En Production Manuel",
	"[6] Recherche base commune",
	"[7] Attente fin production split",
	"[8] ",
	"[9] ",
	"[10] Annulée en Saisie Manuel",
	"[11] Annulée Prête à Produire",
	"[12] Annulée en cours de Production Auto",
	"[13] Annulée à Finir en Manuel",
	"[14] Annulée Erreur de Production",
	"[15] Annulée en cours de Production Manuel",
	"[16] Annulée Pour Sur-Dosage",
	"[17] Annulée Pour Sous-Dosage",
	"[18] Composition Interrompue",
	"[19] Production Terminée Sans Erreur",
	"[20] Annulée Erreur Poursuite de Dosage",
	"[21] Historique Substitution Ingrédient",
	"[22] Historique Eclatement Dilution",
	"[23] Production Terminer Avec Erreurs de Dosages",
	"[24] Historique Réajustement de Poids",
	"[25] Production Terminer Avec Discodance de Tare",
	"[26] Annulée Pour Discordance de Poids",
	"[27] Annulée Pour Erreur Pose Couvercle",
	"[28] ",
	"[29] ",
	"[30] ",
	"[??] Status Formule Inconnu",
	]

list_mode_dosage = [
	"[0] Manuel",
	"[1] Unitaire",
	"[2] Simultané",
	"[3] 95%",
	"[4] Continu",
	"[5] Unitaire Rapide",
	"[6] Auto-Calibration",
	"[7] Calibration Manuelle",
	"[?] Mode de dosage inconnu",
	]

list_status_auto_calibration = [
	"[0] Nouvelle Matière Première",
	"[1] Auto-Calibration Initiale",
	"[2] Calibré",
	"[3] A Recalibrér",
	"[4] Calibration Impossible",
	]

list_calibration_event = [
	"[0]",
	"[1] A Recalibrer",
	"[2] Calibré en Auto",
	"[3] Calibré en Manuel",
	"[4] Calibration Acceptée",
	"[5] Calibration Rejetée",
	"[6] Poids Trop Petit",
	"[7] Calibration Impossible",
	]

list_status_mode_dosage_erreur = [
	"[0] Aucune Erreur",
	"[1] Balance Trop Petite",
	"[2] Seringue Non Disponible",
	"[3] La Seringue à Changée d'Ingrédient",
	"[4] Manque de Stock",
	"[5] Poids < dosage Mini",
	"[6] Mode After Error",
	"[7] Mode Dosage Forcé",
	"[8] Poids < Seuil Dosage Petit Poids",
	"[9] Poids < Seuil Unitaire Rapide",
	"[10] Poids < Seuil Manuel",
	"[11] Poids > Seuil 95%",
	"[12] Poids > Seuil Continu",
	"[13] Inc/mg = 0",
	"[14] Température Ambiante",
	"[15] Ingrédiens Sans Serinque",
	"[16] Récipient Trop Petit",
	"[17] Nombre d'ingrédient Trop Grand",
	"[18] Mode Porduit Visqueux",
	"[19] Temps Sans Dosage",
	"[20] Validée Dépassée",
	"[21] ",
	"[22] ",
	"[23] ",
	"[24] ",
	"[25] ",
	]

list_status_erreur_robot = [
	"[0] Erreur Poursuite Dosage",
	"[1] Ingrédient Réajusté",
	"[2] Sous-dosé",
	"[3] Sur-dosé",
	"[4] Discordance de poids",
	"[5] ",
	"[6] ",
	"[7] ",
	]

list_status_erreur_manuel = [
	"[0] Pic Dosage Manuel",
	"[1] Ingrédient Avec Pesées Partielle",
	"[2] Part Base Commune",
	"[3] Part Coeur",
	"[4] Part Sous-formule",
	"[5] DIL/CO/BC/SF produite",
	"[6] ",
	"[7] ",
	]

list_type_compo = [
	"[0] Compo de Prod",
	"[1] Compo Test",
	"[2] Compo Purge",
	"[3] Base Commune",
	"[4] Coeur",
	"[5] Dilution",
	"[6] Sous-formule",
	"[7] Split Sous-formule",
	"[8] ",
	"[9] ",
	]

#list_ihist_produit = [
list_produit = [
	"[0] Non Produit",
	"[1] Produit en Auto",
	"[2] Produit en Auto + Ajustement Manuel",
	"[3] Produit en Manuel",
	"[4] Produit Dans une Compo Test",
	"[5] Produit Dans une Compo Purge",
	"[6] ",
	"[7] ",
	"[8] ",
	"[9] ",
	]

#dico_ihist_ingrstatus = [
dico_ihist_ing_status = [
	"[0] Production OK",
	"[1] Sous-dosé",
	"[2] Sur-dosé",
	"[3] Production Manuel",
	"[4] ",
	"[5] ",
	"[6] ",
	"[7] ",
	"[8] ",
	"[9] ",
	"[100] Pesée Partielle",
	"[101] Ingrédient Substitué",
	"[102] ",
	"[103] ",
	"[104] ",
	"[105] ",
	]

list_code_etiquette = {
	"01" : "[01] Ingrédient Sans Déstockage (code ingrédient)",
	"02" : "[02] Ingrédient Avec Déstockage (N° ingrédient)",
	"10" : "[10] Ingrédient SAP (code contenant taka_sto)",
	"11" : "[11] Ingrédient Dans Table ingrédientlot",
	"12" : "[12] Tuyàux",
	"20" : "[20] Diver",
	"50" : "[50] Base Commune",
	"51" : "[51] Dilution",
	"52" : "[52] Coeur",
	"53" : "[53] Sous-formule",
	"54" : "[54] Formule de Base",
	"55" : "[55] Compo Test",
	"56" : "[56] Compo Purge",
	"57" : "[57] Split Sous-formule",
	"80" : "[80] Login",
	"81" : "[81] Tare",
	"82" : "[82] Code barre spéciaux",
	}

dico_paramseringue_by_name_5_0_colibri = {
	"non_dose_stock_mini": "dosageimpossible_all",
	"param1": "param1",
	"param2": "param2",
	"param3": "param3",
	"inc_mg": "param4",
	"snif": "param5",
	"cor_ouv": "param6",
	"cor_fer": "param7",
	"param8": "param8",
	"param9": "param9",
	"param10": "param10",
	"param11": "param11",
	"param12": "param12",
	"param13": "param13",
	"diam_seringue_colibri": "param14",
	"param15": "param15",
	"param16": "param16",
	"param17": "param17",
	"param18": "param18",
	"param19": "param19",
	"param20": "param20",
	"param21": "param21",
	"param22": "param22",
	"status_calibration": "param23",
	"param24": "param24",
	"param25": "param25",
	"param26": "param26",
	"param27": "param27",
	"param28": "param28",
	"param29": "param29",
	"param30": "param30",
	"param31": "param31",
	"param32": "param32",
	"param33": "param33",
	"param34": "param34",
	"param35": "param35",
	"param36": "param36",
	"param37": "param3",
	"param38": "param38",
	"param39": "param39",
	}

dico_paramseringue_by_name_5_0_cobra = {
	"non_dose_stock_mini": "dosageimpossible_all",
	"diam_seringue_cobra": "param1",
	"inc_mg": "param2",
	"snif": "param3",
	"inc_purge": "param4",
	"volume_ml": "param5",
	"tol_calbibre": "param6",
	"petite_cal": "param7",
	"grande_cal": "param8",
	"cor_ouv": "param9",
	"cor_fer": "param10",
	"seuil_unitaire_control": "param11",
	"param12": "param12",
	"param13": "param13",
	"diam_seringue_colibri": "param14",
	"param15": "param15",
	"param16": "param16",
	"param17": "param17",
	"param18": "param18",
	"param19": "param19",
	"param20": "param20",
	"param21": "param21",
	"param22": "param22",
	"status_calibration": "param23",
	"param24": "param24",
	"param25": "param25",
	"param26": "param26",
	"param27": "param27",
	"param28": "param28",
	"param29": "param29",
	"param30": "param30",
	"param31": "param31",
	"param32": "param32",
	"param33": "param33",
	"param34": "param34",
	"param35": "param35",
	"param36": "param36",
	"param37": "param3",
	"param38": "param38",
	"param39": "param39",
	}






dico_paramseringue_by_col_5_0_colibri = {
	"dosageimpossible_all" : "non_dose_stock_mini",
	"param1": "param1",
	"param2": "param2",
	"param3": "param3",
	"param4": "inc_mg",
	"param5": "snif",
	"param6": "cor_ouv",
	"param7": "cor_fer",
	"param8": "param8",
	"param9": "param9",
	"param10": "param10",
	"param11": "param11",
	"param12": "param12",
	"param13": "param13",
	"param14": "diam_seringue_colibri",
	"param15": "param15",
	"param16": "param16",
	"param17": "param17",
	"param18": "param18",
	"param19": "param19",
	"param20": "param20",
	"param21": "param21",
	"param22": "param22",
	"param23": "status_calibration",
	"param24": "param24",
	"param25": "param25",
	"param26": "param26",
	"param27": "param27",
	"param28": "param28",
	"param29": "param29",
	"param30": "param30",
	"param31": "param31",
	"param32": "param32",
	"param33": "param33",
	"param34": "param34",
	"param35": "param35",
	"param36": "param36",
	"param37": "param3",
	"param38": "param38",
	"param39": "param39",
	}

dico_paramseringue_by_col_5_0_cobra = {
	"dosageimpossible_all" : "non_dose_stock_mini",
	"param1": "diam_seringue_cobra",
	"param2": "inc_mg",
	"param3": "snif",
	"param4": "inc_purge",
	"param5": "volume_ml",
	"param6": "tol_calbibre",
	"param7": "petite_cal",
	"param8": "grande_cal",
	"param9": "correc_ouvr",
	"param10": "correc_ferm",
	"param11": "seuil_unitaire_control",
	"param12": "param12",
	"param13": "param13",
	"param14": "diam",
	"param15": "param15",
	"param16": "param16",
	"param17": "param17",
	"param18": "param18",
	"param19": "param19",
	"param20": "param20",
	"param21": "param21",
	"param22": "param22",
	"param23": "status_calibration",
	"param24": "param24",
	"param25": "param25",
	"param26": "param26",
	"param27": "param27",
	"param28": "param28",
	"param29": "param29",
	"param30": "param30",
	"param31": "param31",
	"param32": "param32",
	"param33": "param33",
	"param34": "param34",
	"param35": "param35",
	"param36": "param36",
	"param37": "param3",
	"param38": "param38",
	"param39": "param39",
	}



