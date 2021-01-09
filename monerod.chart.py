import json
import time
import requests
from requests.auth import HTTPDigestAuth

from bases.FrameworkServices.SimpleService import SimpleService


update_every = 30

ORDER = [
    'blockindex',
    'difficulty',
    'network_connections',
    'unconfirmed_transactions',
    'last_block_t',
    'uptime',
]

CHARTS = {
    'blockindex': {
        'options': [None, 'Blockchain Index', 'count', 'blockchain', 'monerod.blockindex', 'area'],
        'lines': [
            ['last_block_height', 'blocks', 'absolute'],
        ]
    },
    'difficulty': {
        'options': [None, 'Blockchain Difficulty', 'difficulty', 'blockchain', 'monerod.difficulty', 'line'],
        'lines': [
            ['blockchain_difficulty', '', 'absolute'],
        ],
    },
    'network_connections': {
        'options': [None, 'Network Connections', 'count', 'network', 'monerod.network_connections', 'line'],
        'lines': [
            ['outgoing_connections', 'Outgoing', 'absolute'],
            ['incoming_connections', 'Incoming', 'absolute'],
        ],
    },
    'unconfirmed_transactions': {
        'options': [None, 'Unconfirmed Transactions', 'count', 'network', 'monerod.unconfirmed_transactions', 'line'],
        'lines': [
            ['unconfirmed_tx', 'TX Count', 'absolute'],
        ],
    },
    'last_block_t': {
        'options': [None, 'Time since last block', 'minutes', 'last_block_time', 'monerod.last_block_t', 'line'],
        'lines': [
            ['last_block_timestamp', 'last_block', 'absolute', None, 60],
        ],
    },
    'uptime': {
        'options': [None, 'Uptime in seconds', 'seconds', 'uptime', 'monerod.uptime', 'line'],
        'lines': [
            ['node_uptime', 'uptime', 'absolute'],
        ],
    },
}

METHODS = {
    'get_info': lambda r: {
        'blockchain_difficulty': r['difficulty'],
        'outgoing_connections': r['outgoing_connections_count'],
        'incoming_connections': r['incoming_connections_count'],
        'unconfirmed_tx': r['tx_pool_size'],
        'node_uptime': r['start_time']
    },
    'get_last_block_header': lambda r: dict([
        ('last_block_' + k, v) for (k, v) in r['block_header'].items()
    ]),
}

JSON_RPC_VERSION = '2.0'

class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS

    def _get_data(self):
        rpc_host = self.configuration.get('host', '127.0.0.1')
        rpc_port = self.configuration.get('port', 18081)
        rpc_user = self.configuration.get('user', '')
        rpc_password = self.configuration.get('pass', '')
        rpc_url = 'http://{host}:{port}/json_rpc'.format(host=rpc_host, port=rpc_port)
        connection_timeout = self.configuration.get('timeout', 30)
      
        result = []
        for i, method in enumerate(METHODS):            
            hdr = { 'Content-Type': 'application/json' }
            json_data = { "jsonrpc": JSON_RPC_VERSION, "id": i, "method": method }  
            try:          
                r = requests.post(rpc_url, data=json.dumps(json_data), headers=hdr, timeout=connection_timeout, auth=HTTPDigestAuth(rpc_user, rpc_password))
            except requests.exceptions.RequestException as e: 
                return None
            result.append(json.loads(r.text))

        data = dict()
        for i, (_, handler) in enumerate(METHODS.items()):
            r = result[i]
            data.update(handler(r['result']))

        data["last_block_timestamp"] = time.time() - data["last_block_timestamp"]
        data["node_uptime"] = time.time() - data["node_uptime"]

        return data
