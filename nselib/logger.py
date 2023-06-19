import logging
import sys


# Create a custom logger
def mylogger(logger):
    logger.setLevel(logging.DEBUG)
    # Create handlers
    c_handler = logging.StreamHandler(sys.stdout)
    # Create formatters and add it to handlers
    f_format = logging.Formatter('%(name)s::%(levelname)s::%(message)s')
    c_handler.setFormatter(f_format)
    # Add handlers to the logger
    logger.addHandler(c_handler)
    return logger
