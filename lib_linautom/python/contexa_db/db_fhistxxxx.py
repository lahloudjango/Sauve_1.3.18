# -*- coding: utf-8 -*-
"""
Fonction spécifique au base de données CONTEXA
Ces fonction sont faite par rétro-ingégnerie, sans le support de contexa
Assurez-vous que ces fonctions soient compatible avec votre basse de donnée avant de les utilisées
"""
from __future__ import unicode_literals

__author__ = "Charly GONTERO"
__date__ = "2016-01-20 14:44:57"
__version__ = 1.0
__credits__ = """
 *  db_fhistxxxx.py
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
	"id":					"IDfhist",
	"id_formule":			"IDformule",
	"id_mode_creation":		"modecreation",
	"id_status_formule":	"statusformule",
	"id_type_compo":		"typecompo",
	"id_recipient":			"recipientnum",
	"nom":					"nomformule",
	"code":					"codeformule",
	"commentaire1":			"detailformule",
	"commentaire2":			"detailformule2",
	"commentaire3":			"detailformule3",
	"responsable":			"nomresponsable",
	"date_creation":		"heurecreation",
	"date_debut_fab":		"heuredebutfabrication",
	"date_fin_fab":			"heurefinfabrication",
	"duree_fab":			"dureefabrication",
	"temp_dosage":			"temperature",
	"tare_pm":				"tarepm",
	"nbr_retour_table":		"retourtable",
	"substitution":			"substitution",
	"comment_dory":			"commentOP",
	"comment_parf":			"comment",
	}

V5_0 = {
	"id":					"IDfhist",
	"id_formule":			"IDformule",
	"id_mode_creation":		"modecreation",
	"id_status_formule":	"statusformule",
	"id_type_compo":		"typecompo",
	"id_recipient":			"recipientnum",
	"nom":					"nomformule",
	"code":					"codeformule",
	"commentaire1":			"detailformule",
	"commentaire2":			"detailformule2",
	"commentaire3":			"detailformule3",
	"responsable":			"nomresponsable",
	"date_creation":		"heurecreation",
	"date_debut_fab":		"heuredebutfabrication",
	"date_fin_fab":			"heurefinfabrication",
	"duree_fab":			"dureefabrication",
	"temp_dosage":			"temperature",
	"tare_pm":				"tarepm",
	"nbr_retour_table":		"retourtable",
	"substitution":			"substitution",
	"comment_dory":			"commentOP",
	"comment_parf":			"comment",
	}

V5_13 = {
	"id":					"IDfhist",
	"id_formule":			"IDformule",
	"id_mode_creation":		"modecreation",
	"id_status_formule":	"statusformule",
	"id_type_compo":		"typecompo",
	"id_recipient":			"recipientnum",
	"nom":					"nomformule",
	"code":					"codeformule",
	"commentaire1":			"detailformule",
	"commentaire2":			"detailformule2",
	"commentaire3":			"detailformule3",
	"responsable":			"nomresponsable",
	"date_creation":		"heurecreation",
	"date_debut_fab":		"heuredebutfabrication",
	"date_fin_fab":			"heurefinfabrication",
	"duree_fab":			"dureefabrication",
	"temp_dosage":			"temperature",
	"tare_pm":				"tarepm",
	"nbr_retour_table":		"retourtable",
	"substitution":			"substitution",
	"comment_dory":			"commentOP",
	"comment_parf":			"comment",
	}

db_fhistxxxx  = {"4.3" : V4_3, "5.0" : V5_0, "5.0" : V5_13}

def get_db_fhistxxxx(version, param):
	return db_fhistxxxx[version][param]
