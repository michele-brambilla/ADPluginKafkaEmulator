"""
Driver and database definition for the ADPluginKafka emulator.
"""
import pcaspy.tools

from emulator.loggersim import log

db_base = {
    'KafkaBrokerAddress': {
        'type': 'string',
        'description': 'Broker | Read/Write'
    },
    'KafkaBrokerAddress_RBV': {
        'type': 'string',
        'description': 'Broker | Read'
    },
    'KafkaTopic': {
        'type': 'string',
        'description': 'Topic name | Read/Write'
    },
    'KafkaTopic_RBV': {
        'type': 'string',
        'description': 'Topic name RBV | Read'
    },
    'ConnectionStatus': {
        'type': 'int',
        'description': 'Connection status RBV | Read/Write'
    },
    'ConnectionStatus_RBV': {
        'type': 'int',
        'description': 'Connection status RBV | Read'
    },
    'ConnectionMessage': {
        'type': 'string',
        'description': 'Connection error message RBV | Read/Write'
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

    def __init__(self, **args):
        super(ADKafkaDriver, self).__init__()
        if 'pvdb' not in args:
            raise self.__class__.__name__ + 'Missing required argument "pvdb" ' \
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
        if pv[-4:] == '_RBV':
            log.error('Read-only pv')
            return False
        super(ADKafkaDriver, self).write(pv, value)
        if any(elem in pv for elem in ['KafkaBrokerAddress', 'KafkaTopic',
                                       'ConnectionStatus',
                                       'ConnectionMessage']):
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
