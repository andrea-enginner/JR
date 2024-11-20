import os

IS_PRODUCTION = os.getenv("IS_PRODUCTION", 'False').lower() in ('1', 'true', 't', 'yes', 'y')

if IS_PRODUCTION:
    from .conf.production.settings import *
else:
    from .conf.development.settings import *

# Application definition
INSTALLED_APPS = [
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Enable the inner home (home)   
    'apps.registro',  
    'apps.marketplace',  

]

AUTH_USER_MODEL = 'registro.Usuario'  # Substitua 'app' pelo nome do seu app

LOGIN_REDIRECT_URL = '/login/'  # Redireciona para a página inicial, por exemplo
LOGOUT_REDIRECT_URL = '/login/'  # Substitua pela URL desejada, como a página de login




LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}



# configurações servem apenas para send_common (SMTP using DJango)
EMAIL_HOST = 'smtp.xxxxxxxxx.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@projetosd.com.br'
EMAIL_HOST_PASSWORD = 'xxxxxxxxxx' 
DEFAULT_FROM_EMAIL = 'no-reply@projetosd.com.br'
DEFAULT_REPLY_TO = 'falecom@projetosd.com.br'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'pt-br'

USE_I18N = True
USE_L10N = True

USE_TZ = True
TIME_ZONE = 'America/Recife'