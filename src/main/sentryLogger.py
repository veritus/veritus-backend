import logging

def error(message):
    """
    Wrapper for the sentry logger to make sure it exists.
    It only exists in production so if we are in development
    we do not want to send the message to sentry
    """
    sentry = logging.getLogger('sentry.error')
    sentry.error(message)

def warning(message):
    sentry = logging.getLogger('sentry.error')
    sentry.warning(message)
