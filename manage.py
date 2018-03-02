#!/usr/bin/env python
from __future__ import unicode_literals
import os
import sys

if __name__ == "__main__":

	import os

#	import sys
#	print sys.path[0]
#	APPS_PATH = sys.path[0] + "/" + "sap/dev"
#	sys.path[0] = APPS_PATH
#	print sys.path[0]
#	os.chdir(APPS_PATH)

	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)
