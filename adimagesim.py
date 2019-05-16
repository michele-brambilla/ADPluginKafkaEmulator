from __future__ import absolute_import

import argparse
from time import sleep

from emulator.devicefactory import ADImage
from emulator.epicsdevicesim import EpicsDeviceSimulation
from emulator.loggersim import log
from emulator.sighandler import SignalHandler

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--prefix',
                    default='13SIM1',
                    help='Used as prefix for the epics PVs')
    ap.add_argument('-i', '--image',
                    default='image1',
                    help='Used as prefix for the Kafka PVs')

    args = ap.parse_args()
    image = EpicsDeviceSimulation(prefix=args.prefix,
                                         port=args.image,
                                         device=ADImage)

    image.start()

    signal_handler = SignalHandler()
    while True:
        sleep(1)
        if signal_handler.do_shutdown:
            image.stop()
            break
    log.info('main::done.')
