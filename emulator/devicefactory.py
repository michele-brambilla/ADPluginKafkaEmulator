"""
Devices factory
"""

from __future__ import absolute_import

from emulator.epicsdevicesim import EpicsDevice

from emulator.adpluginkafka import ADKafka, ADKafkaDriver
from emulator.adsimdetector import ADSimulation, ADSimulationDriver


class ADSimDetector(EpicsDevice):
    @staticmethod
    def implement():
        return ADSimulation

    @staticmethod
    def implement_driver():
        return ADSimulationDriver


class ADPluginKafka(EpicsDevice):
    @staticmethod
    def implement():
        return ADKafka

    @staticmethod
    def implement_driver():
        return ADKafkaDriver

