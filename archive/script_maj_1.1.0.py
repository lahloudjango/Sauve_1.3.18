# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from lib_linautom.python import mysql

import codecs
import types

fichier = "PERFUMER CODES TEPL - TAKUS.csv"
#fichier = "test.csv"

ferr = codecs.open(fichier, "r", encoding="ISO-8859-15")

mysql_host = "localhost"
mysql_port = 3306
mysql_user = "root"
mysql_password = "rootmysql"


def print_ascii(text):
	if type(text) == types.UnicodeType:
		print text.encode("ascii", "replace")
	elif type(text) == types.NoneType:
		print "None".encode("ascii", "replace")
	else:
		print text

def espace():
	my = mysql.Mysql()
	my.open(mysql_host, mysql_port, mysql_user, mysql_password )

	querry = "SELECT * FROM `stock`.`stock_labo_nomenclature` WHERE `stock_labo_nomenclature`.`code` LIKE \"% %\""
	reponse = my.execute(querry)
	ligne = 0
	count = 0
	for r in reponse:
		ligne += 1
	#	print r["id"], r["code"]
		querry = "UPDATE `stock`.`stock_labo_nomenclature` SET `code` = \"%s\" WHERE `id` = %s" %(r["code"].replace(" ", ""), r["id"])
	#	print querry
		try:
			rr = my.execute(querry)
			count += 1
		except:
			print_ascii("UPDATE impossible\tid:%6s\tcode:%s" %(r["id"], r["code"]))

	my.close()
	print_ascii("Total code espace supprimé: %s/%s" %(count,ligne))



def code_onet():
	my = mysql.Mysql()
	my.open(mysql_host, mysql_port, mysql_user, mysql_password )
	ligne = 0
	count = 0
	while True:
		f = ferr.readline()[:-1]
		if f == "":
			break

		code = f.split(";")
#		print code
		if code[0] == "" or code[1] == "":
			continue
		ligne += 1
		querry = "SELECT * FROM `stock`.`stock_labo_nomenclature` WHERE `stock_labo_nomenclature`.`code` = \"%s\"" %(code[1])
		r = my.execute(querry)
#		print r
		if len(r) == 1:
#			print ligne, count, r[0]["id"], code[0]
			querry = "UPDATE `stock`.`stock_labo_nomenclature` SET `code` = \"%s\" WHERE `id` = %s" %(code[0], r[0]["id"])
#			print querry
			try:
				rr = my.execute(querry)
				count += 1
			except:
				print_ascii("UPDATE impossible\tid:%6s\tancien code:%8s\tnouveau code:%s" %(r[0]["id"], code[1], code[0]))
			continue
		elif len(r) > 1:
			print_ascii("!!!!! OH ! Réponce multiple\n%s" %(r))

		if code[1].find(" ") != -1:
			ligne += 1
			code[1] = code[1].replace(" ", "")
#			print code
			querry = "SELECT * FROM `stock`.`stock_labo_nomenclature` WHERE `stock_labo_nomenclature`.`code` = \"%s\"" %(code[1])
			r = my.execute(querry)
#			print r
			if len(r) == 1:
#				print ligne, count, r[0]["id"], code[0]
				querry = "UPDATE `stock`.`stock_labo_nomenclature` SET `code` = \"%s\" WHERE `id` = %s" %(code[0], r[0]["id"])
#				print querry
				try:
					rr = my.execute(querry)
					count += 1
				except:
					print_ascii("UPDATE impossible\tid:%6s\tancien code:%8s\tnouveau code:%s" %(r[0]["id"], code[1], code[0]))
			elif len(r) > 1:
				print_ascii("!!!!! OH ! Réponce multiple\n%s" %(r))

	my.close()
	print_ascii("Total code onet: %s modifiée /%s soumissions" %(count,ligne))



def modif_solution():
	my = mysql.Mysql()
	my.open(mysql_host, mysql_port, mysql_user, mysql_password )

	querry = "SELECT * FROM `stock`.`stock_labo_nomenclature` WHERE `stock_labo_nomenclature`.`description` LIKE \"[D-0%\""

	sol = my.execute(querry)

	for s in sol:
	#	print "\n" + unicode(s)
		cut = s["description"].find("] ")
		if cut == -1:
			print_ascii("Découpage description impossible %s" %(s))
		else:
	#		print s["description"][1:cut]
	#		print s["description"][cut+2:]
			querry = "UPDATE `stock`.`stock_labo_nomenclature` SET `code` = \"%s\", `description` = \"%s\" WHERE `id` = %s" %(s["description"][1:cut], s["description"][cut+2:], s["id"])
	#		print querry
			e = my.execute(querry)
		cut2 = s["commentaire"].find("] ")


		if cut2 == -1:
			print_ascii("Découpage commentaire impossible %s" %(s))
		else:
	#		print s["commentaire"][1:cut]
	#		print s["commentaire"][cut+2:]
			querry = "UPDATE `stock`.`stock_labo_nomenclature` SET `commentaire` = \"%s\" WHERE `id` = %s" %(s["commentaire"][cut+2:], s["id"])
	#		print querry
			e = my.execute(querry)

	print_ascii("Total solution modifiées : %s" %(len(sol)))

	my.close()

#modif_solution()

#espace()

code_onet()

