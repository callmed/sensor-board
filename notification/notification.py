from systemd import journal
from uuid import uuid4
import time
import logging


logger = logging.getLogger("sensorboard.notification")


class JournalctlNotification:
    """ This class sends data into journal.
        At the beginning every instance's payload is completely empty and
        must be filled with a dictionary.

        Broadcasting an instance send always the complete payload to journal.
    """

    def __init__(self, message_id, node_id, sensor_id):
        self.logger = logging.getLogger("notifier")
        self.__message_id = message_id
        self.__node_id = node_id
        self.__sensor_id = sensor_id
        self._payload = dict()
        self.logger.debug(f"<{__class__.__name__} Instance created: "
                          f"notify_uuid={self.__message_id}, "
                          f"source={self.__sensor_id}@{self._node_id}>")

    def update(self, **kwargs) -> bool:
        """ Changes the value of given keywords. Not existing keywords
            are ignored and FALSE is returned.
        """
        pass

    def init_payload(keywords: list) -> bool:
        """ Should be called after class initialization with a list of valid
            keywords. The initial value is NONE for each.
        """
        pass

    def get_keywords(self, keywords=None) -> dict:
        """ All keywords available in instance are returned as dictionary.
            If a list of keywords is provided, a dictionary containing only
            these keywords is returned.
        """
        pass

    @property
    def payload(self):
        """ Returns the current payload. """
        return self._payload

    def broadcast(self) -> bool:
        """ Sends payload to journal if not empty. """
        if self._payload:
            journal.send(self.message, self._payload)

    # ToDo: Double check all used variables, maybe non-sense is still there!
    def __str__(self):
        return f"Node:={self.__sensor_node} SID:={self.__sensor_id} \
                MSG:={self.message} MSGID:={self.message_id}"

    def __repr(self):
        return f"<Notification('{self.message}', {self.message_id})>"
