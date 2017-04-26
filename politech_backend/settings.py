"""
Django settings for politech_backend project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DATA_FOLDER = os.path.join(BASE_DIR, 'case_gather','test_data/')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't8&(jop7)*h!v5eug$iufd8l1(l2dpfjxj=(+2xt5knv+7v-!='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'case_gather',
    'django_cron',
    'promises',
    'tags',
    'rest_framework',
    'rest_framework.authtoken',
    'main',
    'parliament',
    'party',
    'district',
    'rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'corsheaders',
]
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'politech_backend.urls'

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

WSGI_APPLICATION = 'politech_backend.wsgi.application'

CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
)

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'politech',
        'USER': os.environ["DB_USER"],
        'PASSWORD': os.environ["DB_PASS"],
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'cronJobHandler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/cronJobs.log',
            'formatter': 'verbose'
        },
        'xmlHelperHandler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/xmlHelper.log',
            'formatter': 'verbose'
        },
        'cronJobServicesHandler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/cronJobServices.log',
            'formatter': 'verbose'
        },
        'xmlParserHandler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/xmlParser.log',
            'formatter': 'verbose'
        },
        'promiseHandler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/promise.log',
            'formatter': 'verbose'
        },

    },
    'loggers': {
        'cronJobs': {
            'handlers': ['cronJobHandler'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'xmlHelper': {
            'handlers': ['xmlHelperHandler'],
            'propagate': True,
            'level': 'DEBUG'
        },
        'xmlParser': {
            'handlers': ['xmlParserHandler'],
            'propagate': True,
            'level': 'DEBUG'
        },
        'cronJobServices': {
            'handlers': ['cronJobServicesHandler'],
            'propagate': True,
            'level': 'DEBUG'
        },
        'promise': {
            'handlers': ['promiseHandler'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}

CRON_CLASSES = [
    "case_gather.cronJobs.gather_cases"
    # "promises.cronJobs.connect_cases_and_promises"
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
REST_SESSION_LOGIN = False
