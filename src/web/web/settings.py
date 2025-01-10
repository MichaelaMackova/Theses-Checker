"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from decouple import config, Choices, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# TODO: set in file .env
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# TODO: set in file .env: production - False; development - True
DEBUG = config('DEBUG', default=False, cast=bool)

# WARNING: update this when you have the production host
# TODO: set in file .env: Allowed values: 'Linux', 'Windows'
OPERATING_SYSTEM = config('OPERATING_SYSTEM', cast=Choices(['Linux', 'Windows']))

# WARNING: update this when you have the production host
# MAX_STORAGE_SPACE (int|None): maximum storage space in bytes, if None, maximum storage space is determined by the system (WARNING: only for Linux, for Windows ignored)
# TODO: set in file .env: Allowed values: None or integer number
MAX_STORAGE_SPACE : (int|None) = None if config('MAX_STORAGE_SPACE', default=None) == None else config('MAX_STORAGE_SPACE', cast=int)

# TODO: set in file .env
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost, 127.0.0.1, [::1]', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}


FORCE_SCRIPT_NAME = config('FORCE_SCRIPT_NAME', default=None)
CSRF_COOKIE_PATH = config('CSRF_COOKIE_PATH', default='/')


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

STATIC_URL = config('STATIC_URL', default='static/')

# Define STATIC_ROOT
relative_static_root = config('RELATIVE_STATIC_ROOT', default=None)
STATIC_ROOT = os.path.join(BASE_DIR, relative_static_root) if relative_static_root is not None else None

STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "static" / "css",
    BASE_DIR / "static" / "js",
    BASE_DIR / "static" / "favicon",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Set this to True to avoid transmitting the session cookie over HTTP accidentally.
CSRF_COOKIE_SECURE = True
