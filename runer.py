import subprocess
from collections import namedtuple
def Ping(host: str, c=2) -> namedtuple:
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

    req = namedtuple('stat', ['host', 'lost', 'avg', 'max', 'min'])
    with subprocess.Popen('cmd /c chcp 437 & ping -n {count} {host}'.format(count=c, host=host),
                               shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE, universal_newlines=True
                          ) as process:
        print(process.pid)
        process.wait()
        for _ in range(10000):
            if process.poll() is not None:
                out = process.stdout.readlines()
                print(out)
                if 'Average' in out[-1]:
                    da = fil(out[-1])
                    return req(host, fil(out[-3])[-1], da[-1], da[1], da[0])
                else:
                    return req(host, 100, 0, 0, 0)

ip = namedtuple('IP', ['falcon', 'url', 'nameserver', 'c'])
mapping = ip(Ping('113.107.161.47'), Ping('www.baidu.com'), Ping('114.114.114.114'), 'GN')
print(mapping)