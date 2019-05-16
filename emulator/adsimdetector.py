"""
Area detector simulation.
Implements only the PVs required for the ADPluginKafkaEmulator.
"""
from __future__ import absolute_import

import pcaspy.tools

from emulator.loggersim import log
from streaming.utils import threaded

from time import sleep

db_base = {
    'ImageMode': {
        'type': 'string',
        'description': 'ImageMode | Read/Write'
    },
    'Acquire': {
        'type': 'int',
        'description': 'Start acquisition | Read/Write'
    },
    'Acquire_RBV': {
        'type': 'int',
        'description': 'Acquisition status | Read'
    },
    'AcquisitionTime': {
        'type': 'int',
        'description': 'Acquisition time | Read/Write'
    },
    'AcquisitionTime_RBV': {
        'type': 'int',
        'description': 'Acquisition time | Read'
    },
    'SizeX': {
        'type': 'int',
        'description': 'Detector X size | Read/Write'
    },
    'SizeX_RBV': {
        'type': 'int',
        'description': 'Detector X size RBV | Read'
    },
    'SizeY': {
        'type': 'int',
        'description': 'Detector Y size | Read/Write'
    },
    'SizeY_RBV': {
        'type': 'int',
        'description': 'Detector Y size RBV | Read'
    },
}


class ADSimulationDriver(pcaspy.Driver):

    def __init__(self, prefix, pvdb):
        super(ADSimulationDriver, self).__init__()
        self.prefix = prefix
        self.pvdb = pvdb
        self.threads = {}

        for pv in pvdb:
            if 'ImageMode' in pv:
                self.setParam(pv, 'Single')
            if 'Acquire' in pv:
                self.setParam(pv, 0)
            if 'AcquisitionTime' in pv:
                self.setParam(pv, 0.001)
            if 'SizeX' in pv:
                self.setParam(pv, 1024)
            if 'SizeY' in pv:
                self.setParam(pv, 1024)

    def write(self, pv, value):
        state = True
        if pv[-4:] == '_RBV':
            log.error('Read-only pv')
            return False
        super(ADSimulationDriver, self).write(pv, value)
        if 'ImageMode' in pv:
            super(ADSimulationDriver, self).write(pv + '_RBV', value)
        if 'Acquire' in pv:
            super(ADSimulationDriver, self).write(pv + '_RBV', value)
            log.warning(self.getParam(self._prefix() + 'AcquisitionTime'))
            mode = self.getParam(self._prefix() + 'ImageMode')
            self._acquire(reason=value, mode=mode)
        if 'AcquisitionTime' in pv:
            super(ADSimulationDriver, self).write(pv + '_RBV', value)
        if 'SizeX' in pv:
            super(ADSimulationDriver, self).write(pv + '_RBV', value)
        if 'SizeY' in pv:
            super(ADSimulationDriver, self).write(pv + '_RBV', value)
        self.updatePVs()
        return state

    def _prefix(self):
        return '%s:' % self.prefix

    def _acquire_single_image(self):
        sleep(self.getParam(self._prefix()+'AcquisitionTime'))
        self.setParam(self._prefix()+'Acquire', 0)
        self.setParam(self._prefix()+'Acquire_RBV', 0)
        self.updatePVs()

    @threaded
    def _acquire(self, *, reason, mode):
        if reason:
            if mode == 'Single':
                self._acquire_single_image()
                return
            # if mode == 'Continous':
            #     while self.getParam('Acquire'):
            #         self._acquire_single_image()



class ADSimulation(object):
    def __init__(self, name):
        self.name = name
        self.api_device = None
        self.driver = None

    def _get_pv_prefix(self):
        return '%s:' % self.name

    def set_driver(self, driver):
        self.driver = driver

    def get_pvdb(self):
        db = {}
        for field in db_base:
            db[self._get_pv_prefix() + field] = db_base[field]
        return db