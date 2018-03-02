# -*- coding: utf-8 -*-
"""
Fonction spécifique au base de données CONTEXA
Ces fonction sont faite par rétro-ingégnerie, sans le support de contexa
Assurez-vous que ces fonctions soient compatible avec votre basse de donnée avant de les utilisées
"""
from __future__ import unicode_literals

__author__ = "Charly GONTERO"
__date__ = "2016-01-25 17:51:09"
__version__ = 1.0
__credits__ = """
 *  status_ing.py
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


#dico_ihist_ingrstatus = [
V4_3 = {
	0:		"[0] Production OK",
	1:		"[1] Sous-dosé",
	2:		"[2] Sur-dosé",
	3:		"[3] Production Manuel",
	4:		"[4] ",
	5:		"[5] ",
	6:		"[6] ",
	7:		"[7] ",
	8:		"[8] ",
	9:		"[9] ",
	100:	"[100] Pesée Partielle",
	101:	"[101] Ingrédient Substitué",
	102:	"[102] ",
	103:	"[103] ",
	104:	"[104] ",
	105:	"[105] ",
	}

V5_0 = {
	0:		"[0] Production OK",
	1:		"[1] Sous-dosé",
	2:		"[2] Sur-dosé",
	3:		"[3] Production Manuel",
	4:		"[4] ",
	5:		"[5] ",
	6:		"[6] ",
	7:		"[7] ",
	8:		"[8] ",
	9:		"[9] ",
	100:	"[100] Pesée Partielle",
	101:	"[101] Ingrédient Substitué",
	102:	"[102] ",
	103:	"[103] ",
	104:	"[104] ",
	105:	"[105] ",
	}

V5_13 = {
	0:		"[0] Production OK",
	1:		"[1] Sous-dosé",
	2:		"[2] Sur-dosé",
	3:		"[3] Production Manuel",
	4:		"[4] ",
	5:		"[5] ",
	6:		"[6] ",
	7:		"[7] ",
	8:		"[8] ",
	9:		"[9] ",
	100:	"[100] Pesée Partielle",
	101:	"[101] Ingrédient Substitué",
	102:	"[102] ",
	103:	"[103] ",
	104:	"[104] ",
	105:	"[105] ",
	}

ing_status  = {"4.3" : V4_3, "5.0" : V5_0, "5.0" : V5_13}

def get_ing_status(version, param):
	return ing_status[version][param]

