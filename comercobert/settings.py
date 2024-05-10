"""
Django settings for comercobert project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#$$g89cw!#ksbdf5kr@z@&tjg+gl6qa)azdeb4xd%94lhqz%f('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
PRODUCCIO = True

if PRODUCCIO:
    URL_BASE = "http://comercobert.svc.cat"
    GDAL_LIBRARY_PATH = '/usr/local/gdal-2.4.3/lib/libgdal.so'
else:
    URL_BASE = "http://svc.jordipalma.cat:8000"

RECAPTCHA_PUBLIC_KEY = '6LfrZNoZAAAAAKH-lDitphlbjUJHOe-XdWE3XRLW'
RECAPTCHA_PRIVATE_KEY = '6LfrZNoZAAAAAKlKP7MdK3Ix9hv_p-WIkMMLvMU4'


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.gis',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'localflavor',
    'bootstrap4',
    'captcha',
    'easy_thumbnails',
    'image_cropping',
    'djrichtextfield',
    'fontawesome_5',
    'ordered_model',
    'django_bootstrap_breadcrumbs',
    'comercos.apps.ComercosConfig',
    'location_field.apps.DefaultConfig',
    'cookielaw',
    
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'comercobert.urls'


SETTINGS_PATH = os.path.normpath(os.path.dirname(__file__))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SETTINGS_PATH, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]


WSGI_APPLICATION = 'comercobert.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

#'ENGINE': 'django.db.backends.mysql',

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql',
        'NAME': 'comercobert',
        'USER': 'comercobert',
        'PASSWORD': 'comerc.2020!',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ca'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True



STATIC_URL = '/static/'
if PRODUCCIO:
    MEDIA_ROOT = '/var/www/html/comercobert/comercobert/media/'
    STATIC_ROOT = '/var/www/html/comercobert/static/'
    MY_STATIC_ROOT = '/var/www/html/comercobert/comercobert/static/'
    STATICFILES_DIRS = [
        MY_STATIC_ROOT,
    ]
else:
    STATIC_ROOT = '/Users/jpalma/Sites/comercobert/static/'
    MY_STATIC_ROOT = '/Users/jpalma/Sites/comercobert/comercobert/static/'
    STATICFILES_DIRS = [
        MY_STATIC_ROOT,
    ]
    MEDIA_ROOT = '/Users/jpalma/Sites/comercobert/comercobert/media/'
MEDIA_URL = '/media/'



from easy_thumbnails.conf import Settings as thumbnail_settings
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

#grapelli settings
GRAPPELLI_ADMIN_TITLE = 'Administració comercobert.svc.cat'


# mail config

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Host for sending e-mail.
EMAIL_HOST = 'smtp-es.securemail.pro'

# Port for sending e-mail.
EMAIL_PORT = 465

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = 'festamajor@ajsvc.cat'
EMAIL_HOST_PASSWORD = '$wY]2rSaaj'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = 'no-reply@ajsvc.cat'


LOCATION_FIELD_PATH = STATIC_URL + 'location_field'


MAPS_API_KEY = 'AIzaSyDaMwOx7ho9O10TuX1WzgrIf1KTY-QDCpk' 

LOCATION_FIELD = {
    'map.provider': 'google',
    'map.zoom': 13,

    'search.provider': 'google',
    'search.suffix': 'Sant Vicenç de Castellet',

    # Google
    'provider.google.api': '//maps.google.com/maps/api/js',
    'provider.google.api_key': MAPS_API_KEY,
    'provider.google.api_libraries': '',
    'provider.google.map.type': 'ROADMAP',

    # Mapbox
    #'provider.mapbox.access_token': '',
    #'provider.mapbox.max_zoom': 18,
    #'provider.mapbox.id': 'mapbox.streets',

    # OpenStreetMap
    #'provider.openstreetmap.max_zoom': 18,

    # misc
    'resources.root_path': LOCATION_FIELD_PATH,
    'resources.media': {
        'js': (
            LOCATION_FIELD_PATH + '/js/form.js',
        ),
    },
}



#EASY_MAPS_CENTER = (1.8610, 41.6674)

