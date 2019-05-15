"""
Bla bla bla
"""

from __future__ import absolute_import, division, print_function

import numpy as np
import logging

from time import time as timestamp

from kafka import KafkaProducer
from streaming.Serializer import ArrayDesc, HistogramFlatbuffersSerializer


class KafkaHistogramForwarder(object):

    def __init__(self, *, broker, topic, source, name='image'):
        self._topic = topic
        self._source = source
        self._name = name
        self._stop = False
        self._size_x = None
        self._size_y = None
        self.array_desc = None
        self._producer = None
        self.set_broker(broker)
        self.serializer = HistogramFlatbuffersSerializer()

    @property
    def size_x(self):
        return self._size_x

    @size_x.setter
    def size_x(self, value):
        self._size_x = value

    @property
    def size_y(self):
        return self._size_y

    @size_y.setter
    def size_y(self, value):
        self._size_y = value

    def set_broker(self, broker):
        if self._producer:
            self._producer.close()
        self._producer = KafkaProducer(bootstrap_servers=broker)

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, value):
        self._topic = value

    def produce(self, values, *, dtype=int):

        if self.size_x * self.size_y == 0:
            logging.error('Image size must be > 0 : (%r,%r)'%(self.size_x,
                                                              self.size_y))
            return

        if self.size_x * self.size_y != len(values):
            logging.error('Data size different from SizeX, SizeY')
            return

        desc = ArrayDesc.ArrayDesc(self._name, [self.size_x, self.size_y],
                                   dtype=dtype)
        x = self.serializer.encode(int(1e9 * timestamp()), desc,
                                   np.array(values),
                                   self._source)
        self._producer.send(self._topic, x)
