from systemd import journal
import time
import logging


logger = logging.getLogger("sensorboard")


class Notification:
    __sensor_node = None
    __sensor_id = None
    __sensor_name = None

    def __init__(self, msg, msg_id, **kwargs):
        self.message = msg
        self.message_id = msg_id

    def update(self, temperature, humidity, timestamp=time.time()):
        self.temperature = temperature
        self.humidity = humidity
        self.timestamp = timestamp

    def send(self):
        payload = {
            "PRIORITY": journal.LOG_INFO,
            "SENSOR_NODE": self.__sensor_node,
            "SENSOR_ID": self.__sensor_id,
            "SENSOR_NAME": self.__sensor_name,
            "SENSOR_MEA_TIMESTAMP": self.timestamp,
            "MESSAGE_ID": self.message_id,
            "SENSOR_MEA_TEMPERATURE": self.temperature,
            "SENSOR_MEA_HUMIDITY": self.humidity
        }
        journal.send(self.message, **payload)

    def __str__(self):
        return f"Node:={self.__sensor_node} SID:={self.__sensor_id} \
                MSG:={self.message} MSGID:={self.message_id}"

    def __repr(self):
        return f"<Notification('{self.message}', {self.message_id})>"
