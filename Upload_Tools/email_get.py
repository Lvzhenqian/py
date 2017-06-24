from poplib import POP3
from email.base64mime import body_decode
from urllib.request import Request, urlopen
from urllib import parse
import json
import re


class mail_down:
	def __index__(self, oa, tag=True):
		with open('./config.json') as f:
			conf = json.loads(f.read())
		self.__username = conf['email']['name']
		self.__passwd = conf['email']['password']
		self.mail = POP3('mail.7road.com')
		self.mail.user(self.__username)
		self.mail.pass_(self.__passwd)
		self.__tag = tag
		self.__oa = oa

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
		for n in range(total, total - 101, -1):
			dic = self.__read_body(n)
			if dic['OA'] == self.__oa:
				return dic
		else:
			return

	def download_pack(self):
		m = self.__choose_mail()
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
		querystring = parse.urlencode(param)
		req = Request(url=url, data=querystring.encode('ascii'), headers=header)
		op = urlopen(req).read()
		with open(r'd:/2.zip', 'wb') as f:
			f.write(op)