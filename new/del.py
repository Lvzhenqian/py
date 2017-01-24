#!/usr/bin/env python
# coding=utf-8
import poplib
from email.header import *
conn = poplib.POP3('mail.7road.com')
conn.user('lv')
conn.pass_('angelo_5566!@')
delnum = conn.stat()[0]
delsub = '告警平台'.encode()
try:
    with open('/tmp/mail.log','a') as fd:
        for num in range(1,delnum+1):
            subject = [x for x in conn.top(num,0)[1] if x.startswith(b'Subject')]
            patter = decode_header(subject.pop().lstrip(b'Subject: ').decode())[0][0]
            if isinstance(patter,bytes)and delsub in patter:
                ret = conn.dele(num)
                if not b'OK' in ret:
                    fd.write(str(num)+'...{}.error....\n'.format(patter.decode('utf8')))
                fd.write(patter.decode('utf8')+'\n')
    conn.quit()
    conn.close()
except KeyboardInterrupt:
    conn.quit()
    conn.close()
