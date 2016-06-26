'''
Django settings, generated using Django 1.9.4.
'''

import os

# Build paths inside the project like this: os.path.join(PROJECT_ROOT, ...)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wb8ua=u$k3cpv*b&#63-@9d!0h)mgozggi8-(%xvxg4i1a-5&x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'bootstrap3', # django-bootstrap3
	'requests',
]

# Make AutoSlugs use unicode characters
from slugify import slugify
AUTOSLUG_SLUGIFY_FUNCTION = slugify

MIDDLEWARE_CLASSES = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = '_project.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [ os.path.join(PROJECT_ROOT, 'static/templates/'), ],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = '_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
	}
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join((PROJECT_ROOT), "_static_root")
MEDIA_ROOT = os.path.join((PROJECT_ROOT), "_media_root")
STATICFILES_DIRS = (
	os.path.join((PROJECT_ROOT), "static", "static"),
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

from django.contrib import messages
MESSAGE_TAGS = { messages.ERROR: 'danger' }

APPEND_SLASH = True




#
# LOGGING
#

LOGGING = {
	'version': 1,
	'disable_existing_loggers': True,
	'root': {
		'level': 'WARNING',
		'handlers': ['sentry'],
	},
	'formatters': {
		'verbose': {
			'format': '%(levelname)s %(asctime)s %(module)s '
					  '%(process)d %(thread)d %(message)s'
		},
	},
	'handlers': {
		'sentry': {
			'level': 'DEBUG', # To capture more than ERROR, change to WARNING, INFO, etc.
			'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
			'tags': {'custom-tag': 'x'},
		},
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'verbose'
		},
		'file': {
			'level': 'DEBUG',
			'class': 'logging.FileHandler',
			'filename': '_logs/debug.log',
			'formatter': 'verbose',
		},
	},
	'loggers': {
		'django.db.backends': {
			'level': 'ERROR',
			'handlers': ['console'],
			'propagate': False,
		},
		'raven': {
			'level': 'DEBUG',
			'handlers': ['console'],
			'propagate': False,
		},
		'sentry.errors': {
			'level': 'DEBUG',
			'handlers': ['console'],
			'propagate': False,
		},
		'django': {
			'handlers': ['file'],
			'level': 'DEBUG',
			'propagate': True,
		},
	},
}

INSTALLED_APPS += ['raven.contrib.django.raven_compat'] # using sentry to log

import raven

RAVEN_CONFIG = {
	'dsn': 'XXXXXXXXXXXXXXX',
#	'release': raven.fetch_git_sha(os.path.dirname(__file__)),
}



##########################
#  Settings localisables :
##########################

# import local_settings if exist
try: from local_settings import *
except ImportError: pass