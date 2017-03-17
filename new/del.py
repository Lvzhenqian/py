#!/usr/bin/env python
# coding=utf-8
import poplib
from email.header import *
import threading
import datetime
import getpass

lock = threading.RLock()
clean = 0


def child(s, e, conn):
    sub = '告警平台'.encode()
    try:
        lock.acquire()
        global clean
        with open('/tmp/mail.log', 'a') as fd:
            for num in range(s, e + 1):
                subject = [x for x in conn.top(num, 0)[1] if x.startswith(b'Subject')]
                patter = decode_header(subject.pop().lstrip(b'Subject: ').decode())[0][0]
                if isinstance(patter, bytes) and sub in patter:
                    ret = conn.dele(num)
                    if b'OK' not in ret:
                        fd.write(str(num) + '...{}.error....\n'.format(patter.decode('utf8')))
                    fd.write(patter.decode('utf8') + '\n')
                    clean += 1
    finally:
        lock.release()


def main():
    now = datetime.datetime.now()
    print('script is running on: {}'.format(now.strftime('%H:%M:%S')))
    connect = poplib.POP3('mail.7road.com')
    while True:
        try:
            user = input('username >>> ')
            if user.lower() == 'quit':
                return
            connect.user(user.strip())
            passwd = getpass.getpass()
            ret = connect.pass_(passwd.strip())
            if b'welcome' in ret:
                print('now:{} is starting.....'.format(now.strftime('%H:%M:%S')))
                break
        except:
            print('username or password is error. please retry!!')
    have = connect.stat()[0]
    print('{} is on the server'.format(have))
    lst = []
    s = 500 if have > 500 else 1
    for i in range(s, have + 1, s):
        st, ed = (i - s) + 1, i
        lst.append(threading.Thread(target=child, args=(st, ed, connect)))
    for c in lst:
        c.start()
    for c in lst:
        c.join()
    connect.quit()
    connect.close()
    end = datetime.datetime.now()
    total = end - now
    print('script \033[1;31m del {} \033[0m, now have {}'.format(clean, have - clean))
    print('script is stop on: {}'.format(end.strftime('%H:%M:%S')))
    print('total: {}'.format(total.total_seconds()))


if __name__ == '__main__':
    main()
