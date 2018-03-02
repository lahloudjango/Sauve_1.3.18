# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Python utils for RFC calls to SAP R/3
Ce module nécessite les librairie :
libsapnwrfc.so
"""

import sys
import saprfcutil
from struct import *
from string import *
import re
from types import *

__author__ = "Charly GONTERO"
__date__ = "2015-09-16 13:55:00"
__version__ = 1.2
#correction de la fonction unhex

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


RFCIMPORT	 = 0
RFCEXPORT	 = 1
RFCTABLE	  = 2

RFCTYPE_CHAR  = 0
RFCTYPE_DATE  = 1
RFCTYPE_BCD   = 2
RFCTYPE_TIME  = 3
RFCTYPE_BYTE  = 4
RFCTYPE_NUM   = 6
RFCTYPE_FLOAT = 7
RFCTYPE_INT   = 8
RFCTYPE_INT2  = 9
RFCTYPE_INT1  = 10

# Valid data types for fields
CHARTYPE = {
	"C": RFCTYPE_CHAR,
	"X": RFCTYPE_BYTE,
	"B": RFCTYPE_INT1,
	"S": RFCTYPE_INT,
	"P": RFCTYPE_BCD,
	"D": RFCTYPE_DATE,
	"T": RFCTYPE_TIME,
	"N": RFCTYPE_NUM,
	"F": RFCTYPE_FLOAT,
	"I": RFCTYPE_INT,
	}

# sysinfo structure size
SYSINFO = [
	{ "NAME": "RFCPROTO",   "LEN": 3 },
	{ "NAME": "RFCCHARTYP", "LEN": 4 },
	{ "NAME": "RFCINTTYP",  "LEN": 3 },
	{ "NAME": "RFCFLOTYP",  "LEN": 3 },
	{ "NAME": "RFCDEST",	"LEN": 32 },
	{ "NAME": "RFCHOST",	"LEN": 8 },
	{ "NAME": "RFCSYSID",   "LEN": 8 },
	{ "NAME": "RFCDATABS",  "LEN": 8 },
	{ "NAME": "RFCDBHOST",  "LEN": 32 },
	{ "NAME": "RFCDBSYS",   "LEN": 10 },
	{ "NAME": "RFCSAPRL",   "LEN": 4 },
	{ "NAME": "RFCMACH",	"LEN": 5 },
	{ "NAME": "RFCOPSYS",   "LEN": 10 },
	{ "NAME": "RFCTZONE",   "LEN": 6 },
	{ "NAME": "RFCDAYST",   "LEN": 1 },
	{ "NAME": "RFCIPADDR",  "LEN": 15 },
	{ "NAME": "RFCKERNRL",  "LEN": 4 },
	{ "NAME": "RFCHOST2",   "LEN": 32 },
	{ "NAME": "RFCSI_RESV", "LEN": 12 },
]

class conn:
	"""
	The main connection class for creating an RFC connection object
	"""

	def __init__(self, ashost="localhost", sysnr=00, lang="EN", client=000, r3name=None,  user=None, passwd=None, getsso2=0, mysapsso2=None, x509cert=None, gwhost=None, gwserv=None, tpname=None, trace=1, trfc=None):
		"""
		The constructor.  Takes the rfc library connection parameters are arguments
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
		self.trfc = trfc
		self.sysinfo = {}
		self.ifacesindex = {}
		self.ifaces = []

	def iface(self, ifc):
		self.ifaces.append(ifc)
		self.ifacesindex[ifc.name] = ifc
		return ifc

	def connect(self):
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
		iping = iface("RFC_PING")
		return saprfcutil.call_receive(self, iping)

	def sapinfo(self):
		if len(self.sysinfo) > 0:
			return self.sysinfo
		isapinfo = iface("RFC_SYSTEM_INFO")
		rfcsi = parm("RFCSI_EXPORT", "", RFCIMPORT, RFCTYPE_CHAR, 200)
		isapinfo.addParm(rfcsi)
		if saprfcutil.call_receive(self, isapinfo) == 0:
			raise NameError, "failed on RFC_SYSTEM_INFO"
		pos = 0
		for field in SYSINFO:
			self.sysinfo[field["NAME"]] = rfcsi.value[pos:pos+field["LEN"]] 
			pos += field["LEN"]
		return self.sysinfo


	def discover(self, name):
		if self.is_connected() == 0:
			raise NameError, "RFC is NOT connected for interface discovery!"
		info = self.sapinfo()
		isapiface = iface("RFC_GET_FUNCTION_INTERFACE_P")
		efuncname = parm("FUNCNAME", "", RFCEXPORT, RFCTYPE_CHAR, len(name), 0, name.upper())
		isapiface.addParm(efuncname)
		tparams = tab("PARAMS_P", "", 215)
		isapiface.addParm(tparams)
		if saprfcutil.call_receive(self, isapiface) == 0:
			raise NameError, "failed on RFC_GET_FUNCTION_INTERFACE_P"

		interface = iface(name)

		if re.compile("^[4-9]\d\w").match(info["RFCSAPRL"]):
			regex = "1s 30s 30s 30s 1s 4s 6s 6s 6s 21s 79s 1s"
		else:
			regex = "1s 30s 10s 10s 1s 4s 6s 6s 6s 21s 79s"
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
# if the character value default is in quotes - remove quotes
			reResult = re.compile("^\"(.*?)\"\s*$").search(default)
			if reResult:
				default = reResult.group(0)
# if the value is an SY- field - we have some of them in sapinfo
			else:
				reResult = re.compile("^SY\-(\w+)\W*$").search(default)
				if reResult:
					default = "RFC" + reResult.group(0)
					if info[default]:
						default = info[default]
					else:
						default = ""
#			if re.compile("^\"(.*?)\"\s*$").search(default):
#				default = group(0)
## if the value is an SY- field - we have some of them in sapinfo
#			elif re.compile("^SY\-(\w+)\W*$").search(default):
#				default = "RFC" + group(0)
#				if info[default]:
#					default = info[default]
#				else:
#					default = ""

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
		if self.is_connected() == 0:
			raise NameError, "RFC is NOT connected for rfc call!"

#		print "inside callrfc - going to call_receive ...\n"
		if saprfcutil.call_receive(self, ifc) == 0:
			raise NameError, "failed on " + ifc.name

#		print "got back again \n"



	def close(self):
		return saprfcutil.close(self.connection)


	def get_ticket(self):
		return saprfcutil.get_ticket(self.connection)


class iface:

	def __init__(self, name, callback=None):
		self.name = name.upper().strip()
		self.parms = []
		self.parmsindex = {}
		self.exceptions = []
		self.callback = callback
		self.error = None

	def __getattr__(self, name):
		if name.upper() == "__STR__":
			return self.name()
		elif name.upper() == "__REPR__":
			return self.name()
		elif self.parmsindex.has_key(name.upper()):
			return self.parmsindex[name.upper()]
		else:
			return None 

	def addParm(self, parm):
		self.parms.append(parm)
		self.parmsindex[parm.name] = parm

	def addException(self, excep):
		self.exceptions.append(excep)

	def handler(self, srfc):
		self.error = None
		return self.callback.handler(self)
	
	def reset(self):
		for p in self.parms:
			p.reset()


class parm:

	def __init__(self, name, structure, type, intype, len=0, decimals=0, value="", default=""):
		self.name = name.upper().strip()
		self.structure = structure
		self.value = value
		self.type = type
		self.intype = int(intype)
		if self.intype == RFCTYPE_DATE:
			self.len = 8
		elif self.intype == RFCTYPE_TIME:
			self.len = 6
		else:
			self.len = int(len)
		self.decimals = int(decimals)
		if self.type == RFCEXPORT:
			self.setValue( value )
			self.default = default
		self.changed = 0


	def hextranslate(self, s):
		res = ""
		for i in range(len(s)/2):
			realIdx = i*2
			res = res + chr(int(s[realIdx:realIdx+2],16))
		return res


	def unhex(self, s):
		res = ""
#		print "unhex_param"+s
		for i in range(len(s)):
			bit = "%02x" % int(ord(s[i]))
			res = res +  bit
		return res


	def setValue(self, val):
		if self.intype == RFCTYPE_BCD:
			if type(val) == StringType:
				if re.compile("^\s+([\s\-\+]\d+(\.\d+)?)\s+?$").match(val):
					val = float(group(0))
				else:
					val = float(0)
			elif type(val) == IntType or type(val) == FloatType or type(val) == LongType:
				val = float(val)
			else:
				val = float(0)
			format = "%0" + repr(((self.len*2) + 1)) + "." + repr(self.decimals) + "f"
			val = format % val

			val = replace(val, ".","")
			if val[0] == "-":
				val += "d"
			else:
				val += "c"
			val = val[1:]
			self.value = self.hextranslate(val)

		elif self.intype == RFCTYPE_FLOAT:
			if val == None or type(val) == StringType and re.compile("^(\s+)?$").match(val): val = 0
			self.value = pack("d", float(val))
			self.len = 8

		elif self.intype == RFCTYPE_INT:
			self.value = pack("l", int(val))
			self.len = 4

		elif self.intype == RFCTYPE_INT2:
			self.value = pack("h", int(val))
			self.len = 2

		elif self.intype == RFCTYPE_INT1:
			self.value = pack("b", int(val))
			self.len = 1

		elif self.intype == RFCTYPE_NUM:
			self.value = zfill(val, self.len) 

		elif self.intype == RFCTYPE_DATE:
			self.value = str(val) 
			self.len = 8

		elif self.intype == RFCTYPE_TIME:
			self.value = str(val) 
			self.len = 6

		else:
			self.value = val
			self.len = len(self.value)

		return self.value



	def getValue(self):
		if self.intype == RFCTYPE_BCD:
			val = self.unhex(self.value)
			if val[-1] == "d":
				val = "-" + val[0:-1]
			else:
				val = val[0:-1]
			if self.decimals != 0:
				val = val[0:(len(val) - self.decimals)] + "." + val[(len(val) - self.decimals):len(val)]
			return val

		elif self.intype == RFCTYPE_FLOAT:
			return unpack("d", self.value)[0]

		elif self.intype == RFCTYPE_INT:
			return unpack("l", self.value)[0]

		elif self.intype == RFCTYPE_INT2:
			return unpack("h", self.value)[0]

		elif self.intype == RFCTYPE_INT1:
			return unpack("b", self.value)[0]

		elif self.intype == RFCTYPE_NUM:
			return self.value

		else:
			return self.value

	def reset(self):
		self.value = self.default


class tab:

	def __init__(self, name, structure, len, value=[]):
		self.name = name.upper().strip()
		self.structure = structure
		self.value = value
		self.type = RFCTABLE
		self.intype = RFCTYPE_BYTE
		self.len = int(len)
		self.changed = 0

	def setValue(self, val):
		self.value = []
		for row in val:
			self.value.append(row.ljust(self.len))

	def rowCount(self):
		return len(self.value)

	def hashRows(self):
		while len(self.value) > 0:
			i = self.value.pop(0)
			yield self.structure.toHash(i)

	def empty(self):
		return self.reset()

	def reset(self):
		self.value = []
		return self.value



class struct:

	def __init__(self, name):
		self.name = name.upper().strip()
		self.fields = []
		self.fieldsindex = {}
		self.value = ""
		self.positions = 0

	def __getattr__(self, name):
		if name.upper() == "__STR__":
			return self.name()
		elif name.upper() == "__REPR__":
			return self.name()
		elif self.fieldsindex.has_key(name.upper()):
			return self.fieldsindex[name.upper()]
		else:
			return None 

	def addField(self, fld):
		fld.position = self.positions = self.positions + 1
		self.fields.append(fld)
		self.fieldsindex[fld.name] = fld

	def getField(self, field):
		if self.fieldsindex.has_key(field.upper()):
			self.fieldsindex[field.upper()]
		else:
			return None

	def pack(self):
		str = ""
		for fld in self.fields:
			val = fld.value
			if fld.intype == RFCTYPE_BCD:
				if type(val) == StringType:
					if re.compile("^\s+([\s\-\+]\d+(\.\d+)?)\s+?$").match(val):
						val = float(group(0))
					else:
						val = float(0)
				elif type(val) == IntType or type(val) == FloatType or type(val) == LongType:
					val = float(val)
				else:
					val = float(0)
				format = "%0" + repr(((fld.len*2) + 1)) + "." + repr(fld.decimals) + "f"
				val = format % val

				val = replace(val, ".","")
				if val[0] == "-":
					val += "d"
				else:
					val += "c"
				val = val[1:]
				val = fld.hextranslate(val)

			elif fld.intype == RFCTYPE_FLOAT:
				if val == None or type(val) == StringType and re.compile("^(\s+)?$").match(val): val = 0
				val = pack("d", float(val))

			elif fld.intype == RFCTYPE_INT:
				val = pack("l", int(val))

			elif fld.intype == RFCTYPE_INT2:
				val = pack("h", int(val))

			elif fld.intype == RFCTYPE_INT1:
				val = pack("b", int(val))

			elif fld.intype == RFCTYPE_NUM:
				val = zfill(val, fld.len) 

			else:
				val = val.ljust(fld.len)

			str += val
		return str


	def unpack(self):
		hash = self.toHash(self.value)
		for fld in self.fields:
			fld.value = hash[fld.name]
		return hash


	def toHash(self, val):
		hash = {}
		fmt = ""
		for fld in self.fields:
			fmt += " " + repr(fld.len) + "s"
		if len(val) < calcsize(fmt):
			val = val.ljust(calcsize(fmt))
		else:
			val = val[0:calcsize(fmt)]
		flds = []
		flds = list( unpack( fmt, val ) )
		value = ""
		for fld in self.fields:
			fldval = flds.pop(0)
			if fld.intype == RFCTYPE_BCD:
				value = fld.unhex(fldval)
				if value[-1] == "d":
					value = "-" + value[0:-1]
				else:
					value = value[0:-1]
				if fld.decimals != 0:
					value = value[0:(len(value) - fld.decimals)] + "." + value[(len(value) - fld.decimals):len(value)]
			elif fld.intype == RFCTYPE_FLOAT:
				value = unpack("d", fldval)[0]

			elif fld.intype == RFCTYPE_INT:
				value = unpack("l", fldval)[0]

			elif fld.intype == RFCTYPE_INT2:
				value = unpack("h", fldval)[0]

			elif fld.intype == RFCTYPE_INT1:
				value = unpack("b", fldval)[0]

			elif fld.intype == RFCTYPE_NUM:
				value = fldval

			else:
				value = fldval
			hash[fld.name] = value

		return hash

	def Value(self):
		self.value = self.pack()
		return self.value



class field:

	def __init__(self, name, intype, decimals, len, offset):
		self.name = name.upper().strip()
		self.value = ""
		self.decimals = int(decimals)
		self.intype = CHARTYPE[intype.upper()]
		self.len = int(len)
		self.offset = int(offset)
		self.position = 0


	def hextranslate(self, s):
		res = ""
		for i in range(len(s)/2):
			realIdx = i*2
			res = res + chr(int(s[realIdx:realIdx+2],16))
		return res


#	def unhex(self, s):
#		res = ""
#		for i in range(len(s)):
#			bit = "%x" % int(ord(s[i]))
#			res = res +  bit
#		return res

	def unhex(self, s):
		res = ""
#		print "unhex_field"+s
		for i in range(len(s)):
			bit = "%02x" % int(ord(s[i]))
			res = res +  bit
		return res
