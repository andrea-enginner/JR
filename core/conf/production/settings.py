# -*- encoding: utf-8 -*-

import os


from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent.parent.parent.parent

def readSecret(envvarname: str):
    return str(open(os.environ[envvarname], 'rb').read(), encoding='ascii').strip()

# python -c "import secrets; print(secrets.token_urlsafe())"
SECRET_KEY = "hLwoS-HbZx4eNUTqrM3osPFdHQamfLcYo38iugUCX4d"

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.getenv("DEBUG", 'False').lower() in ('1', 'true', 't', 'yes', 'y')
DEBUG = 0

# load production server from .env
ALLOWED_HOSTS = [
    'distribulanche.com.br',
    'www.distribulanche.com.br',
]


CSRF_TRUSTED_ORIGINS = [
   
    'https://distribulanche.com.br',
    'https://www.distribulanche.com.br',
    'http://distribulanche.com.br',
    'http://www.distribulanche.com.br',
]


ACCOUNT_DEFAULT_HTTP_PROTOCOL='https'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL SERVER SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = '/marketplace/lanches/'


#LOGOUT_REDIRECT_URL = "home"  # Route defined in home/urls.py
ACCOUNT_LOGOUT_ON_GET = True
TEMPLATE_DIR = os.path.join(BASE_DIR, "apps/templates")  # ROOT dir for templates


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

AUTHENTICATION_BACKENDS = [
    #...
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "projetosd",
            "USER": os.environ['PG_APP_USER'],
            "HOST": 'projetosd_db',
            "PASSWORD": readSecret('PG_APP_PASSWORD_FILE'),
            "PORT": '5432',
        }
}

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = '/code/staticfiles'
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'apps/static'),)