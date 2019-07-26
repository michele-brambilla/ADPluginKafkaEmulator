"""
Area detector simulation.
Implements only the PVs required for the ADPluginKafkaEmulator.
"""
from __future__ import absolute_import

from time import sleep

import pcaspy.tools

from emulator.loggersim import log
from streaming.utils import threaded

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
    'AcquireTime': {
        'type': 'int',
        'description': 'Acquisition time | Read/Write'
    },
    'AcquireTime_RBV': {
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
    'StatusMessage': {
        'type': 'string',
        'description': 'Status message string'
    },
    'DetectorState': {
        'type' : 'string',
        'description': 'Acquisition status'
    },
    'StatusMessage_RBV': {
        'type': 'string',
        'description': 'Status message string'
    },
    'DetectorState_RBV': {
        'type' : 'string',
        'description': 'Acquisition status'
    },
    'TimeRemaining_RBV': {
        'type' : 'int',
        'description': 'Time remaining for current image'
    },
}


class ADSimulationDriver(pcaspy.Driver):

    def __init__(self, **args):
        super(self.__class__, self).__init__()
        for param in ['name', 'pvdb']:
            if param not in args:
                raise self.__class__.__name__+'Missing required argument ' \
                                              +param +' in constructor'
        self.pvdb = args['pvdb']
        self.prefix = args['name']

        for pv in self.pvdb:
            if 'ImageMode' in pv:
                self.setParam(pv, 'Single')
            if 'Acquire' in pv:
                self.setParam(pv, 0)
            if 'AcquireTime' in pv:
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
        if any(elem in pv for elem in ['ImageMode','Acquire','AcquireTime',
                                    'SizeX','SizeY']):
            super(ADSimulationDriver, self).write(pv + '_RBV', value)
        if 'Acquire' in pv:
        #     super(ADSimulationDriver, self).write(pv + '_RBV', value)
            mode = self.getParam(self._prefix() + 'ImageMode')
        #     self._acquire(reason=value, mode=mode)
        # if 'AcquireTime' in pv:
        #     super(ADSimulationDriver, self).write(pv + '_RBV', value)
        # if 'SizeX' in pv:
        #     super(ADSimulationDriver, self).write(pv + '_RBV', value)
        # if 'SizeY' in pv:
        #     super(ADSimulationDriver, self).write(pv + '_RBV', value)
        # self.updatePVs()
        return state

    def _prefix(self):
        return '%s:' % self.prefix

    def _acquire_single_image(self):
        sleep(self.getParam(self._prefix() + 'AcquireTime'))
        self.setParam(self._prefix() + 'Acquire', 0)
        self.setParam(self._prefix() + 'Acquire_RBV', 0)
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
    def __init__(self, **args):
        if 'name' not in args:
            raise self.__class__.__name__ + 'Missing required argument ' \
                                            '"name" in constructor'
        self.name = args['name']

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
