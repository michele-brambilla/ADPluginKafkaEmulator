"""
Driver and database definition for the ADPluginKafka emulator.
"""

import pcaspy.tools

db_base = {
    'KafkaTopic': {
        'type': 'string',
        'description': 'Topic name | Read/Write'
    },
    'KafkaTopic_RBV': {
        'type': 'string',
        'description': 'Topic name RBV | Read'
    },
    'ConnectionStatus_RBV': {
        'type': 'int',
        'description': 'Connection status RBV | Read'
    },
    'ConnectionMessage_RBV': {
        'type': 'string',
        'description': 'Connection error message RBV | Read'
    },
    'KafkaMaxQueueSize': {
        'type': 'int',
        'description': 'Same Kafka parameter | Read/Write'
    },
    'KafkaMaxQueueSize_RBV': {
        'type': 'int',
        'description': 'Same Kafka parameter | Read'
    },
    'UnsentPackets_RBV': {
        'type': 'int',
        'description': 'Number of messages not yet transmitted to the Kafka '
                       'broker | Read/Write'
    },
    'KafkaMaxMessageSize_RBV': {
        'type': 'int',
        'description': 'Maximum message size | Read'
    },
    'KafkaStatsIntervalTime': {
        'type': 'int',
        'description': 'Time between Kafka broker connection stats | '
                       'Read/Write'
    },
    'KafkaStatsIntervalTime_RBV': {
        'type': 'int',
        'description': 'Time between Kafka broker connection stats | '
                       'Read'
    },
    'DroppedArrays_RBV': {
        'type': 'int',
        'description': 'Time between Kafka broker connection stats | '
                       'Read'
    },
}


class ADKafkaDriver(pcaspy.Driver):

    def __init__(self, guide, pvdb):
        super(ADKafkaDriver, self).__init__()
        self.guide = guide
        self.pvdb = pvdb
        self.threads = {}

        for pv in pvdb:
            if 'KafkaTopic' in pv:
                self.setParam(pv, 'sim_data_topic')
            if 'KafkaMaxQueueSize' in pv:
                self.setParam(pv, 100)
            if 'KafkaStatsIntervalTime' in pv:
                self.setParam(pv, 5)

    def write(self, pv, value):
        # log.info('Write: {} = {}'.format(pv, value))
        super(ADKafkaDriver, self).write(pv, value)
        if 'KafkaTopic' in pv:
            super(ADKafkaDriver, self).write(pv + '_RBV', value)
        if 'KafkaMaxQueueSize' in pv:
            super(ADKafkaDriver, self).write(pv + '_RBV', value)
        if 'KafkaStatsIntervalTime' in pv:
            super(ADKafkaDriver, self).write(pv + '_RBV', value)


class ADKafka(object):
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
