# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Class de simulation de communication balance
"""

import sys
import random

__author__ = "Charly GONTERO"
__date__ = "2015-01-03 10:58:37"
__version__ = 1.0
__credits__ = """
 *  balance_simulation.py
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


class Simulation(object):
	"""	
	Simulation
	"""
	UNIT = {

		"mg" : 1,
		"g" : 1000,
		"kg" : 1000000,
		"T" : 1000000000,
		}

	COMMANDE = {
		"print" : "\r\n",
		"tare" : "\r\n",
		"zero" : "\r\n",
		"free_com" : "\r\n",  #ordre libre à définir à la volé"
			}

	def __init__(self, port):
		"""
		Définition des paramètres
		un port commencant par "/dev" est un port local ; tout autre est un port reseau
		"""
		self.erreur = ""
		self.unit_balance = ""
		self.poids = 0.0

	def open(self):
		"""
		Ouverture du port pour la communication
		"""
		pass

	def read(self):
		"""
		Réception du message de la balance
		"""
		pass

	def write(self, commande ):
		"""
		Envoie de commande à la balance
		return renvoie le nombre de byte envoyé
		"""
		pass

	def decodage(self, reponce):
		"""
		Decodage de la chaine de charactaire envoyé par la balance
		le poids est retourné en mg
		"""
		self.unit_balance = "mg"
		self.poids = random.randint(0,1000000)

	def lecture(self,unit="mg"):
		"""
		lecture automatique du poids sur la balance
		"""
		self.decodage("")
		return self.poids/self.UNIT[unit]

	def close(self):
		"""
		fermeture du port de connumication
		"""
		pass


if __name__ == "__main__":
	"""
	Exemple d"utilisation de cette nouvelle classe de gestion des balances Mettler
	"""
#	balance = MettlerSics(port="/dev/ttyUSB0")
	balance = MettlerSics(port="/dev/ttyS0")
	
	balance.open()
	while balance.erreur == "":
		p = balance.lecture(unit="kg")
		print p

	print balance.erreur

	balance.close()


