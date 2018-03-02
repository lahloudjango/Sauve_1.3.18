# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
http://linuxcnc.org/docs/html/gcode/gcode_fr.html
"""

__author__ = "Charly GONTERO"
__date__ = "2017-04-09 16:14:05"
__version__ = 1.0
__credits__ = """
 *  o_code.py
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

class O_Code(object):
	def __init__(self):
		o_num = 100
	def o_sub(code, num=None):
		"""
		code : instruction de la fonction
		num : N° O
		"""
		if num == None:
			self.o_num += 1
			num = self.o_num
		return "O%s sub%s%Os endsub%s" %(num, FIN_DE_LIGNE, code, num, FIN_DE_LIGNE)
	def o_call(num):
		"""
		num : N° de routine à appeler
		"""
		return "O%s call%s" %(num, FIN_DE_LIGNE)
	def o_return(num):
		"""
		num : N° O point de retour
		"""
		return "O%s return%s" %(num, FIN_DE_LIGNE)
	def o_while(code, test, num=None):
		"""
		code : instruction de la boucle
		test : test de fin de boucle
		num : N° O
		"""
		if num == None:
			self.o_num += 1
			num = self.o_num
		return "O%s while [%s]%s%s%O%s endwhile%s" %(num, test, FIN_DE_LIGNE, code, num, FIN_DE_LIGNE)
	def o_do(code, test, num=None):
		"""
		code : instruction de la boucle
		test : test de fin de boucle
		num : N° O
		"""
		if num == None:
			self.o_num += 1
			num = self.o_num
		return "O%s do%s%s%O%s while [%s]%s" %(num, FIN_DE_LIGNE, code, num, FIN_DE_LIGNE)
	def o_if(test_code, num=None):
		"""
		test_code : liste de dico [{"test": "", "code": ""},]
		num : N° O
		"""
		if num == None:
			self.o_num += 1
			num = self.o_num
		i = 0
		x = ""
		while i < len(test_code):
			if i = 0:
				x += "O%s if %s%s%s" %(num, test_code[i]["test"], FIN_DE_LIGNE, test_code[i]["code"])
			else:
				if test_code[i]["test"] == None:
					x += "O%s else%s%s" %(num, FIN_DE_LIGNE, test_code[i]["code"])
				else:
					x += "O%s elseif [%s]%s%s" %(num, test_code[i]["test"], FIN_DE_LIGNE, test_code[i]["code"])
		x += "0%s endif%s" %(num, FIN_DE_LIGNE)
	def orepeat(code, test, num=None):
		"""
		code : instruction de la boucle
		test : test de fin de boucle
		num : N° O
		"""
		if num == None:
			self.o_num += 1
			num = self.o_num
		return "O%s repeat [%s]%s%s%O%s endrepeat%s" %(num, test, FIN_DE_LIGNE, code, num, FIN_DE_LIGNE)

def commentaire(test):
	return "(%s)" %(test)

def message(test):
	return "(MSG, %s)" %(test)

def message_debug(test):
	return "(DEBUG, %s)" %(test)

def message_log(test):
	return "(LOG, %s)" %(test)

def message_erreur(test):
	return "(print, %s)" %(test)



;DEBUG, Selection vitesse boite #<vitesse_b>, vitesse moteur [#<vitesse>*#<vitesse_b>]
