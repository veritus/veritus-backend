from .base import *

DEBUG = True

LOGGING['loggers'].update({'sentry.errors': {
    'level': 'DEBUG',
    'handlers': ['console'],
    'propagate': True,
}})
