"""
Bla bla bla
"""

from __future__ import absolute_import, division, print_function

from threading import Thread
from time import sleep

from numpy.random import randint


# Threaded function snippet
def threaded(fn):
    """To use as decorator to make a function call threaded.
    Needs import
    from threading import Thread"""

    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


# Threaded function snippet returning a callback when the function has finished
def threaded_return(fn, callback_func):
    """To use as decorator to make a function call threaded.
    It will call the callback_func when the function returns.
    Needs import
    from threading import Thread"""

    def wrapper(*args, **kwargs):
        def do_callback():
            callback_func(fn(args, kwargs))

        thread = Thread(target=do_callback)
        thread.start()
        return thread

    return wrapper


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
