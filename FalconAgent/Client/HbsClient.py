from Client.RPC import client
from util.config import HEARTBEAT,Geloger,DEBUG

ADDRS = HEARTBEAT.get('addr')
hbs_log = Geloger(name='Client.HbsClient', file='app.log', debug=DEBUG)


class Hbs(client):
    def __init__(self, addr: tuple):
        super().__init__(addr)
        self.addr = addr

    def ping(self):
        for _ in range(3):
            try:
                self.SendMetric('Agent.TrustableIps', None)
            except Exception as err:
                hbs_log.error(err)
                hbs_log.info('reconnect..')
                self.socket.connect(self.addr)


def __init_Hbs(addrs):
    connects = {}
    if connects.get(addrs) is not None:
        connects[addrs].ping()
    else:
        ip, port = ADDRS.split(':')
        connects[addrs] = Hbs((ip, int(port)))
    return connects[addrs]


def Update(metric):
    ip, port = ADDRS.split(':')
    cl = Hbs((ip, int(port)))
    for _ in range(5):
        try:
            resp = cl.SendMetric('Agent.ReportStatus', metric)
        except Exception as err:
            resp = None
            hbs_log.error(err)
        if resp:
            return resp
