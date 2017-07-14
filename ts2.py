import paramiko

with paramiko.SSHClient() as ssh:
	ssh.connect(('192.168.0.12',22))
	stdin,stdout,stderr = ssh.exec_command('ls /tmp')