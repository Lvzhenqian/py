# coding:utf-8
import poplib
from email.base64mime import body_decode
import threading
import re
from datetime import datetime

mail = []
lock = threading.RLock()


def conn(x, n):
    global mail
    if b'FTP-IN.7ROAD.COM' in x.top(n, 0)[1][0]:
        mail.append(n)
        return
    return


def read_body(c, x):
    c.noop()
    tmp = []
    flag = False
    o = re.compile(r'OA.*:(?P<OA>\d+)<.*md5:(?P<md5>\w+).*<a href=\'(?P<url>.*)\'.*')
    for i in c.retr(x)[1]:
        if i.startswith(b'Content-Transfer-Encoding'):
            flag = True
            continue
        elif i.endswith(b'==--'):
            break
        elif flag:
            tmp.append(i)
    body = b''.join(tmp)
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
    for i in range(total_mail, 1, -1):
        count.append(threading.Thread(target=conn, args=(con, i)))
    for t in count:
        t.start()
        t.join(1)
    con.noop()
    for em in mail:
        dic = read_body(con, em)
        print(dic)
    end = datetime.now() - now
    print(end.total_seconds())
    con.quit()
    con.close()
