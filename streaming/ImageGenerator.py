"""
Bla bla bla
"""

from __future__ import absolute_import, division, print_function

from streaming.utils import threaded

from time import sleep

from numpy.random import randint


class DataGenerator(object):

    def __init__(self, size_x=128, size_y=128):
        self.size_x = size_x
        self.size_y = size_y
        self.values = [0 for x in range(size_x * size_y)]
        self._stop = False
        self._acquire = False
        self._fill_data()

    def kill(self):
        self._stop = True

    def acquire(self, value=True):
        self._acquire = value

    def reset(self):
        self.values = [0 for x in range(self.size_x * self.size_y)]

    @threaded
    def _fill_data(self):
        self._running = True
        while not self._stop:
            while self._acquire and not self._stop:
                sleep(1e-2)
                self.values[
                    randint(low=0, high=self.size_x * self.size_y)] += 1
            sleep(1)
        self._running = False

    def __del__(self):
        self._acquire = False
        self._stop = True
