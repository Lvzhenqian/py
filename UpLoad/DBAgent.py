from hashlib import md5
import zipfile
from shutil import copy2
import os
import subprocess
import argparse

args = argparse.ArgumentParser(prog='DBUpdate-tools', description='DBUpdate client')
args.add_argument('dts', type=str, default=False)
args.add_argument('sqlrun', type=str, default=False)
args.add_argument('AutoUpdate', type=str, default=False)
opt = args.parse_args()


def md5sum(path):
    with open(file=path, mode='rb') as f:
        m = md5(f.read())
        return m.hexdigest()


class DBUpdate:
    def __init__(self, key):
        self.__key = key
        self.ExtracPAth = r'd:\server-new\dandantang'
        self.md5key = os.path.join(self.ExtracPAth, 'md5.key')
        self.UpdatePath = os.path.join(self.ExtracPAth, 'dandantang')
        self.BackupPath = r'd:\server-bak\rollback\dandantang'
        self.Updatelist = []
        self.back_list = []

    def __get_list_from_key(self):
        with open(self.md5key, mode='rt', encoding='utf8') as fd:
            for line in fd:
                md, fp = line.split()
                if md5sum(fp) != md:
                    raise zipfile.BadZipfile('Extrac {} File Bad! please retry!'.format(fp))
                self.Updatelist.append((md, os.path.realpath(fp)))

    def File_Ready(self, path=r'd:\server-new\dandantang.zip'):
        if md5sum(path) != self.__key:
            raise zipfile.BadZipfile('File MD5 is not same,please retry! ')
        zfile = zipfile.ZipFile(path, 'r')
        zfile.extractall(self.ExtracPAth)
        self.__get_list_from_key()

    def backup(self):
        self.back_list = [path.replace(self.UpdatePath, r'd:\dandantang') for path in self.UpdatePath]
        for file in self.back_list:
            dest = file.replace(r'd:\dandantang', self.BackupPath)
            if not os.path.exists(os.path.dirname(dest)):
                os.makedirs(os.path.dirname(dest))
            copy2(src=file, dst=dest)

    def update(self):
        if not self.back_list:
            raise ValueError('not to backup,please backup first!')
        for files in self.Updatelist:
            dest = files.replace(self.UpdatePath, r'd:\dandantang')
            copy2(src=files, dst=dest)
    @classmethod
    def DTS(cls):
        d = subprocess.run('DtsConsole.exe -dts run 400', shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with open('d:\DTSLOG.txt', mode='w', encoding='utf8') as output:
            output.write(d.stdout)
    @classmethod
    def RunSql(cls,sql):
        stats = subprocess.Popen('sqlcmd -S 127.0.0.1,2433 -i {} -E -r0'.format(sql), shell=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stats.wait()
        with open('Sql.log', mode='a', encoding='utf8') as fd:
            fd.write(stats.stdout)
        with open('Sql-err.log', mode='a', encoding='utf8') as fe:
            fe.write(stats.stderr)

    def Update_sql(self):
        sql = [os.path.realpath(x) for x in os.listdir(self.UpdatePath) if os.path.isfile(x) and x.endswith('.sql')]
        if not sql:
            return
        for s in sql:
            self.RunSql(s)

    def AutoUpdate(self):
        self.File_Ready()
        self.backup()
        self.update()
        self.Update_sql()
        self.DTS()


if __name__ == '__main__':
    if opt.dts:
        DBUpdate.DTS()
    if opt.sqlrun:
        DBUpdate.RunSql()
    DBUpdate()
