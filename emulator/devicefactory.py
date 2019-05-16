"""
Devices factory
"""

from __future__ import absolute_import

from emulator.addetector import ADSimulation, ADSimulationDriver
from emulator.adimage import ADImg, ADImgDriver
from emulator.adpluginkafka import ADKafka, ADKafkaDriver
from emulator.epicsdevicesim import EpicsDevice


class ADSimDetector(EpicsDevice):
    @staticmethod
    def implement(**args):
        return ADSimulation(**args)

    @staticmethod
    def implement_driver(**args):
        return ADSimulationDriver(**args)


class ADImage(EpicsDevice):
    @staticmethod
    def implement(**args):
        return ADImg(**args)

    @staticmethod
    def implement_driver(**args):
        return ADImgDriver(**args)


class ADPluginKafka(EpicsDevice):
    @staticmethod
    def implement(**args):
        return ADKafka(**args)

    @staticmethod
    def implement_driver(**args):
        return ADKafkaDriver(**args)
