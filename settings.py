from pathlib import Path
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------- SECURITY ----------------

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-temp")

DEBUG = True

ALLOWED_HOSTS = []

# ---------------- INSTALLED APPS ----------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # custom app
    'twilioapp',
]

# ---------------- MIDDLEWARE ----------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------- URL CONFIG ----------------

ROOT_URLCONF = 'twilioproject.urls'

WSGI_APPLICATION = 'twilioproject.wsgi.application'

# ---------------- DATABASE ----------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------- TEMPLATES ----------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # main templates folder
        'DIRS': [BASE_DIR / 'templates'],

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

# ---------------- PASSWORD VALIDATION ----------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------- LANGUAGE ----------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'   # better for India

USE_I18N = True
USE_TZ = True

# ---------------- STATIC ----------------

STATIC_URL = '/static/'

# STATICFILES_DIRS = [
#     BASE_DIR / "static",
# ]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------- LOGIN SYSTEM ----------------

LOGIN_URL = 'team_login'
LOGIN_REDIRECT_URL = 'sms_page'
LOGOUT_REDIRECT_URL = 'home'

# ---------------- TWILIO ----------------

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
WHATSAPP_FROM = os.getenv("WHATSAPP_FROM")