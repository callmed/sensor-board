import sys
import logging
from os import system
from datetime import datetime, timedelta
from datastorage.database_declaration import MeasurementModel
from sensors.sensors import RASPBERRYPI

try:
    import numpy as np
except ImportError as err:
    print(f"Could not import module, {err}")
    system("python -m pip install numpy")

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import matplotlib.patches as mpatches
except ImportError as err:
    print(f"Could not import module, {err}")
    if not RASPBERRYPI:
        print("Automatic module installation started")
        system("python -m pip install numpy")


logger = logging.getLogger("sensorboard.plotter")

# Define x-axis gap of data
DATE_DELTA_SECONDS = 0
DATE_DELTA_MINUTES = 0
DATE_DELTA_HOURS = 1
DATE_DELTA_DAYS = 0

# Define array datatype of columns
dt = np.dtype[('temperature', 'f4'),
              ('humidity', 'f4'),
              ('timestamp', 'datetime64[ms]')]


def read_data_from_db(conn, table, **kwargs):
    """ Read data from database, converts it into numpy-array and
        returns it.
    """
    data_database = []
    results = conn.query(MeasurementModel).all()
    for res in results:
        data_database.append((res.temperature, res.humidity, res.timestamp))
    X = np.array(data_database, dtype=dt)
    return X


def plot_data_multiplots(data):
    """ Plot data into two separate plots."""
    plt.subplot(2, 1, 1)
    plt.plot(data["timestamp"], data["temperature"], 'o-')
    plt.title("Sensor Boards")
    plt.ylabel("Temperatture")
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.plot(data["timestamp"], data["humidity"], '.-')
    plt.xlabel("Zeitstempel")
    plt.ylabel("Luftfeuchtigkeit")
    plt.grid()

    plt.show()


def plot_data(data):
    # contrained_layout resizes main window to fit all labels
    fig, ax = plt.subplots(constrained_layout=False)
    fig.suptitle("This is a figure sub-title")

    ax.plot_date(data["timestamp"], data["temperature"])
    ax.set_ylim(np.amin(data["temperature"])-10,
                np.mean(data["temperature"])+10)

    plt.grid()
    plt.show()


def plot_data_default(data):
    """ Plot data in a default style plot."""
    logger.info("Start plogging data")
    date_start = data["timestamp"][0]
    date_end = data["timestamp"][-1]
#    date_now = datetime.now()
    date_delta = timedelta(days=DATE_DELTA_DAYS,
                           hours=DATE_DELTA_HOURS,
                           minutes=DATE_DELTA_MINUTES,
                           seconds=DATE_DELTA_SECONDS)

    dates = mdates.drange(date_start.astype(datetime),
                          date_end.astype(datetime),
                          date_delta)

    logger.debug(f"Date conversion started with from {date_start} to "
                 f"{date_end} with steps of {date_delta} / "
                 f"total: {len(dates)}")
    logger.debug(f"Plotting data of these dates: {dates}")
    # contrained_layout resizes main window to fit all labels
    fig, ax = plt.subplots(constrained_layout=False)
    fig.suptitle("This is a figure sub-title")

#    ax.plot_date(dates, y*y)
    # TODO: Need to reduce amount of data in Y-axis based on X-axis
#   ax.plot_date(dates[:-1], data["temperature"])
#   ax.plot_date(dates[:-1], data["humidity"])

    # Labeling
    ax.set_title("Test Label")
    ax.set_xlabel("time [h]")
    ax.set_ylabel("Temperature [°C]")

    # Create label patch in graphic
    blue_patch = mpatches.Patch(color="blue", label="Temperature")
    red_patch = mpatches.Patch(color="red", label="Humidity")
    plt.legend(handles=[blue_patch, red_patch])
    plt.grid()

    # Set the x-axis limits
    ax.set_xlim(dates[0], dates[-1])

    # Define ticks for x-axis
    ax.xaxis.set_major_locator(mdates.HourLocator())
    # every 6 minutes one tick
    ax.xaxis.set_minor_locator(mdates.MinuteLocator(np.arange(0, 60, 6)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

    ax.fmt_xdata = mdates.DateFormatter("%H:%S")
    fig.autofmt_xdate()

    plt.show()


# Links / Documentation
# https://www.python-kurs.eu/numpy_dtype.php
# https://matplotlib.org/examples/pylab_examples/date_demo_convert.html
# https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/date.html
