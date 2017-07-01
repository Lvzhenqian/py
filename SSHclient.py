import paramiko


class SSH:
	def __init__(self, host: str, port: int, user: str, passwd: str, pKey=None, keypass=None):
		self.client = paramiko.Transport((host, port))
		if pKey:
			key = paramiko.RSAKey.from_private_key_file(pKey, password=keypass)
			self.client.connect(username=user, pkey=key)
		else:
			self.client.connect(username=user, password=passwd)

	def runner(self, command: str):
		ssh = paramiko.SSHClient()
		ssh._transport = self.client
		stdin, stdout, stderr = ssh.exec_command(command)
		if stderr:
			return stderr.read().decode()
		return stdout.read().decode()

	def push(self, file: str, path: str):
		sftp = paramiko.SFTPClient.from_transport(self.client)
		return sftp.put(file, path)

	def get(self, path: str, file: str):
		sftp = paramiko.SFTPClient.from_transport(self.client)
		return sftp.get(path, file)

	def __del__(self):
		self.client.close()
