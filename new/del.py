#!/usr/bin/env python
# coding=utf-8
import poplib
from email.header import *
import threading
import datetime

lock = threading.RLock()


def child(s, e, conn):
    delsub = '告警平台'.encode()
    try:
        lock.acquire()
        with open('/tmp/mail.log', 'a') as fd:
            for num in range(s, e + 1):
                subject = [x for x in conn.top(num, 0)[1] if x.startswith(b'Subject')]
                patter = decode_header(subject.pop().lstrip(b'Subject: ').decode())[0][0]
                if isinstance(patter, bytes) and delsub in patter:
                    ret = conn.dele(num)
                    if not b'OK' in ret:
                        fd.write(str(num) + '...{}.error....\n'.format(patter.decode('utf8')))
                    fd.write(patter.decode('utf8') + '\n')
    finally:
        lock.release()



def main():
    now = datetime.datetime.now()
    print('script is running on: {}'.format(now.strftime('%H:%M:%S')))
    connect = poplib.POP3('mail.7road.com')
    connect.user('lv')
    connect.pass_('angelo_5566!@')
    delnum = connect.stat()[0]
    print('{} is on the server'.format(delnum))
    threadlist = []
    s = 500 if delnum > 500 else 1
    for i in range(s, delnum + 1, s):
        st, ed = (i - s) + 1, i
        threadlist.append(threading.Thread(target=child, args=(st, ed, connect)))
    for c in threadlist:
        c.start()
    for c in threadlist:
        c.join()
    connect.quit()
    connect.close()
    end = datetime.datetime.now()
    total = end - now
    print('script is running on: {}'.format(end.strftime('%H:%M:%S')))
    print('total: {}'.format(total.total_seconds()))


if __name__ == '__main__':
    main()
