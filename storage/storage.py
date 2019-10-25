import logging
import time

logger = logging.getLogger(__name__)

try:
    import pickle
    from uuid import uuid4
except ImportError:
    logger.exception("Failure loading module")


# ToDo: Implement a numpy-array initialization to make data available in a
#       more suffisticated way.
class Storage:
    """ Contains any type of data in a list.
        Additionally, min(), max() and mean() values are available. Every
        data is stored as tuple with the timestamp of entry.

    """

    def __init__(self, description=None):
        self._id = uuid4()
        self._storage_count = None
        self._data = []
        self.description = description
        if not Storage.__subclasses__():
            logger.debug(f"<{__class__.__name__} Instance created, "
                         f"id({self._id})")

    def add(self, value):
        """ Add a new value to data with current timestamp. """
        self._data.append((value, time.time()))
        logger.info(f"New value (={value}) added to storage (id={self._id})")

    def mean(self, decimal=2) -> tuple:
        """ Calculates the current mean value of all stored data. """
        sum = 0
        for idx, value in enumerate(self._data, start=1):
            sum = sum + value[0]
        value_mean = round(sum / idx, decimal)
        logger.debug(f"Mean value calculated: {sum} / {idx} = {value_mean}")
        return value_mean, time.time()

    @property
    def MeanValue(self):
        return self.mean()

    def min(self):
        return min(self._data)

    def max(self):
        return max(self._data)

    def data_export(self):
        """ Returns serialized pickle-data."""
        return pickle.dumps(self)

    def last_timestamp(self):
        """ Returns timestamp of last added data. """
        return self._data[-1][1]

    def __repr__(self):
        return f"<Storage({self.description})>"

    def __str__(self):
        return f"<Storage(id:{self._id}, NumberOfData:{self._storage_count}, "\
               f"Data:{self._data}, Description:{self.description})>"
