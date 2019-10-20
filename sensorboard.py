import sys
import logging
import os
import signal
import time
import datastorage.database_declaration as db_declaration
import datastorage.data_plot as dplot
import sensors.boards as boards
import sensors.sensors as sensors

if os.uname()[4][:3] == "arm":
    sensors.RASPBERRYPI = True
else:
    sensors.RASPBERRYPI = False

try:
    # Non-existent modules?!
    import schedule
except ImportError as err:
    print(f"Could not import module, {err}. Automatic installation started")
    os.system("python -m pip install schedule")


SENSOR_TRIGGER_MINUTES = 1
DISPLAY_TRIGGER_MINUTES = 1


def signal_handler_keyboard(sig, frame):
    logger = logging.getLogger(__name__)
    logger.info("Program exits after user interruption")
    sys.exit(1)


def signal_handler_termination(sig, frame):
    logger = logging.getLogger(__name__)
    logger.info("Program terminated from outter space")
    sys.exit(1)

# ToDo: Re-desgin the basic start up proceture to run only on raspb. For data
#       presenting or analysing own scripts are used.
def main():
    if not sensors.RASPBERRYPI:
        # Print sensor data only in non-raspberry mode due to missing display
        data = dplot.read_data_from_db(db_declaration.session,
                                       db_declaration.MeasurementModel)
        dplot.plot_multiplots(data=data)
    else:
        sensorboard = boards.SensorBoard(node="RPI-BRD",
                                         pins={
                                            "ptemp": boards.PIN_SENSOR_DHT22,
                                            "plight": boards.PIN_SENSOR_LIGHT},
                                         simulation=False)
        # ToDo: Include display init into board class init
        # ToDo: Show logo after display init
        try:
            sensorboard.display_init()
        except NameError as err:
            logger.warning("Failed initialization of display", err)

        # DEMO BME280
        # schedule.every(SENSOR_TRIGGER_MINUTES).minutes.do(
        #                                    demo_bme280)

        # Gather sensor data regularly
        schedule.every(SENSOR_TRIGGER_MINUTES).minutes.do(
                                            sensorboard.store2database,
                                            database=db_declaration.session)

        # Update displayed values from sensor(s)
        schedule.every(DISPLAY_TRIGGER_MINUTES).minutes.do(
                                            sensorboard.display_values)

        while True:
            # Define process signal reactions
            signal.signal(signal.SIGINT, signal_handler_keyboard)
            signal.signal(signal.SIGTERM, signal_handler_termination)
            signal.signal(signal.SIGUSR1, signal_handler_termination)
            signal.signal(signal.SIGUSR2, signal_handler_termination)

            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    import logging.config
    # Load the logging configuration
    logging.config.fileConfig('data/logging.conf',
                              defaults={"logfilename": "mylog.log",
                                        'disable_existing_loggers': False}
                              )

    logger = logging.getLogger("sensorboard")
    # ToDo: Make script arguments available
    if sensors.RASPBERRYPI:
        logger.debug("RaspberryPi mode active")
    else:
        logger.debug("Non-RaspberryPi mode")
    main()

# Links to read_data_from_db
# https://www.toptal.com/python/python-design-patterns
# https://lintlyci.github.io/Flake8Rules/
# https://docs.python.org/2/howto/logging.html
# https://www.oreilly.com/library/view/head-first-python/9781491919521/ch04.html
