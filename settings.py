# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import version

DAJAXICE_MEDIA_PREFIX="dajaxice"

DEBUG = True
TEMPLATE_DEBUG = DEBUG


#DEFAULT_CONTENT_TYPE = 'application/xhtml+xml'
DEFAULT_CONTENT_TYPE = 'text/html'
DEFAULT_CHARSET = 'utf-8'


LOGIN_URL = "/django/utilisateur/login/"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#SESSION_COOKIE_AGE = 5 * 60 # seconde

ADMINS = (
	("Charly GONTERO", "charly.gontero@linautom.fr"),
)
MANAGERS = ADMINS

"""
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_FILE_PATH = "./"
EMAIL_HOST = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_HOST_USER = ""
EMAIL_PORT = 25
EMAIL_SUBJECT_PREFIX = "[Django] "
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_SSL_CERTFILE = None
EMAIL_SSL_KEYFILE = None
EMAIL_TIMEOUT = None
DEFAULT_CHARSET = "utf-8"
FILE_CHARSET = "utf-8"
SERVER_EMAIL = "django@linautom.fr"
"""

if version.status_developement["data"] == "prod":
	DATABASES = {
		"default": {
			"ENGINE": "django.db.backends.mysql",	# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
			"NAME": "stock",						# Or path to database file if using sqlite3.
			"USER": "stock",						# Not used with sqlite3.
			"PASSWORD": "stock",					# Not used with sqlite3.
			"HOST": "localhost",					# Set to empty string for localhost. Not used with sqlite3.
			"PORT": "3306",							# Set to empty string for default. Not used with sqlite3.
			"CONN_MAX_AGE" : 30,					# La durée de vie d’une connexion de base de données en seconde ( None = connection persistante )
		}
	}
elif version.status_developement["data"] == "dev":
	DATABASES = {
		"default": {
			"ENGINE": "django.db.backends.mysql",	# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
			"NAME": "stock_dev",					# Or path to database file if using sqlite3.
			"USER": "stock",						# Not used with sqlite3.
			"PASSWORD": "stock",					# Not used with sqlite3.
			"HOST": "localhost",					# Set to empty string for localhost. Not used with sqlite3.
			"PORT": "3306",							# Set to empty string for default. Not used with sqlite3.
			"CONN_MAX_AGE" : 30,					# La durée de vie d’une connexion de base de données en seconde ( None = connection persistante )
		}
	}
else:
	print "!!!!! Statut/source données incorrecte !!!!!"
	DATABASES = {
		"default": {
			"ENGINE": "django.db.backends.mysql",	# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
			"NAME": "",								# Or path to database file if using sqlite3.
			"USER": "",								# Not used with sqlite3.
			"PASSWORD": "",							# Not used with sqlite3.
			"HOST": "",								# Set to empty string for localhost. Not used with sqlite3.
			"PORT": "",								# Set to empty string for default. Not used with sqlite3.
			"CONN_MAX_AGE" : 30,					# La durée de vie d’une connexion de base de données en seconde ( None = connection persistante )
		}
	}
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["172.25.5.90", "localhost", "127.0.0.1", "127.0.1.1"]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "Europe/Paris"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "fr-FR"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ""

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ""

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

ADMIN_MEDIA_PREFIX = "media-admin"
ADMIN_STATIC_PREFIX = "static-admin"

# Additional locations of static files
STATICFILES_DIRS = (
#	"/var/www/django/static/",
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don"t forget to use absolute paths, not relative paths.
    "static",
    "media",
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
	"django.contrib.staticfiles.finders.FileSystemFinder",
	"django.contrib.staticfiles.finders.AppDirectoriesFinder",
#	"django.contrib.staticfiles.finders.DefaultStorageFinder",
)

# Make this unique, and don"t share it with anybody.
SECRET_KEY = "t_2z4jq-yl0b&amp;cnq%lo(1d=6yg&amp;@$s&amp;$o01xxp1aa=6i8kfr7*"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	"django.template.loaders.filesystem.Loader",
	"django.template.loaders.app_directories.Loader",
	"django.template.loaders.eggs.Loader",
)

MIDDLEWARE_CLASSES = (
	"django.middleware.common.CommonMiddleware",
	"django.contrib.sessions.middleware.SessionMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
#	Uncomment the next line for simple clickjacking protection:
#	"django.middleware.clickjacking.XFrameOptionsMiddleware",
#	"django_websocket.middleware.WebSocketMiddleware",

)

ROOT_URLCONF = "urls"

# Python dotted path to the WSGI application used by Django"s runserver.
WSGI_APPLICATION = "wsgi.application"

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don"t forget to use absolute paths, not relative paths.
)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["static/template"],
        "APP_DIRS": True,
        "OPTIONS": {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			]
          # ... some options here ...
        },
    },
]
INSTALLED_APPS = (
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.sites",
	"django.contrib.messages",
	"django.contrib.staticfiles",
	# Uncomment the next line to enable the admin:
	"django.contrib.admin",
	# Uncomment the next line to enable admin documentation:
	"django.contrib.admindocs",
	#"logentry_admin",
	#"dajaxice",


	"stock_labo",
	"stock_labo_pistolet",
	"utilisateur",


)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
	"version": 1,
	"disable_existing_loggers": False,
	"filters": {
		"require_debug_false": {
			"()": "django.utils.log.RequireDebugFalse"
		}
	},
	"handlers": {
		"mail_admins": {
			"level": "ERROR",
			"filters": ["require_debug_false"],
			"class": "django.utils.log.AdminEmailHandler"
		}
	},
	"loggers": {
		"django.request": {
			"handlers": ["mail_admins"],
			"level": "ERROR",
			"propagate": True,
		},
	}
}
