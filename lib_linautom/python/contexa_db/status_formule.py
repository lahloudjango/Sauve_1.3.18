# -*- coding: utf-8 -*-
"""
Fonction spécifique au base de données CONTEXA
Ces fonction sont faite par rétro-ingégnerie, sans le support de contexa
Assurez-vous que ces fonctions soient compatible avec votre basse de donnée avant de les utilisées
"""
from __future__ import unicode_literals

__author__ = "Charly GONTERO"
__date__ = "2016-01-25 18:11:38"
__version__ = 1.0
__credits__ = """
 *  status_formule.py
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
	0:	"[0] Saisie manuelle",
	1:	"[1] Attente de production Auto",
	2:	"[2] En Production Auto",
	3:	"[3] Attente de Production Manuel",
	4:	"[4] Production Manuel Erreur Récipient",
	5:	"[5] En Production Manuel",
	6:	"[6] Recherche base commune",
	7:	"[7] Attente fin production split",
	8:	"[8] ",
	9:	"[9] ",
	10:	"[10] Annulée en Saisie Manuel",
	11:	"[11] Annulée Prête à Produire",
	12:	"[12] Annulée en cours de Production Auto",
	13:	"[13] Annulée à Finir en Manuel",
	14:	"[14] Annulée Erreur de Production",
	15:	"[15] Annulée en cours de Production Manuel",
	16:	"[16] Annulée Pour Sur-Dosage",
	17:	"[17] Annulée Pour Sous-Dosage",
	18:	"[18] Composition Interrompue",
	19:	"[19] Production Terminée Sans Erreur",
	20:	"[20] Annulée Erreur Poursuite de Dosage",
	21:	"[21] Historique Substitution Ingrédient",
	22:	"[22] Historique Eclatement Dilution",
	23:	"[23] Production Terminer Avec Erreurs de Dosages",
	24:	"[24] Historique Réajustement de Poids",
	25:	"[25] Production Terminer Avec Discodance de Tare",
	26:	"[26] Annulée Pour Discordance de Poids",
	27:	"[27] Annulée Pour Erreur Pose Couvercle",
	}

V5_0 = {
	0:	"[0] Saisie manuelle",
	1:	"[1] Attente de production Auto",
	2:	"[2] En Production Auto",
	3:	"[3] Attente de Production Manuel",
	4:	"[4] Production Manuel Erreur Récipient",
	5:	"[5] En Production Manuel",
	6:	"[6] Recherche base commune",
	7:	"[7] Attente fin production split",
	8:	"[8] ",
	9:	"[9] ",
	10:	"[10] Annulée en Saisie Manuel",
	11:	"[11] Annulée Prête à Produire",
	12:	"[12] Annulée en cours de Production Auto",
	13:	"[13] Annulée à Finir en Manuel",
	14:	"[14] Annulée Erreur de Production",
	15:	"[15] Annulée en cours de Production Manuel",
	16:	"[16] Annulée Pour Sur-Dosage",
	17:	"[17] Annulée Pour Sous-Dosage",
	18:	"[18] Composition Interrompue",
	19:	"[19] Production Terminée Sans Erreur",
	20:	"[20] Annulée Erreur Poursuite de Dosage",
	21:	"[21] Historique Substitution Ingrédient",
	22:	"[22] Historique Eclatement Dilution",
	23:	"[23] Production Terminer Avec Erreurs de Dosages",
	24:	"[24] Historique Réajustement de Poids",
	25:	"[25] Production Terminer Avec Discodance de Tare",
	26:	"[26] Annulée Pour Discordance de Poids",
	27:	"[27] Annulée Pour Erreur Pose Couvercle",
	}

V5_13 = {
	0:	"[0] Saisie manuelle",
	1:	"[1] Attente de production Auto",
	2:	"[2] En Production Auto",
	3:	"[3] Attente de Production Manuel",
	4:	"[4] Production Manuel Erreur Récipient",
	5:	"[5] En Production Manuel",
	6:	"[6] Recherche base commune",
	7:	"[7] Attente fin production split",
	8:	"[8] ",
	9:	"[9] ",
	10:	"[10] Annulée en Saisie Manuel",
	11:	"[11] Annulée Prête à Produire",
	12:	"[12] Annulée en cours de Production Auto",
	13:	"[13] Annulée à Finir en Manuel",
	14:	"[14] Annulée Erreur de Production",
	15:	"[15] Annulée en cours de Production Manuel",
	16:	"[16] Annulée Pour Sur-Dosage",
	17:	"[17] Annulée Pour Sous-Dosage",
	18:	"[18] Composition Interrompue",
	19:	"[19] Production Terminée Sans Erreur",
	20:	"[20] Annulée Erreur Poursuite de Dosage",
	21:	"[21] Historique Substitution Ingrédient",
	22:	"[22] Historique Eclatement Dilution",
	23:	"[23] Production Terminer Avec Erreurs de Dosages",
	24:	"[24] Historique Réajustement de Poids",
	25:	"[25] Production Terminer Avec Discodance de Tare",
	26:	"[26] Annulée Pour Discordance de Poids",
	27:	"[27] Annulée Pour Erreur Pose Couvercle",
	}

status_formule  = {"4.3" : V4_3, "5.0" : V5_0, "5.0" : V5_13}

def get_db_formule(version, param):
	return status_formule[version][param]


