import paramiko
from contextlib import closing
from scp import SCPClient
import progressbar


bar = progressbar.ProgressBar()


def get(name, total, pos):
    bar.widgets = ['上传 ', name.decode(), ' ', progressbar.Percentage(),
                   progressbar.Bar(marker='#', left='[', right=']'),
                   progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
    bar.max_value = total
    bar.update(pos)


class SSHclient:
    def __init__(self, ip, port, usrname, passwd):
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=ip, port=port, username=usrname, password=passwd)

    def push(self, file, where):
        with closing(SCPClient(self.ssh.get_transport(), progress=get)) as scp:
            scp.put(file, where)

    def run(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command=command)
        out, err = stdout.read(), stderr.read()
        return err if err or err != b'' else out

    def __del__(self):
        self.ssh.close()
