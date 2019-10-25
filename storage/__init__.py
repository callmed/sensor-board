#
# Author: Daniel P
# Contact: daniel.plev@gmail.com

"""A package to store and/or save data. """


__all__ = ['storage', 'Storage']

import logging
from sys import stdout
from .storage import Storage


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)-7s %(asctime)-19s.%(msecs)03d |"
                              " %(funcName)s@%(name)s | %(message)s",
                              "%d.%m.%Y %H:%M:%S")
console_handler = logging.StreamHandler(stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(__package__ + ".log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

__version__ = '1.0'
__author__ = "Daniel P"
