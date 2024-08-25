import json
import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(setting)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_secret('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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


LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Google Oauth 2.0 setting
GOOGLE_CLIENT_ID = get_secret('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = get_secret('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = get_secret('GOOGLE_REDIRECT_URI')

# Kakao Oauth 2.0 setting
KAKAO_CLIENT_ID = get_secret('KAKAO_CLIENT_ID')
KAKAO_REDIRECT_URI = get_secret('KAKAO_REDIRECT_URI')

# Twitter Oauth 1.0 setting
TWITTER_API_KEY = get_secret('TWITTER_API_KEY')
TWITTER_API_SECRET_KEY = get_secret('TWITTER_API_SECRET_KEY')
TWITTER_OAUTH1_REDIRECT_URI = get_secret('TWITTER_OAUTH1_REDIRECT_URI')

# Twitter Oauth 2.0 setting
TWITTER_CLIENT_ID = get_secret('TWITTER_CLIENT_ID')
TWITTER_CLIENT_SECRET = get_secret('TWITTER_CLIENT_SECRET')
TWITTER_OAUTH2_REDIRECT_URI = get_secret('TWITTER_OAUTH2_REDIRECT_URI')
