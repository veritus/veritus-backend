import logging

def logToSentry(message):
    """
    Wrapper for the sentry logger to make sure it exists.
    It only exists in production so if we are in development
    we do not want to send the message to sentry
    """
    try:
        sentry = logging.getLogger('sentry.error')
        sentry.error(message)
    except BaseException:
        # We send the error to the cronlog file as that is
        # mounted to the host and can be viewed there
        logger = logging.getLogger('cronJobServices')
        logger.error(message)
