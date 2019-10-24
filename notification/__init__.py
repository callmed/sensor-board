# Copyright (C) 2001-2007 Python Software Foundation
# Author: xxx
# Contact: xxx

"""A package for ...."""

__version__ = '1.0'
__all__ = [
            'notification.JournalCtlNotification'
]

import logging
from platform import system
from sys import exit

logger = logging.getLogger(__name__)

try:
    from systemd import journal
    from .notification import JournalCtlNotification
except ImportError:
    if system() != "Linux":
        logger.exception(
                "NOTE: Journald notifications are not available in MS Windows")
    exit(1)
