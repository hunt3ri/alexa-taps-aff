from taps_aff import logger


class NotFound(Exception):
    """ Custom exception to indicate nothing found for request """
    def __init__(self, message):
        if logger:
            logger.info(message)


class TapsAffError(Exception):
    """ Custom exception to alert there's a general problem in the app """
    def __init__(self, message):
        if logger:
            logger.error(message)
