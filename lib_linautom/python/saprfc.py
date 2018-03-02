# -*- coding: utf-8 -*-
"""
Python wrapping for RFC calls to SAP R/3
Ce module nécessite les librairie :
libsapnwrfc.so
"""
from __future__ import unicode_literals
import sys
import saprfcutil
from struct import *
from string import *
import re
from types import *
import datetime
import copy

#DEBUG = False

__author__ = "Charly GONTERO"
__date__ = "2016-05-03 06:51:30"
__version__ = 2.0
__credits__ = """
 *  saprfc.py
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

if sys.version < "2.3":
	print "Wrong Python Version (must be >=2.3) !!!"
	sys.exit(1)


RFCIMPORT	= 0
RFCEXPORT	= 1
RFCTABLE	= 2
RFCCHANGE	= 3


RFCTYPE_CHAR = 				0		#1-byte or multibyte character.
RFCTYPE_DATE = 				1		#date ( YYYYYMMDD )
RFCTYPE_BCD = 				2		#packed number.
RFCTYPE_TIME = 				3		#time (HHMMSS)
RFCTYPE_BYTE = 				4		#raw data, binary,
#RFCTYPE_ITAB = 			5		#internal table
RFCTYPE_NUM = 				6		#digits, fixed size,
RFCTYPE_FLOAT = 			7		#floating point bouble lenght,
RFCTYPE_INT = 				8		#4-byte integer
RFCTYPE_INT2 = 				9		#2-byte integer
RFCTYPE_INT1 = 				10		#1-byte integer
#RFCTYPE_DATE_1 = 			11		#old fashioned date,
#RFCTYPE_DATE_2 = 			12		#old fashioned date,
#RFCTYPE_NULL = 			13		#not supported data type. */
#RFCTYPE_WIDE_2 = 			14		#wide character 2 byte (internal use)*/
#RFCTYPE_WIDE_4 = 			15		#wide character 4 byte (internal use)*/
#RFCTYPE_STRUCTURE = 		16		#structure (internal use) */
#RFCTYPE_ABAP4OBJECT = 		17		#abap/4 object (internal use) */
#RFCTYPE_IUNKNOWN = 		18		#IUnknown object
#RFCTYPE_WSTRING = 			19		#wide character string
#RFCTYPE_SAPAUTOMATION =	20		#sap automation object
#RFCTYPE_STUB = 			21		#remote object's stub
#RFCTYPE_WIRE_OBJECT = 		22		#Object on the wire
RFCTYPE_BLOB = 				23		#binary large object,
#RFCTYPE_CORBA_OBJECT = 	24		#Corba object
#RFCTYPE_PADDING = 			25		#use in dummy fields to ensure proper
RFCTYPE_UNICODE = 			26		#Never used, always use RFCTYPE_CHAR.
RFCTYPE_XMLDATA = 			27		#zero terminated string describing ABAP data
RFCTYPE_STRING = 			28		#zero terminated string */
RFCTYPE_XSTRING = 			29		#raw string with length field in bytes */
RFCTYPE_DECF16 = 			30		#decimal floating point 8 bytes  */
RFCTYPE_DECF34 = 			31		#decimal floating point 16 bytes  */
# Personnal format
#RFCTYPE_BOOL = 				101 	#1-byte :0 = False else True
#RFCTYPE_INT4 = 				102 	#4-byte integer
#RFCTYPE_INT8 = 				103 	#8-byte integer
#RFCTYPE_UINT = 				104 	#4-byte unsigned integer
#RFCTYPE_UINT1 = 			105 	#1-byte unsigned integer
#RFCTYPE_UINT2 = 			106 	#2-byte unsigned integer
#RFCTYPE_UINT4 = 			107 	#4-byte unsigned integer
#RFCTYPE_UINT8 = 			108 	#8-byte unsigned integer
#RFCTYPE_DOUBLE = 			109 	#floating point bouble lenght,
#RFCTYPE_HEX = 				110 	#Hexadecimal coding
#RFCTYPE_NUM_STRING_CHAR = 	111		#Integer numeric string
#RFCTYPE_STRING_CHAR = 		112		#Integer numeric string

RFC_TYPE_SPEC = {
	0   : {"Description" : "String",			"c_name" : "char[]", 				"pack_type" : None,		"len" : None, 	"datetime" : None, 		"sap_type" : "C", 	"intype" : 0, 		"init" : " "},
	1   : {"Description" : "Date", 				"c_name" : "char[]", 				"pack_type" : None,		"len" : 8, 		"datetime" : "%Y%m%d", 	"sap_type" : "D", 	"intype" : 1, 		"init" : None},
	2   : {"Description" : "BCD", 				"c_name" : "char[]", 				"pack_type" : "bcd",	"len" : None, 	"datetime" : None, 		"sap_type" : "P", 	"intype" : 2, 		"init" : "\x00"},
	3   : {"Description" : "Time", 				"c_name" : "char[]", 				"pack_type" : None,		"len" : 6, 		"datetime" : "%H%M%S", 	"sap_type" : "T", 	"intype" : 3, 		"init" : None},
	4   : {"Description" : "Byte", 				"c_name" : "byte", 					"pack_type" : "c",		"len" : 1, 		"datetime" : None, 		"sap_type" : "", 	"intype" : 4, 		"init" : "\x00"},
	6   : {"Description" : "Num", 				"c_name" : "char[]", 				"pack_type" : None,		"len" : None, 	"datetime" : None, 		"sap_type" : "N", 	"intype" : 6, 		"init" : "\x00"},
	7   : {"Description" : "Float", 			"c_name" : "double", 				"pack_type" : "d",		"len" : 8, 		"datetime" : None, 		"sap_type" : "F", 	"intype" : 7, 		"init" : "\x00"},
	8   : {"Description" : "Int", 				"c_name" : "int", 					"pack_type" : "i",		"len" : 4, 		"datetime" : None, 		"sap_type" : "I", 	"intype" : 8, 		"init" : "\x00"},
	9   : {"Description" : "Int 2 bytes",		"c_name" : "short", 				"pack_type" : "h",		"len" : 2, 		"datetime" : None, 		"sap_type" : "s", 	"intype" : 9, 		"init" : "\x00"},
	10  : {"Description" : "Int 1 bytes",		"c_name" : "byte", 					"pack_type" : "b",		"len" : 1, 		"datetime" : None, 		"sap_type" : "b", 	"intype" : 10, 		"init" : "\x00"},
	23  : {"Description" : "Blob ", 			"c_name" : "byte[]", 				"pack_type" : None,		"len" : None, 	"datetime" : None, 		"sap_type" : "X", 	"intype" : 23, 		"init" : "\x00"},
#	101 : {"Description" : "Bool", 				"c_name" : "byte", 					"pack_type" : None,		"len" : 1, 		"datetime" : None, 		"sap_type" : "", 	"intype" : 101, 	"init" : "\x00"},
#	102 : {"Description" : "Int 4 bytes",		"c_name" : "long", 					"pack_type" : "l",		"len" : 4, 		"datetime" : None, 		"sap_type" : "I", 	"intype" : 102, 	"init" : "\x00"},
#	103 : {"Description" : "Int 8 bytes",		"c_name" : "long long",				"pack_type" : "q",		"len" : 8, 		"datetime" : None, 		"sap_type" : "", 	"intype" : 103, 	"init" : "\x00"},
#	104 : {"Description" : "Uint",				"c_name" : "unsigned int",			"pack_type" : "I",		"len" : 4, 		"datetime" : None, 		"sap_type" : "", 	"intype" : 104, 	"init" : "\x00"},
#	105 : {"Description" : "Uint 1 bytes",		"c_name" : "unsigned byte",			"pack_type" : "B",		"len" : 1, 		"datetime" : None, 		"sap_type" : "", 	"intype" : 105, 	"init" : "\x00"},
#	106 : {"Description" : "Uint 2 bytes",		"c_name" : "unsigned short", 		"pack_type" : "H",		"len" : 2, 		"datetime" : None, 		"sap_type" : "", 	"intype" : 106, 	"init" : "\x00"},
#	107 : {"Description" : "Uint 4 bytes",		"c_name" : "unsigned long", 		"pack_type" : "L",		"len" : 4, 		"datetime" : None, 		"sap_type" : "", 	"intype" : 107, 	"init" : "\x00"},
#	108 : {"Description" : "Uint 8 bytes",		"c_name" : "unsigned long long", 	"pack_type" : "Q",		"len" : 8, 		"datetime" : None, 		"sap_type" : "", 	"intype" : 108, 	"init" : "\x00"},
#	109 : {"Description" : "Double", 			"c_name" : "double", 				"pack_type" : "d",		"len" : 8, 		"datetime" : None, 		"sap_type" : "F", 	"intype" : 109, 	"init" : "\x00"},
#	110 : {"Description" : "hex", 				"c_name" : "char[]", 				"pack_type" : None, 	"len" : None, 	"datetime" : None, 		"sap_type" : "", 	"intype" : 110, 	"init" : "\x00"},
#	111 : {"Description" : "Num String Char",	"c_name" : "char[]", 				"pack_type" : None,		"len" : None, 	"datetime" : None, 		"sap_type" : "C", 	"intype" : 111, 	"init" : "0"},
#	112 : {"Description" : "String Char",		"c_name" : "char[]", 				"pack_type" : None,		"len" : None, 	"datetime" : None, 		"sap_type" : "C", 	"intype" : 112, 	"init" : " "},
	}


# Valid data types for fields
CHARTYPE = {
	"C": RFCTYPE_CHAR,
	"X": RFCTYPE_BYTE,
	"b": RFCTYPE_INT1,
	"s": RFCTYPE_INT2,
	"P": RFCTYPE_BCD,
	"D": RFCTYPE_DATE,
	"T": RFCTYPE_TIME,
	"N": RFCTYPE_NUM,
	"F": RFCTYPE_FLOAT,
	"I": RFCTYPE_INT,
	}

# sysinfo structure size
SYSINFO = [
	{ "NAME": "RFCPROTO",	"LEN": 3 },
	{ "NAME": "RFCCHARTYP",	"LEN": 4 },
	{ "NAME": "RFCINTTYP",	"LEN": 3 },
	{ "NAME": "RFCFLOTYP",	"LEN": 3 },
	{ "NAME": "RFCDEST",	"LEN": 32 },
	{ "NAME": "RFCHOST",	"LEN": 8 },
	{ "NAME": "RFCSYSID",	"LEN": 8 },
	{ "NAME": "RFCDATABS",	"LEN": 8 },
	{ "NAME": "RFCDBHOST",	"LEN": 32 },
	{ "NAME": "RFCDBSYS",	"LEN": 10 },
	{ "NAME": "RFCSAPRL",	"LEN": 4 },
	{ "NAME": "RFCMACH",	"LEN": 5 },
	{ "NAME": "RFCOPSYS",	"LEN": 10 },
	{ "NAME": "RFCTZONE",	"LEN": 6 },
	{ "NAME": "RFCDAYST",	"LEN": 1 },
	{ "NAME": "RFCIPADDR",	"LEN": 15 },
	{ "NAME": "RFCKERNRL",	"LEN": 4 },
	{ "NAME": "RFCHOST2",	"LEN": 32 },
	{ "NAME": "RFCSI_RESV",	"LEN": 12 },
]

class conn(object):
	"""
	Gestion de la connunication avec SAP
	"""

	def __init__(self, ashost="localhost", sysnr=00, lang="EN", client=000, r3name=None,  user=None, passwd=None, getsso2=0, mysapsso2=None, x509cert=None, gwhost=None, gwserv=None, tpname=None, trace=0):
		"""
		The constructor.  Takes the rfc library connection parameters are arguments
		trace (OFF/ON/ABAP-DEBUG or also trace ON and ABAP-DEBUG: 0/1/2/3)
		"""
		self.ashost = ashost
		self.sysnr = int(sysnr)
		self.r3name = r3name
		self.lang = lang
		self.client = int(client)
		self.user = user
		self.passwd = passwd
		self.getsso2 = getsso2
		self.mysapsso2 = mysapsso2
		self.x509cert = x509cert
		self.gwhost = gwhost
		self.gwserv = gwserv
		self.tpname = tpname
		self.trace = int(trace)
		self.constr = ""
		self.sysinfo = {}
		self.ifacesindex = {}
		self.ifaces = []

	def iface(self, ifc):
		"""
		Déclare le nom d'une fonction RFC SAP
		"""
		self.ifaces.append(ifc)
		self.ifacesindex[ifc.name] = ifc
		return ifc

	def connect(self):
		"""
		Fonction de connection à SAP ( open )
		"""
		self.constr = ""
		if self.r3name:
			self.constr += "R3NAME=%s "	 % self.r3name
		if self.ashost:
			self.constr += "ASHOST=%s "	 % self.ashost
			self.constr += "SYSNR=%02d "	% self.sysnr
		if self.lang:
			self.constr += "LANG=%s "	   % self.lang
		if self.client:
			self.constr += "CLIENT=%03d "   % self.client
		if self.user:
			self.constr += "USER=%s "	   % self.user
		if self.passwd:
			self.constr += "PASSWD=%s "	 % self.passwd
		if self.trace:
			self.constr += "TRACE=%d "	  % self.trace
		if self.tpname:
			self.constr += "TPNAME=%s "	 % self.tpname
		if self.gwhost:
			self.constr += "GWHOST=%s "	 % self.gwhost
		if self.gwserv:
			self.constr += "GWSERV=%s "	 % self.gwserv
		if self.mysapsso2:
			self.constr += "MYSAPSSO2=%s "  % self.mysapsso2
		if self.getsso2:
			self.constr += "GETSSO2=%d "	% self.getsso2
		if self.x509cert:
			self.constr += "X509CERT=%d "	% self.x509cert
		self.connection = saprfcutil.connect(self)
		return self.connection

	def is_connected(self):
		"""
		Retourne le status de la connection à SAP
		"""
		iping = iface("RFC_PING")
		return saprfcutil.call_receive(self, iping)

	def sapinfo(self):
		"""
		Appel la fonction RFC_SYSTEM_INFO de SAP est retourne les info sys SAP
		"""
		if len(self.sysinfo) > 0:
			return self.sysinfo
		isapinfo = iface("RFC_SYSTEM_INFO")
		rfcsi = parm("RFCSI_EXPORT", None, RFCIMPORT, RFCTYPE_CHAR, 200)
		isapinfo.addParm(rfcsi)
		isapinfo.encode()
		saprfcutil.call_receive_ex(self, isapinfo)
		isapinfo.decode()

		pos = 0
		for i in SYSINFO:
			p = parm(i["NAME"], None, RFCIMPORT, RFCTYPE_CHAR, i["LEN"])
			isapinfo.addParm(p)
			p.value = rfcsi.value[pos:pos+i["LEN"]]

			self.sysinfo[i["NAME"]] = rfcsi.value[pos:pos+i["LEN"]]
			pos += i["LEN"]

		#if DEBUG == True:
		#	for k in self.sysinfo.keys():
		#		print "%15s : %s" %(k, self.sysinfo[k])
		isapinfo.decode()
		return isapinfo

	def discover(self, name):
		"""
		Fonction de detection automatique des paramètres IMPORT EXPORT d'une fonction
		"""
		if self.is_connected() == 0:
			raise NameError, "RFC is NOT connected for interface discovery!"
		info = self.sapinfo()

		isapiface = iface("RFC_GET_FUNCTION_INTERFACE_P")
		efuncname = parm(name = "FUNCNAME",
						structure = "",
						type = RFCEXPORT,
						intype = RFCTYPE_CHAR,
						len = len(name),
						decimals = 0,
						py_value = name.upper(),
						default = "")
		isapiface.addParm(efuncname)

		tparams = tab("PARAMS_P")
		for i in range(25):
			table_row = struct(name="LIGNE%d" %(i))
			table_row.__add__( parm(name="type",
											structure="",
											type=RFCEXPORT,
											intype=RFCTYPE_CHAR,
											len=1,
											decimals=0,
											py_value="",
											default="err_default" ))
			table_row.__add__( parm(name="name",
											structure="",
											type=RFCEXPORT,
											intype=RFCTYPE_CHAR,
											len=30,
											decimals=0,
											py_value="",
											default="err_default" ))
			table_row.__add__( parm(name="tabname",
											structure="",
											type=RFCEXPORT,
											intype=RFCTYPE_CHAR,
											len=30,
											decimals=0,
											py_value="",
											default="err_default" ))
			table_row.__add__( parm(name="field",
											structure="",
											type=RFCEXPORT,
											intype=RFCTYPE_CHAR,
											len=30,
											decimals=0,
											py_value="",
											default="err_default" ))
			table_row.__add__( parm(name="datatype",
											structure="",
											type=RFCEXPORT,
											intype=RFCTYPE_CHAR,
											len=1,
											decimals=0,
											py_value="",
											default="err_default" ))
			table_row.__add__( parm(name="pos",
											structure="",
											type=RFCEXPORT,
											intype=RFCTYPE_CHAR,
											len=4,
											decimals=0,
											py_value="",
											default="err_default" ))
			table_row.__add__( parm(name="off",
											structure="",
											type=RFCEXPORT,
											intype=RFCTYPE_CHAR,
											len=6,
											decimals=0,
											py_value="",
											default="err_default" ))
			table_row.__add__( parm(name="intlen",
											structure="",
											type=RFCEXPORT,
											intype=RFCTYPE_CHAR,
											len=6,
											decimals=0,
											py_value="",
											default="err_default" ))
			table_row.__add__( parm(name="decs",
											structure="",
											type=RFCEXPORT,
											intype=RFCTYPE_CHAR,
											len=6,
											decimals=0,
											py_value="",
											default="err_default" ))
			table_row.__add__( parm(name="default",
											structure="",
											type=RFCEXPORT,
											intype=RFCTYPE_CHAR,
											len=21,
											decimals=0,
											py_value="",
											default="err_default" ))
			table_row.__add__( parm(name="text",
											structure="",
											type=RFCEXPORT,
											intype=RFCTYPE_CHAR,
											len=79,
											decimals=0,
											py_value="",
											default="err_default" ))
			table_row.__add__( parm(name="rem",
											structure="",
											type=RFCEXPORT,
											intype=RFCTYPE_CHAR,
											len=1,
											decimals=0,
											py_value="",
											default="err_default" ))
			tparams.__add__(table_row)

		isapiface.addParm(tparams)
		isapiface.encode()
		if saprfcutil.call_receive(self, isapiface) == 0:
			raise NameError, "failed on RFC_GET_FUNCTION_INTERFACE_P"
		isapiface.decode()
		return isapiface

		if re.compile("^[4-9]\d\w").match(info["RFCSAPRL"]):
			regex = "1s 30s 30s 30s 1s 4s 6s 6s 6s 21s 79s 1s"
		else:
			regex = "1s 30s 10s 10s 1s 4s 6s 6s 6s 21s 79s"
		if self.trace > 0:
			print regex
		for row in tparams.value:
			if len(row) == 215:
				type, name, tabname, field, datatype, pos, off, intlen, decs, default, text, rem  = unpack( regex, row )
			else:
				type, name, tabname, field, datatype, pos, off, intlen, decs, default, text  = unpack( regex, row )
			name = name.strip()
			tabname = tabname.strip()
			field = field.strip()
			intlen = int( intlen )
			decs = int( decs )
			reResult = re.compile("^\"(.*?)\"\s*$").search(default)
			if reResult:
				default = reResult.group(0)
			else:
				reResult = re.compile("^SY\-(\w+)\W*$").search(default)
				if reResult:
					default = "RFC" + reResult.group(0)
					if info[default]:
						default = info[default]
					else:
						default = ""

			structure = ""
			if datatype == "C":
			# Character
				datatype = RFCTYPE_CHAR
				if re.compile("^SPACE\s*$").search(default):
					default = " "
			elif datatype == "X":
			# Hex
				datatype = RFCTYPE_BYTE
				if default:
					default = "%*X" % intlen, default
			elif datatype == "I":
			# Integer
				datatype = RFCTYPE_INT
				if re.compile("^\s+$").match(default):
					default = 0
				else:
					default = int(default)
				intlen = 4
			elif datatype == "s":
			# Short Integer
				datatype = RFCTYPE_INT2
				if re.compile("^\s+$").match(default):
					default = 0
				else:
					default = int(default)
				intlen = 2
			elif datatype == "b":
			# Very Short Integer
				datatype = RFCTYPE_INT1
				if re.compile("^\s+$").match(default):
					default = 0
				else:
					default = int(default)
				intlen = 1
			elif datatype == "D":
			# Date
				datatype = RFCTYPE_DATE
				default = "00000000"
				intlen = 8
			elif datatype == "T":
			# Time
				datatype = RFCTYPE_TIME
				default = "000000"
				intlen = 6
			elif datatype == "P":
			# Binary Coded Decimal eg. CURR QUAN etc
				datatype = RFCTYPE_BCD
			elif datatype == "N":
			#  Numchar
				datatype = RFCTYPE_NUM
				if default == 0 or re.compile("^[0-9]+$").search(default):
					default = sprintf("%0"+intlen+"d", default)
			elif datatype == "F":
			#  Float
				datatype = RFCTYPE_FLOAT
				intlen = 8
			# new style
			elif (datatype == "u" or datatype == "h" or datatype == " " or datatype == "" ) and field == "" and type != "X":
				structure = self.structure( tabname )
				datatype = RFCTYPE_BYTE
			else:
			# Character
				datatype = RFCTYPE_CHAR
				if re.compile("^SPACE\s*$").match(default):
					default = " "
				if datatype == "":
					datatype = RFCTYPE_CHAR

			if type == "I":
			#  Export Parameter - Reverse perspective
				eparam = parm(name, structure, RFCEXPORT, datatype, intlen, decs, default, default)
				interface.addParm(eparam)
			elif type == "E":
			#  Import Parameter - Reverse perspective
				iparam = parm(name, structure, RFCIMPORT, datatype, intlen, decs, "", "")
				interface.addParm(iparam)
			elif type == "T":
			#  Table
				tparam = tab(name, structure, intlen)
				interface.addParm(tparam)
			else:
			# This is an exception definition
				interface.addException( name )

		del efuncname
		del tparams
		del isapiface
		return interface

	def structure(self, strt):
		"""
		discover utilise cette fonction pour intéroger SAP avec la fonction RFC_GET_STRUCTURE_DEFINITION_P
		et connaitre le format d'une stucture
		"""
		if self.is_connected() == 0:
			raise NameError, "RFC is NOT connected for structure discovery!"
		info = self.sapinfo()
		isapstruct = iface("RFC_GET_STRUCTURE_DEFINITION_P")
		etabname = parm("TABNAME", "", RFCEXPORT, RFCTYPE_CHAR, len(strt), 0, strt.upper())
		isapstruct.addParm(etabname)

		tparams = tab("FIELDS", "", 83)
		isapstruct.addParm(tparams)
		if saprfcutil.call_receive(self, isapstruct) == 0:
			raise NameError, "failed on RFC_GET_STRUCTURE_DEFINITION_P"
		s = struct(strt)
		# record structure changes from 3.x to 4.x
		if re.compile("^[4-9]\d\w").match(info["RFCSAPRL"]):
			regex = "30s 30s 4s 6s 6s 6s 1s"
		else:
			regex = "10s 10s 4s 6s 6s 6s 1s"
		for row in tparams.value:
			tabname, fld, pos, off, intlen, decs, exid  = unpack( regex, row )
			s.addField( field(fld, exid, decs, intlen, off) )
		del etabname
		del isapstruct
		return s

	def convtype(self, datatype):
		"""
		Fonction de convertion de type de donnée : saprfc => SAP
		"""
		if datatype == RFCTYPE_CHAR:
			# Character
			return "C"
		elif datatype == RFCTYPE_BYTE:
			# Integer
			return "X"
		elif datatype == RFCTYPE_INT:
			# Hex
			return "I"
		elif datatype == RFCTYPE_INT1:
			# Very Short Integer
			return "b"
		elif datatype == RFCTYPE_INT2:
			# Short Integer
			return "s"
		elif datatype == RFCTYPE_DATE:
			# Date
			return "D"
		elif datatype == RFCTYPE_TIME:
			# Time
			return "T"
		elif datatype == RFCTYPE_BCD:
			# Binary Coded Decimal eg. CURR QUAN etc
			return "P"
		elif datatype == RFCTYPE_NUM:
			#  Numchar
			return "N"
		elif datatype == RFCTYPE_FLOAT:
			#  Float
			return "F"
		else:
			# Character
			return "C"

	def accept(self, callback=None, wait=0):
		if self.tpname == None or self.gwhost == None or self.gwserv == None:
			raise NameError, "RFC - must have tpname, gwhost, and gwserv set to register RFC server"
		self.wait = wait
		self.callback = callback
		conn = "-a " + self.tpname + " -g " + self.gwhost + " -x " + self.gwserv
		if self.trace > 0:
			conn += " -t "
		self.connstr = conn
		s_docu = ""
		for ifc in self.ifaces:
			s_docu += "Function Name: " + ifc.name + "\nIMPORTING\n"
			for p in ifc.parms:
				if p.type == RFCIMPORT:
					s_docu += "		" + "%-30s" % p.name + self.convtype(p.intype) + "(" + str(p.len) + ")\n"
			s_docu += "EXPORTING\n"
			for p in ifc.parms:
				if p.type == RFCEXPORT:
					s_docu += "		" + "%-30s" % p.name + self.convtype(p.intype) + "(" + str(p.len) + ")\n"
			s_docu += "TABLES\n"
			for p in ifc.parms:
				if p.type == RFCTABLE:
					s_docu += "		" + "%-30s" % p.name + "C(" + str(p.len) + ")\n"
			s_docu += "\n"
		docu = []
		for i in s_docu.split("\n"):
			docu.append("%-80s" % i)
		self.docu = docu
		return saprfcutil.accept(self)

	def callrfc(self, ifc):
		"""
		Execution d'une fonction RFC définie par iface avec parametre import et export
		Utilisation de RfcCallReceive()
		"""
		if self.is_connected() == 0:
			raise NameError, "RFC is NOT connected for rfc call!"
		err = saprfcutil.call_receive(self, ifc)
		if err == 0:
			raise NameError, "failed on " + ifc.name
		else:
			return err

	def callrfc_ex(self, ifc):
		"""
		Execution d'une fonction RFC définie par iface avec parametre import export changing et table
		Utilisation de RfcCallReceiveEx()
		"""
		if self.is_connected() == 0:
			raise NameError, "RFC is NOT connected for rfc call!"
		err = saprfcutil.call_receive_ex(self, ifc)
		if err == 0:
			raise NameError, "failed on " + ifc.name
		elif err < 0:
			raise NameError, "failed on %s : %d" %(ifc.name, err)
		else:
			return err

	def close(self):
		"""
		Fermiture de la connection SAP
		"""
		return saprfcutil.close(self.connection)

	def get_ticket(self):
		return saprfcutil.get_ticket(self.connection)



class iface(object):
	"""
	Declaration d'une fonction RFC dans saprfc
	"""
	def __init__(self, name, callback=None):
		self.name = name.upper().strip()
		self.parms = []
		self.parmsindex = {}
		self.exceptions = []
		self.callback = callback
		self.error = None
	def __getattr__(self, key):
		if type(key) == IntType:
			self.parms[key]
		else:
			return self.parmsindex[key]
	def addParm(self, parm):
		"""
		Ajoute un parametre RFCIMPORT, RFCEXPORT, RFCTABLE d'échange entre SAP et saprf
		"""
		self.parms.append(parm)
		self.parmsindex.update({parm.name : parm})
		return
	def addException(self, excep):
		self.exceptions.append(excep)
	def handler(self, srfc):
		self.error = None
		return self.callback.handler(self)
	def encode(self, trace=0):
		if trace == 1:
			print "Encodage/Formatage des données"
		for p in self.parms:
			p.encode(trace=trace)
		return
	def decode(self, trace=0):
		if trace == 1:
			print "Decodage/Formatage des données"
			print self
			print type(self.parms)
			print self.parms
		for p in self.parms:
			if trace == 1:
				print p
			p.decode()
		return
	def reset(self):
		for p in self.parms:
			p.reset()
		return
	def __repr__(self):
		return "Class type iface : %s" %(self.name)
	def __str__(self):
		return "Class type iface : %s" %(self.name)
	def __unicode__(self):
		return "Class type iface : %s" %(self.name)



class parm(object):
	"""
	Définit un parametre RFCIMPORT, RFCEXPORT, RFCTABLE, RFCCHANGE d'échange entre SAP et saprf
		ATTENTION RFCIMPORT et RFCEXPORT sont point de vue saprfc
			le variable export sap sont des RFCIMPORT
			le variable import sap sont des RFCEXPORT
	value : string représentation binaire de la donnée ( format SAP )
	py_value : représentation pythonique de la donnée
	"""
	def __init__(self, name, structure, type, intype, len=0, decimals=0, py_value="", default="",prefix=None, suffix=None):
		self.name = name.upper().strip()
		self.structure = structure
		self.type = type
		self.intype = int(intype)
		if RFC_TYPE_SPEC[self.intype]["len"] != None:
			self.len = RFC_TYPE_SPEC[self.intype]["len"]
		else:
			self.len = len
		self.len = len
		self.decimals = decimals
		self.py_value = py_value
		self.value = ""
		self.default = default
		self.prefix = prefix
		self.suffix = suffix
	def __setattr__(self, attr, val):
		self.__dict__[attr] = val
		return
	def __getattr__(self, attr):
		return self.__dict__[attr]
	def hextranslate(self, s):
		res = ""
		neg = None
		if type(s) == IntType:
			if s < 0:
				str_s = str(s)[1:]
				neg = True
			else:
				str_s = str(s)
				neg = False
		elif type(s) == StringType:
			str_s = s.replace(" ", "")
			if str_s.startswith("-"):
				str_s = str_s[1:]
				neg = True
			else:
				neg = False
		else:
			raise ValueError("s is not an int or a string")
#		for i in range(len(str_s)/2):
#			realIdx = i*2
#			res = res + chr(int(str_s[realIdx:realIdx+2],16))
		realIdx = 0
		while realIdx < len(str_s):
			res = res + chr(int(str_s[realIdx:realIdx+2],16))
			realIdx += 2
		if neg == True:
			res += "\x0d"
		if neg == False:
			res += "\x0c"
		return res
	def unhex(self, s):
		res = ""
		neg = None
		if s.endswith("\x0d"):
			neg = True
			str_s = s[:-1]
		elif s.endswith("\x0c"):
			neg = False
			str_s = s[:-1]
		else:
			str_s = s
#		for i in range(len(str_s)):
#			res += "%x" %(ord(str_s[i]))
		i = 0
		while i < len(str_s):
			res += "%02x" %(ord(str_s[i]))
			i += 1
		if neg == True:
			if self.decimals == 0:
				return int(res)*-1
			else:
				return int(res)*-1/10**self.decimals
		if neg == False:
			if self.decimals == 0:
				return int(res)
			else:
				return int(res)/10**self.decimals
		return None
	def setValue(self, val):
		self.py_value = val
		self.encode()
		return
	def getValue(self):
		self.decode()
		return self.py_value
	def encode(self, trace=0):
		"""
		Encodage format RFC-SAP ( Python => SAP )
		"""
		if self.py_value == None:
			raise ValueError("py_value can not be None")
		elif self.py_value == "":
			if RFC_TYPE_SPEC[self.intype]["init"] != None:
				self.value = RFC_TYPE_SPEC[self.intype]["init"] * self.len
			else:
				self.value = ""
		else:
			if trace == 1:
				print "pack %s methode \"%s\" : %s(%s) ... " %(self.name, RFC_TYPE_SPEC[self.intype]["pack_type"], self.py_value, type(self.py_value))
			if RFC_TYPE_SPEC[self.intype]["pack_type"] != None:
				if type(self.py_value) == UnicodeType:
					if RFC_TYPE_SPEC[self.intype]["pack_type"] == "bcd":
						self.value = self.hextranslate(str(self.py_value))
					else:
						self.value = pack(RFC_TYPE_SPEC[self.intype]["pack_type"], str(self.py_value))
				else:
					if RFC_TYPE_SPEC[self.intype]["pack_type"] == "bcd":
						self.value = hextranslate(self.py_value)
					else:
						self.value = pack(RFC_TYPE_SPEC[self.intype]["pack_type"], self.py_value)
			elif RFC_TYPE_SPEC[self.intype]["datetime"] != None:
				self.value = self.py_value.strftime(RFC_TYPE_SPEC[self.intype]["datetime"])
			else:
				self.value = str(self.py_value).encode("latin_1", "replace")

		if self.prefix != None:
			self.value = self.prefix*(self.len-len(self.py_value)) + self.py_value
		elif self.suffix != None:
			self.value = self.py_value + self.suffix*(self.len-len(self.py_value))

		if len(self.value) < self.len:
			if trace == 1:
				print "Ajustement de longueur de %s : %d => %d" %(self.name, self.len, len(self.value))
			self.len = len(self.value)
		elif len(self.value) > self.len:
			print "Ajustement de longueur de %s : %d => %d" %(self.name, self.len, len(self.value))
			self.value = self.value[:self.len]

		if trace == 1:
			print "%s '%s' => '%s'" %(self.name, self.py_value, self.value)
		return
	def decode(self, trace=0):
		"""
		Decodage format RFC-SAP ( SAP => Python )
		Prend value et le convertie en objet python et place le résultat dans py_value
		"""
		if trace == 1:
			print "name %s methode \"%s\" value  \"%s\"(%s) %s ... " %(self.name, RFC_TYPE_SPEC[self.intype]["pack_type"], self.value, type(self.py_value), self.intype)
		if RFC_TYPE_SPEC[self.intype]["pack_type"] != None:
			if self.value == "" or self.value.replace(" ","") == "":
				if RFC_TYPE_SPEC[self.intype]["pack_type"] == "d":
					self.py_value = None
				elif RFC_TYPE_SPEC[self.intype]["pack_type"] == "s":
					self.py_value = ""
				elif RFC_TYPE_SPEC[self.intype]["pack_type"] == "bcd":
					self.py_value = ""
				else:
					self.py_value = None
			else:
				if RFC_TYPE_SPEC[self.intype]["pack_type"] == "bcd":
					self.py_value = self.unhex(self.value)
				else:
					self.py_value = unpack(RFC_TYPE_SPEC[self.intype]["pack_type"], self.value)
		elif RFC_TYPE_SPEC[self.intype]["datetime"] != None:
			self.py_value = datetime.datetime.strptime(self.value, RFC_TYPE_SPEC[self.intype]["datetime"])
		else:
			self.py_value = self.value.decode("latin_1", "replace").strip()
		if trace == 1:
			print "'%s'" %(self.py_value)
		return
	def reset(self):
		self.py_value = self.default
		return
	def __repr__(self):
		return "Class type parm : %s('%s')" %(self.name, str(self.value))
	def __str__(self):
		return "Class type parm : %s(%s)" %(self.name, self.py_value)
	def __unicode__(self):
		return "Class type parm : %s(%s)" %(self.name, self.py_value)



class struct(object):
	"""
	Défini la stucture d'une ligne d'une table
	name : nom de la stucture
	fields : liste de champs de la stucture de type param
	value : represantation de la structure géréré par encode
	"""
	def __init__(self, name):
		self.name = name.upper()
		self.fields = []
		self.fieldsindex = {}
		self.value = ""
		self.len = 0
		return
	def __getattr__(self, attr):
		return self.__dict__[attr]
	def __setattr__(self, attr, val):
		self.__dict__[attr] = val
		return
	def __getitem__(self, key):
		"""
		renvoie un élément de la stucture en l'appelant par son N°
		"""
		if type(key) == IntType:
			return self.fields[key]
		else:
			return self.fields[self.parmsindex[key]]
	def __add__(self, field):
		"""
		field est un objet de type param
		"""
		self.fields.append(field)
		self.fieldsindex.update({field.name : field})
		self.len += field.len
		return
	def encode(self, trace=0):
		"""
		encode la valeur des champs et place le résultat dans value
		"""
		self.value = ""
		for v in self.fields:
			v.encode()
			self.value += v.value
		self.len = len(self.value)
		return
	def decode(self, trace=0):
		"""
		decode le champ value et place le résutat dans les champs correspondant
		"""
		if trace == 1:
			print self.value
			print self.fields

		pos = 0
		for v in self.fields:
			v.value = self.value[pos:pos+v.len]
			v.decode()

			if trace == 1:
				print unicode(v), type(v)
			pos += v.len
		return
	def reset(self):
		for v in self.fields:
			v.reset()
		return
	def __repr__(self):
		return "Class type struct : %s" %(self.name)
	def __str__(self):
		return "Class type struct : %s" %(self.name)
	def __unicode__(self):
		return "Class type struct : %s" %(self.name)



class tab(object):
	"""
	Class de description d'un table d'échange type RFCTABLE
	"""
	def __init__(self, name):
		"""
		Initialisation de la table
		"""
		self.name = name.upper().strip()
		self.structure = []
		self.value = []
		self.type = RFCTABLE
		self.intype = RFCTYPE_BYTE
		self.len = 0
	def __getattr__(self, attr):
		return self.__dict__[attr]
	def __setattr__(self, attr, val):
		self.__dict__[attr] = val
		return
	def __getitem__(self, key):
		"""
		renvoie un élément de la stucture en l'appelant par son N°
		"""
		return self.structure[key]
	def __add__(self, val):
		self.structure.append(val)
		return
	def encode(self, trace=0):
		self.value = []
		for s in self.structure:
			s.encode()
			self.value.append(s.value)
		self.len_of_data()
		return
	def decode(self, trace=0):
		if trace == 1:
			print self.value
			print self.structure, type(self.structure)
			print len(self.structure), len(self.value)

		while len(self.structure) > len(self.value):
			if trace == 1:
				print "self.value trop petit"
			self.value.append("")
		while len(self.structure) < len(self.value):
			if trace == 1:
				print "self.structure trop petit"
			self.structure.append(copy.copy(self.structure[-1]))
		for s in range(len(self.structure)):
			if trace == 1:
				print self.structure[s]
			self.structure[s].value = self.value[s]
			self.structure[s].decode()
		return
	def len_of_data(self):
		self.len = 0
		for v in self.value:
			self.len += len(v)
		return
	def reset(self):
		for s in self.structure:
			s.reset()
		return
	def __repr__(self):
		return "Class type tab : %s" %(self.name)
	def __str__(self):
		return "Class type tab : %s" %(self.name)
	def __unicode__(self):
		return "Class type tab : %s" %(self.name)








#class field(object):
#
#	def __init__(self, name, intype, decimals, len, offset):
#		self.name = name.upper().strip()
#		self.value = ""
#		self.decimals = int(decimals)
#		self.intype = intype
#		self.len = int(len)
#		self.offset = int(offset)
#		self.position = 0
#
#	def hextranslate(self, s):
#		res = ""
#		for i in range(len(s)/2):
#			realIdx = i*2
#			res = res + chr(int(s[realIdx:realIdx+2],16))
#		return res
#
#	def unhex(self, s):
#		res = ""
#		for i in range(len(s)):
#			bit = "%02x" % int(ord(s[i]))
#			res = res +  bit
#		return res
#	def __str__(self):
#		return "Class type field, sap_type : %s ; %s=%s" %(self.intype, self.name, self.value)
#	def __unicode__(self):
#		return "Class type field, sap_type : %s ; %s=%s" %(self.intype, self.name, self.value)
#

