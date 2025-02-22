from pathlib import Path
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-qub@7k3%5^6j+bva4_2_ikijzgf0mne%qthz4wiz3d(xwu1ao-"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True   

ALLOWED_HOSTS = ['localhost' , '127.0.0.1' , '192.168.1.6']  # Add your domain/IP here

APPEND_SLASH=True
# Application definition

INSTALLED_APPS = [
    'jazzmin',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "Layali_elhelmia",
    "pgcrypto",
   


]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',  # أضف هذا السطر هنا


]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates'),
        os.path.join(BASE_DIR, 'templates/errors'),],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"
ASGI_APPLICATION = "Layaly_elhelmia.routing.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
password_key = os.getenv("DATABASE_KEY").encode()
f = Fernet(password_key)
DATABASES = {

    'default': {
        'ENGINE': str(f.decrypt(b'gAAAAABnoTB4OfIMh1e4qb1woIqezv9icpYsHlT1UQAN7yOG4eYMCnZbnrGtXWgWmu8p1FyOPlYPoFbK6k6fkzf2SAeeXg0T5jp-2zrcE_CZrrEP3SfpXf8=')).split('\'')[1],
        'NAME': str(f.decrypt(b'gAAAAABnoTA9olO_gIlZi2GYm1JwzQwvl-uEGKSwkWh8v6eYVLL2VSwN0Y4jqMV7RrkNLmngm01YCjybTacji-HokciJZHQ4Gw==')).split("'")[1],
        'USER': str(f.decrypt(b'gAAAAABnoTD6vKayoHaAvxnfIofVQPCS5xQEbxAd3AnkBImCgOEL3d6oz-ZBPfgUKPr4Lh10eJ7frGADIJS7WLHLYKEZuk-TsQ==')).split("'")[1],
        'PASSWORD': str(f.decrypt(b'gAAAAABnnkTdDUgq5X-KBQ-N_7EMhO4SimA8VEEPtcuJuQOaFanDXddy3SVKFZ0Fc0JcwjOUnqKFU8PR3h7IsUMYdkjRuh_CCcUjT8CvGtMgnn4eqKPKkqg=')).split("'")[1],
        'HOST': 'localhost',
        'PORT': str(f.decrypt(b'gAAAAABnoTEwNGtRPMUZgZVfgl17bJv96IpWo9NjGxC8lUbg3J3ceDp8S9yM63ISbYEHs1m_8kJQWqa9kmlljgAUgiInkA6tYA==')).split("'")[1],
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Dubai"

USE_I18N = True

USE_TZ = True

PGCRYPTO_DEFAULT_KEY = os.environ.get('FIELD_ENCRYPTION_KEY').encode()# Must be 32 bytes

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'Layali_elhelmia.Admins'

JAZZMIN_SETTINGS = {
    "site_title": "Layali ElHelmia Admin Portal",
    "site_header": "Layali ElHelmia Administration",
    "site_brand": "Layali ElHelmia",
    "welcome_sign": "Welcome to the Layali ElHelmia Admin Panel",
    "site_logo": '../static/images/main-img/logo.png',
    # ... other Jazzmin settings ...
}
MAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'layalyelhelmiaorders@gmail.com' #sender's email-id
EMAIL_HOST_PASSWORD= 'cfqa fmhr kqbj mero'