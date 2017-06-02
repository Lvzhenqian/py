from util.config import *
from Client.RPC import client

ADDRS = TRANSFER['addrs']


class Transfer(client):
    def __init__(self, addr: tuple):
        super().__init__(addr)
        self.addr = addr

    def Ping(self):
        for _ in range(3):
            try:
                self.SendMetric('Transfer.Ping', None)
            except Exception as err:
                logging.error(err)
                logging.error('rebuild connect.')
                self.socket.connect(self.addr)


def __init_client(addr):
    connections = {}
    if connections.get(addr) is not None:
        connections[addr].Ping()
    else:
        ip, port = addr.split(':')
        connections[addr] = Transfer((ip, int(port)))
    return connections[addr]


def UpdateMetric(metrics: list):
    if isinstance(ADDRS, list):
        for add in ADDRS:
            ip, port = add.split(':')
            c = __init_client((ip, int(port)))
            for _ in range(5):
                resp = c.SendMetric('Transfer.Update', metrics)
                if resp.get('Message', 'fail') == 'ok':
                    return resp
        else:
            logging.error("无法发送到Transfer，请检查网络！")
