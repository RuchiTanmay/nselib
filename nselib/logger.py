import logging
import sys


def enable_logging(level=logging.DEBUG):
    """
    Optional helper function for developers to quickly view nselib logs to the console.
    """
    logger = logging.getLogger("nselib")
    logger.setLevel(level)

    # Check if we already have a StreamHandler to avoid duplicate logs
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
