import threading, sys
import datetime, socket
from pytz import timezone
import argparse


def opt():
    options = argparse.ArgumentParser(description='out put time size')
    options.add_argument(
        '--port', '-p',
        nargs='*',
        dest='port',
        help='bind in port'
    )
    options.add_argument(
        '--timezone', '-z',
        nargs='*',
        dest='zone',
        help='select timezone to show'
    )
    return options.parse_args()


def Tzone(zones='Asia/Shanghai'):
    while True:
        zon = timezone(zones)
        now = datetime.datetime.now(zon).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        return now


def sock_bind(ip, port, n,e):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((ip, int(port)))
        s.listen()
        (conn, client) = s.accept()
        while True:
            if op.zone:
                ret = Tzone(op.zone[n])
            else:
                ret = Tzone()
            conn.send(ret.encode() + b'\n')
            e.wait(1)
    except BrokenPipeError:
        pass
    except KeyboardInterrupt:
        pass
    except StopIteration:
        print('is ending...')
        e.set()
    conn.close()


if __name__ == '__main__':
    event = threading.Event()
    threadinglist = []
    op = opt()
    if not op.port:
        sys.exit()

    for n, p in enumerate(op.port[1:]):
            threadinglist.append(threading.Thread(target=sock_bind, args=(op.port[0], p, n,event)))
    print(threadinglist)
    while True:
        try:

            for tread in threadinglist:
                if not tread.is_alive():
                    print(threadinglist)
                    tread.start()

        except KeyboardInterrupt:
            pass
