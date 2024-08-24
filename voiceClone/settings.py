from pathlib import Path
import mongoengine
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
APPEND_SLASH = False
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0v7h3n#=jj!bhybxiu&a!&4831l!2#e9(szm233a2f(#1os7d%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'corsheaders',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'myapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
]

CORS_ALLOW_HEADERS = [
    'Content-Type',
    'Authorization',
]
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
ROOT_URLCONF = 'voiceClone.urls'

ALLOWED_HOST = [
    'http://localhost:3000',
]
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

WSGI_APPLICATION = 'voiceClone.wsgi.application'

# MongoDB settings
MONGODB_DATABASE_NAME = 'voiceCloneapp'
MONGODB_HOST = 'mongodb+srv://barsoremi61:xN438NN5wdKKMuD5@voiceclone.sfivx.mongodb.net/?retryWrites=true&w=majority&appName=voiceClone'
MONGODB_PORT = 27017

# Connect to MongoDB
mongoengine.connect(
    db=MONGODB_DATABASE_NAME,
    host=MONGODB_HOST,
    port=MONGODB_PORT
)

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 465  # or 587 for TLS
EMAIL_USE_SSL = True  # Use SSL for port 465
EMAIL_USE_TLS = False  # TLS should be False if SSL is True
EMAIL_HOST_USER = 'admin@codesignite.com'
EMAIL_HOST_PASSWORD = 'Abayomi1994@'
DEFAULT_FROM_EMAIL = 'admin@codesignite.com'



