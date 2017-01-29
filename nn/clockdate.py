import threading, sys
import datetime, socket
from pytz import timezone, all_timezones
import argparse


def opt():
    options = argparse.ArgumentParser(description='out put time size')
    options.add_argument('address',
                         nargs='?',
                         type=str,
                         help='bind address'
                         )
    options.add_argument('-s',
                         '--show-timezone',
                         action='store_true',
                         default=False,
                         dest='show',
                         help='show how many timezone you can use it'
                         )
    options.add_argument(
        '--port', '-p',
        nargs='?',
        dest='port',
        help='bind in port,you can use "," to more ports'
    )
    options.add_argument(
        '--timezone', '-z',
        nargs='?',
        dest='zone',
        help='select timezone to show, you can use "," to more timezone'
    )
    return options.parse_args()


def Tzone(zones='Asia/Shanghai'):
    while True:
        zon = timezone(zones)
        now = datetime.datetime.now(zon).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        return now


def sock_bind(ip, port, time):
    event = threading.Event()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, int(port)))
    s.listen()

    def client_send(con, zone, ev):
        o = opt()
        try:
            while not ev.is_set():
                if o.zone and zone <= len(o.zone.split(','))-1:
                    ret = Tzone(o.zone.split(',')[zone])
                else:
                    ret = Tzone()
                con.send(ret.encode() + b'\n')
                ev.wait(1)
        except BrokenPipeError:
            return con.close()
        return

    while not event.is_set():
        (conn, client) = s.accept()
        t = threading.Thread(target=client_send, args=(conn, time, event))
        t.start()
        event.wait(1)
    return


if __name__ == '__main__':
    op = opt()
    if op.show:
        for x in all_timezones:
            print(x)
        sys.exit()

    if not op.address:
        print('not bind any IP address,please retry.')
        sys.exit()

    if not op.port:
        print('not bind any ports,please retry.')
        sys.exit()

    for n, p in enumerate(op.port.split(',')):
        b = threading.Thread(target=sock_bind, args=(op.address, p, n))
        b.start()
