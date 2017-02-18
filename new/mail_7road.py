# coding:utf-8
import poplib
from email.base64mime import body_decode
import threading
import re
from datetime import datetime

mail = []
lock = threading.RLock()


def conn(x, n):
    try:
        lock.acquire()
        global mail
        if b'FTP-IN.7ROAD.COM' in x.top(n, 0)[1][0]:
            mail.append(n)
            return
        else:
            return
    finally:
        lock.release()


def read_body(c, x, code=None):
    tmp = []
    flag = False
    o = re.compile(
        r'OA单号为:(?P<oa>.*)<br/>成.*md5:(?P<md5>.*)<br/>作.*project:::(?P<project>.*)dba:::(?P<dba>\w{1,3})cross:::(?P<cross>\w{1,3})yufabu:::(?P<yufabu>\w{1,3})stop:::(?P<stop>\w{1,3}).*<a href=\'(?P<url>.*)\'>点.*')
    for i in c.retr(x)[1]:
        if i.startswith(b'Content-Transfer-Encoding'):
            code = i.rstrip()[-1]
            flag = True
            continue
        elif i.endswith(b'==--'):
            break
        elif flag:
            tmp.append(i)
    body = b''.join(tmp)
    if code == 'base64':
        ret = o.match(body_decode(body).decode('utf-8'))
        if ret:
            return ret.groupdict()


if __name__ == '__main__':
    now = datetime.now()
    print(now.strftime('%H:%M:%S'))
    count = []
    con = poplib.POP3('mail.7road.com')
    con.user('lv')
    con.pass_('angelo_5566!@')
    total_mail = con.stat()[0]
    print('mail server have: {}'.format(total_mail))
    for i in range(total_mail, int(total_mail // 2), -1):
        count.append(threading.Thread(target=conn, args=(con, i)))
    for t in count:
        if not mail:
            t.start()
            t.join(1)
    for em in mail:
        dic = read_body(con,em)
        print(dic)
    end = datetime.now() - now
    print(end.total_seconds())

