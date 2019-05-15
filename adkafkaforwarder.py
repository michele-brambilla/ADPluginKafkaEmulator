from __future__ import absolute_import, division, print_function

from emulator.loggersim import log
from emulator.sighandler import SignalHandler

from time import sleep

from streaming.HistogramForwarder import KafkaHistogramForwarder
from streaming.ImageGenerator import DataGenerator
from epics.devices import ad_base, ad_image
import argparse


class SimADKafkaPlugin(object):

    def __init__(self, *, camera, image, kafka, broker, topic,
                 source='areaDetector'):
        self.kafkapv = kafka
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
            log.warning('%r : %r' % (pvname, value))
            log.warning('\tSizeX : %r' % self.camera.SizeX)
            log.warning('\tSizeY : %r' % self.camera.SizeY)
        except Exception as e:
            log.error('%r' % e)

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
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--prefix', default='13SIM1',
                    help='Used as prefix for the epics PVs')
    ap.add_argument('-c', '--camera', default='cam1', help='Camera port')
    ap.add_argument('-i', '--image', default='image1', help='Image port')
    ap.add_argument('-k', '--kafka', default='kafka1', help='Kafka port')
    ap.add_argument('-b', '--broker', default='ess01.psi.ch:9092',
                    help='Kafka broker')
    ap.add_argument('-t', '--topic', default='sim_data_topic',
                    help='Kafka topic')

    args = ap.parse_args()
    camera_prefix = args.prefix+':'+args.camera+':'
    image_prefix = args.prefix+':'+args.image+':'
    kafka_prefix = args.prefix + ':' + args.kafka + ':'
    ad = SimADKafkaPlugin(camera=camera_prefix, image=image_prefix,
                          kafka=kafka_prefix, broker=args.broker,
                          topic=args.topic)

    signal_handler = SignalHandler()
    while True:
        sleep(1)
        if signal_handler.do_shutdown:
            break
    log.info('main::done.')