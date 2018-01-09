import logging
import os

import zmq

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s')
log = logging.getLogger()

ctx = zmq.Context()


class Zmq:

    def send(self, thing):
        log.info("send %s", thing)
        return self.socket.send_json(thing)

    def receive(self):
        return self.socket.recv_json()


class ZmqClient(Zmq):

    def __init__(self, host, port):
        self.endpoint = 'tcp://{}:{}'.format(host, port)
        self.socket = ctx.socket(zmq.REQ)
        self.socket.connect(self.endpoint)
        log.info('client: %s', self.endpoint)

    def run(self):
        req = {}
        for _ in range(10):
            self.send(req)
            req = self.receive()
        assert req['payload'] == 10


class ZmqServer(Zmq):

    def __init__(self, port):
        self.endpoint = 'tcp://*:{}'.format(port)
        self.socket = ctx.socket(zmq.REP)
        self.socket.bind(self.endpoint)
        log.info('server: %s', self.endpoint)

    def run(self):
        while True:
            req = self.receive()
            req['payload'] = req.get('payload', 0) + 1
            self.send(req)


if __name__ == '__main__':
    host = os.environ.get('HOST', 'localhost')
    port = os.environ.get('PORT', 5000)
    role = ZmqServer(port) if os.environ.get('ROLE', '') == 'server' else ZmqClient(host, port)
    role.run()
