from uuid import uuid4
from random import uniform, randint
# import threading
import logging


RASPBERRYPI = False
logger = logging.getLogger("sensorboard")


try:
    # Non-existent modules on non-raspberry pi systems
    import Adafruit_DHT
    import RPi.GPIO as GPIO
    # Display
#    import Adafruit_GPIO.SPI as SPI
#    import Adafruit_SSD1306
    # Image functions
#    from PIL import Image
#    from PIL import ImageDraw
#    from PIL import ImageFont
    RASPBERRYPI = True
except ImportError:
    RASPBERRYPI = False
    logger.warning("Module not found")

PIN_SENSOR_DHT22 = 4
PIN_SENSOR_LIGHT = 27


class SensorBase:
    """ Class SensorBase only includes a minimum of functions to handle sensors.
        Simulating sensor values is possible by attribute.
    """
    __sensor_index = 0

    def __init__(self, name=None, node=None, description=None):
        self.logger = logging.getLogger("sensorlogger")
        SensorBase.__sensor_index += 1
        self._uuid = uuid4()
        self.name = name
        self.node = node
        self.description = description
        self._number_of_readings = 0
        self._last_reading = None
        self.logger.debug(f"<{__class__.__name__} Instance created: "
                          f"UUID={self._uuid}, name={self.name}@{self.node}, "
                          f"description={self.description}>")

    def read(self):
        """ Read and return values from real hardware sensors."""
        self._number_of_readings += 1
        self.logger.info(f"<{__class__.__name__} uuid={self._uuid}> "
                         f"Sensor communication active")
        self.logger.debug(f"<{__class__.__name__} uuid={self._uuid}> "
                          f"Total readings: {self._number_of_readings} "
                          f"Last reading: {self._last_reading}")
        return self._last_reading

    @staticmethod
    def _simulate_sensor(lower_limit=0, higher_limit=100, random_int=False):
        """ Return a random float value within 'lower' and 'higher' limit. """
        if not random_int:
            return uniform(lower_limit, higher_limit)
        else:
            return randint(0, 1)

    def __str__(self):
        return f"<Sensor: UUID: {self._uuid} NAME: {self.name} " \
               f"NODE: {self.node} DESCR.:{self.description}: " \
               f"LAST-READ: {self._last_reading} " \
               f"TOTAL-READINGS: {self._number_of_readings}>"

    def __repr__(self):
        return f"<SensorBase({self._uuid}, {self.name}, " \
            f"{self.node}, {self.description})>"


class SensorLight(SensorBase):
    def __init__(self, pin, name=None, node=None,
                 description=None, simulation=False):
        SensorBase.__init__(self, name, node, description)
        self.logger = logging.getLogger("sensorlogger")
        self._simulation = simulation
        self._pin = pin
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self._pin, GPIO.IN)
        except NameError:
            if RASPBERRYPI:
                logger.warning("Something went wrong. "
                               "GPIO module not loaded correctly")
        self.logger.debug(f"<{__class__.__name__} Instance created: "
                          f"UUID={self._uuid}, Name={self.name}@{self.node}, "
                          f"pin={self._pin} "
                          f"description={self.description}>")

    def read(self, threaded=True):
        if not self._simulation:
            # sensor level is inverted!
            sensor_reading = not GPIO.input(PIN_SENSOR_LIGHT)
        else:
            self.logger.warning(f"<{__class__.__name__} uuid={self._uuid}> "
                                f"Simulate sensor reading")
            sensor_reading = self._simulate_sensor(random_int=True)
        self._last_reading = bool(sensor_reading)
        super(SensorLight, self).read()
        if not threaded:
            return self._last_reading

    def __repr__(self):
        return f"<SensorBase({self._uuid}, {self._pin}, {self.name}, " \
            f"{self.node}, {self.description}, {self._simulation})>"


class SensorDHT22(SensorBase):
    try:
        __sensor_type = Adafruit_DHT.DHT22
    except NameError:
        if RASPBERRYPI:
            logger.warning("Something went wrong. "
                           "Adafruit module not loaded correctly")

    def __init__(self, pin, name=None, node=None,
                 description=None, simulation=False):
        SensorBase.__init__(self, name, node, description)
        self.logger = logging.getLogger("sensorlogger")
        self._simulation = simulation
        self._pin = pin

        self.logger.debug(f"<{__class__.__name__} Instance created: "
                          f"UUID={self._uuid}, Name={self.name}@{self.node}, "
                          f"pin={self._pin} "
                          f"description={self.description}>")

    def read(self, threaded=True):
        """ Read function for hardware sensor explicitely."""
        if not self._simulation:
            humidity, temperature = Adafruit_DHT.read_retry(
                                        SensorDHT22.__sensor_type, self._pin)
        else:
            self.logger.warning(f"<{__class__.__name__} uuid={self._uuid}> "
                                f"Simulate sensor reading")
            temperature = self._simulate_sensor(lower_limit=14,
                                                higher_limit=35)
            humidity = self._simulate_sensor(lower_limit=50, higher_limit=100)
        self._last_reading = (round(humidity, 2), round(temperature, 2))
        super(SensorDHT22, self).read()
        if not threaded:
            return self._last_reading

    def __str__(self):
        return f"<Sensor: UUID: {self._uuid} NAME: {self.name} " \
               f"NODE: {self.node} DESCR.:{self.description}: " \
               f"LAST-READ: {self._last_reading[0]}%, " \
               f"{self._last_reading[1]}°C, " \
               f"TOTAL-READINGS: {self._number_of_readings}>"

    def __repr__(self):
        return f"<SensorBase({self._uuid}, {self._pin}, {self.name}, " \
            f"{self.node}, {self.description}, {self._simulation})>"
