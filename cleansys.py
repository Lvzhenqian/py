from hashlib import md5
from shutil import move as mv
import os, threading
from queue import Queue


class dispatcher:
	def __init__(self, sourcefile):
		self.q = Queue(maxsize=1000)
		self.source = self.md5sum(sourcefile)

	def md5sum(self, file: str) -> str:
		try:
			with open(file, 'rb') as fd:
				return md5(fd.read()).hexdigest()
		except FileNotFoundError:
			return ''

	def Do_delete(self, dst):
		tmp = r'D:\temp'
		if not os.path.exists(tmp):
			os.mkdir(tmp)
		if self.md5sum(dst) == self.source:
			mv(dst, tmp)
			print('move {} successful'.format(dst))
		return

	def ds(self, xpath):
		for enter in os.scandir(xpath):
			if enter.is_file():
				yield enter.path
			else:
				self.ds(enter.path)

	def put(self, path):
		print('start,producer')

		g = self.ds(path)
		while True:
			try:
				data = next(g)
				self.q.put(data)
			except StopIteration:
				break

	def get(self):
		print('start get')
		d = self.q.get(1)
		self.Do_delete(d)
		print('sss')


if __name__ == '__main__':
	condition = dispatcher(r'e:\adpcqsppehzolpenarg.sys')
	q = threading.Thread(target=condition.put, args=(r'C:\Windows\System32\drivers',), name='put')
	g = threading.Thread(target=condition.get, name='consumer')
	q.start()
	g.start()
