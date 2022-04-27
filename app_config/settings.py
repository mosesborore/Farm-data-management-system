import os
import warnings
from pathlib import Path

import dj_database_url
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY and DEBUG:
    warnings.warn("SECRET_KEY not configured, using a random temporary key.")
    SECRET_KEY = get_random_secret_key()


def get_list(text):
    return [item.strip() for item in text.split(",")]


ALLOWED_HOSTS = get_list(os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1"))

INTERNAL_IPS = ["127.0.0.1"]

OPENWEATHER_API_KEY = os.environ.get(
    "OPENWEATHER_API_KEY", "a3fe7f88aab145543cf50a8d30d16a8f"
)
if not OPENWEATHER_API_KEY:
    warnings.warn("OPENWEATHER_API_KEY not configured")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # "debug_toolbar",
    # Local app
    "account",
    "farm",
    "input",
    "farming",
    "task",
    "weather",
    # External apps
    "widget_tweaks",
    "django_prices",
    "versatileimagefield",
    "phonenumber_field",
    "tinymce",
]

AUTH_USER_MODEL = "account.Login"

LOGIN_URL = "/account/login"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "app_config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR.joinpath("templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
            ],
        },
    },
]

WSGI_APPLICATION = "app_config.wsgi.application"

# DATABASES
DATABASES = {}
if os.environ.get("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.config(
        default=os.environ.get("DATABASE_URL"), conn_max_age=300
    )
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "FarmData",
            "USER": "orion",
            "PASSWORD": "orion-master",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    }
]

DEFAULT_COUNTRY = os.environ.get("DEFAULT_COUNTRY", "KE")
DEFAULT_CURRENCY = os.environ.get("DEFAULT_CURRENCY", "KSH")
DEFAULT_DECIMAL_PLACES = 2
DEFAULT_MAX_DIGITS = 12
DEFAULT_CURRENCY_CODE_LENGTH = 3


# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Nairobi"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# MEDIA
MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR.joinpath("media"))

# static
STATIC_URL = "/static/"
STATICFILES_DIRS = (str(BASE_DIR.joinpath("static")),)
STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# PHONE-NUMBER FIELD
PHONENUMBER_DEFAULT_REGION = "KE"
PHONENUMBER_DB_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_FORMAT = "NATIONAL"

# VERSATILE SETTINGS
VERSATILEIMAGEFIELD_SETTINGS = {
    # images should be pre-generated
    "create_images_on_demand": False,
}

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    "user_avatars": [
        ("default", "thumbnail__445x445"),
        ("profile_medium", "thumbnail__300x300"),
    ]
}

TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 300,
    "menubar": False,
    "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
    "fullscreen,table,paste,"
    "help,wordcount",
    "toolbar": "undo redo | formatselect | "
    "bold italic |"
    "bullist outdent indent | "
    "removeformat | help",
}
