import socket, sys
import threading,os
import argparse


def opt():
    options = argparse.ArgumentParser(description='out put time size')
    options.add_argument(
        '--port', '-p',
        nargs='*',
        dest='port',
        help='connect to port'
    )
    return options.parse_args()


class cli:
    def __init__(self):
        self.dic = {}

    def sock_conn(self, ip, port,names,ev):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        try:
            while not ev.is_set():
                d = s.recv(29)
                self.dic[names] = d.replace(b'\n', b'').decode()
        except KeyboardInterrupt:
            pass
        return self.dic


if __name__ == '__main__':
    event = threading.Event()
    op = opt()
    cla = cli()
    lst = []
    if not op.port:
        sys.exit()
    for name,p in enumerate(op.port[1:]):
        t = threading.Thread(target=cla.sock_conn, args=(op.port[0], p,str(name),event))
        t.start()


    try:
        while True:
            if len(cla.dic.keys()) == len(op.port[1:]):
                for k in cla.dic.keys():
                    lst.append(cla.dic[k])
                print('|'.join(tuple(lst)),end='\r')
            lst.clear()
            event.wait(0.9)

    except KeyboardInterrupt:
        print('client is end...')