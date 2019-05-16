"""
Devices factory
"""

from __future__ import absolute_import

from emulator.adimage import ADImg, ADImgDriver
from emulator.adpluginkafka import ADKafka, ADKafkaDriver
from emulator.adsimdetector import ADSimulation, ADSimulationDriver
from emulator.epicsdevicesim import EpicsDevice


class ADSimDetector(EpicsDevice):
    @staticmethod
    def implement():
        return ADSimulation

    @staticmethod
    def implement_driver():
        return ADSimulationDriver


class ADImage(EpicsDevice):
    @staticmethod
    def implement():
        return ADImg

    @staticmethod
    def implement_driver():
        return ADImgDriver


class ADPluginKafka(EpicsDevice):
    @staticmethod
    def implement():
        return ADKafka

    @staticmethod
    def implement_driver():
        return ADKafkaDriver
