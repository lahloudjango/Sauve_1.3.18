# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Module de communication avec un MCP342x : mesure de tension
"""
import codecs
from smbus import SMBus
import time

__author__ = "Charly GONTERO"
__date__ = "2017-04-25 21:44:23"
__version__ = 1.0
__credits__ = """
 *  MCP342x.py
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


class MCP3428(object):
	"""
	"""
	def __init__(self):
		self.LSB_12BITS = 0.001000
		self.LSB_14BITS = 0.000250
		self.LSB_16BITS = 0.0000625

		self.CW_RDY    = 0b10000000
		self.CW_C1     = 0b00000000
		self.CW_C2     = 0b00100000
		self.CW_C3     = 0b01000000
		self.CW_C4     = 0b01100000

		self.CW_CC     = 0b00010000
		self.CW_CM     = 0b00000000

		self.CW_240SPS = 0b00000000
		self.CW_60SPS  = 0b00000100
		self.CW_15SPS  = 0b00001000

		self.CW_G1     = 0b00000000
		self.CW_G2     = 0b00000001
		self.CW_G4     = 0b00000010
		self.CW_G8     = 0b00000011

		self.addr = 0
		self.mode = self.CW_CC
		self.sps = self.CW_15SPS
		self.lsb = self.LSB_16BITS
		self.gain = self.CW_G1

	def open(self, bus_num, bus=None):
		if bus != None:
			self.bus = bus
		else:
			self.bus = SMBus()
			self.bus.open(bus_num)

	def addr_is(self, pin0, pin1):
		"""
		Calcule l'addresse du chip avec la configuration des pin adresse pin0 et pin1
		None : pin floatante
		True : V+
		False : GND
		"""
		BASE_ADDR = 0b1101000
		if pin0 == None and pin1 == None:
			return BASE_ADDR|0b000
		if pin0 == False and pin1 == False:
			return BASE_ADDR|0b000
		if pin0 == False and pin1 == None:
			return BASE_ADDR|0b001
		if pin0 == False and pin1 == True:
			return BASE_ADDR|0b010
		if pin0 == None and pin1 == False:
			return BASE_ADDR|0b011
		if pin0 == True and pin1 == False:
			return BASE_ADDR|0b100
		if pin0 == True and pin1 == None:
			return BASE_ADDR|0b101
		if pin0 == True and pin1 == True:
			return BASE_ADDR|0b110
		if pin0 == None and pin1 == True:
			return BASE_ADDR|0b111

	def set_addr(self, addr):
		self.addr = addr

	def set_mode(self, mode):
		self.mode = mode&0b10010011

	def set_channel(self, CW_Cx):
		self.bus.write_byte(self.addr, self.CW_RDY|CW_Cx|self.mode|self.sps|self.gain)
		time.sleep(0.12)
		return

	def close(self):
		bus.close()

	def get_value(self):
		buf = self.bus.read_i2c_block_data(self.addr, 0, 2)
		#print buf
		if self.gain == self.CW_G1:
			return (buf[0] << 8 | buf[1]) * self.lsb
		if self.gain == self.CW_G2:
			return (buf[0] << 8 | buf[1]) * self.lsb / 2
		if self.gain == self.CW_G4:
			return (buf[0] << 8 | buf[1]) * self.lsb / 4
		if self.gain == self.CW_G8:
			return (buf[0] << 8 | buf[1]) * self.lsb / 8

	def set_lsb(self, lsb):
		self.lsb = lsb
		if self.lsb == self.LSB_12BITS:
			self.sps = self.CW_240SPS
		if self.lsb == self.LSB_14BITS:
			self.sps = self.CW_60SPS
		if self.lsb == self.LSB_16BITS:
			self.sps = self.CW_15SPS
		return self.sps

	def set_sps(self, sps):
		self.sps = sps
		if self.sps == self.CW_240SPS:
			self.lsb = self.LSB_12BITS
		if self.sps == self.CW_60SPS:
			self.lsb = self.LSB_14BITS
		if self.sps == self.CW_15SPS:
			self.lsb = self.LSB_16BITS
		return self.lsb

	def close(self):
		self.bus.close()

	def send_general_reset(self):
		self.bus.write_byte(self.addr, 0x06)
		time.sleep(0.5)
		return

	def send_general_latch(self):
		self.bus.write_byte(self.addr, 0x04)
		time.sleep(0.12)
		return

	def send_general_conversion(self):
		self.bus.write_byte(self.addr, 0x08)
		time.sleep(0.12)
		return

	def set_gain(self, gain):
		self.gain = gain

if __name__ == "__main__":
	chip = MCP3428()
	chip.open(2)
	chip.set_addr(chip.addr_is(pin0=True, pin1=True))
	chip.set_lsb(chip.LSB_16BITS)
	chip.set_mode(chip.CW_CM)

	i = 0
	while i < 10:
		chip.set_channel(chip.CW_C1)
		print chip.get_value(),"V"
		time.sleep(0.1)
		i += 1

	chip.set_channel(chip.CW_C2)
	print chip.get_value(),"V"

	chip.set_channel(chip.CW_C3)
	print chip.get_value(),"V"

	chip.set_channel(chip.CW_C4)
	print chip.get_value(),"V"

	chip.close()
