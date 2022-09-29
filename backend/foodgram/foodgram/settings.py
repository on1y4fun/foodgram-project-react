import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '^(o9q205e*=ah&q&1xtgd)(&hg5b_9yai8jt91mft_!(0)95&o'

DEBUG = True

load_dotenv(dotenv_path=os.path.join(os.path.dirname(BASE_DIR), 'infra/.env'))


ALLOWED_HOSTS = ['127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'recipes.apps.RecipesConfig'
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

ROOT_URLCONF = 'foodgram.urls'

# TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
print(os.path.dirname(os.path.dirname(BASE_DIR)))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.dirname(os.path.dirname(BASE_DIR))],
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

WSGI_APPLICATION = 'foodgram.wsgi.application'

DATABASES = {
    'default': {
        # 'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.postgresql'),
        # 'NAME': os.getenv('DB_NAME', default='postgres'),
        # 'USER': os.getenv('POSTGRES_USER', default='postgres'),
        # 'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
        # 'HOST': os.getenv('DB_HOST', default='127.0.0.1'),
        # 'PORT': os.getenv('DB_PORT', default='8000')
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static/'),)

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
