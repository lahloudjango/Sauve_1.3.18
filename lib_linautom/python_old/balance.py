# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Module global de communication avec les balances
"""
import threading
import time
import socket
import serial
import random

__author__ = "Charly GONTERO"
__date__ = "2015-09-16 14:24:00"
__version__ = 2.3
__credits__ = """
 *  balance.py
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


PROTOCOL = {
	1 : "Simulation".upper(),
	11 : "Sartorius".upper(),
	21 : "Mettler_SICS".upper(),
	}
BAUDRATE = {
	0: 0,
	50: 1,
	75: 2,
	110: 3,
	150: 5,
	134: 4,
	200: 6,
	300: 7,
	600: 8,
	1200: 9,
	1800: 10,
	2400: 11,
	4800: 12,
	9600: 13,
	19200: 14,
	38400: 15,
	57600: 4097,
	115200: 4098,
	230400: 4099,
	460800: 4100,
	500000: 4101,
	576000: 4102,
	921600: 4103,
	1000000: 4104,
	1152000: 4105,
	1500000: 4106,
	2000000: 4107,
	2500000: 4108,
	3000000: 4109,
	3500000: 4110,
	4000000: 4111,
	}
BYTESIZE = {
	"5": serial.FIVEBITS,
	"6": serial.SIXBITS,
	"7": serial.SEVENBITS,
	"8": serial.EIGHTBITS,
	}
STOP = {
	"1":   serial.STOPBITS_ONE,
	"1.5": serial.STOPBITS_ONE_POINT_FIVE,
	"2":   serial.STOPBITS_TWO,
	}
PARITY = {
	"E": serial.PARITY_EVEN,
	"M": serial.PARITY_MARK,
	"N": serial.PARITY_NONE,
	"O": serial.PARITY_ODD,
	"S": serial.PARITY_SPACE,
	}

UNIT = {
	"mg" : 1,
	"g"  : 1000,
	"kg" : 1000000,
	"T"  : 1000000000,
	}

def whatisit(a):
	print type(a)
	print dir(a)
	print a

class BalancePortErreur(Exception):
	"""
	Port incorrect
	"""
	def __init__(self, *args, **kwargs):
		pass

class BalanceParamErreur(Exception):
	"""
	Paramètre incorrect
	"""
	def __init__(self, *args, **kwargs):
		pass

class BalanceRetourErreur(Exception):
	"""
	Format de retour de la balance incorrect
	"""
	def __init__(self, *args, **kwargs):
		pass

class BalanceSurcharge(Exception):
	"""
	La balance est en surcharge
	"""
	def __init__(self, *args, **kwargs):
		pass

class BalanceSousCharge(Exception):
	"""
	La balance est en souscharge
	"""
	def __init__(self, *args, **kwargs):
		pass

class BalanceProtocolInconnu(Exception):
	"""
	Type de balance/protocole inconnu
	"""
	def __init__(self, *args, **kwargs):
		pass

class TimeOutComError(Exception):
	"""
	Exeption TimeOut ; Pas de réponce balance
	"""
	def __init__(self, *args, **kwargs):
		pass

class BalanceDecodageUnDefined(Exception):
	"""
	La fonction décodage n'est pas défini
	"""
	def __init__(self, *args, **kwargs):
		pass

class BalanceCom(object):
	"""
	Gestion des balances
	"""

	def __init__(self, port, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, fin_de_ligne="\r\n"):
		"""
		Définition des paramètres
		"""
		self.port = port
		self.baudrate = baudrate
		self.parity = parity
		self.stopbits = stopbits
		self.bytesize = bytesize
		self.fin_de_ligne = fin_de_ligne
		self.erreur = ""
		self.reponce_balance = ""
		self.unit_balance = ""
		self.poids = 0.0
		self.stabilitee = False

	def open(self):
		"""
		Ouverture du port pour la communication
		un port commencant par "/dev" est un port local ; tout autre est un port reseau
		"""
		if self.port.startswith("/dev"):
			try:
				self.com = serial.Serial(port=self.port, baudrate=self.baudrate, parity=self.parity, stopbits=self.stopbits, bytesize=self.bytesize)
			except serial.serialutil.SerialException:
				self.stabilitee = False
				self.poids = 0
				self.erreur = "Connexion impossible sur la balance sur %s" %(self.port)
				raise BalancePortErreur()
		else:
			self.com = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			TCP_HOST, TCP_PORT = self.port.split(":")
			try:
				self.com.connect((self.port.split(":")[0], int(self.port.split(":")[1])))
			except socket.error:
				self.com.close()
				self.stabilitee = False
				self.poids = 0
				self.erreur = "Connexion impossible sur la balance sur %s" %(self.port)
				raise BalancePortErreur()

	def read(self, *arg, **kwargs):
		"""
		Réception du message de la balance
		"""
		self.reponce_balance = ""
		if self.port.startswith("/dev"):
			while self.reponce_balance[-len(self.fin_de_ligne):] != self.fin_de_ligne:
				try:
					self.reponce_balance += self.com.read(1)
				except serial.serialutil.SerialException:
					pass
			return self.reponce_balance[:-len(self.fin_de_ligne)]
		else:
			while self.reponce_balance[-len(self.fin_de_ligne):] != self.fin_de_ligne:
				self.reponce_balance += self.com.recv(1)
			return self.reponce_balance[:-len(self.fin_de_ligne)]

	def write(self, commande, param=""):
		"""
		Envoie de commande à la balance
		return renvoie le nombre de byte envoyé
		"""
		if self.port.startswith("/dev"):
#			print self.COMMANDE[commande]+param+self.fin_de_ligne
			return self.com.write(self.COMMANDE[commande]+param+self.fin_de_ligne)
		else:
#			print self.COMMANDE[commande]+param+self.fin_de_ligne
			return self.com.send(self.COMMANDE[commande]+param+self.fin_de_ligne)

	def lecture(self, unit="mg", timeout=5):
		"""
		lecture automatique du poids sur la balance
		"""
		print "WRITE"
		self.write("print")
		print "OUVERTURE DU THREAD"
		t = threading.Thread(group=None, target=self.read, name="com_balance", args=(self,), kwargs={})
		t.start()
		t.join(timeout)
		if t.is_alive():
			t._Thread__stop()
			print "Thread tuée"
			self.stabilitee = False
			self.poids = 0
			self.erreur = "Timeout ; Pas de réponse de la balance sur %s" %(str(self.port))
			raise TimeOutComError()
		else:
			print "Fin normal"
			self.decodage(self.reponce_balance)
			return self.poids/UNIT[unit]

	def close(self):
		"""
		fermeture du port de connumication
		"""
		if self.port.startswith("/dev"):
			self.com.close()
		else:
			return self.com.send("\x03"+fin_de_ligne) # fonctionnement avec pond raspberry pi
			self.com.close()

	def decodage(self, reponce):
		"""
		Definir "ICI" la fonction de décodage de retour de communication
		"""
		raise BalanceDecodageUnDefined

class Simulation(object):
	"""
	Simulation
	"""
	UNIT = {

		"mg" : 1,
		"g" : 1000,
		"kg" : 1000000,
		"T" : 1000000000,
		}

	COMMANDE = {
		"print" : "\r\n",
		"tare" : "\r\n",
		"zero" : "\r\n",
		"free_com" : "\r\n",  #ordre libre à définir à la volé"
			}

	def __init__(self):
		"""
		Définition des paramètres
		un port commencant par "/dev" est un port local ; tout autre est un port reseau
		"""
		self.port = ""
		self.baudrate = ""
		self.parity = ""
		self.stopbits = ""
		self.bytesize = ""
		self.fin_de_ligne = ""
		self.erreur = ""
		self.reponce_balance = ""
		self.unit_balance = ""
		self.poids = 0.0
		self.stabilitee = False

	def open(self):
		"""
		Ouverture du port pour la communication
		"""
		pass

	def read(self):
		"""
		Réception du message de la balance
		"""
		pass

	def write(self, commande ):
		"""
		Envoie de commande à la balance
		return renvoie le nombre de byte envoyé
		"""
		pass

	def decodage(self, reponce):
		"""
		Decodage de la chaine de charactaire envoyé par la balance
		le poids est retourné en mg
		"""
		self.unit_balance = "mg"
		self.poids = random.randint(0,6000000)
		self.stabilitee = True

	def lecture(self,unit="mg", timeout=5):
		"""
		lecture automatique du poids sur la balance
		"""
		self.decodage("")
		return self.poids/self.UNIT[unit]

	def close(self):
		"""
		fermeture du port de connumication
		"""
		pass

class Sartorius(BalanceCom):
	"""
	Gestion des balances Sartorius
	"""

	COMMANDE = {
		"balance" : "\x1Bx1_",				# Inquiry of balance data
		"version" : "\x1Bx3_",				# Inquiry of balance SW version and type definition number
		"serial" : "\x1Bx2_",				# Inquiry of serial number
		"print" : "\x1BP",					# Send stable weight value
		"print_i" : "\x1BP",				# Send weight value immediately
		"zero" : "\x1Bf3_",					# Zero
		"zero_i" : "\x1Bf3_",				# Zero immediately
		"tare" : "\x1BT",					# Tare
		"tare_v" : "\x1Bf4_",				# Inquiry/setting of tare weight value
		"tare_c" : "\x1Bf4_",				# Clear tare value
		"tare_i" : "\x1Bf4_",				# Tare Immediately
		"type" : "\x1Bx9_",					# Balance type
		"free_com" : "???", #ordre libre à définir à la volé"
			}

	def decodage(self, reponce):
		"""
		Decodage de la chaine de charactaire envoyé par la balance
		le poids est retourné en mg
		"""
		reponce_nettoye = []
		split_reponce = reponce.split(" ")

		if split_reponce[0] == "":
			split_reponce[0] = "+"

		i = 0
		while i < len(split_reponce):
			if split_reponce[i] != "":
				reponce_nettoye.append(split_reponce[i])
			i += 1

		self.poids = 0
		if reponce_nettoye[0] == "H" or reponce_nettoye[0] == "HH":
			self.erreur = "SURCHARGE"
			raise BalanceSurcharge
		elif reponce_nettoye[0] == "L" or reponce_nettoye[0] == "LL":
			self.erreur = "SOUSCHARGE"
			raise BalanceSouscharge
		else:
			try:
				self.poids = float(reponce_nettoye[1])
			except ValueError:
				self.erreur = reponce
				raise BalanceRetourErreur

		if reponce_nettoye[2] in UNIT.keys():
			self.unit_balance = reponce_nettoye[2]
			self.stabilitee = True
		else:
			self.stabilitee = False

		if self.unit_balance != "":
			self.poids *= UNIT[self.unit_balance]
			if reponce_nettoye[0] == "-":
				self.poids *= -1
			self.erreur = ""
		else:
			self.poids = 0
			self.erreur = "Unité inconnu"

class MettlerSics(BalanceCom):
	"""
	Gestion des balances Sartorius
	"""
	COMMANDE = {
		"commande_liste" : "I0",		# Inquiry of all implemented MT-SICS commands
		"commande_level" : "I1",		# Inquiry of MT-SICS level and MT-SICS versions
		"balance" : "I2",				# Inquiry of balance data
		"version" : "I3",				# Inquiry of balance SW version and type definition number
		"serial" : "I4",				# Inquiry of serial number
		"print" : "S",					# Send stable weight value
		"print_i" : "SI",				# Send weight value immediately
		"print_i_r" : "SIR",			# Send weight value immediately and repeat
		"zero" : "Z",					# Zero
		"zero_i" : "ZI",				# Zero immediately
		"reset" : "@",					# Reset
		"display" : "D",				# Balance display
		"display_w" : "DW",				# Weight display (Display show Weight)
		"key" : "K",					# Key control
		"print_c" : "SR",				# Send weight value on weight change (Send and Repeat)
		"tare" : "T",					# Tare
		"tare_v" : "TA",				# Inquiry/setting of tare weight value
		"tare_c" : "TAC",				# Clear tare value
		"tare_i" : "TI",				# Tare Immediately
		"cal_param" : "C0",				# Inquiry/setting of calibration setting
		"cal" : "C1",					# Initiate calibration according to current setting
		"cal_i" : "C2",					# Initiate calibration with external weight
		"cal_e" : "C3",					# Initiate calibration with internal weight
		"type" : "I11",					# Balance type
		"M" : "M",						#
		"MW" : "MW",					#
		"power" : "PWR",				# Power on/off
		"P100" : "P100",				#
		"P101" : "P101",				#
		"P102" : "P102",				#
		"P120" : "P120",				#
		"P121" : "P121",				#
		"P122" : "P122",				#
		"P123" : "P123",				#
		"P124" : "P124",				#
		"print_d_s_r" : "SNR",			# Send stable weight value and repeat after each deflection
		"print_d_s_r_u" : "SNRU",		# Send stable weight value with currently displayed unit and repeat after each deflection
		"print_k" : "ST",				# Send stable weight value after pressing ± (transfer) key
		"print_u" : "SU",				# Send stable weight value with currently displayed unit
		"print_i_u" : "SIU",			# Send weight value with currently displayed unit immediately
		"print_i_u_r" : "SIRU",			# Send weight value with currently displayed unit immediately and repeat
		"print_d_i_r" : "SRU",			# Send stable weight value with currently displayed unit after deflection
		"test0" : "TST0",				# Inquiry/setting of the test function
		"test1" : "TST1",				# Initiate test function in the current setting
		"test2" : "TST2",				# Initiate test function with external weight
		"test3" : "TST3",				# Initiate test function with internal weight
		"SM0" : "SM0",					# Cancel commands SM2 and SM3
		"SM1" : "SM1",					# Start dynamic weighing immediately and transfer a result
		"SM2" : "SM2",					# Start dynamic weighing and transfer a result
		"SM3" : "SM3",					# Start dynamic weighing, transfer result and repeat
		"free_com" : "???",  			#ordre libre à définir à la volé"
			}


	def decodage(self, reponce):
		"""
		Decodage de la chaine de charactaire envoyé par la balance
		le poids est retourné en mg
		"""
		reponce_nettoye = []
		split_reponce = reponce.split(" ")

		if split_reponce[0] == "":
			split_reponce[0] = "+"

		i = 0
		while i < len(split_reponce):
			if split_reponce[i] != "":
				reponce_nettoye.append(split_reponce[i])
			i += 1

		self.poids = 0
		if reponce_nettoye[1] == "+":
			self.erreur = "SURCHARGE"
			raise BalanceSurcharge
		elif reponce_nettoye[1] == "-":
			self.erreur = "SOUSCHARGE"
			raise BalanceSouscharge
		else:
			try:
				self.poids = float(reponce_nettoye[2])
			except ValueError:
				self.erreur = reponce
				raise BalanceRetourErreur

		if reponce_nettoye[3] in UNIT.keys():
			self.unit_balance = reponce_nettoye[3]

		if reponce_nettoye[0] == "S" and reponce_nettoye[1] == "S":
			self.stabilitee = True
		else:
			self.stabilitee = False

		if self.unit_balance != "":
			self.poids *= UNIT[self.unit_balance]
		else:
			self.poids = 0
			self.erreur = "Unité inconnu"
			return 0

class Balance(object):
	"""
	Gestion de la comunication balance
	"""

	COMMANDE = {
		"free_com" : "???", #ordre libre à définir à la volé"
		}

	def __init__(self, com, timeout_com=5):
		"""
		Initialisation du protocol
		com est un dictionnaire des paramètre de communication
		clefs :
				protocol 		: protocol de la balance ( dico PROTOCOL )
				port			: le port de communication ex : /dev/ttyUSB0 ; module réseau : 172.25.9.18:9000
				baudrate 		: vitesse de transmition ( le parametrage des module réseau n'est pas pris en charge ( dico BAUDRATE )
				parity			: bit de parité : ( dico PARITY )
				stopbits		: nombre bit de stop ( dico STOP )
				bytesize		: nombre de bit par octet ( dico BYTESIZE )
				fin_de_ligne 	: caractaire de fin de transmition, générallement "\r\n" (CRLF)
		"""
		self.stabilitee = False
		self.erreur = ""
		self.timeout_com = timeout_com
		self.sleep_continu_read = None;
		self.poids_mg = 0.0
		self.poids_unit = 0.0

		if com.has_key("protocol"):
			self.protocol = com["protocol"]
		else:
			self.protocol = None

		if com.has_key("port"):
			self.host_port = com["port"]
		else:
			self.host_port = None

		if com.has_key("baudrate"):
			self.baudrate = com["baudrate"]
		else:
			self.baudrate = None

		if com.has_key("parity"):
			self.parity = com["parity"]
		else:
			self.parity = None

		if com.has_key("stopbits"):
			self.stopbits = com["stopbits"]
		else:
			self.stopbits = None

		if com.has_key("bytesize"):
			self.bytesize = com["bytesize"]
		else:
			self.bytesize = None

		if com.has_key("fin_de_ligne"):
			if com["fin_de_ligne"] == "CR":
				self.fin_de_ligne = "\r"
			elif com["fin_de_ligne"] == "LF":
				self.fin_de_ligne = "\n"
			elif com["fin_de_ligne"] == "CRLF":
				self.fin_de_ligne = "\r\n"
			else:
				self.fin_de_ligne = com["fin_de_ligne"]
		else:
			self.fin_de_ligne = "\r\n"

		if self.protocol == PROTOCOL[1]: # Simulation
			self.balance = Simulation()
		elif self.protocol == PROTOCOL[11]: # Sartorius
			self.balance = Sartorius(port=self.host_port, baudrate=self.baudrate, parity=self.parity, stopbits=self.stopbits, bytesize=self.bytesize, fin_de_ligne=self.fin_de_ligne)
		elif self.protocol == PROTOCOL[21]: # Mettler_SICS
			self.balance = MettlerSics(port=self.host_port, baudrate=self.baudrate, parity=self.parity, stopbits=self.stopbits, bytesize=self.bytesize, fin_de_ligne=self.fin_de_ligne)
		else:
			raise BalanceProtocolInconnu()

	def open(self):
		"""
		Ouverture du port pour la communication
		"""
		if self.protocol == PROTOCOL[1]: # Simulation
			self.balance.open()
		elif self.protocol == PROTOCOL[11]: # Sartorius
			self.balance.open()
		elif self.protocol == PROTOCOL[21]: # Mettler_SICS
			self.balance.open()
		else:
			raise BalanceProtocolInconnu

	def read(self):
		"""
		Réception du message de la balance
		"""
		r = ""
		if self.protocol == PROTOCOL[1]: # Simulation
			r = self.balance.read()
		elif self.protocol == PROTOCOL[11]: # Sartorius
			r = self.balance.read()
		elif self.protocol == PROTOCOL[21]: # Mettler_SICS
			r = self.balance.read()
		else:
			raise BalanceProtocolInconnu
		return r

	def write(self, commande, param=""):
		"""
		Envoie de commande à la balance
		return renvoie le nombre de byte envoyé
		"""
		if self.protocol == PROTOCOL[1]: # Simulation
			self.balance.write(commande, param=param)
		elif self.protocol == PROTOCOL[11]: # Sartorius
			self.balance.write(commande, param=param)
		elif self.protocol == PROTOCOL[21]: # Mettler_SICS
			self.balance.write(commande, param=param)
		else:
			raise BalanceProtocolInconnu

	def decodage(self, reponce):
		"""
		Decodage de la chaine de charactaire envoyé par la balance
		le poids est retourné en mg
		"""
		balance.decodage(reponce)

	def close(self):
		"""
		fermeture du port de connumication
		"""
		self.balance.close()

	def lecture(self, unit="mg"):
		"""
		lecture automatique du poids sur la balance
		"""
		if self.sleep_continu_read == None:
			self.poids_unit = self.balance.lecture(unit, timeout=self.timeout_com)
			self.erreur = self.balance.erreur
			self.poids_mg = self.balance.poids
			self.stabilitee = self.balance.stabilitee
			return {"poids" : self.poids_unit, "stabilitee" : self.balance.stabilitee}
		else:
			return {"poids" : self.poids_unit, "stabilitee" : self.balance.stabilitee}



if __name__ == "__main__":
	"""
	Exemple d"utilisation de cette nouvelle classe de gestion des balances Sartorius
	"""
#	balance = Sartorius(port="/dev/ttyUSB0")
#	balance = Sartorius(port="/dev/ttyS0")
#	balance = Sartorius(port="/dev/tty31")
#	balance = Sartorius(port="192.168.252.62:8000")
#	balance = Balance(host_port="Mettler_SICS:///dev/ttyUSB0/9600/8/1/N", timeout_com=5, fin_de_ligne="\r\n")
	com = {}
	com.update({"protocol" : "SARTORIUS"})
	com.update({"port" : "155.66.213.219:2001"})
	com.update({"baudrate" : "9000"})
	com.update({"parity" : "S"})
	com.update({"stopbits" : "1"})
	com.update({"bytesize" : "8"})
	com.update({"fin_de_ligne" : "CRLF"})




	balance = Balance(com=com, timeout_com=15)

	balance.open()

	while balance.erreur == "":
		p = balance.lecture(unit="mg")
		print p
	print balance.erreur

#	balance.write("tare_v", " 123.23 g")
#	print balance.read()
#	time.sleep(2)

#	balance.write("tare_v", " -123.23 g")
#	print balance.read()
#	time.sleep(2)

#	balance.write("tare_c")
#	print balance.read()
#	time.sleep(2)


#	while True:
#		print balance.read()



	try:
		balance.close()
	except AttributeError:
		print "Aucun port ouvert"


