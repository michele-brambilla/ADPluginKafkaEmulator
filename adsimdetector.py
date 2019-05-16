from __future__ import absolute_import

import argparse
from time import sleep

from emulator.devicefactory import ADSimDetector
from emulator.epicsdevicesim import EpicsDeviceSimulation
from emulator.loggersim import log
from emulator.sighandler import SignalHandler

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--prefix',
                    default='13SIM1',
                    help='Used as prefix for the epics PVs')
    ap.add_argument('-c', '--camera',
                    default='cam1',
                    help='Used as prefix for the Kafka PVs')

    args = ap.parse_args()

    areadetector = EpicsDeviceSimulation(prefix=args.prefix,
                                         port=args.camera,
                                         device=ADSimDetector)

    areadetector.start()

    signal_handler = SignalHandler()
    while True:
        sleep(1)
        if signal_handler.do_shutdown:
            areadetector.stop()
            break
    log.info('main::done.')
