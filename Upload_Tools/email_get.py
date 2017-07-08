from poplib import POP3
from email.base64mime import body_decode
from contextlib import closing
import progressbar
import requests
from urllib import parse
import re
import os


class mail_down:
    def __init__(self, user, pswd, oa, tag=False):

        self.__username = user
        self.__passwd = pswd
        self.mail = POP3('mail.7road.com')
        self.mail.user(self.__username)
        self.mail.pass_(self.__passwd)
        self.__tag = tag  # True 表示匹配国内的邮件，反之则是海外的。
        self.__oa = oa
        self.Md5 = None

    def __read_body(self, mail_num):
        tmp = []
        flag = False
        if self.__tag:
            o = re.compile(r'OA.*:(?P<OA>\d+)<.*md5:(?P<md5>\w+).*<a href=\'(?P<url>.*)\'.*')
        else:
            o = re.compile(r'OA.*:(?P<OA>\d+)<.*md5:(?P<md5>\w+).*=(?P<agent>\w+)<br>.*<a href=\'(?P<url>.*)\'.*')
        for i in self.mail.retr(mail_num)[1]:
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

    def __choose_mail(self):
        total = self.mail.stat()[0]
        for n in range(total, 1, -1):
            fp = self.mail.top(n, 0)[1]
            if b'From: ftpin@7road.com' in fp:
                dic = self.__read_body(n)
                if dic and dic['OA'] == self.__oa:
                    return dic
        else:
            return

    def download_pack(self, save_path):
        requests.packages.urllib3.disable_warnings()
        m = self.__choose_mail()
        if not m:
            return
        self.Md5 = m['md5']
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.76 Safari/537.36'
        }
        urlp = parse.urlsplit(m['url'])
        _, keywd = urlp.query.split('=', 1)
        url = 'http://ftpin.7road.com:8080/down'.replace('ftpin.7road.com', urlp.hostname)
        param = {
            'username': self.__username,
            'password': self.__passwd,
            'key': keywd}
        with closing(requests.request(method='POST', url=url, data=param, headers=header, stream=True)) as response:
            chunk_size = 1024  # 单次请求最大值
            content_size = int(response.headers['content-length'])
            # flag = 0 if content_size % chunk_size == 0 else 1
            # mxv = (content_size // chunk_size) + flag
            pkg = os.path.realpath(os.path.join(save_path,'update.zip'))
            with open(pkg, 'wb') as f:
                widgets = ['下载：', progressbar.Percentage(), progressbar.Bar(marker='#', left='[', right=']'),
                           progressbar.ETA()]
                with progressbar.ProgressBar(widgets=widgets, maxval=content_size) as bar:
                    n = 0
                    while n < content_size:
                        chunk = next(response.iter_content(chunk_size=chunk_size))
                        if chunk:
                            f.write(chunk)
                            f.flush()
                        bar.update(n)
                        n += len(chunk)

                    # n = 0
                    # for chunk in response.iter_content(chunk_size=chunk_size):
                    #     if chunk:
                    #         f.write(chunk)
                    #         f.flush()
                    #     bar.update(n)
                    #     n += 1
        return os.path.realpath(pkg)

    def __del__(self):
        return self.mail.close()
