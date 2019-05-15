from __future__ import absolute_import

import argparse
from time import sleep

from emulator.loggersim import log
from emulator.sighandler import SignalHandler
from emulator.epicsdevicesim import EpicsDeviceSimulation
from emulator.devicefactory import ADPluginKafka, ADSimDetector


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--prefix',
                    default='13SIM1',
                    help='Used as prefix for the epics PVs')
    ap.add_argument('-k', '--kafka',
                    default='kafka1',
                    help='Used as prefix for the Kafka PVs')

    args = ap.parse_args()
    simulation = EpicsDeviceSimulation(prefix=args.prefix,
                                       port=args.kafka,
                                       device=ADPluginKafka)

    areadetector = EpicsDeviceSimulation(prefix=args.prefix,
                                       port='cam1',
                                       device=ADSimDetector)

    simulation.start()
    areadetector.start()

    signal_handler = SignalHandler()
    while True:
        sleep(1)
        if signal_handler.do_shutdown:
            simulation.stop()
            areadetector.stop()
            break
    log.info('main::done.')
