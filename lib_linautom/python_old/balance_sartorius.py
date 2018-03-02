# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Module de communication avec les balance Sartorius
"""

import serial
import socket
import sys
import signal


__author__ = "Charly GONTERO"
__date__ = "2015-01-03 10:58:37"
__version__ = 2.1
__credits__ = """
 *  sartorius.py
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
	"""
	Version 1.0
		Conunication avec un port local
	Version 2.0
		Conunication avec un port local
		Conunication avec un port reseau
	Version 2.1
		Conunication avec un port local
		Conunication avec un port reseau
		Gestion time out réponse balance
	"""
	return __version__



class TimeExceededError(Exception):
	"""
	Exeption TimeOut ; Pas de réponce balance
	"""

	def __init__(self, *args, **kwargs):
		pass

class Sartorius(object):
	"""
	Gestion des balances Sartorius
	"""
	UNIT = {
		"mg" : 1,
		"g"  : 1000,
		"kg" : 1000000,
		"T"  : 1000000000,
		}

	COMMANDE = {
		"print" : "\x1BP\r\n",
		"tare" : "\x1BT\r\n",
		"zero" : "\x1BZ\r\n",
		"free_com" : "\r\n", #ordre libre à définir à la volé"
			}

	def __init__(self, port, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, fin_de_ligne="\r\n"):
		"""
		Définition des paramètres
		un port commencant par "/dev" est un port local ; tout autre est un port reseau
		"""
		self.port = port
		self.baudrate = baudrate
		self.parity = parity
		self.stopbits = stopbits
		self.bytesize = bytesize
		self.fin_de_ligne = fin_de_ligne
		self.erreur = ""
		self.unit_balance = ""
		self.poids = 0.0
		self.stabilitee = False

	def timeout_action(signum, frame, *args, **kwargs):
		"""
		Action déclanché au time out
		"""
		raise TimeExceededError



	def open(self):
		"""
		Ouverture du port pour la communication
		GET=etiquette
		try:
		  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error, msg:
		  sys.stderr.write("[ERROR] %s\n" % msg[1])
		  sys.exit(1)

		try:
		  sock.connect((TCP_HOST, TCP_PORT))
		except socket.error, msg:
		  sys.stderr.write("[ERROR] %s\n" % msg[1])
		  sys.exit(2)
		"""
		if self.port.startswith("/dev"):
			try:
				self.com = serial.Serial(port=self.port, baudrate=self.baudrate, parity=self.parity, stopbits=self.stopbits, bytesize=self.bytesize)
			except serial.serialutil.SerialException:
				self.stabilitee = False
				self.poids = 0
				self.erreur = "Connexion impossible sur la balance sur %s" %(self.port)
			return 0
		else:
			self.com = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			TCP_HOST, TCP_PORT = self.port.split(":")
			try:
				self.com.connect((TCP_HOST, int(TCP_PORT)))
			except socket.error:
				self.com.close()
				self.stabilitee = False
				self.poids = 0
				self.erreur = "Connexion impossible sur la balance sur %s" %(self.port)
			return 0

	def read(self):
		"""
		Réception du message de la balance
		"""
		reponce = ""
		if self.port.startswith("/dev"):
			while reponce[-len(self.fin_de_ligne):] != self.fin_de_ligne:
				reponce += self.com.read(1)
			return reponce
		else:
			while reponce[-len(self.fin_de_ligne):] != self.fin_de_ligne:
				reponce += self.com.recv(1)
			return reponce

	def write(self, commande ):
		"""
		Envoie de commande à la balance
		return renvoie le nombre de byte envoyé
		"""
		if self.port.startswith("/dev"):
			return self.com.write(self.COMMANDE[commande])
		else:
			return self.com.send(self.COMMANDE[commande])

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

		try:
			self.poids = float(reponce_nettoye[1])
		except ValueError:
			self.poids = 0
			if reponce_nettoye[1] == "H":
				self.erreur = "SURCHARGE"
				return -1
			elif reponce_nettoye[1] == "L":
				self.erreur = "SOUSCHARGE"
				return -1
			else:
				self.erreur = reponce
				return -1

		if reponce_nettoye[2] in self.UNIT.keys():
			self.unit_balance = reponce_nettoye[2]
			self.stabilitee = True
		else:
			self.stabilitee = False

		if self.unit_balance != "":
			self.poids *= self.UNIT[self.unit_balance]
			if reponce_nettoye[0] == "-":
				self.poids *= -1
			self.erreur = ""
			return 0
		else:
			self.poids = 0
			self.erreur = "Unité inconnu"
			return 0

	def lecture(self,unit="mg", timeout=5):
		"""
		lecture automatique du poids sur la balance
		"""
		signal.signal(signal.SIGALRM, self.timeout_action)
		signal.alarm(timeout)
		try:
			self.write("print")
			r = self.read()
			self.decodage(r)
			signal.alarm(0)
			return self.poids/self.UNIT[unit]
		except TimeExceededError:
			signal.alarm(0)
			self.stabilitee = False
			self.poids = 0
			self.erreur = "Timeout ; Pas de réponse de la balance sur %s" %(self.port)

	def close(self):
		"""
		fermeture du port de connumication
		"""
		self.com.close()


if __name__ == "__main__":
	"""
	Exemple d"utilisation de cette nouvelle classe de gestion des balances Sartorius
	"""
#	balance = Sartorius(port="/dev/ttyUSB0")
#	balance = Sartorius(port="/dev/ttyS0")
#	balance = Sartorius(port="/dev/tty31")
#	balance = Sartorius(port="155.66.213.254:2001")
	balance = Sartorius(port="localhost:2001")

	balance.open()
	while balance.erreur == "":
		p = balance.lecture(unit="kg")
		print p

	print balance.erreur

	try:
		balance.close()
	except AttributeError:
		print "Aucun port ouvert"

