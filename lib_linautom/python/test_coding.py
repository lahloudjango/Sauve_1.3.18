# -*- coding: utf-8 -*-

from __future__ import unicode_literals

def whatisit(a):
	print type(a)
	print dir(a)
	print a

import locale
print locale.getdefaultlocale()[1]
print locale.getdefaultlocale()


a = "aÀ"
b = "aÀ".encode('ascii', 'replace')

whatisit(a)
whatisit(b)

