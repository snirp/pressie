# Default settings for quick start (not for production)
# Recommended to use a server-specific settings_local.py file,
# which also contains secret information for production and development.
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates',),)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = "/media/"

STATIC_URL = '/static/'

SECRET_KEY = 'MyGoodFriend,ThisIsNotTheSecretKeyYouAreLookingFor'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

ALLOWED_HOSTS = ['.conditie.org']

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'rest_framework',
    'onderhoud',
    'onderhoudapi',
    'inlees',
    'sorl.thumbnail',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pressie.urls'

WSGI_APPLICATION = 'pressie.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

LANGUAGE_CODE = 'nl-NL'

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# This import should stay at the bottom as to override the general setttings.
# Local settings contain secret information and settings specific to the server.
# These should never be part of the repository.
try:
    from .settings_local import *
except Exception:
    pass
