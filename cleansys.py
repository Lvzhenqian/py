from hashlib import md5
from shutil import move as mv
import os, sys
import threading
import logging

class dispatcher:
	def __init__(self, sourcefile):
		self.source = self.md5sum(sourcefile)
		self.data = None
		self.event = threading.Event()
		self.cond = threading.Condition()

	def md5sum(self, file: str) -> str:
		try:
			with open(file, 'rb') as f:
				return md5(f.read()).hexdigest()
		except FileNotFoundError:
			return ''

	def Do_delete(self, source, destion: list):
		tmp = r'D:\temp'
		if not os.path.exists(tmp):
			os.mkdir(tmp)
		for d in destion:
			if self.md5sum(d) == source:
				mv(d, tmp)
				print('move {} successful'.format(d))
		return True

	def read_date(self, path):
		dl = []
		for root, _, file in os.walk(path):
			if file:
				l = [os.path.join(root, x) for x in file]
				dl.extend(l)
		return dl

	def producer(self):
		data = self.read_date(r'C:\Windows\System32\drivers')
		print(len(data))
		index, n = 0, 1 if len(data) % 1000 else 0
		for _ in range((len(data) // 1000) + n):
			self.data = data[index:index + 1000]
			with self.cond:
				self.cond.notifyAll()
			self.event.wait()
			index += 1000
		self.event.set()

	def consumer(self):
		while not self.event.is_set():
			with self.cond:
				self.cond.wait()
				self.Do_delete(self.source, self.data)


if __name__ == '__main__':
	condition = dispatcher(sys.argv[1])
	master = threading.Thread(target=condition.producer, name='producer')
	for x in range(20):
		threading.Thread(target=condition.consumer, name='consumer').start()
	master.start()
	sys.exit()
