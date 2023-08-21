from pathlib import Path
from datetime import timedelta
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n1p%op6!rsm_cd*rrbxw%myuxzjn2$e=7&)t-!es39_0e=3_d+'

# SECURITY WARNING: don't run with debug turned on in production!

STATIC_ROOT = 'static'
STATIC_URL = 'static/'

CSRF_TRUSTED_ORIGINS = [
    'https://zweidevs-internal-backend.herokuapp.com',
    'https://api.internal.zweidevs.com'
]


# Application definition


AUTH_USER_MODEL = 'employee.Employee'



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_object_actions',
    'general',
    'employee',
    'salary',
    'lunch',
    'attendance',
    'corsheaders',
    'dashboard',
    'storages',
    'django_admin_listfilter_dropdown',
    'rangefilter',
    ]

CORS_ALLOWED_ORIGINS = os.environ['ZI_ALLOWED_CORS'].split(",")

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'zweidevs_internal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['general/templates'],
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

WSGI_APPLICATION = 'zweidevs_internal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

REST_FRAMEWORK = {
   
    'DEFAULT_AUTHENTICATION_CLASSES': (
        
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'EXCEPTION_HANDLER': 'common_utilities.custom_exception_handler.custom_exception_handler',
    'DEFAULT_RENDERER_CLASSES': [
        'common_utilities.renderers.CustomRenderer'
    ],
    
}

EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = config('SENDGRID_API_KEY')
SENDGRID_SANDBOX_MODE_IN_DEBUG=False


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



AWS_ACCESS_KEY_ID =os.environ['ZI_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY =os.environ['ZI_AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME =os.environ['ZI_AWS_STORAGE_BUCKET_NAME']
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_REGION_NAME='ap-south-1'
AWS_S3_ADDRESSING_STYLE = 'virtual'

