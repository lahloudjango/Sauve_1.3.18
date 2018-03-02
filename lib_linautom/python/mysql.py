#-*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Module d'enrobage autour de MySQLdb avec mise en forme des données en dictionaire

"""

import MySQLdb

__author__ = "Charly GONTERO"
__date__ = "2016-08-10 18:44:57"
__version__ = 1.3
__credits__ = """
 *  mysql.py
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


class Mysql(object):
	"""
	Definie les connections vers les serveurs de base de donnees contenant les base de reference et les base à mettre à jour
	"""
	def __init__(self):
		"""
		Rien a faire
		"""
		pass


	def open(self, mysql_host, mysql_port, mysql_user, mysql_password, autocommit=True, charset="utf8", use_unicode=True):
		"""
		Ouvre les connection vers les serveur de base de donnees
		"""
#		print mysql_host
#		print mysql_port
#		print mysql_user
#		print mysql_password

		self.mysql_con = MySQLdb.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_password, db="information_schema" ,use_unicode=use_unicode, charset=charset)
		self.mysql_con_curseur = self.mysql_con.cursor(MySQLdb.cursors.DictCursor)
		if autocommit == True:
			self.mysql_con_curseur.execute("set autocommit=1")


	def execute(self, querry):
		"""
		Execute les requetes SQL:
		"""
#		print querry
		self.mysql_con_curseur.execute(querry)
		resultat = self.mysql_con_curseur.fetchall()
#		print resultat
		return resultat

	def commit(self):
		self.mysql_con_curseur.execute("commit")

	def close(self):
		"""
		Ferme les connection vers les serveur de base de donnees
		"""
		self.mysql_con.close()
