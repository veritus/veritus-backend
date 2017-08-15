from .base import *
import raven

DEBUG = False

# We only want to add sentry in production
INSTALLED_APPS.append(
    'raven.contrib.django.raven_compat',
)

RAVEN_CONFIG = {
    'dsn': os.environ["SENTRY_DSN"],
}

LOGGING['handlers'].update({'sentry': {
    'level': 'ERROR', # To capture more than ERROR, change to WARNING, INFO, etc.
    # Only want to log to sentry in production. Otherwise we log to console
    'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
    'formatter': 'verbose'
}}),

LOGGING['loggers'].update({'raven': {
    'level': 'DEBUG',
    'handlers': ['console'],
    'propagate': False,
}}),


LOGGING['loggers'].update({'sentry.errors' : {
    'level': 'DEBUG',
    'handlers': ['console'],
    'propagate': False,
}})
