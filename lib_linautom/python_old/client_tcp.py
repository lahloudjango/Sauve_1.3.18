# coding: utf-8
from __future__ import unicode_literals

import socket
import binascii

hote = "192.168.252.60"
port = 2001
buffer_size = 128


connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))

print("Connexion établie avec le serveur sur le port %s:%s" %(hote, str(port)))


msg_a_envoyer = b"\x1BP\r\n"
#msg_a_envoyer = b"bonjour\r\n"
print repr(msg_a_envoyer)

connexion_avec_serveur.send(msg_a_envoyer)

msg_recu = connexion_avec_serveur.recv(buffer_size)

print repr(msg_recu)

print("Fermeture de la connexion")
connexion_avec_serveur.close()
