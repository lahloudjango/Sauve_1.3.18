# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
stock labo paris
Programme utilisant le framework django

"""

import codecs

__author__ = "Charly GONTERO"
__date__ = "2016-03-28 11:19:34"
__version__ = codecs.open("VERSION.txt", "r", encoding="utf-8").readline().split("\n")[0]
__credits__ = """
 *  Stock Labo Paris
 *
 *  Copyright 2015 Charly GONTERO
 *
 *  Ce programme est propriété de Takasago à l'exclusion des librairies 
 *  explicitement déclaré sous licence GPL
 *
"""
#!!!!! Atention au daemon/django_*.py au APPS_PATH
status_developement = {
	"code": "prod",
	"data": "prod",
	"oracle": "onet_prod"
	}

if status_developement["code"] == "prod":
	status_developement.update({"info": ""})
elif status_developement["code"] == "dev":
	if status_developement["data"] == "prod":
		status_developement.update({"info": "Environement de dévelopement connecté sur les données de production"})
	elif status_developement["data"] == "dev":
		status_developement.update({"info": "Environement et données de dev"})
	else:
		status_developement.update({"info": "!!??"})
else:
	status_developement.update({"info": "!!??"})



VERSION = __version__
def version():
	return __version__


