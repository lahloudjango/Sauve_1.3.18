# -*- coding: utf-8 -*-
"""
Fonction spécifique au base de données CONTEXA
Ces fonction sont faite par rétro-ingégnerie, sans le support de contexa
Assurez-vous que ces fonctions soient compatible avec votre basse de donnée avant de les utilisées
"""
from __future__ import unicode_literals

__author__ = "Charly GONTERO"
__date__ = "2016-01-26 21:19:46"
__version__ = 1.0
__credits__ = """
 *  type_compo.py
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
	0:	"[0] Compo de Prod",
	1:	"[1] Compo Test",
	2:	"[2] Compo Purge",
	3:	"[3] Base Commune",
	4:	"[4] Coeur",
	5:	"[5] Dilution",
	6:	"[6] Sous-formule",
	7:	"[7] Split Sous-formule",
	}

V5_0 = {
	0:	"[0] Compo de Prod",
	1:	"[1] Compo Test",
	2:	"[2] Compo Purge",
	3:	"[3] Base Commune",
	4:	"[4] Coeur",
	5:	"[5] Dilution",
	6:	"[6] Sous-formule",
	7:	"[7] Split Sous-formule",
	}

V5_13 = {
	0:	"[0] Compo de Prod",
	1:	"[1] Compo Test",
	2:	"[2] Compo Purge",
	3:	"[3] Base Commune",
	4:	"[4] Coeur",
	5:	"[5] Dilution",
	6:	"[6] Sous-formule",
	7:	"[7] Split Sous-formule",
	}

type_compo  = {"4.3" : V4_3, "5.0" : V5_0, "5.0" : V5_13}

def get_type_compo(version, param):
	return type_compo[version][param]
