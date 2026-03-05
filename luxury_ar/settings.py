import os
import dj_database_url
from pathlib import Path

# --- BASE DIRECTORY ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY WARNINGS ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-unique-key-here')
DEBUG = True

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']

# --- APPLICATION DEFINITION ---
INSTALLED_APPS = [
    'cloudinary_storage',         # 1. Cloudinary Storage (Must be top)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # 2. Django Static Files
    'cloudinary',                 # 3. Cloudinary Base
    'rest_framework',
    'corsheaders',
    'furniture',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serves static files on Render
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'luxury_ar.urls'

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

WSGI_APPLICATION = 'luxury_ar.wsgi.application'

# --- DATABASE CONFIGURATION ---
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:Bilal1234@127.0.0.1:5432/AR&3D_db',
        conn_max_age=600
    )
}

# --- CLOUDINARY CONFIGURATION ---
CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
API_KEY = os.environ.get('CLOUDINARY_API_KEY')
API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

# Fail-Fast Validation for Production
if not DEBUG and not all([CLOUD_NAME, API_KEY, API_SECRET]):
    raise ValueError("CRITICAL ERROR: Missing one or more Cloudinary Environment Variables on Render!")

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUD_NAME,
    'API_KEY': API_KEY,
    'API_SECRET': API_SECRET,
    'SECURE': True,
}

# --- STATIC & MEDIA CONFIGURATION ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = f'https://res.cloudinary.com/{CLOUD_NAME}/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- STORAGE ENGINES ---
# Bypassing WhiteNoise compression to prevent Django 5.1 FileNotFoundError crashes
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Legacy setting required by django-cloudinary-storage to prevent AttributeError
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- SYSTEM SETTINGS ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True

# Upload limits for 3D Models and Images
FILE_UPLOAD_TEMP_DIR = '/tmp'
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_MAX_MEMORY_SIZE = 2097152      # 2MB in bytes
DATA_UPLOAD_MAX_MEMORY_SIZE = 150000000    # ~143MB
