# coding:utf-8
from .util import config
from urllib import request, parse, error
from subprocess import Popen, PIPE, DEVNULL, STARTUPINFO, STARTF_USESHOWWINDOW
from platform import machine, release
from shutil import move, rmtree
import socket, requests, json, time, os, logging, win32serviceutil
from hashlib import md5 as md5sum
from zipfile import ZipFile



class Agent:
	Install_Path = r'c:\7roadyw\agent'

	def __init__(self):
		self.__ip = 'http://ip.7road.net'
		self.__zk_ip = 'http://yw.7road-inc.com:8081/queryAssetsByIpJson'
		self.__Agent = 'http://fe.open-falcon.7road.net:9526/windows/agent.zip'
		self.AgentMd5 = 'http://fe.open-falcon.7road.net:9526/windows/md5.txt'
		self.__AgentManage = 'http://fe.open-falcon.7road.net:9526/windows/AgentUpgrade.exe'
		self.__Manage_Path = os.path.join(r'c:\7roadyw', 'AgentUpgrade.exe')
		self.__Download_Path = r'C:\falcon_agent'
		self.__Download_File = r'C:\falcon_agent\agent.zip'
		self.__Backup_Path = self.Install_Path + '_%s' % time.strftime('%Y-%m-%d')

	def __ChangeFile(self, ip, x):
		try:
			with open(x, mode='rt', encoding='utf8') as r:
				dit = r.read()
			fdit = json.loads(dit)
			fdit['hostname'] = ip
			logging.info('Change hostname=%s ' % ip)
			wf = os.path.join(self.__Download_Path, r'agent\cfg.json')
			logging.info('write to source file!')
			with open(wf, mode='wt', encoding='utf8') as w:
				wbody = json.dumps(fdit)
				w.write(wbody)
			logging.info('ChangeFile successful.')
			return True
		except FileNotFoundError:
			logging.error('Not File!')
			return False
		except FileExistsError:
			logging.error('Not File!')
			return False

	@classmethod
	def TestPort(cls, port: int):
		try:
			test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			test.connect(('127.0.0.1', port))
			time.sleep(1)
			test.close()
			return True
		except ConnectionRefusedError:
			logging.error('Cat not Client %s port!' % port)
			return False

	def __SelectIp(self):
		logging.info('Select IP for cfg.json')
		try:
			internet = request.urlopen(self.__ip).read().split()
			net, we = internet[0].decode(), internet[1]
			parms = {
				'ips': net,
				'props': 'ip1'
			}
			url = parse.urlencode(parms)
			req = request.urlopen(self.__zk_ip + '?' + url).read().decode()
			resp = json.loads(req)
			if resp['code'] == 0:
				zk_res, status = resp['data'][0][net]['ip1'], resp['code']
				if we == '中国'.encode():
					return zk_res, os.path.join(self.__Download_Path, 'agent\cfg.json')
				else:
					return zk_res, os.path.join(self.__Download_Path, 'agent\hwcfg.json')
			else:
				return net, os.path.join(self.__Download_Path, 'agent\cfg.json')
		except error.HTTPError:
			hsn = socket.gethostname()
			return socket.gethostbyname(hsn), os.path.join(self.__Download_Path, 'agent\cfg.json')

	def Download_Package(self, s_md5):
		try:
			if not os.path.isdir(self.__Download_Path):
				os.mkdir(self.__Download_Path)
			logging.info('Download Package.')
			agent = request.urlopen(self.__Agent).read()
			with open(self.__Download_File, 'wb') as f:
				f.write(agent)
			logging.info('Download AgentManage.')
			manage = request.urlopen(self.__AgentManage).read()
			with open(os.path.join(self.__Download_Path, 'AgentUpgrade.exe'), 'wb') as f:
				f.write(manage)
			with open(self.__Download_File, 'rb') as ff:
				down_md5 = md5sum(ff.read())
			if s_md5.split()[0].decode() == down_md5.hexdigest():
				logging.info('Install the package.now!')
				install_status = self.__Install(self.__Download_File, self.__Download_Path)
				rmtree(self.__Download_Path)
				if not install_status:
					return False
				return logging.info('Update finish.')
			else:
				return logging.warning('Download warning! please try to Download of yourself.')

		except error.HTTPError:
			return logging.error("Can't download the package.please check the Url.")

	def __Install(self, x: str, ds: str):
		Manage_Download = os.path.join(self.__Download_Path, 'AgentUpgrade.exe')

		def AddService():
			logging.info('Add To System service.')
			os.system(r'{server} install FalconAgent {exe}'.format(
				server=os.path.join(
					self.Install_Path, 'nssm64.exe') if machine() == 'AMD64' else os.path.join(
					self.Install_Path, 'nssm32.exe'),
				exe=os.path.join(self.Install_Path, 'windows-agent.exe')
			))
			time.sleep(2)
			try:
				win32serviceutil.StartService('falconagent')
			except Exception as e:
				logging.error(e)
			return True

		try:
			logging.info('unzip....plz wait.')
			f = ZipFile(x, mode='r')
			f.extractall(ds)
			logging.info('Starting.Install Thread!')
			ip, addr = self.__SelectIp()
			Change = self.__ChangeFile(ip, addr)
			if not Change:
				logging.error("Change File Error!")
				return False

			if not os.path.isdir(self.Install_Path):
				logging.info('Copying to %s' % self.Install_Path)
				move(os.path.join(self.__Download_Path, 'agent'), self.Install_Path)
				move(Manage_Download, self.__Manage_Path)
				AddService()
			elif Agent.TestPort(1988):
				try:
					logging.info('Stop service...')
					win32serviceutil.StopService('falconagent')
					time.sleep(3)
					if not os.path.exists(self.__Backup_Path):
						logging.info('Backup File to {}'.format(self.__Backup_Path))
						move(self.Install_Path, self.__Backup_Path)
					logging.info('Updating...')
					move(os.path.join(self.__Download_Path, 'agent'), self.Install_Path)
					if not os.path.exists(self.__Manage_Path):
						move(Manage_Download, self.__Manage_Path)
					logging.info('starting service...')
					win32serviceutil.StartService('falconagent')
				except Exception as e:
					logging.error(e)


			else:
				logging.info('Backup File to {}'.format(self.__Backup_Path))
				try:
					if not os.path.exists(self.__Backup_Path):
						logging.info('Backup File to {}'.format(self.__Backup_Path))
						move(self.Install_Path, self.__Backup_Path)
					logging.info('Updating...')
					move(os.path.join(self.__Download_Path, 'agent'), self.Install_Path)
					if not os.path.exists(self.__Manage_Path):
						move(Manage_Download, self.__Manage_Path)
					AddService()
				except Exception as e:
					logging.error(e)

			logging.info('Download the md5.txt file')
			request.urlretrieve(self.AgentMd5, os.path.join(self.Install_Path, 'md5.txt'))
			return True
		except error.HTTPError:
			return logging.error('MD5 File Download error!')
		except Exception:
			return

	@classmethod
	def Tasks(cls, name: str):
		# 去除pyinstaller 编译后的黑框
		si = STARTUPINFO()
		si.dwFlags |= STARTF_USESHOWWINDOW
		# check tasks
		if release() == '2003Server':
			req = Popen('schtasks /Query', shell=True,
			            stdin=DEVNULL, stdout=PIPE, stderr=DEVNULL,
			            startupinfo=si, env=os.environ)
			for i in req.stdout:
				if name.encode() in i:
					return logging.info('Exists Task: {}'.format(i.split()[0].decode()))
			code = os.system(os.path.join(Agent().Install_Path, '2003.bat'))
			if code != 0:
				logging.error(
					r'please use the 2003.bat File to Install the task.On:[{}\2003.bat]'.format(cls.Install_Path))
			return logging.info('Server 2003 Tasks install Successful')
		else:
			req = Popen('cmd /c chcp 437 & schtasks /Query /TN {}'.format(name),
			            shell=True, stdin=DEVNULL, stdout=PIPE, stderr=DEVNULL,
			            universal_newlines=True, startupinfo=si, env=os.environ)
			for i in req.stdout:
				if name in i:
					return logging.info('Exists Task: {}'.format(i.split()[0]))
			ret = Popen(
				r'schtasks /create /sc minute /mo 5 /tn "{name}" /tr "{PATH}"'.format(
					name=name,
					PATH=Agent().__Manage_Path),
				shell=True, stdout=PIPE, stderr=DEVNULL, stdin=DEVNULL, universal_newlines=True, startupinfo=si,
				env=os.environ
			).stdout
			return logging.info(ret.read())