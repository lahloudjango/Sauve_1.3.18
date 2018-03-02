# -*- coding: utf-8 -*-
"""
Fonction spécifique au base de données CONTEXA
Ces fonction sont faite par rétro-ingégnerie, sans le support de contexa
Assurez-vous que ces fonctions soient compatible avec votre basse de donnée avant de les utilisées
"""
from __future__ import unicode_literals

__author__ = "Charly GONTERO"
__date__ = "2016-01-25 17:38:58"
__version__ = 1.0
__credits__ = """
 *  code_etiquette.py
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
	"01":	"[01] Ingrédient Sans Déstockage (code ingrédient)",
	"02":	"[02] Ingrédient Avec Déstockage (N° ingrédient)",
	"10":	"[10] Ingrédient SAP (code contenant taka_sto)",
	"11":	"[11] Ingrédient Dans Table ingrédientlot",
	"12":	"[12] Tuyàux",
	"20":	"[20] Diver",
	"50":	"[50] Base Commune",
	"51":	"[51] Dilution",
	"52":	"[52] Coeur",
	"53":	"[53] Sous-formule",
	"54":	"[54] Formule de Base",
	"55":	"[55] Compo Test",
	"56":	"[56] Compo Purge",
	"57":	"[57] Split Sous-formule",
	"80":	"[80] Login",
	"81":	"[81] Tare",
	"82":	"[82] Codes barres spéciaux",
	}

V5_0 = {
	"01":	"[01] Ingrédient Sans Déstockage (code ingrédient)",
	"02":	"[02] Ingrédient Avec Déstockage (N° ingrédient)",
	"10":	"[10] Ingrédient SAP (code contenant taka_sto)",
	"11":	"[11] Ingrédient Dans Table ingrédientlot",
	"12":	"[12] Tuyàux",
	"20":	"[20] Diver",
	"50":	"[50] Base Commune",
	"51":	"[51] Dilution",
	"52":	"[52] Coeur",
	"53":	"[53] Sous-formule",
	"54":	"[54] Formule de Base",
	"55":	"[55] Compo Test",
	"56":	"[56] Compo Purge",
	"57":	"[57] Split Sous-formule",
	"80":	"[80] Login",
	"81":	"[81] Tare",
	"82":	"[82] Codes barres spéciaux",
	}

V5_13 = {
	"01":	"[01] Ingrédient Sans Déstockage (code ingrédient)",
	"02":	"[02] Ingrédient Avec Déstockage (N° ingrédient)",
	"10":	"[10] Ingrédient SAP (code contenant taka_sto)",
	"11":	"[11] Ingrédient Dans Table ingrédientlot",
	"12":	"[12] Tuyàux",
	"20":	"[20] Diver",
	"50":	"[50] Base Commune",
	"51":	"[51] Dilution",
	"52":	"[52] Coeur",
	"53":	"[53] Sous-formule",
	"54":	"[54] Formule de Base",
	"55":	"[55] Compo Test",
	"56":	"[56] Compo Purge",
	"57":	"[57] Split Sous-formule",
	"80":	"[80] Login",
	"81":	"[81] Tare",
	"82":	"[82] Codes barres spéciaux",
	}

code_etiquette  = {"4.3" : V4_3, "5.0" : V5_0, "5.0" : V5_13}

def get_code_etiquette(version, param):
	return code_etiquette[version][param]
