import sys
import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = "sensorboard.log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_timedfile_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_rotatefile_handler():
    file_handler = RotatingFileHandler(LOG_FILE,
                                       maxBytes=(50*1024),
                                       backupCount=3)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_timedfile_handler())
    # with this pattern, it's rarely necessary to propagate
    # the error up to parent
    logger.propagate = False
    return logger

# Links:
# https://www.toptal.com/python/in-depth-python-logging
