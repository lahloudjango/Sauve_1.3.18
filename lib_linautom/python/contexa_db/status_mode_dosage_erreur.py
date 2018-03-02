# -*- coding: utf-8 -*-
"""
Fonction spécifique au base de données CONTEXA
Ces fonction sont faite par rétro-ingégnerie, sans le support de contexa
Assurez-vous que ces fonctions soient compatible avec votre basse de donnée avant de les utilisées
"""
from __future__ import unicode_literals

__author__ = "Charly GONTERO"
__date__ = "2016-01-26 21:19:59"
__version__ = 1.0
__credits__ = """
 *  status_mode_dosage_erreur.py
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
	0:	"[0] Aucune Erreur",
	1:	"[1] Balance Trop Petite",
	2:	"[2] Seringue Non Disponible",
	3:	"[3] La Seringue à Changée d'Ingrédient",
	4:	"[4] Manque de Stock",
	5:	"[5] Poids < dosage Mini",
	6:	"[6] Mode After Error",
	7:	"[7] Mode Dosage Forcé",
	8:	"[8] Poids < Seuil Dosage Petit Poids",
	9:	"[9] Poids < Seuil Unitaire Rapide",
	10:	"[10] Poids < Seuil Manuel",
	11:	"[11] Poids > Seuil 95%",
	12:	"[12] Poids > Seuil Continu",
	13:	"[13] Inc/mg = 0",
	14:	"[14] Température Ambiante",
	15:	"[15] Ingrédiens Sans Serinque",
	16:	"[16] Récipient Trop Petit",
	17:	"[17] Nombre d'ingrédient Trop Grand",
	18:	"[18] Mode Porduit Visqueux",
	19:	"[19] Temps Sans Dosage",
	20:	"[20] Validée Dépassée",
	}

V5_0 = {
	0:	"[0] Aucune Erreur",
	1:	"[1] Balance Trop Petite",
	2:	"[2] Seringue Non Disponible",
	3:	"[3] La Seringue à Changée d'Ingrédient",
	4:	"[4] Manque de Stock",
	5:	"[5] Poids < dosage Mini",
	6:	"[6] Mode After Error",
	7:	"[7] Mode Dosage Forcé",
	8:	"[8] Poids < Seuil Dosage Petit Poids",
	9:	"[9] Poids < Seuil Unitaire Rapide",
	10:	"[10] Poids < Seuil Manuel",
	11:	"[11] Poids > Seuil 95%",
	12:	"[12] Poids > Seuil Continu",
	13:	"[13] Inc/mg = 0",
	14:	"[14] Température Ambiante",
	15:	"[15] Ingrédiens Sans Serinque",
	16:	"[16] Récipient Trop Petit",
	17:	"[17] Nombre d'ingrédient Trop Grand",
	18:	"[18] Mode Porduit Visqueux",
	19:	"[19] Temps Sans Dosage",
	20:	"[20] Validée Dépassée",
	}

V5_13 = {
	0:	"[0] Aucune Erreur",
	1:	"[1] Balance Trop Petite",
	2:	"[2] Seringue Non Disponible",
	3:	"[3] La Seringue à Changée d'Ingrédient",
	4:	"[4] Manque de Stock",
	5:	"[5] Poids < dosage Mini",
	6:	"[6] Mode After Error",
	7:	"[7] Mode Dosage Forcé",
	8:	"[8] Poids < Seuil Dosage Petit Poids",
	9:	"[9] Poids < Seuil Unitaire Rapide",
	10:	"[10] Poids < Seuil Manuel",
	11:	"[11] Poids > Seuil 95%",
	12:	"[12] Poids > Seuil Continu",
	13:	"[13] Inc/mg = 0",
	14:	"[14] Température Ambiante",
	15:	"[15] Ingrédiens Sans Serinque",
	16:	"[16] Récipient Trop Petit",
	17:	"[17] Nombre d'ingrédient Trop Grand",
	18:	"[18] Mode Porduit Visqueux",
	19:	"[19] Temps Sans Dosage",
	20:	"[20] Validée Dépassée",
	}

status_mode_dosage_erreur  = {"4.3" : V4_3, "5.0" : V5_0, "5.0" : V5_13}

def get_status_mode_dosage_erreur(version, param):
	return status_mode_dosage_erreur[version][param]


