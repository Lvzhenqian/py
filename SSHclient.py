import os
import select
from stat import S_ISDIR
import sys
import socket
import termios
import tty

import paramiko
import logging
import progressbar
from colorlog import ColoredFormatter

LOGFORMAT = ColoredFormatter(
	fmt='[%(asctime)s]:[%(funcName)s]:%(log_color)s%(lineno)d:%(reset)s%(log_color)s'
		'%(levelname)s%(reset)s:%(message_log_color)s%(message)s',
	log_colors={
		'DEBUG': 'cyan',
		'INFO': 'green',
		'ERROR': 'red',
		'WARNING': 'yellow',
		'CRITICAL': 'red,bg_white',
	}, secondary_log_colors={
		'message': {
			'ERROR': 'red',
			'CRITICAL': 'red',
			'DEBUG': 'white',
			'INFO': 'white',
			'WARNING': 'yellow'
		}
	})

class Progress:
	def __init__(self, address, name):
		self.bar = progressbar.ProgressBar()
		self.bar.widgets = [
			address, ":", name, " ", progressbar.Percentage(),
			progressbar.Bar(marker="█", left='|', right="|"),
			progressbar.ETA(), " ", progressbar.FileTransferSpeed()
		]
		self.bar.start()

	def update(self, pos, total):
		self.bar.max_value = total
		self.bar.update(pos)

	def __del__(self):
		self.bar.finish()


class SSH:
	def __init__(self, host: str, port: int, user: str, passwd: str, pKey=None, keypass=None, invoke=False):
		# loger
		self.loger = logging.getLogger("SSH")
		self.loger.setLevel(logging.DEBUG)
		self.loger.propagate = False
		console = logging.StreamHandler(stream=sys.stdout)
		console.setLevel(logging.DEBUG)
		console.setFormatter(LOGFORMAT)
		self.loger.addHandler(console)
		# client
		self.address = (host, port)
		self.client = paramiko.Transport(self.address)
		if invoke:
			self.client.start_client()
			self.client.auth_password(username=user, password=passwd)
		elif pKey:
			key = paramiko.RSAKey.from_private_key_file(pKey, password=keypass)
			self.client.connect(username=user, pkey=key)
			self.sftp = paramiko.SFTPClient.from_transport(self.client)
		else:
			self.client.connect(username=user, password=passwd)
			self.sftp = paramiko.SFTPClient.from_transport(self.client)


	def runner(self, command: str):
		ssh = paramiko.SSHClient()
		ssh._transport = self.client
		stdin, stdout, stderr = ssh.exec_command(command, get_pty=True, bufsize=0)
		while True:
			try:
				out = stdout.readline()
				err = stderr.readline()
				linebreak = b'\r\n' if b'\r' in out else b'\n'
				st = out.split(linebreak)
				for s in st:
					if s:
						self.loger.info(s.decode('utf8'))
			except KeyboardInterrupt:
				break
			except Exception as e:
				break
			if out == '' and err == '':
				break
			if err:
				break

	def other_run(self, command):
		channel = self.client.open_session()
		channel.get_pty()
		# self.loger.debug(command)
		# self.loger.warning("aaaa")
		channel.exec_command(command)
		while not channel.exit_status_ready():
			try:
				rlist, wlist, xlist = select.select([channel], [], [], 1)
				if len(rlist) > 0:
					recv = channel.recv(65533)
					linebreak = b'\r\n' if b'\r' in recv else b'\n'
					lines = recv.split(linebreak)
					for s in lines:
						if s:
							self.loger.info(s.decode('utf8'))
			except KeyboardInterrupt:
				channel.send("\x03")  # 发送 ctrl+c
				channel.close()
				self.client.close()

	def put(self, file: str, path: str):
		bar = Progress(address=self.address[0], name=os.path.basename(file))
		self.sftp.put(file, path, callback=bar.update)

	def put_all(self, localpath: str, remotepath: str):
		os.chdir(os.path.split(localpath)[0])
		parent = os.path.split(localpath)[1]
		for walker in os.walk(parent):
			try:
				self.sftp.mkdir(os.path.join(remotepath, walker[0]))
			except:
				pass
			for file in walker[2]:
				self.put(os.path.join(walker[0], file), os.path.join(remotepath, walker[0], file))

	def get(self, path: str, file: str):
		bar = Progress(address=self.address[0], name=os.path.basename(file))
		self.sftp.get(path, file, callback=bar.update)

	def sftp_walk(self, remotepath):
		path = remotepath
		files = []
		folders = []
		for f in self.sftp.listdir_attr(remotepath):
			if S_ISDIR(f.st_mode):
				folders.append(f.filename)
			else:
				files.append(f.filename)
		print(path, folders, files)
		yield path, folders, files
		for folder in folders:
			new_path = os.path.join(remotepath, folder)
			for x in self.sftp_walk(new_path):
				yield x

	def get_all(self, remotepath, localpath):
		self.sftp.chdir(os.path.split(remotepath)[0])
		parent = os.path.split(remotepath)[1]
		try:
			os.mkdir(localpath)
		except:
			pass
		for walker in self.sftp_walk(parent):
			try:
				os.mkdir(os.path.join(localpath, walker[0]))
			except:
				pass
			for file in walker[2]:
				self.get(os.path.join(walker[0], file), os.path.join(localpath, walker[0], file))

	def start(self):
		channel = self.client.open_session()
		channel.get_pty()
		channel.invoke_shell()
		oldtty = termios.tcgetattr(sys.stdin)
		try:
			tty.setraw(sys.stdin)
			channel.settimeout(0)
			while True:
				r, w, e = select.select([channel, sys.stdin], [], [], 1)

				if channel in r:
					try:
						x = channel.recv(1024)
						if len(x) == 0:
							print("\r退出登录\r")
							break
						# self.loger.debug(x)
						sys.stdout.write(x.decode())
						sys.stdout.flush()
					except socket.timeout:
						pass

				if sys.stdin in r:
					i = sys.stdin.read(1)
					if len(i) == 0:
						break
					channel.send(i)
		finally:
			termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.client.close()

	def __del__(self):
		self.client.close()


if __name__ == '__main__':
	with SSH(host='192.168.19.21', port=22, user='root', passwd='hd8832508',invoke=True) as ssh:
		# ssh.other_run("ping -c3 www.baidu.com")
		ssh.start()
		# ssh.runner('w')
