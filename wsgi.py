# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
WSGI config for sap project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys

#import os
#import sys
#APPS_PATH = "sap/dev"
#sys.path.append(APPS_PATH)
#os.chdir(APPS_PATH)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
