# coding:utf-8
#!bin/python
import argparse
import logging
import csv
import sys
import threading
from collections import namedtuple
from urllib.request import urlopen

import paramiko
from scp import SCPClient

opt = argparse.ArgumentParser(prog='7road合区辅助工具', add_help=False,
							  description='从当前merge.csv文件读取出合区信息，然后传输合区工具，停防火墙，停WebServer')
opt.add_argument('tools', nargs='*', type=str, help='指定合区工具路径并上传到主区上。执行方法：脚本名 工具路径。')
opt.add_argument('run', dest='run', default=False, action='store_true', help='直接运行这个工具，列出其中的方法来执行！')

log = logging.StreamHandler()
log.setLevel(logging.INFO)
fmt = logging.Formatter('%(threadName)s: %(message)s')
log.setFormatter(fmt)
console = logging.getLogger()
console.addHandler(log)


def iplist():
	db = {}
	gs = {}
	url = 'http://yw.7road-inc.com:8081/LoadGameData?g=6000,-1&s=1&gameId=22'
	req = urlopen(url).read()
	body = req.decode('utf8')
	for lines in body.split('|||'):
		line = lines.split('|')
		if len(line) > 1 and 'DB' in line[1]:
			db[line[5]] = (line[5], line[2])
		if len(line) > 1 and 'Web' in line[1]:
			gs[line[5]] = (line[5], line[2])
	return db, gs


class SSHclient:
	def __init__(self, ip, port, usrname, passwd):
		self.ssh = paramiko.SSHClient()
		self.ssh.load_system_host_keys()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.ssh.connect(hostname=ip, port=port, username=usrname, password=passwd)

	def push(self, file):
		scp = SCPClient(self.ssh)
		scp.put(file, '/cygdrive/d')
		return scp.close()

	def run(self, command):
		stdin, stdout, stderr = self.ssh.exec_command(command=command)
		return stderr.read() if stderr or stderr != b'' else stdout.read()

	def __del__(self):
		self.ssh.close()


class MergeTools:
	def __init__(self, MergeExcel):
		self.db_map, self.gs_map = iplist()
		self.csv = MergeExcel
		self.name = None

	def __ReadCsv(self):
		with open(self.csv) as f:
			f_csv = csv.reader(f)
			_ = next(f_csv)
			data = namedtuple('data', ['name', 'more', 'master'])
			while True:
				try:
					i = next(f_csv)
					yield data(i[11], i[14], i[15])
				except StopIteration:
					break

	def Get_Work_List(self, master=False):
		rule = {
			"百度": 'baidu_{:0>4}'.format,
			"7road官网": '7road_{:0>4}'.format,
			"多玩": 'duowan_{:0>4}'.format,
			"7k7k": '7k7k_{:0>4}'.format,
			"开心": 'kxwang_{:0>4}'.format,
			"奇虎": 'qihu360_{:0>4}'.format,
			"上海淘米": 'taomi_{:0>4}'.format,
			"4399": '4399_{:0>4}'.format
		}
		ret = []
		ft = lambda st: ''.join([x for x in st.split('-')[0] if x in '0123456789'])
		excel = self.__ReadCsv()
		for lines in excel:
			if master:
				ms = ft(lines.master)
				if lines.name:
					self.name = lines.name
				if '7road' in self.name or '官网' in self.name:
					site = rule["7road官网"](ms)
					ret.append(self.db_map[site])
				if '360' in self.name or '奇虎' in self.name:
					site = rule["奇虎"](ms)
					ret.append(self.db_map[site])
				if 'kx' in self.name or '开心' in self.name:
					site = rule["开心"](ms)
					ret.append(self.db_map[site])
				if 'taomi' in self.name or '淘米' in self.name:
					site = rule["上海淘米"](ms)
					ret.append(self.db_map[site])
				site = rule[self.name](ms)
				ret.append(self.db_map[site])
			else:
				add = lambda x: ret.append(x) if x not in ret else None
				for ne in lines.more.split('、'):
					n = ft(ne)
					if lines.name:
						self.name = lines.name
					if '7road' in self.name or '官网' in self.name:
						site = rule["7road官网"](n)
						add(site)
					if '360' in self.name or '奇虎' in self.name:
						site = rule["奇虎"](n)
						add(site)
					if 'kx' in self.name or '开心' in self.name:
						site = rule["开心"](n)
						add(site)
					if 'taomi' in self.name or '淘米' in self.name:
						site = rule["上海淘米"](n)
						add(site)
					site = rule[self.name](n)
					add(site)
		return ret

	def SendMergeTools(self, tool):
		for site, ip in self.Get_Work_List(master=True):
			scp = SSHclient(ip, port=26333, usrname='7RoAdmin', passwd="AO%7Ro*AD35@bTa")
			console.info('开始合区工具传送到{site}--{ip}'.format(site=site, ip=ip))
			threading.Thread(target=scp.push, args=(tool,), name=site).start()

	def OFF_Firewalled(self):
		cmd = 'netsh ipsec static set policy name=7road assign=n'
		for site in self.Get_Work_List():
			s, ip = self.db_map[site]
			console.info('开始停止{site}--{ip}防火墙'.format(site=s, ip=ip))
			scp = SSHclient(ip, port=26333, usrname='7RoAdmin', passwd="AO%7Ro*AD35@bTa")
			threading.Thread(target=scp.run, args=(cmd,), name=s).start()

	def OFF_WebServer(self):
		cmd = '/root/cgddt.sh stop'
		for sites in self.Get_Work_List():
			site, ip = self.gs_map[sites]
			ssh = SSHclient(ip, port=16333, usrname='root', passwd='#!9BVAPlDJ2%Nj@z')
			console.info('开始停止{site}--{ip}Web服务器'.format(site=site, ip=ip))
			threading.Thread(target=ssh.run, args=(cmd,), name=site).start()


if __name__ == '__main__':
	args = opt.parse_args()
	master = MergeTools('./merge.csv')
	if args.tools:
		master.SendMergeTools(args.tools)
		sys.exit()
	if args.run:
		print('''
		1. 传送mergetools.zip 到DB服务器上。
		2. 停掉所有全区的DB防火墙
		3. 停掉WebServer的游戏进程（5分钟倒计时）
		4. 退出程序
		''')
		while True:
			n = input('输入要执行的操作[1.Send|2.StopFirewall|3.StopWeb|4.quit]：')
			if n == '1' or n.lower() == 'send':
				master.SendMergeTools('./mergetools.zip')
			if n == '2' or n.lower() == 'stopfirewall':
				master.OFF_Firewalled()
			if n == '3' or n.lower() == 'stopweb':
				master.OFF_WebServer()
			if n == '4' or n.lower() == 'quit':
				break
		sys.exit()
