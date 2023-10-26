
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

VERNE_CLIENTES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'verne_clientes',
        'USER': 'produccion_database_clarity',
        'PASSWORD': 'PR4D5CC34N#B5H4$CL1R3TY%22',
        'HOST': '144.126.221.28',
        'PORT': 5432,
    }		
 }

SERVIDOR = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'verne_demo_buho',
        'USER': 'produccion_database_clarity',
        'PASSWORD': 'PR4D5CC34N#B5H4$CL1R3TY%22',
        'HOST': '144.126.221.28',
        'PORT': 5432,
    }	
}


PRUEBAS_SERVIDOR = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'verne_2 pruebas',
        'USER': 'produccion_database_clarity',
        'PASSWORD': 'PR4D5CC34N#B5H4$CL1R3TY%22',
        'HOST': '144.126.221.28',
        'PORT': 5432,
    }	
}