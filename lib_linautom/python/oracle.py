#-*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Module d'enrobage autour de cx_Oracle avec mise en forme des données en dictionaire
"""

__author__ = "Charly GONTERO"
__date__ = "2016-11-29 09:42:12"
__version__ = "2.1.0"
__credits__ = """
 *  oracle.py
 *
 *  Copyright 2015 Charly GONTERO
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

import subprocess
import time

def auto_detect():
	print "Oracle import auto detect"
	ldd_version = subprocess.Popen("ldd --version", shell=True, stdout=subprocess.PIPE)
	ldd_version.lignes = ldd_version.stdout.readlines()
	ldd_version.ligne0_split = ldd_version.lignes[0].split(" ")
	ldd_version.distribution = ldd_version.ligne0_split[1][1:]
	ldd_version.serie = ldd_version.ligne0_split[2]
	ldd_version.version = float(ldd_version.ligne0_split[4][:-1])
	ldd_version.version_ = ldd_version.ligne0_split[4][:-1].replace(".","_")
	print ldd_version.distribution
	print ldd_version.serie
	print ldd_version.version
	print ldd_version.version_
	if ldd_version.serie == "EGLIBC": #cx_Oracle_EGLIBC_2_13.so
		if 2.13 == ldd_version.version:
			ldd_version.version_select = "2_13"
		else:
			print "!! Oracle version libc incompatible : %s" %(ldd_version.version_)
	elif ldd_version.serie == "GLIBC": #cx_Oracle_GLIBC_2_13.so
		if 2.14 == ldd_version.version:
			ldd_version.version_select = "2_14"
		if 2.19 == ldd_version.version:
			ldd_version.version_select = "2_19"
		else:
			print "!! Oracle version libc incompatible : %s" %(ldd_version.version_)
	else:
		print "!! Oracle serie libc incompatible : %s" %(ldd_version.serie)
	print ldd_version.version_select
	lib_check = subprocess.Popen("ls -lah ./lib_linautom/python/cx_Oracle.* | grep %s | grep %s" %(ldd_version.serie, ldd_version.version_select), shell=True, stdout=subprocess.PIPE)
	lib_check.lignes = lib_check.stdout.readlines()
	if len(lib_check.lignes) == 0:
		print "Librairie oracle incorrect"
		lib_rm = subprocess.Popen("cd ./lib_linautom/python/ ; rm cx_Oracle.so", shell=True, stdout=subprocess.PIPE)
		print lib_rm.stdout.readlines()
		lib_ln = subprocess.Popen("cd ./lib_linautom/python/ ; ln -s cx_Oracle_%s_%s.so cx_Oracle.so" %(ldd_version.serie, ldd_version.version_select), shell=True, stdout=subprocess.PIPE)
		print lib_ln.stdout.readlines()
		print "link modifié pour import"
	else:
		print "Librairie oracle correct"

	time.sleep(1)
	list_f = subprocess.Popen("ls -lah ./lib_linautom/python/cx_Oracle*", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	list_f.lignes = list_f.stdout.readlines()

auto_detect()

import cx_Oracle

VERSION = __version__
def version():
	return __version__


class Oracle(object):
	"""
	Definie les connections vers les serveurs de base de donnees contenant les base de reference et les base à mettre à jour
	"""
	def __init__(self):
		"""
		Rien a faire
		"""

	def open(self, oracle_host, oracle_port, oracle_user, oracle_password, oracle_sid=None, oracle_sn=None):
		"""
		Ouvre les connection vers les serveur de base de donnees
		Création de la connection avec le SID ou le service name
		"""
		if oracle_sid != None:
			self.oracle_con = cx_Oracle.connect(oracle_user, oracle_password, cx_Oracle.makedsn(oracle_host, oracle_port, oracle_sid))
		elif oracle_sn != None:
			self.oracle_con = cx_Oracle.connect("%s/%s@%s:%s/%s" %(oracle_user, oracle_password, oracle_host, oracle_port, oracle_sn))
		else:
			raise ValueError("")
		self.oracle_con_curseur = self.oracle_con.cursor()

	def execute(self, querry):
		"""
		Execute les requetes SQL:
		"""
		self.oracle_con_curseur.execute(querry)
		resultat = self.oracle_con_curseur.fetchall()
		if len(resultat) > 0:
			col_liste_num = range(0, len(resultat[0]))
			col_liste_nom = []
			for c in self.oracle_con_curseur.description:
				col_liste_nom.append(c[0])
			resultat_dict = []
			for ligne in resultat:
				l = {}
				for colonne in col_liste_num:
					l.update({col_liste_nom[colonne]:ligne[colonne]})
				resultat_dict.append(l)
			return resultat_dict
		else:
			return []

	def close(self):
		"""
		Ferme les connection vers les serveur de base de donnees
		"""
		self.oracle_con_curseur.close()
		self.oracle_con.close()



if __name__ == "__main__":
	"""
	Exemple d"utilisation de connexion oracle
	"""
	#Connection avec un SID
	client_sid = {
		"oracle_user": "charly",
		"oracle_password": "charly",
		"oracle_host": "172.25.5.11",
		"oracle_port": 1521,
		"oracle_sid": 'MTRIF12GFSARA',
	}
	#Connection avec un Service Name
	client_sn = {
		#"oracle_user": "frag_mgr",
		#"oracle_password": "trifoil",
		#"oracle_host": "172.25.5.14",
		#"oracle_port": 1521,
		#"oracle_sn": 'MTRIF12',
		"oracle_user": "suser_tepl_erp",
		"oracle_password": "takasago",
		"oracle_host": "10.120.15.176",
		"oracle_port": 9101,
		"oracle_sn": "GDB01",
	}
	o=Oracle()

	projet = "16-02367"
	param_oracle = "onet_test"

	o.open(**client_sn)
	querry = """
select c.batch_number,
	c.xinumber,
	c.frmlname,
	c.profilenumber,
	c.TME_COMPSUBMIT,
	cust.aliasname,
	ka.keyaccountname
from PMIS_APPS.HIS_FRML_COMPHDR c
	left join pmis_master.gpmis_projects_cl   p     on  p.projectnumber = c.profilenumber
	join pmis_master.gpmis_customer_dtl       cust  on  cust.custid = p.custid
	join pmis_master.gpmis_customer           ka    on  ka.keyaccountid = cust.keyaccountid
where robot_location = 'TEPL' and rownum < 10"""

	querry = """
SELECT
	c.batch_number      AS BATCH_NUMBER,
	c.xinumber          AS CODE,
	trim(c.frmlname)    AS DESCRIPTION,
	c.profilenumber     AS PROJET,
	cust.aliasname      AS CLIENT,
	ka.keyaccountname   AS CLIENT_KA
FROM pmis_apps.his_frml_comphdr              c
	LEFT JOIN pmis_master.gpmis_projects_cl  p     ON p.projectnumber = c.profilenumber
	LEFT JOIN pmis_master.gpmis_customer_dtl cust  ON cust.custid = p.custid
	LEFT JOIN pmis_master.gpmis_customer     ka    ON ka.keyaccountid = cust.keyaccountid
WHERE 
	c.batch_number = '20170630085310000105'
	AND rownum < 10
"""
	print querry
	oracle_client = o.execute(querry)
	for c in oracle_client:
		print c

	querry = """
SELECT 
	c.profilenumber     AS PROJET,
	cust.aliasname      AS CLIENT,
	ka.keyaccountname   AS CLIENT_KA
FROM pmis_apps.his_frml_comphdr              c
	LEFT JOIN pmis_master.gpmis_projects_cl  p     ON p.projectnumber = c.profilenumber
	LEFT JOIN pmis_master.gpmis_customer_dtl cust  ON cust.custid = p.custid
	LEFT JOIN pmis_master.gpmis_customer     ka    ON ka.keyaccountid = cust.keyaccountid
WHERE c.profilenumber = '17-11732/1'
	AND rownum < 10
"""
	print querry
	oracle_client = o.execute(querry)
	for c in oracle_client:
		print c

	querry = """
SELECT
	CUSTNAME as CLIENT,
	KA as CLIENT_KA,
	PROJECTNUMBER as PROJET
FROM PROJECTS_CUSTOMERS_KA
WHERE PROJECTNUMBER = '17-11732/1'
"""
	print querry
	oracle_client = o.execute(querry)
	for c in oracle_client:
		print c

