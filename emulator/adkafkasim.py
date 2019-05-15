from __future__ import absolute_import

import argparse
from time import sleep

from epicsdevicesim import EpicsDeviceSimulation, EpicsDevice
from loggersim import log
from sighandler import SignalHandler


class ADPluginKafka(EpicsDevice):
    pass


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
                                       kafka=args.kafka,
                                       device=ADPluginKafka)
    simulation.start()

    signal_handler = SignalHandler()
    while True:
        sleep(1)
        if signal_handler.do_shutdown:
            simulation.stop()
            break
    log.info('main::done.')
