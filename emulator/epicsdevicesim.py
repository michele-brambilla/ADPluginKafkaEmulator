"""
epicsdevicesim.py: Generic (?) device for epics emulators
"""

import pcaspy
import pcaspy.tools

from emulator.loggersim import log


class EpicsDevice(object):

    def __init__(self, *, prefix, ports):
        self.prefix = prefix
        self.devices = {}
        self._pvdb = {}

        for port in ports:
            device = self.implement()(port)
            self.devices[port] = device
            self._pvdb.update(device.get_pvdb())

        self.server = pcaspy.SimpleServer()
        self.server.createPV(self.prefix + ':', self._pvdb)
        self.server_thread = pcaspy.tools.ServerThread(self.server)

        self.driver = self.implement_driver()(self, self._pvdb)

        for _,device in self.devices.items():
            device.set_driver(self.driver)

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
    def __init__(self, *, prefix, port='kafka', device=EpicsDevice):
        self.device = device(prefix=prefix, ports=[port,])

    def start(self):
        self.device.start()

    def stop(self):
        try:
            log.info('stopping simulation')
            self.device.stop()
        except Exception as e:
            log.info('Simulation did not shut down cleanly: %r' % e)
