"""
epicsdevicesim.py: Generic (?) device for epics emulators
"""
from __future__ import absolute_import

import pcaspy
import pcaspy.tools

from emulator.loggersim import log


class EpicsDevice(object):

    def __init__(self, *, prefix, port):
        self.prefix = prefix

        self.device = self.implement(name=port)
        self.pvdb = self.device.get_pvdb()

        self.server = pcaspy.SimpleServer()
        self.server.createPV(self.prefix + ':', self.pvdb)
        self.server_thread = pcaspy.tools.ServerThread(self.server)

        driver = self.implement_driver(name=port, pvdb=self.pvdb)
        self.device.set_driver(driver)

    @staticmethod
    def implement():
        pass

    @staticmethod
    def implement_driver():
        pass

    def start(self):
        # process CA transactions
        self.server_thread.start()
        return

    def stop(self):
        log.info('{}::stop'.format(type(self).__name__))
        self.server_thread.stop()


class EpicsDeviceSimulation(object):
    def __init__(self, *, prefix, port, device=EpicsDevice):
        self.device = device(prefix=prefix, port=port)

    def start(self):
        self.device.start()

    def stop(self):
        try:
            log.info('stopping simulation')
            self.device.stop()
        except Exception as e:
            log.info('Simulation did not shut down cleanly: %r' % e)
