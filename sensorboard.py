import sys
if os.uname()[4][:3] == "arm":
    RASPBERRYPI = True
else
    RASPBERRYPI = False

try:
    # Non-existent modules?!
    import schedule
except ImportError as err:
    print(f"Could not import module, {err}. Automatic installation started")
    os.system("python -m pip install schedule")

import logging, logging.config
import os
import signal
import time

import datastorage.database_declaration as db_declaration
# rename module to data_plot
import datastorage.plot_data as plot_data
from sensors.sensors import PIN_SENSOR_DHT22, PIN_SENSOR_LIGHT, RASPBERRYPI
import sensors.boards as boards


# Load the logging configuration
logging.config.fileConfig('data/logging.conf',
                                defaults={"logfilename": "mylog.log",
                                'disable_existing_loggers': False})
logger = logging.getLogger("sensorboard")


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


def main():
    # Print sensor data only in non-raspberry mode due to missing display
    if not RASPBERRYPI:
        data = plot_data.read_data_from_db( db_declaration.session,
                                            db_declaration.MeasurementModel)
        plot_data.plot_data_multiplots(data=data)

    sensorboard = boards.SensorBoard(node="RPI-BRD",
                                pins={
                                        "ptemp":PIN_SENSOR_DHT22,
                                        "plight":PIN_SENSOR_LIGHT},
                                simulation=False)
    # ToDo: Include display init into board class init
    # ToDo: Show logo after display init
    sensorboard.init_display()

    # Gather sensor data regularly
    schedule.every(SENSOR_TRIGGER_MINUTES).minutes.do(
                                            sensorboard.store2database,
                                            database=db_declaration.session)

    # Update displayed values from sensor(s)
    schedule.every( DISPLAY_TRIGGER_MINUTES).minutes.do(
                                            sensorboard.display)

    while True:
        # Define process signal reactions
        signal.signal(signal.SIGINT, signal_handler_keyboard)
        signal.signal(signal.SIGTERM, signal_handler_termination)
        signal.signal(signal.SIGUSR1, signal_handler_termination)
        signal.signal(signal.SIGUSR2, signal_handler_termination)

        schedule.run_pending()
        time.sleep(1)

        #try:
            # Update display values
            #schedule.every(DISPLAY_TRIGGER_MINUTES).minutes.do(
            #
            #                                    sensorboard.display)
        #    pass
        #except NameError:
        #    logger.warning("Module schedule not loaded somehow")
        #    break


if __name__ == "__main__":
    # ToDo: Make script arguments available
    if RASPBERRYPI = True
        logger.debug("RaspberryPi mode active")
    else:
        logger.debug("Non-RaspberryPi mode")
    main()
