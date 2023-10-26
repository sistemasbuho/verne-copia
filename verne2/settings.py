"""Django settings for verne2 project.

Generated by 'django-admin startproject' using Django 2.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# cargo el archivo externo que contiene la base de datos
import verne2.db as db

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9)^=fw^uden2u+hn!s^20yijjp^od59&xdt*!uc@6(fhlydws3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*'] #Abierto para conexiones

from django.contrib.messages import constants as messages


MESSAGE_TAGS = {
	messages.DEBUG: 'alert-info',
	messages.INFO: 'alert-info',
	messages.SUCCESS: 'alert-success',
	messages.WARNING: 'alert-warning',
	messages.ERROR: 'alert-danger',
}

# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.sites', 
	'django.contrib.humanize',
	#Aplicaciones propias ordenadas por jeraquia en los modelos
	'apps.idea',
	'apps.meeting',
	'apps.prize',
	'apps.activity',
	'apps.indicators',
	'apps.home',
	'apps.users',


	# Librería de terceros
	'import_export',
	'bootstrap4',
	'simple_history',
	'django_filters',
	'widget_tweaks',
	'django_extensions', 
	'debug_toolbar', #Permite analizar el rendimiento de las consultas SQL 
	'ckeditor',
    'ckeditor_uploader',
    
	# Lìbrerìa de Microsoft
    'microsoft_auth',
    
	# Lìbrerìa de Google
	#'allauth', 
	#'allauth.account', 
	#'allauth.socialaccount', 
	#'allauth.socialaccount.providers.google', 
	
	# API
	'rest_framework',
	'corsheaders', #Uso del cors
	'rest_framework_swagger', #Documentacion

]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	#django_toolbar
	'debug_toolbar.middleware.DebugToolbarMiddleware',
	#Cors adicional
	'corsheaders.middleware.CorsMiddleware',
	#'django.middleware.csrf.CsrfViewMiddleware',
	'corsheaders.middleware.CorsPostCsrfMiddleware',
]

REST_FRAMEWORK = { 
	#Habilita el uso del la documentación
	'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
	#Habilita en el proyecto el uso de filters
	'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}

#django_toolbar
INTERNAL_IPS = [
	# ...
	'127.0.0.1',
	# ...
]

ROOT_URLCONF = 'verne2.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': ['templates'],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
                'microsoft_auth.context_processors.microsoft',
			],
		},
	},
]

WSGI_APPLICATION = 'verne2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = db.SERVIDOR

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp.office365.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'verne@gnilat.com'
EMAIL_HOST_PASSWORD = 'buho1234*'

DEFAULT_FROM_EMAIL = 'verne@gnilat.com'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [

	{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
	{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
	{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
	{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# values you got from step 2 from your Mirosoft app

#ramo
#MICROSOFT_AUTH_CLIENT_ID = '09011840-4960-425a-9e34-476756fcdb88'
#
#MICROSOFT_AUTH_CLIENT_SECRET = 'usq8Q~ui53lSkOD.Ofl5dBwLewvZ3Xpd9-kzebI~'
#Cambio 
MICROSOFT_AUTH_CLIENT_ID = '59e6d4f7-3272-4103-aab5-e71b4cc101ec'
MICROSOFT_AUTH_CLIENT_SECRET = '2ci8Q~DR8sa.9s5xFc-XXlYkNzBRe4Kql2bEkaCB'


# pick one MICROSOFT_AUTH_LOGIN_TYPE value
# Microsoft authentication
# include Microsoft Accounts, Office 365 Enterpirse and Azure AD accounts
MICROSOFT_AUTH_LOGIN_TYPE = 'ma'

# Xbox Live authentication

# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = False


#SOCIALACCOUNT_PROVIDERS = {
#     "google": {
#        # For each OAuth based provider, either add a ``SocialApp``
#        # (``socialaccount`` app) containing the required client
#        # credentials, or list them here:
#        "APP": {
#            'client_id': '790385665851-f9hoohsltitef2uv8fe7m38fn78ib1ah.apps.googleusercontent.com',
#            'secret': '6Yb4DvL11xFCMcTKwd5dTLqm',
#            "key": ""
#        },
#        # These are provider-specific settings that can only be
#        # listed here:
#        "SCOPE": [
#            "profile",
#            "email",
#        ],
#        "AUTH_PARAMS": {
#            "access_type": "online",
#        },
#        "verified_email": "true",
#    }
#}

# Static files (CSS, JavaScript, Images)https://docs.djangoproject.com/en/2.2/howto/static-files/
#estaticos para usar los estilos de la plantilla de AdminLTE 3

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR,'static'),)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline','Strike'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['Image', 'Smiley','Table','Iframe','Specialchar','Print'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor']
      
        ]
 
    }
}

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    'apps.users.backends.MicrosoftAuthenticationBackend',
)

SITE_ID = 1 # Identifica el servicio de terceros

LOGOUT_REDIRECT_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'

#SOCIALACCOUNT_ADAPTER = 'verne2.adapter.MySocialAccountAdapter' # Se ejecuta un disparador para validar si el usuario local tiene cuenta en Google y permite el acceso
#ACCOUNT_AUTHENTICATION_METHOD = "email" # Defaults to username_email
#ACCOUNT_USERNAME_REQUIRED = False       # Defaults to True
#ACCOUNT_EMAIL_REQUIRED = True           # Defaults to False
#SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED
#SOCIALACCOUNT_AUTO_SIGNUP = True
#SOCIALACCOUNT_EMAIL_REQUIRED = False
#ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5 #Evita el spam y bloquea al superar el numero de intentos asignados
#VERIFIED_EMAIL = False

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
VIRTUAL_PROTO= 'https'

