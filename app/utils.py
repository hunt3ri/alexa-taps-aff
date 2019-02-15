import logging


class NotFound(Exception):
    """ Custom exception to indicate nothing found for request """
    def __init__(self, message):
        logger = logging.getLogger("taps_aff")

        if logger:
            logger.error(message)


class TapsAffError(Exception):
    """ Custom exception to alert there's a general problem in the app """
    def __init__(self, message):
        logger = logging.getLogger("taps_aff")

        if logger:
            logger.error(message)
