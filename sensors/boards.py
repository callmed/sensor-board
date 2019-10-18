import sensors.sensors as sensors
from datetime import datetime
from datastorage.database_declaration import MeasurementModel, exc
from uuid import uuid4
import threading
import logging

RASPBERRYPI = False
logger = logging.getLogger("sensorboard")

try:
    # Non-existent modules on non-raspberry pi systems
    # Display
    import Adafruit_SSD1306
    # Image functions
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
    RASPBERRYPI = True
except ImportError:
    RASPBERRYPI = False
    logger.warning("Module not found")


# payload for class Notification
# payload = {
#     "PRIORITY": journal.LOG_INFO,
#     "SENSOR_NODE": self.__sensor_node,
#     "SENSOR_ID": self.__sensor_id,
#     "SENSOR_NAME": self.__sensor_name,
#     "SENSOR_MEA_TIMESTAMP": self.timestamp,
#     "MESSAGE_ID": self.message_id,
#     "SENSOR_MEA_TEMPERATURE": self.temperature,
#     "SENSOR_MEA_HUMIDITY": self.humidity
# }

class SensorBoard:
    def __init__(self, node=None, pins={
                                        "ptemp": sensors.PIN_SENSOR_DHT22,
                                        "plight": sensors.PIN_SENSOR_LIGHT},
                 description=None, simulation=False):
        self.logger = logging.getLogger(__name__)
        self._uuid = uuid4()
        self.node = node
        self.description = description
        self._simulation = simulation
        self._data_storage = []
        self.pin_temp = pins["ptemp"]
        self.pin_light = pins["plight"]

        self.sensor_temperature = sensors.SensorDHT22(
                                                pin=self.pin_temp,
                                                name="Env.-Sensor",
                                                node=self.node,
                                                simulation=self._simulation)
        self.sensor_light = sensors.SensorLight(
                                                pin=self.pin_light,
                                                name="Light-Sensor",
                                                node=self.node,
                                                simulation=self._simulation)

        self.logger.debug(f"<{__class__.__name__} Instance created: "
                          f"UUID={self._uuid}, Node={self.node}, "
                          f"description={self.description}>")

    def read(self, threaded=True):
        threads = []

        thread_sensor_temp = threading.Thread(
                                        target=self.sensor_temperature.read())
        threads.append(thread_sensor_temp)
        thread_sensor_light = threading.Thread(
                                        target=self.sensor_light.read())
        threads.append(thread_sensor_light)

        for index, th in enumerate(threads):
            self.logger.debug(f"<Sensor-Thread {index} started")
            th.start()

        for thread in threads:
            thread.join()

        self._last_timestamp = datetime.now()
        self._last_reading = (self.sensor_temperature._last_reading
                              + (self.sensor_light._last_reading, ))
        return (self._last_reading + (self._last_timestamp, ))

    def store(self, value_return=False):
        self.read()
        self.logger.info(f"<{__class__.__name__} "
                         f"UUID={self._uuid}, Node={self.node}: "
                         f"Sensor data stored")
        self._data_storage.append(self._last_reading
                                  + (self._last_timestamp, ))
        if value_return:
            return self._data_storage[-1]
        return len(self._data_storage)

    def list(self):
        """ Show stored data. Testing purpose only."""
        print(f"Data-Storage: {self._data_storage}")

    def store2database(self, database) -> bool:
        database_conn = database

        humidity, temperature, light, timestamp = self.store(value_return=True)

        new_entity = MeasurementModel(node_uuid=str(self._uuid),
                                      timestamp=timestamp,
                                      temperature=temperature,
                                      humidity=humidity,
                                      pressure=None,
                                      light_on=light)
        database_conn.add(new_entity)
        database_conn.commit()
        self.logger.debug(f"<{__class__.__name__} Database updated: "
                          f"UUID={self._uuid}, Node={self.node}>")
        return True

    def display_init(self):
        rst = 24
        # 128x64 display with hardware I2C:
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=rst)
        # Initialize library.
        self.disp.begin()
        # Clear display
        self.disp.clear()
        self.disp.display()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.image = Image.new('1', (self.disp.width, self.disp.height))
        self.draw = ImageDraw.Draw(self.image)

    def display_logo(self, path_logo=None):
        """ Load monochrome bitmap and show it on display."""
        if self.disp.height == 64:
            image = Image.open(path_logo).convert("1")
            logger.debug("Image loaded for 64 pixel height-display")
        else:
            image = Image.open(path_logo).convert("1")
            logger.debug("Image loaded for 32 pixel height-display")
        # Display image
        logger.debug("Display image now")
        self.disp.image(image)
        self.disp.display()

    def display_values(self):
        value_temp = 0
        value_humi = 0
        value_light = False
        time = None

        value_humi, value_temp, value_light, time = self._data_storage[-1]

        width = self.disp.width
        height = self.disp.height
        padding = -2
        top = padding
        # bottom = height-padding
        x = 0

        # Load default font
        font = ImageFont.load_default()

        self.draw.rectangle((0, 0, width, height), outline=0, fill=0)
        self.draw.text((x, top), "Sensor-Board v1", font=font, fill=255)
        self.draw.text((x, top+8), f"T:{value_temp}°C H:{value_humi}%",
                       font=font, fill=255)
        self.draw.text((x, top+16), f"L:{value_light}", font=font, fill=255)
        self.draw.text((x, top+24), f"{time}", font=font, fill=255)

        self.disp.image(self.image)
        self.disp.display()

    def __str__(self):
        return f"<Sensor-Board: UUID: {self._uuid} NODE: {self.node} "
        f"DESCR.:{self.description}: "
        f"LAST-READ: {self._last_reading[0]}%, "
        f"{self._last_reading[1]}°C, "
        f"{self._last_reading[2]}, timestamp: {self._last_timestamp}>"

    def __repr__(self):
        return f"<SensorBoard({self._uuid}, {self.node}, " \
               f"{self.description}, {self._simulation})>"

    def write_to_db(self) -> bool:
        """ Save received data to database"""
        if self._last_reading is not None and self._database is not None:
            try:
                new_measurement = MeasurementModel(
                                    sensor_id=self.id,
                                    timestamp=datetime.now(),
                                    temperature=round(self._last_reading, 2))
                self._database.add(new_measurement)
                return self._database.commit()
            except exc.SQLAlchemyError as e:
                print(f"Database write not possible {e}")
        else:
            logger.warning(f"Sensor <self.name>: Could not write data to "
                           f"database. No database connection!")
            return False

    def average(self, consider_last=5):
        """ Return the average value of 'consider_last' available
            measurements in database.
        """
        query = f"""SELECT avg(temperature), avg(humidity), avg(pressure)
                FROM ( SELECT * FROM measurements ORDER by id
                DESC LIMIT {consider_last})"""
        if self._last_reading is not None and self._database is not None:
            result = self._database.execute(query)
            for avg_temp, avg_humi, avg_pres in result:
                return avg_temp, avg_humi, avg_pres
