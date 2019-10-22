import time
import pickle


# ToDo: Implement a numpy-array initialization to make data available in a
#       more suffisticated way.
class Storage:
    __puffer_size = 10

    def __init__(self):
        self._storage_count = 0
        self._data = []

    def add(self, value):
        self._data.append(value, time.time())

    def mean(self):
        temp = 0
        cnt = 0
        for v, ts in self._data:
            temp += v
            cnt += 1
        return (round(temp / cnt, 2), time.time())

    def min(self):
        return min(self._data)

    def max(self):
        return max(self._data)

    def data_export(self):
        return pickle.dumps(self)
