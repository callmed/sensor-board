from systemd import journal
from uuid import uuid4
import time
import logging


logger = logging.getLogger("sensorboard.notification")


class Notification:
    """ Class to contain a flexible number of attributes to publish in
        journalctl logfile.
    """

    def __init__(self, node_id, sensor_id):
        self.logger = logging.getLogger("notifier")
        self.__uuid = uuid4()
        self._node_id = node_id
        self.sensor_id = sensor_id
        self._payload = dict()
        self.logger.debug(f"<{__class__.__name__} Instance created: "
                          f"notify_uuid={self.__uuid}, "
                          f"source={self.__sensor_id}@{self._node_id}>")

    def update(self, **kwargs):
        pass

    def init_payload(keywords: list) -> bool:
        pass

    def add_keywords(keywords: list) -> bool:
        pass

    def get_keywords(self, keywords=None) -> list:
        """ If keywords are given, only those were returned.
            Else, all keywords are returned.
        """
        pass

    def get_payload(self) -> dict:
        pass

    def update_payload(self, **kwargs) -> bool:
        pass

    def send_payload() -> bool:
        pass

    def broadcast(self) -> bool:
        journal.send(self.message, self.payload)

    def __str__(self):
        return f"Node:={self.__sensor_node} SID:={self.__sensor_id} \
                MSG:={self.message} MSGID:={self.message_id}"

    def __repr(self):
        return f"<Notification('{self.message}', {self.message_id})>"
