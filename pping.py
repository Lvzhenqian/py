import subprocess, json, time,os
from collections import namedtuple
from urllib import request, error

file = r'c:\windows\7roadyw\agent\cfg.json'
try:
    with open(file, mode='r', encoding='utf8') as f:
        cfg = json.loads(f.read())
    hostname = cfg['hostname']
    req = request.urlopen('http://ip.7road.net/')
    country = req.read().split()[1]
except error.HTTPError:
    hostname, country = '', ''
except json.JSONDecodeError:
    hostname, country = '', ''
count = 2


def Ping(host: str, c=count) -> namedtuple:
    def fil(x):
        ret, tmp = [], ''
        for i in x:
            switch = True if i.isdigit() else False
            if switch:
                tmp = tmp + i
            elif tmp:
                ret.append(int(tmp))
                tmp = ''
        return ret

    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    req = namedtuple('stat', ['host', 'lost', 'avg', 'max', 'min'])
    with subprocess.Popen('cmd /c chcp 437 & ping -n {count} {host}'.format(count=c, host=host),
                          shell=True,
                          stderr=subprocess.DEVNULL, stdout=subprocess.PIPE, stdin=subprocess.DEVNULL,
                          universal_newlines=True,
                          startupinfo=si,env=os.environ) as process:
        try:
            process.wait(180)
            out = [x.strip() for x in process.stdout if 'Average' in x or 'Lost' in x]
            if len(out) > 1:
                *_, lost = fil(out[0])
                mi, ma, avg = fil(out[1])
                return req(host, lost, avg, ma, mi)
            else:
                return req(host, 100, 0, 0, 0)
        except TimeoutError:
            process.kill()
            return req(host, 100, 0, 0, 0)


ip = namedtuple('IP', ['falcon', 'url', 'nameserver', 'c'])
if country == '中国'.encode():
    mapping = ip(Ping('113.107.161.47'), Ping('www.baidu.com'), Ping('114.114.114.114'), 'GN')
else:
    mapping = ip(Ping('8.8.4.4'), Ping('www.google.com'), Ping('8.8.8.8'), 'HW')
date = int(time.time())
metric = [{
    "metric": 'ping.lost.{}'.format(mapping.c),
    "endpoint": hostname,
    "timestamp": date,
    "step": 300,
    "value": mapping.falcon.lost,
    "counterType": "GAUGE",
    "tags": 'test_ip={}'.format(mapping.falcon.host)
}, {
    "metric": 'ping.avg.{}'.format(mapping.c),
    "endpoint": hostname,
    "timestamp": date,
    "step": 300,
    "value": mapping.falcon.avg,
    "counterType": "GAUGE",
    "tags": 'test_ip={}'.format(mapping.falcon.host)
}, {
    "metric": 'ping.min.{}'.format(mapping.c),
    "endpoint": hostname,
    "timestamp": date,
    "step": 300,
    "value": mapping.falcon.min,
    "counterType": "GAUGE",
    "tags": 'test_ip={}'.format(mapping.falcon.host)
}, {
    "metric": 'ping.max.{}'.format(mapping.c),
    "endpoint": hostname,
    "timestamp": date,
    "step": 300,
    "value": mapping.falcon.max,
    "counterType": "GAUGE",
    "tags": 'test_ip={}'.format(mapping.falcon.host)
}, {
    "metric": 'ping.lost.{}'.format(mapping.c),
    "endpoint": hostname,
    "timestamp": date,
    "step": 300,
    "value": mapping.url.lost,
    "counterType": "GAUGE",
    "tags": 'test_ip={}'.format(mapping.url.host)
}, {
    "metric": 'ping.avg.{}'.format(mapping.c),
    "endpoint": hostname,
    "timestamp": date,
    "step": 300,
    "value": mapping.url.avg,
    "counterType": "GAUGE",
    "tags": 'test_ip={}'.format(mapping.url.host)
}, {
    "metric": 'ping.min.{}'.format(mapping.c),
    "endpoint": hostname,
    "timestamp": date,
    "step": 300,
    "value": mapping.url.min,
    "counterType": "GAUGE",
    "tags": 'test_ip={}'.format(mapping.url.host)
}, {
    "metric": 'ping.max.{}'.format(mapping.c),
    "endpoint": hostname,
    "timestamp": date,
    "step": 300,
    "value": mapping.url.max,
    "counterType": "GAUGE",
    "tags": 'test_ip={}'.format(mapping.url.host)
}, {
    "metric": 'ping.lost.{}'.format(mapping.c),
    "endpoint": hostname,
    "timestamp": date,
    "step": 300,
    "value": mapping.nameserver.lost,
    "counterType": "GAUGE",
    "tags": 'test_ip={}'.format(mapping.nameserver.host)
}, {
    "metric": 'ping.avg.{}'.format(mapping.c),
    "endpoint": hostname,
    "timestamp": date,
    "step": 300,
    "value": mapping.nameserver.avg,
    "counterType": "GAUGE",
    "tags": 'test_ip={}'.format(mapping.nameserver.host)
}, {
    "metric": 'ping.min.{}'.format(mapping.c),
    "endpoint": hostname,
    "timestamp": date,
    "step": 300,
    "value": mapping.nameserver.min,
    "counterType": "GAUGE",
    "tags": 'test_ip={}'.format(mapping.nameserver.host)
}, {
    "metric": 'ping.max.{}'.format(mapping.c),
    "endpoint": hostname,
    "timestamp": date,
    "step": 300,
    "value": mapping.nameserver.max,
    "counterType": "GAUGE",
    "tags": 'test_ip={}'.format(mapping.nameserver.host)
}
]
