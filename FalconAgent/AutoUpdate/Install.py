# coding:utf-8
from ..util.config import *
from urllib import request, parse, error
from platform import machine
from shutil import move, rmtree
import socket, json, time, os, win32serviceutil, psutil
from hashlib import md5 as md5sum
from zipfile import ZipFile

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s --[%(threadName)10s]--[%(levelname)7s]: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


class Upgrade:
	Install_Path = INSTALL

	def __init__(self):
		self.__ip = 'http://ip.7road.net'
		self.__zk_ip = 'http://yw.7road-inc.com:8081/queryAssetsByIpJson'
		self.__Agent = 'http://fe.open-falcon.7road.net:9526/windows/agent.zip'
		self.AgentMd5 = 'http://fe.open-falcon.7road.net:9526/windows/md5.txt'
		self.__Download_Path = r'C:\falcontemp'
		self.__Download_File = r'C:\falcontemp\agent.zip'
		self.__Backup_Path = self.Install_Path + '_%s' % time.strftime('%Y-%m-%d')

	def __ChangeFile(self, ip, x):
		try:
			with open(x, mode='rt', encoding='utf8') as r:
				dit = r.read()
			fdit = json.loads(dit)
			fdit['hostname'] = ip
			logging.info('更改 hostname=%s ' % ip)
			wf = os.path.join(self.__Download_Path, r'agent\cfg.json')
			logging.info('write to source file!')
			with open(wf, mode='wt', encoding='utf8') as w:
				wbody = json.dumps(fdit)
				w.write(wbody)
			logging.info('更改cfg.json文件成功.')
			return True
		except FileNotFoundError:
			logging.error('找不到cfg.json文件!')
			return False

	def __SelectIp(self):
		logging.info('选择IP 与 cfg.json文件')
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

	def Download_And_Install(self, s_md5):
		try:
			if not os.path.isdir(self.__Download_Path):
				os.mkdir(self.__Download_Path)
			logging.info('下载更新包！')
			agent = request.urlopen(self.__Agent).read()
			with open(self.__Download_File, 'wb') as f:
				f.write(agent)
			logging.info("比对下载包的Md5值。")
			with open(self.__Download_File, 'rb') as ff:
				down_md5 = md5sum(ff.read())
			if s_md5.split()[0].decode() == down_md5.hexdigest():
				logging.info('开始安装更新！')
				install_status = self.__Install(self.__Download_File, self.__Download_Path)
				if install_status:
					logging.info('下载Md5.txt文件')
					request.urlretrieve(self.AgentMd5, os.path.join(self.Install_Path, 'md5.txt'))
				else:
					return False
				logging.info('清理临时目录！')
				rmtree(self.__Download_Path)
				return logging.info('安装 更新包完成！')
			else:
				return logging.warning('下载出错！请手动下载更新包，地址：%s' % self.__Agent)

		except error.HTTPError:
			return logging.error("无法下载，请检查网络！地址：%s" % self.__Agent)

	def __AddService(self):
		logging.info('加入系统服务.')
		os.system(r'{server} install FalconAgent {exe}'.format(
			server=os.path.join(
				self.Install_Path, 'nssm64.exe') if machine() == 'AMD64' else os.path.join(
				self.Install_Path, 'nssm32.exe'),
			exe=os.path.realpath(__file__)
		))
		time.sleep(2)
		try:
			self.__services_manage('start')
		except Exception as e:
			logging.error(e)
		return True

	def __services_manage(self, action, service='falconagent'):
		rule = {'stop': win32serviceutil.StopService, 'start': win32serviceutil.StartService,
		        'restart': win32serviceutil.RestartService}
		if action == 'status':
			try:
				s = psutil.win_service_get(service)
				return s.status()
			except Exception as err:
				return logging.error(err)
		else:
			return rule.get(action, 'restart')(service)

	def __Install(self, x: str, ds: str):
		logging.info('解压，请等待！')
		f = ZipFile(x, mode='r')
		f.extractall(ds)
		# 更改IP文件
		logging.info('开始安装客户端！')
		ip, addr = self.__SelectIp()
		Change = self.__ChangeFile(ip, addr)
		if not Change:
			logging.error("修改cfg.json文件错误，请检查cfg.json文件！")
			return False
		# 开始安装
		if not os.path.isdir(self.Install_Path):  # 没有此目录时
			logging.info('安装到： %s' % self.Install_Path)
			move(os.path.join(self.__Download_Path, 'agent'), self.Install_Path)
			self.__AddService()

		elif self.__services_manage('status') == 'running':  # 当服务存在时
			try:
				logging.info('停止服务中')
				self.__services_manage('stop')
				time.sleep(3)
				if not os.path.exists(self.__Backup_Path):  # 检查备份路径是否已经存在
					logging.info('备份到：{}'.format(self.__Backup_Path))
					move(self.Install_Path, self.__Backup_Path)
				logging.info('开始更新文件...')
				move(os.path.join(self.__Download_Path, 'agent'), self.Install_Path)
				logging.info('启动服务！')
				self.__services_manage('start')
			except Exception as err:
				logging.error(err)
				return False

		else:  # 当有目录，但是无服务，或者服务没有启动时。
			logging.info('备份到：{}'.format(self.__Backup_Path))
			try:
				if not os.path.exists(self.__Backup_Path):
					logging.info('Backup File to {}'.format(self.__Backup_Path))
					move(self.Install_Path, self.__Backup_Path)
				logging.info('开始更新文件...')
				move(os.path.join(self.__Download_Path, 'agent'), self.Install_Path)
				if self.__services_manage('status') == 'stopped':
					try:
						self.__services_manage('start')
					except Exception as err:
						logging.error(err)
				else:
					self.__AddService()
			except Exception as err:
				logging.error(err)
