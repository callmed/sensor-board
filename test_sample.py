import sensors.boards as boards
import logging
from sensors.sensors import PIN_SENSOR_DHT22, PIN_SENSOR_LIGHT, RASPBERRYPI
from os import uname, path
from sys import exit


def main():

    sensorboard = boards.SensorBoard(node="RPI-BRD",
                                     pins={
                                        "ptemp": PIN_SENSOR_DHT22,
                                        "plight": PIN_SENSOR_LIGHT},
                                     simulation=False)
    sensorboard.display_init()
    path_image = path.join(path.getcwd(), "data/test.pbm")
    logger.info(f"Image file: {path_image}")
    sensorboard.display_logo(path_image)


if __name__ == "__main__":
    import logging.config
    # Load the logging configuration
    logging.config.fileConfig('data/logging.conf',
                              defaults={"logfilename": "mylog.log",
                                        'disable_existing_loggers': False}
                              )
    logger = logging.getLogger("sensorboard")
    if not uname()[4][:3] == "arm":
        exit(1)
    main()
