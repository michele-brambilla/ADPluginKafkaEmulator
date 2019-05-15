from __future__ import absolute_import, division, print_function

import logging
from time import sleep

from HistogramForwarder import KafkaHistogramForwarder
from ImageGenerator import DataGenerator
from epics.devices import ad_base, ad_image


class SimADKafkaPlugin(object):

    def __init__(self, *, camera, image, broker, topic, source='areaDetector'):
        self.broker = broker
        self.topic = topic
        self.camera = ad_base.AD_Camera(camera)
        self.camera.ImageMode = 'Single'
        self.image = ad_image.AD_ImagePlugin(image)

        self.camera.add_callback('Acquire_RBV', self._on_acquire)
        self.camera.add_callback('SizeX_RBV', self._on_size_change)
        self.camera.add_callback('SizeY_RBV', self._on_size_change)
        self.array_size = self.camera.SizeX * self.camera.SizeY

        self.data_generator = DataGenerator(self.camera.SizeX,
                                            self.camera.SizeY)
        self.kafka_producer = KafkaHistogramForwarder(broker=broker,
                                                      topic=topic,
                                                      source=source)
        self.kafka_producer.size_x = self.camera.SizeX
        self.kafka_producer.size_y = self.camera.SizeY


    @property
    def values(self):
        return self.data_generator.values

    def on_change(self, pvname=None, value=None, char_value=None, **kw):
        try:
            logging.warning('%r : %r' % (pvname, value))
            logging.warning('\tSizeX : %r' % self.camera.SizeX)
            logging.warning('\tSizeY : %r' % self.camera.SizeY)
        except Exception as e:
            logging.error('%r' % e)

    def _on_size_change(self, pvname=None, value=None, char_value=None, **kw):
        if pvname == 'SizeX_RBV':
            self.data_generator.size_x = value
            self.kafka_producer.size_x = value
        if pvname == 'SizeY_RBV':
            self.data_generator.size_y = value
            self.kafka_producer.size_y = value

    def _on_acquire(self, pvname=None, value=None, char_value=None,
                    **kw):
        if value:
            self.data_generator.reset()
            self.data_generator.acquire()
        else:
            self.data_generator.acquire(False)
            self.kafka_producer.produce(self.values)


if __name__ == '__main__':

    ad = SimADKafkaPlugin(camera='13SIM1:cam1:', image='13SIM1:image1:',
                          broker='ess01.psi.ch:9092', topic='sim_data_topic')



    while True:
        logging.info(ad.values)
        sleep(1)
