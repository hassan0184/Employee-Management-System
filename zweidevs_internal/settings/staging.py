from os import environ
from .base import *


DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['ZI_DATABASE_NAME'],
        'USER': os.environ['ZI_DATABASE_USER'],
        'PASSWORD': os.environ['ZI_DATABASE_PASS'],
        'HOST': os.environ['ZI_DATABASE_HOST'],
        'PORT': os.environ['ZI_DB_PORT'],
    }
}