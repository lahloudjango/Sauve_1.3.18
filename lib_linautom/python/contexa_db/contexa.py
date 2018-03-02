# -*- coding: utf-8 -*-
"""
Fonction spécifique au base de données CONTEXA
Ces fonction sont faite par rétro-ingégnerie, sans le support de contexa
Assurez-vous que ces fonctions soient compatible avec votre basse de donnée avant de les utilisées
"""
from __future__ import unicode_literals

import datetime
import re
import types


__author__ = "Charly GONTERO"
__date__ = "2016-10-21 22:17:49"
__version__ = 2.0
__credits__ = """
 *  contexa.py
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


version_db_contexa = {
	"--" : "Inconnu",
	"4.3" : "4.3.xx",
	"5.0" : "5.0.xx",
	"5.13" : "5.13.xx",
	}

def mois_courant():
	"""
	Retourne le N° du mois courant formaté pour le N° de table d'historique
	"""
	date = datetime.datetime.now()
	return date.strftime("%y%m")

def list_mois_recherche_hist_formule(nbr_mois_recherche, mysql_con, db_hist, base_table="fhist"):
	"""
	Retourne la list formaté de mois d'historique accécible suivant base_table
	"""
	if mysql_con != None:
		sql_querry = """
			SELECT SUBSTRING(`TABLE_NAME`,6,10) AS `mois` FROM `information_schema`.`TABLES`
			WHERE `TABLE_SCHEMA` = "%s"
				AND `TABLE_NAME` LIKE "fhist%%"
				AND `TABLE_NAME` NOT LIKE "%%merge%%"
			ORDER BY `TABLE_NAME` DESC
			LIMIT %d
			""" %(db_hist, nbr_mois_recherche+2)
	list_mois_hist = [ h["mois"] for h in mysql_con.execute(sql_querry) ]
	#print list_mois_hist
	return list_mois_hist

def list_table_f_ing_recherche(nbr_mois_recherche, mysql_con, db_prin, db_hist, recherche_db_prin=True):
	"""
	Retourne une liste de dict pour la recherche d'une formule en présentant à la fois la recherche dans la base princicale et dans la base d'historique
	"""
	if recherche_db_prin == True :
		l = [{"db": db_prin, "f": "formules", "ing": "ingredientsformule"},]
	else:
		l = []
	hist_rech = list_mois_recherche_hist_formule(nbr_mois_recherche, mysql_con, db_hist, base_table="fhist")
	for t in hist_rech:
		l.append({"db": db_hist, "f": "fhist%s" %(t), "ing": "ihist%s" %(t)})
	return l

def code_formule_base(code):
	"""
	extraction du code formule de base d'une code formule
	"""
	if code.startswith("CO-"):
		return code_formule_base(code[3:])
	if code.startswith("BC-"):
		return code
	m = re.search("^SF[0-9]+\-", code)
	if type(m) != types.NoneType:
		return code_formule_base(code[len(m.group(0)):])
	m = re.search("^FS[0-9]/[0-9]+\-", code)
	if type(m) != types.NoneType:
		return code_formule_base(code[len(m.group(0)):])
	return code

def list_mois_recherche_hist_entre_date(date_debut, date_fin, mysql_con, db_hist, base_table="fhist"):
	"""
	Retourne la list formaté de mois d'historique accécible suivant table_base
	date_debut < date_fin
	date_debut > 2000
	date_fin > 2000
	"""
	if mysql_con != None:
		sql_querry = """
			SELECT `mois`
			FROM (
				SELECT SUBSTRING(`TABLE_NAME`,6,10) AS `mois` FROM `information_schema`.`TABLES`
				WHERE `TABLE_SCHEMA` = "%s"
					AND `TABLE_NAME` LIKE "%s%%"
					AND `TABLE_NAME` NOT LIKE "%%merge%%"
				ORDER BY `TABLE_NAME`
				) as zz
			WHERE `mois` >= "%s" AND `mois` <= "%s"
			""" %(db_hist, base_table, date_debut.strftime("%y%m"), date_fin.strftime("%y%m"))
	list_mois_hist = [ h["mois"] for h in mysql_con.execute(sql_querry) ]
	#print list_mois_hist
	return list_mois_hist


if __name__ == '__main__':
	date_debut = datetime.datetime.strptime("2015-05-22", "%Y-%m-%d")
	date_fin = datetime.datetime.now()
	mysql_con = None
	db_hist = None
	print list_mois_recherche_hist_entre_date(date_debut, date_fin, mysql_con, db_hist, base_table="fhist")


