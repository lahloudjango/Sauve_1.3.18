# -*- coding: utf-8 -*-

import ctypes

libname = "C:/TwinCAT/ADS Api/TcAdsDll/AdsDll.dll"

class struct_test(ctypes.Structure):
	"""Structure PLC
	"""
	_fields_ = [
				('var_dint', ctypes.c_int32),
				('var_byte', ctypes.c_int8),
				]


type_matching = {'int': ctypes.c_int,
				 'str': ctypes.c_char_p,
				 'float': ctypes.c_float,
				 'BYTE': ctypes.c_byte,
				 'WORD': ctypes.c_short,
				 'INT': ctypes.c_int,
				 'DINT': ctypes.c_long,
				 'DOUBLE': ctypes.c_double,
				}


class AmsAddr(ctypes.Structure):
	"""Addr ADS
	"""
	_fields_ = [
				('netid1', ctypes.c_ubyte),  #unsigned char b[6]
				('netid2', ctypes.c_ubyte),  #unsigned char b[6]
				('netid3', ctypes.c_ubyte),  #unsigned char b[6]
				('netid4', ctypes.c_ubyte),  #unsigned char b[6]
				('netid5', ctypes.c_ubyte),  #unsigned char b[6]
				('netid6', ctypes.c_ubyte),  #unsigned char b[6]
				('port', ctypes.c_ushort),
				]


erreur = ctypes.c_long()
port = ctypes.c_long()
offset = ctypes.c_ulong()
addr_ads = AmsAddr()
addr_ads.port = ctypes.c_ushort(801)
var_name = ctypes.c_char_p("test")


#dll_adsdll = ctypes.CDLL(libname)
dll_adsdll = ctypes.cdll.LoadLibrary(libname)
#librfc=ctypes.cdll.LoadLibrary('librfccm.so')
#libc=ctypes.cdll.LoadLibrary('/lib/libc.so.6')
#librfc=ctypes.windll.librfc32
#libc=ctypes.cdll.msvcrt

#dll_adsdll = ctypes.windll.AdsDll


test = struct_test()

test.var_dint = 5
test.var_byte = 11



port = dll_adsdll.AdsPortOpen();
print "port", port
erreur = dll_adsdll.AdsGetLocalAddress(ctypes.byref(addr_ads));
print erreur
print "addr_ads.netid1",addr_ads.netid1
print "addr_ads.netid2",addr_ads.netid2
print "addr_ads.netid3",addr_ads.netid3
print "addr_ads.netid4",addr_ads.netid4
print "addr_ads.netid5",addr_ads.netid5
print "addr_ads.netid6",addr_ads.netid6
print "addr_ads.port",addr_ads.port


erreur1 = dll_adsdll.AdsSyncReadWriteReq(ctypes.byref(addr_ads),
										0xF003,
										0x0,
										ctypes.sizeof(offset),
										ctypes.byref(offset),
										ctypes.sizeof(var_name),
										ctypes.byref(var_name),
										)
print erreur1
print "ctypes.byref(addr_ads)", ctypes.byref(addr_ads)
print "ctypes.sizeof(offset)", ctypes.sizeof(offset)
print "ctypes.byref(offset)", ctypes.byref(offset)
print "offset", offset
print "ctypes.sizeof(var_name)", ctypes.sizeof(var_name)
print "ctypes.byref(var_name)", ctypes.byref(var_name)
print "var_name", var_name


erreur2 = dll_adsdll.AdsSyncWriteReq(ctypes.byref(addr_ads), 
				int("0xF005", 16),
				offset,
				ctypes.sizeof(test),
				ctypes.byref(test) );
print erreur2

	

#func = self._dll_linsat.linsat_open
#r = func(ctypes.byref(self._linsat_mem))
