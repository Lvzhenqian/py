import paramiko
import socket
import os
from stat import S_ISDIR


class SSH:
	def __init__(self, host: str, port: int, user: str, passwd: str, pKey=None, keypass=None):
		self.client = paramiko.Transport((host, port))
		if pKey:
			key = paramiko.RSAKey.from_private_key_file(pKey, password=keypass)
			self.client.connect(username=user, pkey=key)
		else:
			self.client.connect(username=user, password=passwd)
		# self.client.start_client()
		self.sftp = paramiko.SFTPClient.from_transport(self.client)

	def runner(self, command: str):
		ssh = paramiko.SSHClient()
		ssh._transport = self.client
		stdin, stdout, stderr = ssh.exec_command(command,get_pty=True,bufsize=0)
		while True:
			try:
				out = stdout.readline()
				err = stderr.readline()
				print(out.strip('\n'))
			except KeyboardInterrupt:
				break
			except Exception as e:
				break
			if out == '' and err == '':
				break
			if err:
				break

	# def other_run(self,command):
	# 	ssh = paramiko.SSHClient()
	# 	ssh._transport = self.client
	# 	channel = self.client.open_session()

	def put(self, file: str, path: str):
		self.sftp.put(file, path)

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
		self.sftp.get(path, file)

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

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.client.close()

	def __del__(self):
		self.client.close()


if __name__ == '__main__':
	with SSH(host='192.168.8.231', port=22, user='root', passwd='hd8832508') as ssh:
		ssh.runner("ping -c3 www.baidu.com")
