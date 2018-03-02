# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Module forwarding TCP <=> RS232
Fichier de configuration
"""

tcp_hote = "0.0.0.0"
tcp_port = 2001
tcp_nbr_connection = 2
tcp_buffer_size = 128

serial_timeout = 8
serial_port = "/dev/ttyUSB0"
serial_baudrate = 9600
serial_parity = serial.PARITY_NONE
serial_stopbits = serial.STOPBITS_ONE
serial_bytesize = serial.EIGHTBITS
serial_fin_de_ligne = "\r\n"

fichier_log = "/var/log/server_tcp-rs232.log"

#Affichage des log sur la console
console = False
#console = True
