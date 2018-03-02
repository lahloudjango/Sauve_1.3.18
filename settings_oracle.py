# -*- coding: utf-8 -*-
from __future__ import unicode_literals



DATABASES_ORACLE = {
	"client_test":
	{
		"oracle_user": "charly",
		"oracle_password": "charly",
		"oracle_host": "172.25.5.11",
		"oracle_port": 1521,
		"oracle_sid": 'MTRIF12GFSARA',
	},
	"client":
	{
		"oracle_user": "frag_mgr",
		"oracle_password": "trifoil",
		"oracle_host": "172.25.5.14",
		"oracle_port": 1521,
		"oracle_sid": 'MTRIF12',
	},
#Database OneT de TEST
	"onet_test":
	{
		"oracle_user": "suser_tepl_erp",
		"oracle_password": "tepl",
		"oracle_host": "10.120.15.200",
		"oracle_port": 1521,
		"oracle_sid": "PMIS",
	},
#Database OneT de PROD
	"onet_prod":
	{
		"oracle_user": "suser_tepl_erp",
		"oracle_password": "takasago",
		"oracle_host": "10.120.15.176",
		"oracle_port": 9101,
		"oracle_sn": "GDB01",
	},
}
