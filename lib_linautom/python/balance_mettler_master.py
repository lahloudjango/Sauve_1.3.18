# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Module reproduisant le fonctionnement d'une balance mettler SICS level 1

Erreur :
=> ES : Syntax erreur
=> ET : transmition erreur
=> EL : Logiciel erreur

I0 Inquiry of all implemented MT-SICS commands
<= IO
=> I0 B x1 "1.Command" : B=une autre ligne suit, x1=SICS level, code de la commande (T, SI, S ... )
=> I0 B x1 "1.Command"
=> I0 A x1 "last Command" : A=dernière ligne
=> I0 I : indisponible

I1 Inquiry of MT-SICS level and MT-SICS versions
<= I1
=> I1 A "x1" "x2" "x3" "x4" "x5" x1=SICS level connu (23=level2+level3 )
=> I1 I : indisponible

I2 Inquiry of balance data
<= I2
=> I2 "Impémentation du protocol SICS par Charly GONTERO
=> I2 I : indisponible

I3 Inquiry of balance SW version and type definition number
<= I3
=> I3 "version number"
=> I3 I : indisponible

I4 Inquiry of serial number
<= I4
=> I4 "serial number"
=> I4 I : indisponible

I5 SW-Identification number
<= I5
=> I5 "ID number"
=> I5 I : indisponible

S Send stable weight value
<= S
=> S S WeightValue Unit  : poids stable
=> S I : indisponible
=> S + : sur charge
=> S - : sous charge

SI Send weight value immediately
<= SI
=> S S WeightValue Unit  : poids stable
=> S D WeightValue Unit  : poids instable
=> S I : indisponible
=> S + : sur charge
=> S - : sous charge

SIR Send weight value immediately and repeat
<= SI
=> S D WeightValue Unit  : poids instable
=> S S WeightValue Unit  : poids stable
=> S I : indisponible
=> S + : sur charge
=> S - : sous charge

Z Zero
<= Z
=> Z A : tare OK
=> Z I : indisponible
=> Z + : sur charge
=> Z - : sous charge

ZI Zero immediately
<= ZI
=> Z S : tare OK sur valeur stable
=> Z D : tare OK sur valeur dinamique
=> Z I : indisponible
=> Z + : sur charge
=> Z - : sous charge

@ Reset/restart
<= @
balance resart => I4 "serial number"

D Balance display
<= D "test"
=> D A
=> D R
=> D I : indisponible
=> D L : non executable

DW Weight display (Display show Weight)
<= DW
=> DW A
=> DW I : indisponible

K Key control
<= K *
=> K L : non executable
SR Send weight value on weight change (Send and Repeat)
<= SR *
=> SR L : non executable

T Tare
<= T
=> T S WeightValue Unit : Tare OK avec la valeur ( display = 0 )
=> T I : indisponible
=> T + : sur charge
=> T - : sous charge

TA Inquiry/setting of tare weight value
<= TA TarePresetValue Unit
=> T S WeightValue Unit : Tare OK avec la valeur ( display = TarePresetValue )
=> T I : indisponible
=> T + : sur charge
=> T - : sous charge

TAC Clear tare value
<= TAC
=> TAC A : Tare = 0 
=> TAC I : indisponible
=> TAC + : sur charge
=> TAC - : sous charge

TI Tare Immediately
<= TI
=> TI S WeightValue Unit : Tare OK avec la valeur ( display = 0 )
=> TI D WeightValue Unit : Tare OK avec la valeur ( display = 0 )
=> TI I : indisponible
=> TI L : non executable
=> TI + : sur charge
=> TI - : sous charge
"""


import serial
import socket
import sys
import signal


__author__ = "Charly GONTERO"
__date__ = "2016-01-20 14:44:57"
__version__ = 1.1
__credits__ = """
 *  mettler_sics_l1_master.py
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
	"""
	Version 1.0
	"""
	return __version__



class TimeExceededError(Exception):
	"""
	Exeption TimeOut ; Pas de réponce balance
	"""

	def __init__(self, *args, **kwargs):
		pass



class Sartorius(object):
	"""	
	Mettler Master SICS
	"""
	UNIT = {
		"mg" : 1,
		"g" : 1000,
		"kg" : 1000000,
		"T" : 1000000000,
		}

	COMMANDE = {
		"I0" : "Inquiry of all implemented MT-SICS commands",
		"I1" : "Inquiry of MT-SICS level and MT-SICS versions",
		"I2" : "Inquiry of balance data",
		"I3" : "Inquiry of balance SW version and type definition number",
		"I4" : "Inquiry of serial number",
		"I5" : "SW-Identification number",
		"S" : "Send stable weight value",
		"SI" : "Send weight value immediately",
		"SIR" : "Send weight value immediately and repeat",
		"Z" : "Zero",
		"ZI" : "Zero immediately",
		"D" : "Balance display",
		"DW" : "Weight display (Display show Weight)",
		"K" : "Key control",
		"SR" : "Send weight value on weight change (Send and Repeat)",
		"T" : "Tare",
		"TA" : "Inquiry/setting of tare weight value",
		"TAC" : "Clear tare value",
		"TI" : "Tare Immediately",
			}

	def reception(self):
		"""
		reception de la commande
		"""
		

	def decodage(self):
		"""
		Decodage de la commande
		"""
		

	def execution_commande(self):
		"""
		Déclanchement des actions
		"""
		

	def codage(self):
		"""
		Formation du message de retour
		"""
		

	def envoie(self):
		"""
		Envoie de la réponce
		"""




