import logging

def error(message):
    """
    Wrapper for the sentry logger to make sure it exists.
    It only exists in production so if we are in development
    we do not want to send the message to sentry
    """
    try:
        sentry = logging.getLogger('sentry.error')
        sentry.error(message)
    except BaseException:
        console = logging.getLogger('console')
        console.error(message)

def info(message):
    try:
        sentry = logging.getLogger('sentry.error')
        sentry.info(message)
    except BaseException:
        console = logging.getLogger('console')
        console.info(message)
