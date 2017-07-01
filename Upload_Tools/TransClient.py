import paramiko
from scp import SCPClient

class SSHclient:
	def __init__(self, ip, port, usrname, passwd):
		self.ssh = paramiko.SSHClient()
		self.ssh.load_system_host_keys()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.ssh.connect(hostname=ip, port=port, username=usrname, password=passwd)

	def push(self, file, where):
		scp = SCPClient(self.ssh)
		scp.put(file, where)
		return scp.close()

	def run(self, command):
		stdin, stdout, stderr = self.ssh.exec_command(command=command)
		return stderr.read() if stderr or stderr != b'' else stdout.read()

	def __del__(self):
		self.ssh.close()