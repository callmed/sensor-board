#
# Author: Daniel P
# Contact: daniel.plev@gmail.com

"""A package for Journald notifications. These message type is only available
    on Linux system.
"""

import logging
from sys import stdout, exit
from platform import system


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)-7s %(asctime)-19s.%(msecs)03d |"
                              " %(funcName)s@%(name)s | %(message)s",
                              "%d.%m.%Y %H:%M:%S")
console_handler = logging.StreamHandler(stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# file_handler = logging.FileHandler(__package__ + ".log")
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

if system() != "Linux":
    logger.error("The system calling this module is not Linux but Journald "
                 "only works with Linux.")
    exit(1)

try:
    from .notification import JournalCtlNotification
except ImportError:
    logger.exception("Failure in loading module")

__version__ = '1.0'
__author__ = "Daniel P."
__all__ = ['notification']
