"""
Driver and database definition for the ADPluginKafka emulator.
"""

import pcaspy.tools

db_base = {
    'KafkaBrokerAddress' : {
        'type': 'string',
        'description': 'Broker address | Read/Write'
    },
    'KafkaBrokerAddress_RBV' : {
        'type': 'string',
        'description': 'Broker address | Read'
    },
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
    'ConnectionStatus': {
        'type': 'int',
        'description': 'Connection status setter| Read/Write'
    },
    'ConnectionMessage': {
        'type': 'string',
        'description': 'Connection error message setter | Read/Writer'
    },
}

class ADKafkaDriver(pcaspy.Driver):

    def __init__(self, **args):
        super(ADKafkaDriver, self).__init__()
        if 'pvdb' not in args:
            raise self.__class__.__name__+'Missing required argument "pvdb" ' \
                                          'in constructor'
        self.pvdb = args['pvdb']

        for pv in self.pvdb:
            if 'KafkaBrokerAddress' in pv:
                self.setParam(pv, 'ess01.psi.ch:9092')
            if 'KafkaTopic' in pv:
                self.setParam(pv, 'sim_data_topic')
            if 'KafkaMaxQueueSize' in pv:
                self.setParam(pv, 100)
            if 'KafkaStatsIntervalTime' in pv:
                self.setParam(pv, 5)

    def write(self, pv, value):
        # log.info('Write: {} = {}'.format(pv, value))
        super(ADKafkaDriver, self).write(pv, value)
        if 'KafkaBrokerAddress' in pv:
            super(ADKafkaDriver, self).write(pv + '_RBV', value)
        if 'KafkaTopic' in pv:
            super(ADKafkaDriver, self).write(pv + '_RBV', value)
        if 'KafkaMaxQueueSize' in pv:
            super(ADKafkaDriver, self).write(pv + '_RBV', value)
        if 'KafkaStatsIntervalTime' in pv:
            super(ADKafkaDriver, self).write(pv + '_RBV', value)
        if any([k in pv for k in ['ConnectionStatus_RBV',
                                  'ConnectionMessage_RBV']]):
            return False
        if any([k in pv for k in ['ConnectionStatus',
                                  'ConnectionMessage']]):
            super(ADKafkaDriver, self).write(pv, value)
            super(ADKafkaDriver, self).write(pv + '_RBV', value)
        self.updatePVs()
        return True

class ADKafka(object):
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
