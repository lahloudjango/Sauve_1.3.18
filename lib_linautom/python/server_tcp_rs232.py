# -*- coding: utf-8 -*-
"""
Module forwarding TCP <=> RS232
"""

import serial
import socket
import sys
import signal
import traceback
import datetime

__author__ = "Charly GONTERO"
__date__ = "2016-01-09 10:18:44"
__version__ = 1.1
__credits__ = """
 *  server_tcp-rs232.py
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

VERSION = __version__
def version():
	"""
	Version 1.0
	Version 1.1
		fermeture du port TCP coté raspberry pi avec \x03 + fin_de_ligne
	"""
	return __version__

from server_tcp_rs232_conf import *

#Affichage des log sur la console
console = False
console = True

last_purge_rs = datetime.datetime.now()

class TimeExceededError(Exception):
	"""
	Exeption TimeOut ; Pas de réponce balance
	"""
	def __init__(self, *args, **kwargs):
		pass

def timeout_action(signum, frame, *args, **kwargs):
	"""
	Action déclanché au time out
	"""
	raise TimeExceededError

def whatisit(a):
	print type(a)
	print dir(a)
	print a

def log_print(*text):
	"""
	Fonction de login automatique
	"""
	if console == True:
		print text
	f_log = open(fichier_log, "a")
	d = datetime.datetime.now().strftime("%a, %Y-%m-%d %X ")
	for t in text:
		l = d + str(t) + "\n"
		f_log.writelines(l)
	f_log.close()

def sig_iterrupt(signal, frame):
	"""
	Gestionnaire d'interruption
	"""
	log_print("Arrêt Demandé")
	log_print("Stoppée")






signal.signal(signal.SIGINT, sig_iterrupt)
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connexion_principale.bind((tcp_hote, tcp_port))

connexion_principale.listen(tcp_nbr_connection)
log_print("Le serveur écoute à présent sur le port %s:%s" %(tcp_hote, str(tcp_port)))

while True:
	try:
		connexion_avec_client, infos_connexion = connexion_principale.accept()
		log_print("connecxion client %s:%s" %(infos_connexion[0], infos_connexion[1]))
		connection = True
		while connection: # ETX = end of transmision
			msg_recu = connexion_avec_client.recv(tcp_buffer_size)
			log_print("<= %s" %(repr(msg_recu)))
			if msg_recu[0] == "\x03":
				connection = False
				continue
			signal.signal(signal.SIGALRM, timeout_action)
			signal.alarm(serial_timeout)

			try:
				delta_time = datetime.datetime.now() - last_purge_rs
				last_purge_rs = datetime.datetime.now()
				if delta_time.seconds > 60*10:
					f = open(serial_port, r)
					buf = f.read()
					f.close()
					if buf != "":
						log_print("!!!!! BUFFER RS232 NON VIDE !!!!!")
						log_print(buf)
						log_print("!!!!! BUFFER RS232 NON VIDE !!!!!")

				com = serial.Serial(port=serial_port, baudrate=serial_baudrate, parity=serial_parity, stopbits=serial_stopbits, bytesize=serial_bytesize)
				com.write(msg_recu)

				reponce = ""
				while reponce[-len(serial_fin_de_ligne):] != serial_fin_de_ligne:
					reponce += com.read(1)
#				reponce = "Voici le poids !!!!!"
				signal.alarm(0)
			except TimeExceededError:
				signal.alarm(0)
				reponce = "Timeout balance  \r\n"
			except:
				reponce = "Erreur avec le port serie  \r\n"
				tb = traceback.format_exc()
				log_print("!!!!! ERREUR !!!!!")
				log_print(tb)
				log_print("!!!!! ERREUR !!!!!\n\n")

			log_print("=> %s" %(repr(reponce)))
			connexion_avec_client.send(reponce)
			log_print("=> OK")

		log_print("Fermeture de la connexion client")
		connexion_avec_client.close()
	except:
		tb = traceback.format_exc()
		log_print("!!!!! ERREUR !!!!!")
		log_print(tb)
		log_print("!!!!! ERREUR !!!!!\n\n")

log_print("Fermeture de la connexion principal")
connexion_principale.close()
