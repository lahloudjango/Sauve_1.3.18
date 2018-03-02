# -*- coding: utf-8 -*-
"""
Fonction spécifique au base de données CONTEXA
Ces fonction sont faite par rétro-ingégnerie, sans le support de contexa
Assurez-vous que ces fonctions soient compatible avec votre basse de donnée avant de les utilisées
"""
from __future__ import unicode_literals

__author__ = "Charly GONTERO"
__date__ = "2016-01-20 14:44:57"
__version__ = 1.4
__credits__ = """
 *  _produit_status.py
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


#list_ihist_produit = [
V4_3 = {
	0:	"[0] Non Produit",
	1:	"[1] Produit en Auto",
	2:	"[2] Produit en Auto + Ajustement Manuel",
	3:	"[3] Produit en Manuel",
	4:	"[4] Produit Dans une Compo Test",
	5:	"[5] Produit Dans une Compo Purge",
	6:	"[6] ",
	7:	"[7] ",
	8:	"[8] ",
	9:	"[9] ",
	}

V5_0 = {
	0:	"[0] Non Produit",
	1:	"[1] Produit en Auto",
	2:	"[2] Produit en Auto + Ajustement Manuel",
	3:	"[3] Produit en Manuel",
	4:	"[4] Produit Dans une Compo Test",
	5:	"[5] Produit Dans une Compo Purge",
	6:	"[6] ",
	7:	"[7] ",
	8:	"[8] ",
	9:	"[9] ",
	}

V5_13 = {
	0:	"[0] Non Produit",
	1:	"[1] Produit en Auto",
	2:	"[2] Produit en Auto + Ajustement Manuel",
	3:	"[3] Produit en Manuel",
	4:	"[4] Produit Dans une Compo Test",
	5:	"[5] Produit Dans une Compo Purge",
	6:	"[6] ",
	7:	"[7] ",
	8:	"[8] ",
	9:	"[9] ",
	}

_produit_status  = {"4.3" : V4_3, "5.0" : V5_0, "5.0" : V5_13}

def get__produit_status(version, param):
	return _produit_status[version][param]
