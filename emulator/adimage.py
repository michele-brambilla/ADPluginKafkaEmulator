"""
Area detector simulation.
Implements only the PVs required for the ADPluginKafkaEmulator.
"""

import numpy
import pcaspy.tools
from epics import PV

from emulator.loggersim import log

MAX_POINTS = 1024 * 1024

db_base = {
    'ArrayData': {
        'type': 'int',
        'count': MAX_POINTS,
        'description': 'Image data as an array | Read/Write',
        'value': numpy.zeros(MAX_POINTS, dtype=int)
    },
}


class ADImgDriver(pcaspy.Driver):

    def __init__(self, **args):
        super(self.__class__, self).__init__()
        if 'pvdb' not in args:
            raise self.__class__.__name__+'Missing required argument "pvdb" ' \
                                          'in constructor'
        self.pvdb = args['pvdb']

    def write(self, pv, value):
        super(self.__class__, self).write(pv, value)


class ADImg(object):
    def __init__(self, **args):
        if 'name' not in args:
            raise self.__class__.__name__ + 'Missing required argument ' \
                                            '"name" in constructor'
        self.name = args['name']
        self.api_device = None
        self.driver = None
        self.pvs = {}

    def on_size_change(self, pvname=None, value=None, **kw):
        log.warning('%r : %r'%(pvname,value))

    def register_cb(self, *, pvname, on_change):
        if pvname not in self.pvs:
            entry = PV(pvname,callback=on_change)
            self.pvs[pvname] = entry

    def _get_pv_prefix(self):
        return '%s:' % self.name

    def set_driver(self, driver):
        self.driver = driver

    def get_pvdb(self):
        db = {}
        for field in db_base:
            db[self._get_pv_prefix() + field] = db_base[field]
        return db
