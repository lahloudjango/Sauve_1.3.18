# -*- coding: utf-8 -*-
"""
Fonction spécifique au base de données CONTEXA
Ces fonction sont faite par rétro-ingégnerie, sans le support de contexa
Assurez-vous que ces fonctions soient compatible avec votre basse de donnée avant de les utilisées
"""
from __future__ import unicode_literals

__author__ = "Charly GONTERO"
__date__ = "2016-01-25 17:51:23"
__version__ = 1.0
__credits__ = """
 *  mode_creation_formule.py
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
	0:	"[0] Automatique (fichier)",
	1:	"[1] Manuel en Cours",
	2:	"[2] Manuel Terminer",
	3:	"[3] A Doser Manuellement",
	4:	"[4] Automatique Avec Mode de Dosage (fichier)",
	}

V5_0 = {
	0:	"[0] Automatique (fichier)",
	1:	"[1] Manuel en Cours",
	2:	"[2] Manuel Terminer",
	3:	"[3] A Doser Manuellement",
	4:	"[4] Automatique Avec Mode de Dosage (fichier)",
	}

V5_13 = {
	0:	"[0] Automatique (fichier)",
	1:	"[1] Manuel en Cours",
	2:	"[2] Manuel Terminer",
	3:	"[3] A Doser Manuellement",
	4:	"[4] Automatique Avec Mode de Dosage (fichier)",
	}

mode_creation_formule  = {"4.3" : V4_3, "5.0" : V5_0, "5.0" : V5_13}

def get_mode_creation_formule(version, param):
	return mode_creation_formule[version][param]


