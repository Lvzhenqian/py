from hashlib import md5
from shutil import move as mv
import os, sys
import threading
from queue import Queue

class dispatcher:
	def __init__(self, sourcefile):
		self.q = Queue(maxsize=1000)
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
		for enter in  os.scandir(path):
			if enter.is_file():
				self.q.put(enter.path)
			else:
				self.read_date(enter.path)

	def producer(self):
		with self.cond:
			self.read_date(r'C:\Windows\System32\drivers')
			self.cond.notifyAll()
		self.event.wait()
		self.event.set()

	def consumer(self):
		while not self.event.is_set():
			with self.cond:
				self.cond.wait()
				self.Do_delete(self.source, self.q.get())


if __name__ == '__main__':
	condition = dispatcher(sys.argv[1])
	master = threading.Thread(target=condition.producer, name='producer')
	for x in range(20):
		threading.Thread(target=condition.consumer, name='consumer').start()
	master.start()
	sys.exit()
