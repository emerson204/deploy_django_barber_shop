
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q(psv&9%!^x1%!6mdw4p&+uc3_th%@%62wu%#%q$m72k@_%j&*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'authentication',
    'services',
    'transactions',
    'rest_framework',
    'rest_framework_simplejwt',
]

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

# Esto de "DEFAULT_RENDERER_CLASES" sirve para evitar mostrar el formulario que nos aparecia en una interfaz cuando el metodo era POST y nos aparecia un formulario para crear los datos , ahora solo vizualesaremos JSON , esto es opcional si quieres lo pones si no no porque ya utilizas swagger
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    
    #Esto es de JWT Simple
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

ROOT_URLCONF = 'django_barber_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'django_barber_shop.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Esto sirve para indicarle a django que nuestro nuevo user es MyUserModel y no el por defecto que tiene 
AUTH_USER_MODEL = 'authentication.MyUserModel'

SIMPLE_JWT = {
  # El refresh token siempre tiene que durar mas que el access token
  'ACCESS_TOKEN_LIFETIME': timedelta(days=5), # Dias
  'REFRESH_TOKEN_LIFETIME': timedelta(weeks=2), # Semanas
}

SWAGGER_SETTINGS = {
  'SECURITY_DEFINITIONS': {
    'Bearer': {
      'type': 'apiKey',
      'name': 'Authorization',
      'in': 'header'
    }
  }
}



# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI0NTQ5MTQ2LCJpYXQiOjE3MjQxMTcxNDYsImp0aSI6ImM4Y2Q3YTJiNTM5YzRiN2M4Zjk2YWI5OGQyOWUzNzVlIiwidXNlcl9pZCI6NiwiZW1haWwiOiJkcmFnb0BnbWFpbC5jb20iLCJuYW1lIjoiZHJhZ28ifQ.1Al_0tfNxV8eXTFs6SuQjJgTG5CQQSQSoeMaq1yHqEI