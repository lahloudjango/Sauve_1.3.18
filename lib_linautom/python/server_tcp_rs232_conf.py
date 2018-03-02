# -*- coding: utf-8 -*-
"""
Module forwarding TCP <=> RS232
Fichier de configuration
"""

import serial

tcp_hote = "0.0.0.0"
tcp_port = 2001
tcp_nbr_connection = 2
tcp_buffer_size = 128

serial_timeout = 2
serial_port = "/dev/ttyUSB0"
serial_baudrate = 9600
serial_parity = serial.PARITY_NONE			# PARITY_EVEN, PARITY_MARK, PARITY_NONE, PARITY_ODD, PARITY_SPACE
serial_stopbits = serial.STOPBITS_ONE		# STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO
serial_bytesize = serial.SEVENBITS			# FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS
serial_fin_de_ligne = "\r\n"

fichier_log = "/var/log/server_tcp_rs232.log"
fichier_log = "/tmp/server_tcp_rs232.log"

#Affichage des log sur la console
console = False
console = True




