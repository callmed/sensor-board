import logging
from sys import exit
from platform import system

logger = logging.getLogger(__name__)

try:
    from systemd import journal
except ModuleNotFoundError:
    logger.exception(
                "NOTE: Journald notifications are not available in MS Windows "
                "on Linux install the missing package")
    exit(1)

except ImportError:
    if system() != "Linux":
        logger.exception(
                "NOTE: Journald notifications are not available in MS Windows")
    exit(1)


__all__ = ["JournalCtlNotification"]


class JournalCtlNotification:
    """ This class sends data into journal.
        At the beginning every instance's payload is completely empty and
        must be filled with a dictionary.

        Broadcasting an instance send always the complete payload to journal.
    """

    def __init__(self, message_id, node_id, sensor_id):
        self.logger = logging.getLogger("notifier.journal")
        self.__message_id = message_id
        self.__node_id = node_id
        self.__sensor_id = sensor_id
        self._payload = dict()
        self.logger.debug(f"<{__class__.__name__} Instance created: "
                          f"message-id={self.__message_id}, "
                          f"source={self.__sensor_id}@{self.__node_id}>")

    def update(self, **kwargs) -> bool:
        """ Changes the value of given keywords. Not existing keywords
            are ignored and FALSE is returned.
        """
        error_update = False
        for key, value in kwargs:
            try:
                self._payload[key] = value
            except KeyError:
                logger.warning(f"Unknow key cannot be updated, {key, value}")
                error_update = True
                continue
        return error_update is False

    def payload_init(self, keywords: list) -> bool:
        """ Should be called after class initialization with a list of valid
            keywords. The initial value is NONE for each.
        """
        print(f"Keywords-Type:{type(keywords)}")
        if keywords is not None:
            try:
                self._payload = {k: None for k in keywords}
            except KeyError:
                logger.debug("Error in payload initialization")
        return self._payload is not None

    @property
    def payload(self):
        """ Returns the current payload. """
        return self._payload

    def broadcast(self) -> bool:
        """ Sends payload to journal if not empty. """
        if self._payload is not None:
            journal.send(str(self.__message_id), self._payload)
            logger.info(f"Notification ({self.__message_id}) broadcasted")
        else:
            logger.warning("Notification not broadcasted due to empty payload")

    @property
    def keywords(self, keywords=None) -> dict:
        """ All keywords available in instance are returned as dictionary.
            If a list of keywords is provided, a dictionary containing only
            these keywords is returned.
        """
        if keywords is None:
            return self._payload.items()
        else:
            temp_payload = dict()
            for key in keywords.keys():
                try:
                    temp_payload[key] = self._payload[key]
                except KeyError:
                    logger.debug(f"Unknown Key-Value {key} requested")
                    continue
                finally:
                    return temp_payload

    def __str__(self):
        return f"SENSOR: {self.__sensor_id}@{self.__node_id}; " \
               f"MESSAGE-ID: {self.__message_id} ; PAYLOAD: {self._payload}"

    def __repr(self):
        return f"<Notification({self.__message_id}, {self.__node_id}, " \
               f"{self.__sensor_id})>"
