# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
http://linuxcnc.org/docs/html/gcode/m-code_fr.html
"""

__author__ = "Charly GONTERO"
__date__ = "2017-04-09 16:14:05"
__version__ = 1.0
__credits__ = """
 *  m_code.py
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
FIN_DE_LIGNE="\n"
VERSION = __version__
def version():
	return __version__

class M_Code(object):
	def M0(self):
		"""Pause"""
		return "M0"
	def M1(self):
		"""Pause optionnel"""
		return "M1"
	def M2(self):
		"""Fin de programme"""
		return "M2"
	def M3(self, S=None):
		"""Marche broche horraire"""
		if S == None:
			return "M3"
		else:
			return "M3 S%s" %(S)
	def M4(self, S=None):
		"""Marche broche anti-horraire"""
		if S == None:
			return "M4"
		else:
			return "M4 S%s" %(S)
	def M5(self):
		"""Arret broche"""
		return "M5"
	def M6(self, T=None):
		"""Changement d'outil
		Utiliser Tx précédament pour selectionner un outil"""
		if T=None:
			return "M6"
		else:
			return "T%s M6" %(T)
	def M7(self):
		"""Arrosage 1"""
		return "M7"
	def M8(self):
		"""Arrosage 2"""
		return "M8"
	def M9(self):
		"""Arret Arrosage"""
		return "M9"
	def M19(self, R, Q, P=0):
		"""Orientation de la broche
			R - Position à atteindre à partir de 0, cette valeur doit être comprise entre 0 et 360 degrés.
			Q - Durée d’attente en secondes pour compléter l’orientation. Si motion.spindle.is_oriented n’est pas devenue vraie dans le temps imparti par Q, une erreur de timeout se produira.
			P - Direction de rotation vers la position cible.
				0 - rotation pour petit mouvement angulaire (défaut)
				1 - rotation toujours en sens horaire (même direction qu’avec M3)
				2 - rotation toujours en sens anti-horaire (même direction qu’avec M4)
		"""
		return "M19 R%s Q%s P%s" %(R, Q, P)
	def M48(self):
		"""Autorise les curseurs de corrections de vitesses de broche et celui de vitesse d’avance travail"""
		return "M48"
	def M49(self0):
		"""Inhibe les deux curseurs"""
		return "M49"
	def M30(self):
		"""Fin de programme, déchargement pièce"""
		return "M30"
	def M50(self, P=0):
		"""Contrôle du correcteur de vitesse travail"""
		return "M50 P%s%s" %(P)
	def M51(self, P=0):
		"""Contrôle du correcteur de vitesse broche"""
		return "M51 P%s%s" %(P)
	def M52(self, P=0):
		"""Contrôle de vitesse adaptative"""
		return "M52 P%s%s" %(P)
	def M53(self, P=0):
		"""Contrôle de vitesse adaptative"""
		return "M53 P%s%s" %(P)
	def M60(self):
		"""Pause changement de pièce"""
		return "M60"
	def M61(self, Q):
		"""Défini le n° de l'outil courrant"""
		return "M61 Q%s" %(Q)
	def M62(self, P):
		"""Active un bit de sortie numérique en synchronisme avec un mouvement"""
		return "M62 P%s" %(P)
	def M63(self, P):
		"""Désactive un bit de sortie numérique en synchronisme avec un mouvement"""
		return "M63 P%s" %(P)
	def M64(self, P):
		"""Active immédiatement un bit de sortie numérique"""
		return "M64 P%s" %(P)
	def M65(self, P):
		"""Désactive immédiatement un bit de sortie numérique"""
		return "M65 P%s" %(P)
	def M70(self):
		"""Enregistrement de l'état modal"""
		return "M70"
	def M71(self):
		"""Invalidation de l'état modal enregistré"""
		return "M71"
	def M72(self):
		"""Restauration de l'état modal"""
		return "M72"
	def M73(self):
		"""Enregistrement et auto-restauration de l'état modal"""
		return "M73"
	def M90(self):
		"""Restauration sélective de l'état modal par le test de paramètres prédéfinis"""
		return "M90"






