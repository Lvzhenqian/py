import poplib, pickle
from email.header import *


class MailStatus:
	def __init__(self):
		self.__config = './me.ini'
		self.config_read(self.__config)

	def config_read(self, x):
		with open(x, 'r', encoding='utf-8') as red:
			for line in red:
				if line.startswith('link'):
					self.__link = line.rstrip('\n').split('=')[1].strip()
				elif line.startswith('user'):
					self.__user = line.rstrip('\n').split('=')[1].strip()
				elif line.startswith('password'):
					self.__password = line.rstrip('\n').split('=')[1].strip()
				elif line.startswith('localmail'):
					self.localmail = int(line.rstrip('\n').split('=')[1].strip())

	def __stat_write(self, x, str):
		## write in config
		with open(x, 'r+') as fd:
			while True:
				line = fd.readline()
				if line.startswith('localmail'):
					c = (fd.tell() - len(line))
					break
			fd.seek(0)
			fd.seek(c)
			localstr = 'localmail = {}'.format(str)
			fd.writelines(localstr)

	def Conn(slef):

		p = poplib.POP3(slef.__link)
		p.user(slef.__user)
		p.pass_(slef.__password)
		ret = p.stat()
		if not slef.localmail or slef.localmail == 0:
			slef.localmail = 1
		for n in range(slef.localmail, ret[0] + 1):
			fp = p.top(n, 0)[1]
			if b'From: ftpin@7road.com' in fp:
				subject = [x for x in fp if x.startswith(b'Subject') or x.startswith(b' =?')]
				st = b''
				for i in range(len(subject)):
					t1, code = decode_header(subject[i].strip(b'Subject: ').decode())[0]
					if isinstance(t1, bytes):
						st += t1
					else:
						slef.write_body(t1)
				if st:
					slef.write_body(st.decode(code))
		slef.__stat_write(slef.__config, str=ret[0])

	def write_body(self, string):
		with open('/tmp/log.me', 'a') as fd:
			fd.writelines(string + '\n')


if __name__ == '__main__':
	email = MailStatus()
	email.Conn()
	print(email.localmail)
