# -*- coding: utf-8 -*-
"""
Fonction spécifique au base de données CONTEXA
Ces fonction sont faite par rétro-ingégnerie, sans le support de contexa
Assurez-vous que ces fonctions soient compatible avec votre basse de donnée avant de les utilisées
"""
from __future__ import unicode_literals
import contexa
import codecs

__author__ = "Charly GONTERO"
__date__ = "2016-01-22 16:02:27"
__version__ = 1.0
__credits__ = """
 *  requete_statistique_sql.py
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

LIST_FILTRE_BASE = ["demandeur", "assistant", "robot", "global"]

# Fonction de base
def append_uniq(liste, k):
	"""
	
	"""
	if k in liste:
		return
	else:
		liste.append(k)

def querry_union(list_select):
	"""

	"""
	return "\nUNION ALL\n".join(list_select)

def querry_select(list_select, list_from, where=None, list_group_by=None, list_order_by=None):
	"""

	"""
	querry = "SELECT " + ", ".join(list_select)
	querry += "\nFROM " + ", ".join(list_from)
	if where != None:
		querry += "\nWHERE " + where
	if list_group_by != None:
		querry += "\nGROUP BY " + ", ".join(list_group_by)
	if list_order_by != None:
		querry += "\nORDER BY " + ", ".join(list_order_by)

	return querry

def where_and(list_and):
	"""

	"""
	return " ( " + "\n  AND ".join(list_and) + " )"

def where_or(list_and):
	"""

	"""
	return " ( " + "\n  OR ".join(list_and) + " )"

def sub_querry(querry, name):
	"""

	"""
	ident = "  "
	return (" (\n" + ident + querry.replace("\n", "\n"+ident) + "\n) AS " + name)

def filtre_base(filtre_de_base, date_debut, date_fin, info):
	"""
	Donne les critaires de base pour la selection des entrée dans la base de donnée
	"""
	if filtre_de_base == "demandeur":
		filtre = []
		if date_debut == None:
			filtre.append("`heurecreation` >= \"%s 00:00:00\"" %(date_debut.strftime("%Y-%m-%d")))
		if date_fin == None:
			filtre.append("`heurecreation` <= \"%s 23:59:59\"" %(date_fin.strftime("%Y-%m-%d")))
		filtre.append("`statusformule` NOT IN (10, 11)")
		filtre.append("`modecreation` IN (0, 4)")
		return filtre
	elif filtre_de_base == "assistant":
		filtre = []
		if date_debut == None:
			filtre.append("`heureprod` >= \"%s 00:00:00\"" %(date_debut.strftime("%Y-%m-%d")))
		if date_fin == None:
			filtre.append("`heureprod` <= \"%s 23:59:59\"" %(date_fin.strftime("%Y-%m-%d")))
		filtre.append("%(nom_responsable_dosage)s != \"\"" %(info))
		filtre.append("`RobotNumber` != \"0\"")
		filtre.append("`RobotNumber` >= \"100\"")
		filtre.append("`IDformulebase` = 0")
		filtre.append("`IDformulecoeur` = 0")
		filtre.append("`IDbasecommune` = 0")
		filtre.append("`IDcoeur` = 0")
		filtre.append("`IDsousformule` = 0")
		filtre.append("`IDformuleSF` = 0")
		return filtre
	elif filtre_de_base == "robot":
		filtre = []
		if date_debut == None:
			filtre.append("`heureprod` >= \"%s 00:00:00\"" %(date_debut.strftime("%Y-%m-%d")))
		if date_fin == None:
			filtre.append("`heureprod` <= \"%s 23:59:59\"" %(date_fin.strftime("%Y-%m-%d")))
		filtre.append("%(nom_responsable_dosage)s != \"\"" %(info))
		filtre.append("`RobotNumber` != \"0\"")
		filtre.append("`RobotNumber` < \"100\"")
		filtre.append("`IDformulebase` = 0")
		filtre.append("`IDformulecoeur` = 0")
		filtre.append("`IDbasecommune` = 0")
		filtre.append("`IDcoeur` = 0")
		filtre.append("`IDsousformule` = 0")
		filtre.append("`IDformuleSF` = 0")
		return filtre
	elif filtre_de_base == "global":
		filtre = []
		if date_debut == None:
			filtre.append("`heureprod` >= \"%s 00:00:00\"" %(date_debut.strftime("%Y-%m-%d")))
		if date_fin == None:
			filtre.append("`heureprod` <= \"%s 23:59:59\"" %(date_fin.strftime("%Y-%m-%d")))
		filtre.append("%(nom_responsable_dosage)s != \"\"" %(info))
		filtre.append("`RobotNumber` != \"0\"")
		filtre.append("`IDformulebase` = 0")
		filtre.append("`IDformulecoeur` = 0")
		filtre.append("`IDbasecommune` = 0")
		filtre.append("`IDcoeur` = 0")
		filtre.append("`IDsousformule` = 0")
		filtre.append("`IDformuleSF` = 0")
		return filtre
	else:
		raise ValueError("%s n'est pas dans %s" %(filtre_de_base, LIST_FILTRE_BASE))


# Analyse historique
def index_fhist(mysql_con, filtre_de_base, date_debut, date_fin, db_hist):
	"""
	"""
	sql_querry = """ 
		SELECT SUBSTRING(`TABLE_NAME`,6,10) AS `mois` FROM `information_schema`.`TABLES`                                                                                 
		WHERE `TABLE_SCHEMA` = "%(db_hist)s"
			AND `TABLE_NAME` LIKE "%(db_table)s%%"
			AND `TABLE_NAME` NOT LIKE "%%merge%%"
		ORDER BY `TABLE_NAME`
		""" %({"db_hist" : db_hist, "db_table" : "fhist"})
	list_mois_hist = [ h["mois"] for h in mysql_con.execute(sql_querry) ]

	for mois in list_mois_hist:
		#print mois
		sql_querry = """ 
			SELECT COUNT(*) AS nbr_index
			FROM INFORMATION_SCHEMA.STATISTICS
			WHERE TABLE_SCHEMA = "%(db_hist)s" AND TABLE_NAME = "%(db_table)s%(mois)s" AND INDEX_NAME = "%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index";
			""" %({"db_hist" : db_hist, "db_table" : "fhist", "mois" : mois, "table_index" : "idformule"})
		if mysql_con.execute(sql_querry)[0]["nbr_index"] == 0:
			sql_querry = """ 
				ALTER TABLE `%(db_hist)s`.`%(db_table)s%(mois)s` ADD INDEX `%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index` ( `%(table_index)s` ASC );
				""" %({"db_hist" : db_hist, "db_table" : "fhist", "mois" : mois, "table_index" : "idformule"})
			mysql_con.execute(sql_querry)
		sql_querry = """ 
			SELECT COUNT(*) AS nbr_index
			FROM INFORMATION_SCHEMA.STATISTICS
			WHERE TABLE_SCHEMA = "%(db_hist)s" AND TABLE_NAME = "%(db_table)s%(mois)s" AND INDEX_NAME = "%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index";
			""" %({"db_hist" : db_hist, "db_table" : "fhist", "mois" : mois, "table_index" : "codeformule"})
		if mysql_con.execute(sql_querry)[0]["nbr_index"] == 0:
			sql_querry = """ 
				ALTER TABLE `%(db_hist)s`.`%(db_table)s%(mois)s` ADD INDEX `%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index` ( `%(table_index)s` ASC );
				""" %({"db_hist" : db_hist, "db_table" : "fhist", "mois" : mois, "table_index" : "codeformule"})
			mysql_con.execute(sql_querry)
	return None	

def index_ihist(mysql_con, filtre_de_base, date_debut, date_fin, db_hist):
	"""
	"""
	sql_querry = """ 
		SELECT SUBSTRING(`TABLE_NAME`,6,10) AS `mois` FROM `information_schema`.`TABLES`                                                                                 
		WHERE `TABLE_SCHEMA` = "%(db_hist)s"
			AND `TABLE_NAME` LIKE "%(db_table)s%%"
			AND `TABLE_NAME` NOT LIKE "%%merge%%"
		ORDER BY `TABLE_NAME`
		""" %({"db_hist" : db_hist, "db_table" : "ihist"})
	list_mois_hist = [ h["mois"] for h in mysql_con.execute(sql_querry) ]

	for mois in list_mois_hist:
		#print mois
		sql_querry = """ 
			SELECT COUNT(*) AS nbr_index
			FROM INFORMATION_SCHEMA.STATISTICS
			WHERE TABLE_SCHEMA = "%(db_hist)s" AND TABLE_NAME = "%(db_table)s%(mois)s" AND INDEX_NAME = "%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index";
			""" %({"db_hist" : db_hist, "db_table" : "ihist", "mois" : mois, "table_index" : "idformule"})
		if mysql_con.execute(sql_querry)[0]["nbr_index"] == 0:
			sql_querry = """ 
				ALTER TABLE `%(db_hist)s`.`%(db_table)s%(mois)s` ADD INDEX `%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index` ( `%(table_index)s` ASC );
				""" %({"db_hist" : db_hist, "db_table" : "ihist", "mois" : mois, "table_index" : "idformule"})
			mysql_con.execute(sql_querry)

		sql_querry = """ 
			SELECT COUNT(*) AS nbr_index
			FROM INFORMATION_SCHEMA.STATISTICS
			WHERE TABLE_SCHEMA = "%(db_hist)s" AND TABLE_NAME = "%(db_table)s%(mois)s" AND INDEX_NAME = "%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index";
			""" %({"db_hist" : db_hist, "db_table" : "ihist", "mois" : mois, "table_index" : "codeingredient"})
		if mysql_con.execute(sql_querry)[0]["nbr_index"] == 0:
			sql_querry = """ 
				ALTER TABLE `%(db_hist)s`.`%(db_table)s%(mois)s` ADD INDEX `%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index` ( `%(table_index)s` ASC );
				""" %({"db_hist" : db_hist, "db_table" : "ihist", "mois" : mois, "table_index" : "codeingredient"})
			mysql_con.execute(sql_querry)

		sql_querry = """ 
			SELECT COUNT(*) AS nbr_index
			FROM INFORMATION_SCHEMA.STATISTICS
			WHERE TABLE_SCHEMA = "%(db_hist)s" AND TABLE_NAME = "%(db_table)s%(mois)s" AND INDEX_NAME = "%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index";
			""" %({"db_hist" : db_hist, "db_table" : "ihist", "mois" : mois, "table_index" : "idformulebase"})
		if mysql_con.execute(sql_querry)[0]["nbr_index"] == 0:
			sql_querry = """ 
				ALTER TABLE `%(db_hist)s`.`%(db_table)s%(mois)s` ADD INDEX `%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index` ( `%(table_index)s` ASC );
				""" %({"db_hist" : db_hist, "db_table" : "ihist", "mois" : mois, "table_index" : "idformulebase"})
			mysql_con.execute(sql_querry)

		sql_querry = """ 
			SELECT COUNT(*) AS nbr_index
			FROM INFORMATION_SCHEMA.STATISTICS
			WHERE TABLE_SCHEMA = "%(db_hist)s" AND TABLE_NAME = "%(db_table)s%(mois)s" AND INDEX_NAME = "%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index";
			""" %({"db_hist" : db_hist, "db_table" : "ihist", "mois" : mois, "table_index" : "idformulecoeur"})
		if mysql_con.execute(sql_querry)[0]["nbr_index"] == 0:
			sql_querry = """ 
				ALTER TABLE `%(db_hist)s`.`%(db_table)s%(mois)s` ADD INDEX `%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index` ( `%(table_index)s` ASC );
				""" %({"db_hist" : db_hist, "db_table" : "ihist", "mois" : mois, "table_index" : "idformulecoeur"})
			mysql_con.execute(sql_querry)

		sql_querry = """ 
			SELECT COUNT(*) AS nbr_index
			FROM INFORMATION_SCHEMA.STATISTICS
			WHERE TABLE_SCHEMA = "%(db_hist)s" AND TABLE_NAME = "%(db_table)s%(mois)s" AND INDEX_NAME = "%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index";
			""" %({"db_hist" : db_hist, "db_table" : "ihist", "mois" : mois, "table_index" : "idbasecommune"})
		if mysql_con.execute(sql_querry)[0]["nbr_index"] == 0:
			sql_querry = """ 
				ALTER TABLE `%(db_hist)s`.`%(db_table)s%(mois)s` ADD INDEX `%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index` ( `%(table_index)s` ASC );
				""" %({"db_hist" : db_hist, "db_table" : "ihist", "mois" : mois, "table_index" : "idbasecommune"})
			mysql_con.execute(sql_querry)

		sql_querry = """ 
			SELECT COUNT(*) AS nbr_index
			FROM INFORMATION_SCHEMA.STATISTICS
			WHERE TABLE_SCHEMA = "%(db_hist)s" AND TABLE_NAME = "%(db_table)s%(mois)s" AND INDEX_NAME = "%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index";
			""" %({"db_hist" : db_hist, "db_table" : "ihist", "mois" : mois, "table_index" : "idcoeur"})
		if mysql_con.execute(sql_querry)[0]["nbr_index"] == 0:
			sql_querry = """ 
				ALTER TABLE `%(db_hist)s`.`%(db_table)s%(mois)s` ADD INDEX `%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index` ( `%(table_index)s` ASC );
				""" %({"db_hist" : db_hist, "db_table" : "ihist", "mois" : mois, "table_index" : "idcoeur"})
			mysql_con.execute(sql_querry)

		sql_querry = """ 
			SELECT COUNT(*) AS nbr_index
			FROM INFORMATION_SCHEMA.STATISTICS
			WHERE TABLE_SCHEMA = "%(db_hist)s" AND TABLE_NAME = "%(db_table)s%(mois)s" AND INDEX_NAME = "%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index";
			""" %({"db_hist" : db_hist, "db_table" : "ihist", "mois" : mois, "table_index" : "robotnumber"})
		if mysql_con.execute(sql_querry)[0]["nbr_index"] == 0:
			sql_querry = """ 
				ALTER TABLE `%(db_hist)s`.`%(db_table)s%(mois)s` ADD INDEX `%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index` ( `%(table_index)s` ASC );
				""" %({"db_hist" : db_hist, "db_table" : "ihist", "mois" : mois, "table_index" : "robotnumber"})
			mysql_con.execute(sql_querry)

		sql_querry = """ 
			SELECT COUNT(*) AS nbr_index
			FROM INFORMATION_SCHEMA.STATISTICS
			WHERE TABLE_SCHEMA = "%(db_hist)s" AND TABLE_NAME = "%(db_table)s%(mois)s" AND INDEX_NAME = "%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index";
			""" %({"db_hist" : db_hist, "db_table" : "ihist", "mois" : mois, "table_index" : "idsousformule"})
		if mysql_con.execute(sql_querry)[0]["nbr_index"] == 0:
			sql_querry = """ 
				ALTER TABLE `%(db_hist)s`.`%(db_table)s%(mois)s` ADD INDEX `%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index` ( `%(table_index)s` ASC );
				""" %({"db_hist" : db_hist, "db_table" : "ihist", "mois" : mois, "table_index" : "idsousformule"})
			mysql_con.execute(sql_querry)

		sql_querry = """ 
			SELECT COUNT(*) AS nbr_index
			FROM INFORMATION_SCHEMA.STATISTICS
			WHERE TABLE_SCHEMA = "%(db_hist)s" AND TABLE_NAME = "%(db_table)s%(mois)s" AND INDEX_NAME = "%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index";
			""" %({"db_hist" : db_hist, "db_table" : "ihist", "mois" : mois, "table_index" : "idformulesf"})
		if mysql_con.execute(sql_querry)[0]["nbr_index"] == 0:
			sql_querry = """ 
				ALTER TABLE `%(db_hist)s`.`%(db_table)s%(mois)s` ADD INDEX `%(db_hist)s_%(db_table)s%(mois)s_%(table_index)s_index` ( `%(table_index)s` ASC );
				""" %({"db_hist" : db_hist, "db_table" : "ihist", "mois" : mois, "table_index" : "idformulesf"})
			mysql_con.execute(sql_querry)




	return None	

def hist_nombre_de_formule(mysql_con, filtre_de_base, date_debut, date_fin, db_hist):
	"""
	Retourne une requete SQL donnant lo nombre de formule total
	"""
	querry1 = []
	for mois in contexa.list_mois_recherche_hist_entre_date(date_debut, date_fin, mysql_con, db_hist, base_table="fhist"):
		info = {"db_hist":db_hist, "mois":mois, "nom_responsable_dosage":"`ihist%s`.`nomresponsable`" %(mois), "nom_responsable_formule":"`fhist%s`.`nomresponsable`" %(mois)}

		if filtre_de_base in ("demandeur",):
			list_select = ["`fhist%(mois)s`.`IDformule` AS `id_formule`" %(info), "ROUND(SUM(`poids`),0) AS `poids_total`"]
			#list_from = ["`%(db_hist)s`.`fhist%(mois)s`" %(info),]
			list_from = ["`%(db_hist)s`.`fhist%(mois)s` LEFT JOIN `%(db_hist)s`.`ihist%(mois)s` ON `fhist%(mois)s`.`IDformule` = `ihist%(mois)s`.`IDformule`" %(info),]
			where = where_and(filtre_base(filtre_de_base, date_debut, date_fin, info))
			list_group_by = ["`fhist%(mois)s`.`IDformule`" %(info),]
			list_order_by = None
			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)

			list_select = ["COUNT(DISTINCT(`id_formule`)) AS `nbr_formule`", "SUM(`poids_total`) AS `poids_total`"]
			list_from = [sub_querry(querry2,"`zz`"),]
			where = None
			list_group_by = None
			list_order_by = None
			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = ["`nbr_formule`", "`poids_total`", "ROUND(`poids_total`/`nbr_formule`,2) AS `moyenne_poids`"]
			list_from = [sub_querry(querry3,"`yy`"),]
			where = None
			list_group_by = None
			list_order_by = None
			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
		elif filtre_de_base in ("assistant", "robot", "global"):
			list_select = ["`IDformule` AS `id_formule`", "ROUND(SUM(`poids`),0) AS `poids_total`"]
			list_from = ["`%(db_hist)s`.`ihist%(mois)s`" %(info),]
			where = where_and(filtre_base(filtre_de_base, date_debut, date_fin, info))
			list_group_by = ["`IDformule`",]
			list_order_by = None
			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)

			list_select = ["COUNT(DISTINCT(`id_formule`)) AS `nbr_formule`", "SUM(`poids_total`) AS `poids_total`"]
			list_from = [sub_querry(querry2,"`zz`"),]
			where = None
			list_group_by = None
			list_order_by = None
			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = ["`nbr_formule`", "`poids_total`", "ROUND(`poids_total`/`nbr_formule`,2) AS `moyenne_poids`"]
			list_from = [sub_querry(querry3,"`yy`"),]
			where = None
			list_group_by = None
			list_order_by = None
			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
		else:
			raise ValueError("%s n'est pas dans %s" %(filtre_de_base, LIST_FILTRE_BASE))

	return querry4

def hist_nombre_de_formule_jour(mysql_con, filtre_de_base, date_debut, date_fin, db_hist):
	"""
	Retourne une requete SQL donnant lo nombre de formule total
	"""
	querry1 = []
	for mois in contexa.list_mois_recherche_hist_entre_date(date_debut, date_fin, mysql_con, db_hist, base_table="fhist"):
		info = {"db_hist":db_hist, "mois":mois, "nom_responsable_dosage":"`ihist%s`.`nomresponsable`" %(mois), "nom_responsable_formule":"`fhist%s`.`nomresponsable`" %(mois)}

		if filtre_de_base in ("demandeur",):
			list_select = ["DATE(`heurecreation`) AS `jour`", "COUNT(DISTINCT(`fhist%(mois)s`.`IDformule`)) as `nbr_formule`" %(info), "ROUND(SUM(`poids`),0) AS `poids_total`"]
			#list_from = ["`%(db_hist)s`.`fhist%(mois)s`" %(info),]
			list_from = ["`%(db_hist)s`.`fhist%(mois)s` LEFT JOIN `%(db_hist)s`.`ihist%(mois)s` ON `fhist%(mois)s`.`IDformule` = `ihist%(mois)s`.`IDformule`" %(info),]
			where = where_and(filtre_base(filtre_de_base, date_debut, date_fin, info))
			list_group_by = ["`fhist%(mois)s`.`IDformule`" %(info), "`jour`"]
			list_order_by = None
			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)

			list_select = ["`jour`", "SUM(`nbr_formule`) AS `nbr_formule`", "SUM(`poids_total`) AS `poids_total`"]
			list_from = [sub_querry(querry2,"`zz`"),]
			where = None
			list_group_by = ["`jour`",]
			list_order_by = ["`jour`",]
			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = ["jour", "`nbr_formule`", "`poids_total`", "ROUND(`poids_total`/`nbr_formule`,2) AS `moyenne_poids`"]
			list_from = [sub_querry(querry3,"`yy`"),]
			where = None
			list_group_by = None
			list_order_by = None
			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
		elif filtre_de_base in ("assistant", "robot", "global"):
			list_select = ["DATE(`heureprod`) AS `jour`", "COUNT(DISTINCT(`IDformule`)) as `nbr_formule`", "ROUND(SUM(`poids`),0) AS `poids_total`"]
			list_from = ["`%(db_hist)s`.`ihist%(mois)s`" %(info),]
			where = where_and(filtre_base(filtre_de_base, date_debut, date_fin, info))
			list_group_by = ["`IDformule`", "`jour`"]
			list_order_by = None
			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)

			list_select = ["`jour`", "SUM(`nbr_formule`) AS `nbr_formule`", "SUM(`poids_total`) AS `poids_total`"]
			list_from = [sub_querry(querry2,"`zz`"),]
			where = None
			list_group_by = ["`jour`",]
			list_order_by = ["`jour`",]
			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = ["jour", "`nbr_formule`", "`poids_total`", "ROUND(`poids_total`/`nbr_formule`,2) AS `moyenne_poids`"]
			list_from = [sub_querry(querry3,"`yy`"),]
			where = None
			list_group_by = None
			list_order_by = None
			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
		else:
			raise ValueError("%s n'est pas dans %s" %(filtre_de_base, LIST_FILTRE_BASE))

	return querry4

def hist_nombre_de_formule_mois(mysql_con, filtre_de_base, date_debut, date_fin, db_hist):
	"""
	Retourne une requete SQL donnant lo nombre de formule total
	"""
	querry1 = []
	querry4 = None
	for mois in contexa.list_mois_recherche_hist_entre_date(date_debut, date_fin, mysql_con, db_hist, base_table="fhist"):
	#for mois in [a+m for a in ["12", "13", "14", "15", "16", "17"] for m in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] ]:
		info = {"db_hist":db_hist, "mois":mois, "nom_responsable_dosage":"`ihist%s`.`nomresponsable`" %(mois), "nom_responsable_formule":"`fhist%s`.`nomresponsable`" %(mois)}

		if filtre_de_base in ("demandeur",):
			list_select = [
				"\"20%s-%s\" AS `annee-mois`" %(mois[:2],mois[2:]),
				"YEAR(`heurecreation`) AS `annee`",
				"MONTH(`heurecreation`) AS `mois`",
				"COUNT(DISTINCT(`fhist%(mois)s`.`IDformule`)) as `nbr_formule`" %(info),
				"ROUND(SUM(`poids`),0) AS `poids_total`",
				]
			list_from = ["`%(db_hist)s`.`fhist%(mois)s` LEFT JOIN `%(db_hist)s`.`ihist%(mois)s` ON `fhist%(mois)s`.`IDformule` = `ihist%(mois)s`.`IDformule`" %(info),]
			where = where_and(filtre_base(filtre_de_base, date_debut, date_fin, info))
			list_group_by = ["`fhist%(mois)s`.`IDformule`" %(info), "`annee`", "`mois`"]
			list_order_by = None
			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)

			list_select = ["annee-mois", "`annee`", "`mois`", "SUM(`nbr_formule`) AS `nbr_formule`", "SUM(`poids_total`) AS `poids_total`"]
			list_from = [sub_querry(querry2,"`zz`"),]
			where = None
			list_group_by = ["`annee`", "`mois`"]
			list_order_by = ["`annee`", "`mois`"]
			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = ["annee-mois", "`annee`", "`mois`", "`nbr_formule`", "`poids_total`", "ROUND(`poids_total`/`nbr_formule`,2) AS `moyenne_poids`"]
			list_from = [sub_querry(querry3,"`yy`"),]
			where = None
			list_group_by = None
			list_order_by = None
			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
		elif filtre_de_base in ("assistant", "robot", "global"):
			list_select = [
				"\"20%s-%s\" AS `annee-mois`" %(mois[:2],mois[2:]),
				"YEAR(`heureprod`) AS `annee`",
				"MONTH(`heureprod`) AS `mois`",
				"COUNT(DISTINCT(`IDformule`)) as `nbr_formule`",
				"ROUND(SUM(`poids`),0) AS `poids_total`",
				]
			list_from = ["`%(db_hist)s`.`ihist%(mois)s`" %(info),]
			where = where_and(filtre_base(filtre_de_base, date_debut, date_fin, info))
			list_group_by = ["`IDformule`", "`annee`", "`mois`"]
			list_order_by = None
			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)

			list_select = [
				"`annee-mois`",
				"`annee`",
				"`mois`",
				"SUM(`nbr_formule`) AS `nbr_formule`",
				"SUM(`poids_total`) AS `poids_total`",
				]
			list_from = [sub_querry(querry2,"`zz`"),]
			where = None
			list_group_by = ["`annee`", "`mois`"]
			list_order_by = ["`annee`", "`mois`"]
			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = [
				"`annee-mois`",
				"`annee`",
				"`mois`",
				"`nbr_formule`",
				"`poids_total`",
				"ROUND(`poids_total`/`nbr_formule`,2) AS `moyenne_poids`",
				]
			list_from = [sub_querry(querry3,"`yy`"),]
			where = None
			list_group_by = None
			list_order_by = None
			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
		else:
			raise ValueError("%s n'est pas dans %s" %(filtre_de_base, LIST_FILTRE_BASE))

	return querry4

def hist_nombre_de_dosage(mysql_con, filtre_de_base, date_debut, date_fin, db_hist):
	"""
	Retourne une requete SQL donnant le nombre de dosage total
	"""
	querry1 = []
	for mois in contexa.list_mois_recherche_hist_entre_date(date_debut, date_fin, mysql_con, db_hist, base_table="fhist"):
		info = {"db_hist":db_hist, "mois":mois, "nom_responsable_dosage":"`ihist%s`.`nomresponsable`" %(mois), "nom_responsable_formule":"`fhist%s`.`nomresponsable`" %(mois)}

		if filtre_de_base in ("demandeur",):
			list_select = ["COUNT(*) AS `nbr_dosage`", "ROUND(SUM(`poids`),0) AS `poids_total`"]
			list_from = ["`%(db_hist)s`.`fhist%(mois)s` LEFT JOIN `%(db_hist)s`.`ihist%(mois)s` ON `fhist%(mois)s`.`IDformule` = `ihist%(mois)s`.`IDformule`" %(info),]
			where = where_and(filtre_base(filtre_de_base, date_debut, date_fin, info))
			list_group_by = None
			list_order_by = None
			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)

			list_select = ["SUM(`nbr_dosage`) AS `nbr_dosage`", "SUM(`poids_total`) AS `poids_total`"]
			list_from = [sub_querry(querry2,"`zz`"),]
			where = None
			list_group_by = None
			list_order_by = None
			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = ["`nbr_dosage`", "`poids_total`", "ROUND(`poids_total`/`nbr_dosage`,2) AS `moyenne_poids`"]
			list_from = [sub_querry(querry3,"`yy`"),]
			where = None
			list_group_by = None
			list_order_by = None
			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
		elif filtre_de_base in ("assistant", "robot", "global"):
			list_select = ["COUNT(*) AS `nbr_dosage`", "ROUND(SUM(`poids`),0) AS `poids_total`"]
			list_from = ["`%(db_hist)s`.`ihist%(mois)s`" %(info),]
			where = where_and(filtre_base(filtre_de_base, date_debut, date_fin, info))
			list_group_by = None
			list_order_by = None
			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)

			list_select = ["SUM(`nbr_dosage`) AS `nbr_dosage`", "SUM(`poids_total`) AS `poids_total`"]
			list_from = [sub_querry(querry2,"`zz`"),]
			where = None
			list_group_by = None
			list_order_by = None
			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = ["`nbr_dosage`", "`poids_total`", "ROUND(`poids_total`/`nbr_dosage`,2) AS `moyenne_poids`"]
			list_from = [sub_querry(querry3,"`yy`"),]
			where = None
			list_group_by = None
			list_order_by = None
			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
		else:
			raise ValueError("%s n'est pas dans %s" %(filtre_de_base, LIST_FILTRE_BASE))

	return querry3

def hist_nombre_de_dosage_jour(mysql_con, filtre_de_base, date_debut, date_fin, db_hist):
	"""
	Retourne une requete SQL donnant le nombre de dosage total
	"""
	querry1 = []
	for mois in contexa.list_mois_recherche_hist_entre_date(date_debut, date_fin, mysql_con, db_hist, base_table="fhist"):
		info = {"db_hist":db_hist, "mois":mois, "nom_responsable_dosage":"`ihist%s`.`nomresponsable`" %(mois), "nom_responsable_formule":"`fhist%s`.`nomresponsable`" %(mois)}

		if filtre_de_base in ("demandeur"):
			list_select = ["DATE(`heurecreation`) AS `jour`", "COUNT(*) as `nbr_dosage`", "ROUND(SUM(`poids`),0) AS `poids_total`"]
			list_from = ["`%(db_hist)s`.`fhist%(mois)s` LEFT JOIN `%(db_hist)s`.`ihist%(mois)s` ON `fhist%(mois)s`.`IDformule` = `ihist%(mois)s`.`IDformule`" %(info),]
			where = where_and(filtre_base(filtre_de_base, date_debut, date_fin, info))
			list_group_by = ["`jour`"]
			list_order_by = None
			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)

			list_select = ["`jour`", "SUM(`nbr_dosage`) AS `nbr_dosage`", "SUM(`poids_total`) AS `poids_total`"]
			list_from = [sub_querry(querry2,"`zz`"),]
			where = None
			list_group_by = ["jour",]
			list_order_by = ["jour",]
			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = ["`jour`", "`nbr_dosage`", "`poids_total`", "ROUND(`poids_total`/`nbr_dosage`,2) AS `moyenne_poids`"]
			list_from = [sub_querry(querry3,"`yy`"),]
			where = None
			list_group_by = None
			list_order_by = None
			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
		elif filtre_de_base in ("assistant", "robot", "global"):
			list_select = ["DATE(`heureprod`) AS `jour`", "COUNT(*) as `nbr_dosage`", "ROUND(SUM(`poids`),0) AS `poids_total`"]
			list_from = ["`%(db_hist)s`.`ihist%(mois)s`" %(info),]
			where = where_and(filtre_base(filtre_de_base, date_debut, date_fin, info))
			list_group_by = ["`jour`"]
			list_order_by = None
			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)

			list_select = ["`jour`", "SUM(`nbr_dosage`) AS `nbr_dosage`", "SUM(`poids_total`) AS `poids_total`"]
			list_from = [sub_querry(querry2,"`zz`"),]
			where = None
			list_group_by = ["jour",]
			list_order_by = ["jour",]
			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = ["`jour`", "`nbr_dosage`", "`poids_total`", "ROUND(`poids_total`/`nbr_dosage`,2) AS `moyenne_poids`"]
			list_from = [sub_querry(querry3,"`yy`"),]
			where = None
			list_group_by = None
			list_order_by = None
			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
		else:
			raise ValueError("%s n'est pas dans %s" %(filtre_de_base, LIST_FILTRE_BASE))

	return querry3

def hist_nombre_de_dosage_mois(mysql_con, filtre_de_base, date_debut, date_fin, db_hist):
	"""
	Retourne une requete SQL donnant le nombre de dosage total
	"""
	querry1 = []
	for mois in contexa.list_mois_recherche_hist_entre_date(date_debut, date_fin, mysql_con, db_hist, base_table="fhist"):
		info = {"db_hist":db_hist, "mois":mois, "nom_responsable_dosage":"`ihist%s`.`nomresponsable`" %(mois), "nom_responsable_formule":"`fhist%s`.`nomresponsable`" %(mois)}

		if filtre_de_base in ("demandeur",):
			list_select = [
				"\"20%s-%s\" AS `annee-mois`" %(mois[:2],mois[2:]),
				"YEAR(`heurecreation`) AS `annee`",
				"MONTH(`heurecreation`) AS `mois`",
				"COUNT(*) as `nbr_dosage`",
				"ROUND(SUM(`poids`),0) AS `poids_total`",
				]
			list_from = ["`%(db_hist)s`.`fhist%(mois)s` LEFT JOIN `%(db_hist)s`.`ihist%(mois)s` ON `fhist%(mois)s`.`IDformule` = `ihist%(mois)s`.`IDformule`" %(info),]
			where = where_and(filtre_base(filtre_de_base, date_debut, date_fin, info))
			list_group_by = ["`annee`", "`mois`"]
			list_order_by = None
			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)

			list_select = [
				"annee-mois", 
				"`annee`",
				"`mois`",
				"SUM(`nbr_dosage`) AS `nbr_dosage`",
				"SUM(`poids_total`) AS `poids_total`",
				]
			list_from = [sub_querry(querry2,"`zz`"),]
			where = None
			list_group_by = ["`annee`", "`mois`"]
			list_order_by = ["`annee`", "`mois`"]
			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = [
				"annee-mois", 
				"`annee`",
				"`mois`",
				"`nbr_dosage`",
				"`poids_total`",
				"ROUND(`poids_total`/`nbr_dosage`,2) AS `moyenne_poids`",
				]
			list_from = [sub_querry(querry3,"`yy`"),]
			where = None
			list_group_by = None
			list_order_by = None
			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
		elif filtre_de_base in ("assistant", "robot", "global"):
			list_select = [
				"\"20%s-%s\" AS `annee-mois`" %(mois[:2],mois[2:]),
				"YEAR(`heureprod`) AS `annee`",
				"MONTH(`heureprod`) AS `mois`",
				"COUNT(*) as `nbr_dosage`",
				"ROUND(SUM(`poids`),0) AS `poids_total`",
				]
			list_from = ["`%(db_hist)s`.`fhist%(mois)s` LEFT JOIN `%(db_hist)s`.`ihist%(mois)s` ON `fhist%(mois)s`.`IDformule` = `ihist%(mois)s`.`IDformule`" %(info),]
			where = where_and(filtre_base(filtre_de_base, date_debut, date_fin, info))
			list_group_by = ["`annee`", "`mois`"]
			list_order_by = None
			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)

			list_select = [
				"annee-mois", 
				"`annee`",
				"`mois`",
				"SUM(`nbr_dosage`) AS `nbr_dosage`",
				"SUM(`poids_total`) AS `poids_total`",
				]
			list_from = [sub_querry(querry2,"`zz`"),]
			where = None
			list_group_by = ["`annee`", "`mois`"]
			list_order_by = ["`annee`", "`mois`"]
			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = [
				"annee-mois", 
				"`annee`",
				"`mois`",
				"`nbr_dosage`",
				"`poids_total`",
				"ROUND(`poids_total`/`nbr_dosage`,2) AS `moyenne_poids`",
				]
			list_from = [sub_querry(querry3,"`yy`"),]
			where = None
			list_group_by = None
			list_order_by = None
			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
		else:
			raise ValueError("%s n'est pas dans %s" %(filtre_de_base, LIST_FILTRE_BASE))

	return querry4

def hist_nombre_de_dosage_pid(mysql_con, filtre_de_base, date_debut, date_fin, db_hist):
	"""
	Retourne une requete SQL donnant la répartition du nombre de dosage par PID assistant (doseur)
	"""
	querry1 = []
	for mois in contexa.list_mois_recherche_hist_entre_date(date_debut, date_fin, mysql_con, db_hist, base_table="fhist"):
		info = {"db_hist":db_hist, "mois":mois, "nom_responsable_dosage":"`ihist%s`.`nomresponsable`" %(mois), "nom_responsable_formule":"fhist%s`.`nomresponsable" %(mois)}

		if filtre_de_base in ("demandeur", "assistant", "robot", "global"):
			list_select = [
				"UPPER(%(nom_responsable_dosage)s) AS `nom_responsable_dosage`" %(info),
				"`RobotNumber` AS `robot_number`",
				"SUM(`dosingtime`) AS `temps_total`",
				"COUNT(*) AS `nombre_dosage`",
				"ROUND(SUM(`poids`),0) AS `poids_total`",
				]
			list_from = ["`%(db_hist)s`.`fhist%(mois)s` LEFT JOIN `%(db_hist)s`.`ihist%(mois)s` ON `fhist%(mois)s`.`IDformule` = `ihist%(mois)s`.`IDformule`" %(info),]
			where = where_and(filtre_base(filtre_de_base, date_debut, date_fin, info))
			list_group_by = ["`nom_responsable_dosage`", "`robot_number`"]
			list_order_by = None
			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)

			list_select = [
				"`nom_responsable_dosage`",
				"`robot_number`",
				"SUM(`temps_total`) AS `temps_total`",
				"SUM(`nombre_dosage`) AS `nombre_dosage`",
				"SUM(`poids_total`) AS `poids_total`",
				]
			list_from = [sub_querry(querry2,"`zz`"),]
			where = None
			list_group_by = ["`nom_responsable_dosage`", "`robot_number`"]
			list_order_by = None
			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = [
				"`nom_responsable_dosage`",
				"`robot_number`",
				"`temps_total`",
				"`nombre_dosage`",
				"ROUND(`temps_total`/`nombre_dosage`,2) AS `moyenne_temps`",
				"`poids_total`",
				"ROUND(`poids_total`/`nombre_dosage`,0) AS `moyenne_poids`",
				]
			list_from = [sub_querry(querry3,"`yy`"),]
			where = None
			list_group_by = None
			list_order_by = ["`nom_responsable_dosage`", "`robot_number`"]
			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
		else:
			raise ValueError("%s n'est pas dans %s" %(filtre_de_base, LIST_FILTRE_BASE))

	return querry4

def hist_nombre_de_dosage_station(mysql_con, filtre_de_base, date_debut, date_fin, db_hist):
	"""
	Retourne une requete SQL donnant la répartition du nombre de dosage par station de travail (RobotNumber)
	"""
	querry1 = []
	for mois in contexa.list_mois_recherche_hist_entre_date(date_debut, date_fin, mysql_con, db_hist, base_table="fhist"):
		info = {"db_hist":db_hist, "mois":mois, "nom_responsable_dosage":"`ihist%s`.`nomresponsable`" %(mois), "nom_responsable_formule":"`fhist%s`.`nomresponsable`" %(mois)}

		if filtre_de_base in ("demandeur", "assistant", "robot", "global"):
			list_select = ["UPPER(%(nom_responsable_dosage)s) AS `nom_responsable_dosage`" %(info), "`RobotNumber` AS `robot_number`", "SUM(`dosingtime`) AS `temps_total`", "COUNT(*) AS `nombre_dosage`", "ROUND(SUM(`poids`),0) AS `poids_total`"]
			list_from = ["`%(db_hist)s`.`fhist%(mois)s` LEFT JOIN `%(db_hist)s`.`ihist%(mois)s` ON `fhist%(mois)s`.`IDformule` = `ihist%(mois)s`.`IDformule`" %(info),]
			where = where_and(filtre_base(filtre_de_base, date_debut, date_fin, info))
			list_group_by = ["`robot_number`", "`nom_responsable_dosage`"]
			list_order_by = None
			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)

			list_select = ["`robot_number`", "`nom_responsable_dosage`", "SUM(`temps_total`) AS `temps_total`", "SUM(`nombre_dosage`) AS `nombre_dosage`", "SUM(`poids_total`) AS `poids_total`"]
			list_from = [sub_querry(querry2,"`zz`"),]
			where = None
			list_group_by = ["`robot_number`", "`nom_responsable_dosage`"]
			list_order_by = None
			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = ["`nom_responsable_dosage`", "`robot_number`", "`temps_total`", "`nombre_dosage`", "ROUND(`temps_total`/`nombre_dosage`,2) AS `moyenne_temps`", "`poids_total`", "ROUND(`poids_total`/`nombre_dosage`,0) AS `moyenne_temps`"]
			list_from = [sub_querry(querry3,"`yy`"),]
			where = None
			list_group_by = None
			list_order_by = ["`robot_number`", "`nom_responsable_dosage`"]
			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
		else:
			raise ValueError("%s n'est pas dans %s" %(filtre_de_base, LIST_FILTRE_BASE))

	return querry4

def hist_productivite_mois(mysql_con, filtre_de_base, date_debut, date_fin, db_hist):
	querry1 = []
	for mois in contexa.list_mois_recherche_hist_entre_date(date_debut, date_fin, mysql_con, db_hist, base_table="fhist"):
	#for mois in [a+m for a in ["12", "13", "14", "15", "16", "17"] for m in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] ]:
		info = {"db_hist":db_hist, "mois":mois, "nom_responsable_dosage":"`ihist%s`.`nomresponsable`" %(mois), "nom_responsable_formule":"`fhist%s`.`nomresponsable`" %(mois)}

		if filtre_de_base in ("robot"):
			list_select = [
				mois,
				"IF(`RobotNumber` < 99, 1, 0) AS robot",
				"IF(`RobotNumber` > 99, 1, 0) AS manuel",
				]
			list_from = ["`%(db_hist)s`.`fhist%(mois)s` LEFT JOIN `%(db_hist)s`.`ihist%(mois)s` ON `fhist%(mois)s`.`IDformule` = `ihist%(mois)s`.`IDformule`" %(info),]
			where = where_and([
				"IDbasecommune = 0",
				"IDcoeur = 0",
				"IDformulebase = 0",
				"IDformuleSF = 0",
				"IDsousformule = 0",
				"IDformulecoeur = 0",
				])
			list_group_by = None
			list_order_by = None

			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = [
				"\"20%s-%s\" AS `mois`" %(mois[:2],mois[2:]),
				"SUM(robot) AS nbr_robot", "SUM(manuel) AS nbr_manuel"
				]
			list_from = [sub_querry(querry3,"`zz`"),]
			where = None
			list_group_by = None
			list_order_by = None

			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = [
				"`annee-mois`",
				"nbr_robot",
				"nbr_manuel",
				"((nbr_robot+nbr_manuel)/nbr_robot)*100 AS pc_auto"
				]
			list_from = [sub_querry(querry4,"`yy`"),]
			where = None
			list_group_by = None
			list_order_by = None

			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)


		else:
			raise ValueError("%s n'est pas dans %s" %(filtre_de_base, LIST_FILTRE_BASE))

	return querry2

def hist_temps_reponse(mysql_con, filtre_de_base, date_debut, date_fin, db_hist):
	"""
	"""
	querry1 = []
	for mois in contexa.list_mois_recherche_hist_entre_date(date_debut, date_fin, mysql_con, db_hist, base_table="fhist"):
	#for mois in [a+m for a in ["12", "13", "14", "15", "16", "17"] for m in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] ]:
		info = {"db_hist":db_hist, "mois":mois, "nom_responsable_dosage":"`ihist%s`.`nomresponsable`" %(mois), "nom_responsable_formule":"`fhist%s`.`nomresponsable`" %(mois)}

		if filtre_de_base in ("demandeur",):
			list_select = [
				"codeformule",
				"MIN(heurecreation) AS heurecreation",
				"MAX(heuredebutfabrication) AS heuredebutfabrication",
				"MAX(heurefinfabrication) AS heurefinfabrication",
				]
			list_from = ["`%(db_hist)s`.`fhist%(mois)s`" %(info),]
			#where = where_and(filtre_base(filtre_de_base, date_debut, date_fin, info))
			w_or = where_or(["codeformule like \"SF1-%\"", "codeformule like \"SF2-%\"", "codeformule like \"SF3-%\"", "codeformule like \"SF12-%\"", "codeformule like \"SF23-%\"", "codeformule like \"CT%\"", "codeformule like \"CC%\"", "codeformule like \"CP%\"", "codeformule like \"CO-%\"", "codeformule like \"DI-%\"", "codeformule like \"BC-%\""])
			where = "NOT ( %s )" %(w_or)
			list_group_by = ["codeformule",]
			list_order_by = None

			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = [
				"codeformule",
				"heurecreation",
				"heuredebutfabrication",
				"heurefinfabrication",
				"(heuredebutfabrication - heurecreation)/60 AS temps_reaction",
				"(heurefinfabrication - heuredebutfabrication)/60 AS temps_fabrication", 
				"(heurefinfabrication - heurecreation)/60 AS temps_reponse",
				]
			list_from = [sub_querry(querry3,"`zz`"),]
			where = None
			list_group_by = None
			list_order_by = None

			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = [
				"\"20%s-%s\" AS `mois`" %(mois[:2],mois[2:]),
				"ROUND(MIN(temps_reaction),0) AS temps_reaction_min",
				"ROUND(MAX(temps_reaction),0) AS temps_reaction_max",
				"ROUND(AVG(temps_reaction),0) AS temps_reaction_avg",
				"ROUND(STD(temps_reaction),0) AS temps_reaction_std",
				"ROUND(MIN(temps_reponse),0) AS temps_reponse_min",
				"ROUND(MAX(temps_reponse),0) AS temps_reponse_max",
				"ROUND(AVG(temps_reponse),0) AS temps_reponse_avg",
				"ROUND(STD(temps_reponse),0) AS temps_reponse_std",
				"ROUND(MIN(temps_fabrication),0) AS temps_fabrication_min",
				"ROUND(MAX(temps_fabrication),0) AS temps_fabrication_max",
				"ROUND(AVG(temps_fabrication),0) AS temps_fabrication_avg",
				"ROUND(STD(temps_fabrication),0) AS temps_fabrication_std",
				]
			list_from = [sub_querry(querry4,"`yy`"),]
			where = where_and(["temps_reaction < 60*24*5", "temps_reponse < 60*24*5", "temps_fabrication < 60*24*5"])
			list_group_by = None
			list_order_by = None

			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)

		elif filtre_de_base in ("robot",):
			list_select = [
				"codeformule",
				"MIN(heurecreation) AS heurecreation",
				"MAX(heuredebutfabrication) AS heuredebutfabrication",
				"MAX(heurefinfabrication) AS heurefinfabrication",
				]
			list_from = ["`%(db_hist)s`.`fhist%(mois)s`" %(info),]
			where = where_or(["codeformule like \"SF1-%\"", "codeformule like \"SF2-%\"", "codeformule like \"SF3-%\"", "codeformule like \"SF12-%\"", "codeformule like \"SF23-%\""])
			list_group_by = ["codeformule",]
			list_order_by = None

			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = [
				"codeformule",
				"heurecreation",
				"heuredebutfabrication",
				"heurefinfabrication",
				"(heuredebutfabrication - heurecreation)/60 AS temps_reaction",
				"(heurefinfabrication - heuredebutfabrication)/60 AS temps_fabrication", 
				"(heurefinfabrication - heurecreation)/60 AS temps_reponse",
				]
			list_from = [sub_querry(querry3,"`zz`"),]
			where = None
			list_group_by = None
			list_order_by = None

			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = [
				"\"20%s-%s\" AS `mois`" %(mois[:2],mois[2:]),
				"ROUND(MIN(temps_reaction),0) AS temps_reaction_min",
				"ROUND(MAX(temps_reaction),0) AS temps_reaction_max",
				"ROUND(AVG(temps_reaction),0) AS temps_reaction_avg",
				"ROUND(STD(temps_reaction),0) AS temps_reaction_std",
				"ROUND(MIN(temps_reponse),0) AS temps_reponse_min",
				"ROUND(MAX(temps_reponse),0) AS temps_reponse_max",
				"ROUND(AVG(temps_reponse),0) AS temps_reponse_avg",
				"ROUND(STD(temps_reponse),0) AS temps_reponse_std",
				"ROUND(MIN(temps_fabrication),0) AS temps_fabrication_min",
				"ROUND(MAX(temps_fabrication),0) AS temps_fabrication_max",
				"ROUND(AVG(temps_fabrication),0) AS temps_fabrication_avg",
				"ROUND(STD(temps_fabrication),0) AS temps_fabrication_std",
				]
			list_from = [sub_querry(querry4,"`yy`"),]
			where = where_and(["temps_reaction < 60*24*5", "temps_reponse < 60*24*5", "temps_fabrication < 60*24*5"])
			list_group_by = None
			list_order_by = None

			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)


		elif filtre_de_base in ("assistant",):
			list_select = [
				"codeformule",
				"MIN(heurecreation) AS heurecreation",
				"MAX(heuredebutfabrication) AS heuredebutfabrication",
				"MAX(heurefinfabrication) AS heurefinfabrication",
				]
			list_from = ["`%(db_hist)s`.`fhist%(mois)s`" %(info),]
			w_or = where_or(["codeformule like \"SF1-%\"", "codeformule like \"SF2-%\"", "codeformule like \"SF3-%\"", "codeformule like \"SF12-%\"", "codeformule like \"SF23-%\""])
			where = "NOT ( %s )" %(w_or)
			list_group_by = ["codeformule",]
			list_order_by = None

			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = [
				"codeformule",
				"heurecreation",
				"heuredebutfabrication",
				"heurefinfabrication",
				"(heuredebutfabrication - heurecreation)/60 AS temps_reaction",
				"(heurefinfabrication - heuredebutfabrication)/60 AS temps_fabrication", 
				"(heurefinfabrication - heurecreation)/60 AS temps_reponse",
				]
			list_from = [sub_querry(querry3,"`zz`"),]
			where = None
			list_group_by = None
			list_order_by = None

			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = [
				"\"20%s-%s\" AS `mois`" %(mois[:2],mois[2:]),
				"ROUND(MIN(temps_reaction),0) AS temps_reaction_min",
				"ROUND(MAX(temps_reaction),0) AS temps_reaction_max",
				"ROUND(AVG(temps_reaction),0) AS temps_reaction_avg",
				"ROUND(STD(temps_reaction),0) AS temps_reaction_std",
				"ROUND(MIN(temps_reponse),0) AS temps_reponse_min",
				"ROUND(MAX(temps_reponse),0) AS temps_reponse_max",
				"ROUND(AVG(temps_reponse),0) AS temps_reponse_avg",
				"ROUND(STD(temps_reponse),0) AS temps_reponse_std",
				"ROUND(MIN(temps_fabrication),0) AS temps_fabrication_min",
				"ROUND(MAX(temps_fabrication),0) AS temps_fabrication_max",
				"ROUND(AVG(temps_fabrication),0) AS temps_fabrication_avg",
				"ROUND(STD(temps_fabrication),0) AS temps_fabrication_std",
				]
			list_from = [sub_querry(querry4,"`yy`"),]
			where = where_and(["temps_reaction < 60*24*5", "temps_reponse < 60*24*5", "temps_fabrication < 60*24*5"])
			list_group_by = None
			list_order_by = None

			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)

		elif filtre_de_base in ("global",):
			list_select = [
				"codeformule",
				"MIN(heurecreation) AS heurecreation",
				"MAX(heuredebutfabrication) AS heuredebutfabrication",
				"MAX(heurefinfabrication) AS heurefinfabrication",
				]
			list_from = ["`%(db_hist)s`.`fhist%(mois)s`" %(info),]
			where = None
			list_group_by = ["codeformule",]
			list_order_by = None

			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = [
				"codeformule",
				"heurecreation",
				"heuredebutfabrication",
				"heurefinfabrication",
				"(heuredebutfabrication - heurecreation)/60 AS temps_reaction",
				"(heurefinfabrication - heuredebutfabrication)/60 AS temps_fabrication", 
				"(heurefinfabrication - heurecreation)/60 AS temps_reponse",
				]
			list_from = [sub_querry(querry3,"`zz`"),]
			where = None
			list_group_by = None
			list_order_by = None

			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = [
				"\"20%s-%s\" AS `mois`" %(mois[:2],mois[2:]),
				"ROUND(MIN(temps_reaction),0) AS temps_reaction_min",
				"ROUND(MAX(temps_reaction),0) AS temps_reaction_max",
				"ROUND(AVG(temps_reaction),0) AS temps_reaction_avg",
				"ROUND(STD(temps_reaction),0) AS temps_reaction_std",
				"ROUND(MIN(temps_reponse),0) AS temps_reponse_min",
				"ROUND(MAX(temps_reponse),0) AS temps_reponse_max",
				"ROUND(AVG(temps_reponse),0) AS temps_reponse_avg",
				"ROUND(STD(temps_reponse),0) AS temps_reponse_std",
				"ROUND(MIN(temps_fabrication),0) AS temps_fabrication_min",
				"ROUND(MAX(temps_fabrication),0) AS temps_fabrication_max",
				"ROUND(AVG(temps_fabrication),0) AS temps_fabrication_avg",
				"ROUND(STD(temps_fabrication),0) AS temps_fabrication_std",
				]
			list_from = [sub_querry(querry4,"`yy`"),]
			where = where_and(["temps_reaction < 60*24*5", "temps_reponse < 60*24*5", "temps_fabrication < 60*24*5"])
			list_group_by = None
			list_order_by = None

			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)

		else:
			raise ValueError("%s n'est pas dans %s" %(filtre_de_base, LIST_FILTRE_BASE))

	return querry2

def hist_suivie_sfx(mysql_con, filtre_de_base, date_debut, date_fin, db_hist):
	"""
	"""
	querry1 = []
	for mois in contexa.list_mois_recherche_hist_entre_date(date_debut, date_fin, mysql_con, db_hist, base_table="fhist"):
	#for mois in [a+m for a in ["12", "13", "14", "15", "16", "17"] for m in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] ]:
		info = {"db_hist":db_hist, "mois":mois, "nom_responsable_dosage":"`ihist%s`.`nomresponsable`" %(mois), "nom_responsable_formule":"`fhist%s`.`nomresponsable`" %(mois)}

		if filtre_de_base in ("robot",):
			list_select = [
				"base.IDformule AS base_IDformule",
				"base.codeformule AS base_codeformule",
				"base.nomformule AS base_nomformule",
				"base.heuredebutfabrication AS base_heuredebutfabrication",
				"base.heurefinfabrication AS base_heurefinfabrication",
				"base.dureefabrication AS base_dureefabrication",
				"base.statusformule AS base_statusformule",
				"base.heurecreation AS base_heurecreation",
				"base.modecreation AS base_modecreation",
				#"base.typecompo AS base_typecompo",

				#"ing.IDformule AS ing_IDformule",
				"ing.codeingredient AS ing_codeingredient",
				"ing.nomingredient AS ing_nomingredient",
				#"ing.poids AS ing_poids",
				#"ing.tete AS ing_tete",
				#"ing.module AS ing_module",
				#"ing.seringue AS ing_seringue",
				"ing.produit AS ing_produit",
				#"ing.modechoisi AS ing_modechoisi",
				"ing.heureprod AS ing_heureprod",
				"ing.IDformulebase AS ing_IDformulebase",
				"ing.IDformulecoeur AS ing_IDformulecoeur",
				"ing.IDbasecommune AS ing_IDbasecommune",
				"ing.IDcoeur AS ing_IDcoeur",
				"ing.RobotNumber AS ing_RobotNumber",
				"ing.IDsousformule AS ing_IDsousformule",
				"ing.IDformuleSF AS ing_IDformuleSF",
				"ing.dosingtime AS ing_dosingtime",
				#"ing.typecompo AS ing_typecompo",
				]
			list_from = ["`%(db_hist)s`.`fhist%(mois)s` AS base\nLEFT JOIN %(db_hist)s.ihist%(mois)s AS ing ON base.IDformule = ing.IDformule" %(info),]
			where = where_and(["statusformule IN (19 , 23, 25)", "ing.IDsousformule != 0"])
			list_group_by = None
			list_order_by = None

			querry3 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = [
				"base_IDformule",
				"base_codeformule",
				"base_nomformule",
				"base_heurecreation AS reception_formule_base",
				"sf.heurecreation AS reception_formule_SFx",

				#"sf.heuredebutfabrication AS debut_fabrication_SFx",
				#"sf.heurefinfabrication AS fin_fabrication_SFx",
				#"base_heuredebutfabrication AS debut_fabrication_formule_base",
				#"base_heurefinfabrication AS fin_fabrication_formule_base",
				#"ing_dosingtime AS dosage_SFx_dans_formule_base",

				"(sf.heuredebutfabrication-sf.heurecreation)/60 AS reaction_SFx",
				"(sf.heurefinfabrication-sf.heurecreation)/60 AS reponse_SFx",
				"(sf.heurefinfabrication-sf.heuredebutfabrication)/60 AS fabrication_SFx",
				"(base_heuredebutfabrication-base_heurecreation)/60 AS reaction_formule_base",
				"(base_heurefinfabrication-base_heurecreation)/60 AS reponse_formule_base",
				"(base_heurefinfabrication-base_heuredebutfabrication)/60 AS fabrication_formule_base",

				"(ing_heureprod-sf.heurefinfabrication)/60 AS reaction_utilisation_SFx",
				]
			list_from = [sub_querry(querry3,"`zz`")+"\nLEFT JOIN %(db_hist)s.fhist%(mois)s AS sf on zz.ing_IDsousformule = sf.IDformule" %(info),]
			where = "sf.IDformule IS NOT NULL"
			list_group_by = None
			list_order_by = None

			querry4 =  querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = ["*",]
			list_from = [sub_querry(querry4,"`yy`"),]
			where = "reponse_SFx < 60*24*10"
			list_group_by = None
			list_order_by = None

			querry5 = querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

			list_select = [
				"\"20%s-%s\" AS `mois`" %(mois[:2],mois[2:]),
				"ROUND(AVG(reaction_SFx),1) AS reaction_SFx",
				"ROUND(AVG(reponse_SFx),1) AS reponse_SFx",
				"ROUND(AVG(fabrication_SFx),1) AS fabrication_SFx",
				"ROUND(AVG(reaction_formule_base),1) AS reaction_formule_base",
				"ROUND(AVG(reponse_formule_base),1) AS reponse_formule_base",
				"ROUND(AVG(fabrication_formule_base),1) AS fabrication_formule_base",

				"ROUND(AVG(reaction_utilisation_SFx),1) AS reaction_utilisation_SFx",
				]
			list_from = [sub_querry(querry5,"`xx`"),]
			where = None
			list_group_by = None
			list_order_by = None

			querry1.append( querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by) )

			querry2 = querry_union(querry1)


		else:
			raise ValueError("%s n'est pas dans %s" %(filtre_de_base, LIST_FILTRE_BASE))

	return querry2



# Analyse activité actuel ( base principale )
def list_personne_connecter(mysql_con, db_hist):
	"""
	Recherche dans la table d'historique les nouvelles connexion du jours
	"""
	#info = {"db_hist" : db_hist, "mois" : datetime.datetime.now().strftime("%y%m"), "jour" : datetime.datetime.now().strftime("%y-%m-%d")}
	info = {"db_hist" : db_hist, "mois" : "1707", "jour" : "2017-07-20"}

	list_select = ["IF( UPPER(SUBSTRING(`username`, 1, 5 )) = \"SUPER\",SUBSTRING(`username`, 6, 50 ), UPPER(`username`)) AS `nom_responsable_dosage`",]
	list_from = ["`%(db_hist)s`.`log%(mois)s`" %(info),]
	where = where_and(["`starttime` >= \"%(jour)s 00:00:00\"" %(info),"`endtime` = \"2000-01-01 00:00:00\"", "`username` != \"\"", "robotnumber >= 100"])
	list_group_by = ["`nom_responsable_dosage`",]
	list_order_by = ["`nom_responsable_dosage`",]
	querry = querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)

	resultat =  mysql_con.execute(querry)

	return [ x["nom_responsable_dosage"] for x in resultat]

def list_demandeur_assistante(mysql_con, db_prin, db_hist):
	"""
	Recherche la liste des demandeur et des assistantes
	"""
	querry = "SELECT UPPER(`formules`.`nomresponsable`) AS `nom_responsable_formule` FROM `%s`.`formules` GROUP BY `nom_responsable_formule`" %(db_prin)

	resultat =  mysql_con.execute(querry)

	demandeur = []
	assistante = list_personne_connecter(mysql_con, db_hist)

	for r in resultat:
		rr = r["nom_responsable_formule"].split("/")
		if len(rr) == 0:
			append_uniq(demandeur, "inconnu")
		else:
			append_uniq(demandeur, rr[0])
			if len(rr) == 1:
				append_uniq(assistante, "inconnu")
			else:
				for rrr in rr[1:]:
					append_uniq(assistante, rrr)

	demandeur.sort()
	assistante.sort()
	return demandeur, assistante

def nombre_formule_demandeur(mysql_con, db_prin, db_hist):
	"""
	Recherche le nombre de formule par demandeur
	"""
	demandeur, assistante = list_demandeur_assistante(mysql_con, db_prin, db_hist)

	querry = """SELECT
				UPPER(SUBSTRING(`formules`.`nomresponsable`, 1, IF (POSITION("/" IN `formules`.`nomresponsable`) = 0,50,POSITION("/" IN `formules`.`nomresponsable`)-1))) AS `demandeur`,
				COUNT(*) AS `nombre_formule`
				FROM `%s`.`formules`
				GROUP BY `demandeur`""" %(db_prin)
	formule_demandeur =  mysql_con.execute(querry)

	#formule_demandeur = []
	#for d in demandeur:
	#	list_select = ["""UPPER(SUBSTRING(`formules`.`nomresponsable`, 1, IF (POSITION("/" IN `formules`.`nomresponsable`) = 0,50,POSITION("/" IN `formules`.`nomresponsable`)-1))) AS `demandeur`""",]
	#	list_from = ["`%s`.`formules`" %(db_prin),]
	#	where = None
	#	list_group_by = None
	#	list_order_by = None
	#	querry1 = querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
	#	list_select = 	["COUNT(*) AS `nombre_formule`",]
	#	list_from = [sub_querry(querry1,"`zz`"),]
	#	where = "`demandeur` like \"%%%s%%\"" %(d)
	#	list_group_by = None
	#	list_order_by = None
	#	querry2 = querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
	#	resultat =  mysql_con.execute(querry2)
	#
	#	formule_demandeur.append({"demandeur" : d, "nombre_formule" : resultat[0]["nombre_formule"]})

	return formule_demandeur

def nombre_formule_assistante(mysql_con, db_prin, db_hist):
	"""
	Recherche le nombre de formule adressé à chaque assistante
	"""
	demandeur, assistante = list_demandeur_assistante(mysql_con, db_prin, db_hist)

	formule_assistante = []
	for a in assistante:
		if a == "inconnu":
			list_select = ["UPPER(SUBSTRING(`formules`.`nomresponsable`, POSITION("/" IN `formules`.`nomresponsable`), 50)) AS `demandeur`",]
			list_from = ["`%s`.`formules`" %(db_prin),]
			where = None
			list_group_by = None
			list_order_by = None
			querry1 = querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
			list_select = 	["COUNT(*) AS `nombre_formule`",]
			list_from = [sub_querry(querry1,"`zz`"),]
			where = "`demandeur` = \"\""
			list_group_by = None
			list_order_by = None
			querry2 = querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
			resultat =  mysql_con.execute(querry2)
		else:
			list_select = ["""UPPER(SUBSTRING(`formules`.`nomresponsable`, POSITION("/" IN `formules`.`nomresponsable`), 50)) AS `demandeur`""",]
			list_from = ["`%s`.`formules`" %(db_prin),]
			where = None
			list_group_by = None
			list_order_by = None
			querry1 = querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
			list_select = 	["COUNT(*) AS `nombre_formule`",]
			list_from = [sub_querry(querry1,"`zz`"),]
			where = "`demandeur` like \"%%%s%%\"" %(a)
			list_group_by = None
			list_order_by = None
			querry2 = querry_select(list_select=list_select, list_from=list_from, where=where, list_group_by=list_group_by, list_order_by=list_order_by)
			resultat =  mysql_con.execute(querry2)

		formule_assistante.append({"assistante" : a, "nombre_formule" : resultat[0]["nombre_formule"]})

	return formule_assistante

def formule_sans_assistante(mysql_con, db_prin, db_hist):
	"""
	Recherche les formule qui ne pourront pas être produites : les assistantes sont absentent
	"""
	assistante = list_personne_connecter(mysql_con, db_hist)
	querry = "SELECT IDformule AS id_formule, codeformule AS code_formule, nomresponsable AS nom_responsable FROM %s.formules WHERE nomresponsable NOT REGEXP \"%s\"" %(db_prin, "|".join(assistante))
	#print querry
	resultat =  mysql_con.execute(querry)
	return resultat



def export_csv(resultat, nom_fichier, separateur=";", fin_de_ligne="\n", encoding="utf-8"):
	"""
	"""
	if len(resultat) > 0:
		csv_entete = [ k for k in resultat[0]] 
		csv = []
		csv.append( separateur.join(csv_entete) )
		for r in resultat:
			csv_ligne = []
			for k in csv_entete:
				csv_ligne.append( unicode(r[k]) )
			csv.append( separateur.join(csv_ligne) )

		f = codecs.open(nom_fichier, "w", encoding=encoding)
		fichier_csv = f.write(fin_de_ligne.join(csv))
		f.close()
	
	else:
		print "rien n'a enregistrer"





# Fonction de test
def f_print(fonc, list_filtre_de_base):
	my = mysql.Mysql()

	#my.open(mysql_host="localhost", mysql_port=3306, mysql_user="root", mysql_password="rootmariadb", autocommit=True, charset="utf8", use_unicode=True)
	my.open(mysql_host="localhost", mysql_port=3306, mysql_user="swap-rw", mysql_password="F1rmen1ch123", autocommit=True, charset="utf8", use_unicode=True)

	mysql_con = my
	print "_"*80
	print " "*40 + fonc.__name__.upper()
	date_debut = datetime.datetime.strptime("2017-06-01", "%Y-%m-%d")
	date_debut = datetime.datetime.strptime("2012-01-01", "%Y-%m-%d")
	date_fin = datetime.datetime.strptime("2017-07-30", "%Y-%m-%d")
	date_fin = datetime.datetime.strptime("2017-12-31", "%Y-%m-%d")
	db_prin = "dorygva"
	db_hist = "dorygva_hist"
	for filtre_de_base in list_filtre_de_base:
		print "-"*20 + filtre_de_base.upper()
		querry = fonc(mysql_con, filtre_de_base, date_debut, date_fin, db_hist)
		print querry
		if querry != None:
			resultat =  my.execute(querry)
			for r in resultat:
				print r
			export_csv(resultat=resultat, nom_fichier=fonc.__name__+"_"+filtre_de_base+".csv", separateur=";", fin_de_ligne="\r\n")
				
	my.close()

def f_print1(fonc, list_filtre_de_base):
	my = mysql.Mysql()

	#my.open(mysql_host="localhost", mysql_port=3306, mysql_user="root", mysql_password="rootmariadb", autocommit=True, charset="utf8", use_unicode=True)
	my.open(mysql_host="localhost", mysql_port=3306, mysql_user="swap-rw", mysql_password="F1rmen1ch123", autocommit=True, charset="utf8", use_unicode=True)

	mysql_con = my
	print "_"*80
	print " "*40 + fonc.__name__.upper()
	db_prin = "dorygva"
	db_hist = "dorygva_hist"
	
	r = fonc(mysql_con, db_prin, db_hist)
	for rr in r:
		print rr

	my.close()

def f_print2(fonc, list_filtre_de_base):
	my = mysql.Mysql()

	#my.open(mysql_host="localhost", mysql_port=3306, mysql_user="root", mysql_password="rootmariadb", autocommit=True, charset="utf8", use_unicode=True)
	my.open(mysql_host="localhost", mysql_port=3306, mysql_user="swap-rw", mysql_password="F1rmen1ch123", autocommit=True, charset="utf8", use_unicode=True)

	mysql_con = my
	print "_"*80
	print " "*40 + fonc.__name__.upper()
	db_prin = "dorygva_hist"
	db_hist = "dorygva_hist"
	
	r = fonc(mysql_con, db_prin)
	print r

	my.close()

if __name__ == '__main__':
	import mysql
	import datetime
	import sys
	print sys.argv

	#f_print(index_fhist, sys.argv[1:])
	#f_print(index_ihist, sys.argv[1:])

	#f_print(hist_nombre_de_formule, sys.argv[1:])
	#f_print(hist_nombre_de_formule_jour, sys.argv[1:])
	#f_print(hist_nombre_de_formule_mois, sys.argv[1:])
	#f_print(hist_nombre_de_dosage, sys.argv[1:])
	#f_print(hist_nombre_de_dosage_jour, sys.argv[1:])
	#f_print(hist_nombre_de_dosage_mois, sys.argv[1:])
	#f_print(hist_nombre_de_dosage_pid, sys.argv[1:])
	#f_print(hist_nombre_de_dosage_station, sys.argv[1:])
	#f_print(hist_productivite_mois, sys.argv[1:])
	#f_print(hist_temps_reponse, sys.argv[1:])
	f_print(hist_suivie_sfx, sys.argv[1:])

	#f_print1(nombre_formule_demandeur, sys.argv[1:])
	#f_print1(nombre_formule_assistante, sys.argv[1:])
	#f_print1(formule_sans_assistante, sys.argv[1:])
	#f_print2(list_personne_connecter, sys.argv[1:])

