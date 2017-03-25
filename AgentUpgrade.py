# coding:utf-8
from urllib import request, parse
from urllib import error
from threading import Thread
import win32serviceutil
import socket,requests,json,time,os,logging,shutil
from hashlib import md5 as md5sum
from zipfile import ZipFile

logging.basicConfig(level=logging.INFO,
                    format='[%(process)s %(processName)s]--[%(threadName)10s]--[%(asctime)s] %(levelname)7s %(message)s',
                    filename='cron.log',
                    filemode='a')
class Agent:
	def __init__(self):
		self.__ip = 'http://ip.7road.net'
		self.__zk_ip = 'http://yw.7road-inc.com:8081/queryAssetsByIpJson'
		self.__Agent = 'http://fe.open-falcon.7road.net:9526/windows/agent.zip'
		self.AgentMd5 = 'http://fe.open-falcon.7road.net:9526/windows/md5.txt'
		self.__Download_Path = r'C:\falcon_agent'
		self.__Download_File = r'C:\falcon_agent\agent.zip'
		self.Install_Path = r'c:\windows\system32\7roadyw\agent'


	def __ChangeFile(self,ip,x):
		with open(x) as r:
			dit = r.read()
		fdit = json.loads(dit)
		fdit['hostname'] = ip
		logging.info('Change hostname=%s '%ip)
		wf = os.path.join(self.__Download_Path,r'agent\cfg.json')
		logging.info('write to source file!')
		with open(wf, mode='w') as w:
			wbody = json.dumps(fdit)
			w.write(wbody)
		return True

	@classmethod
	def TestPort(cls,port:int):
		try:
			test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			test.connect(('127.0.0.1', port))
			time.sleep(1)
			test.close()
			return True
		except ConnectionRefusedError:
			logging.error('Cat not connect %s port!'%port)
			return False

	def __SelectIp(self):
		try:
			internet = request.urlopen(self.__ip).read().split()
			net,we=internet[0].decode(),internet[1]
			parms = {
				'ips': net,
				'props': 'ip1'
			}
			url = parse.urlencode(parms)
			req = request.urlopen(self.__zk_ip + '?' + url).read().decode()
			resp = json.loads(req)
			zk_res, status = resp['data'][0][net]['ip1'], resp['code']
			if we == '中国'.encode() and zk_res == '':
				return net,os.path.join(self.__Download_File,'agent\cfg.json')
			elif zk_res == '':
				return net,os.path.join(self.__Download_File,'agent\hwcfg.json')
			else:
				return zk_res,os.path.join(self.__Download_File,'agent\hwcfg.json')
		except error.HTTPError:
			hsn = socket.gethostname()
			return socket.gethostbyname(hsn), os.path.join(self.__Download_File,'agent\cfg.json')

	def Download_Package(self, s_md5):
		try:
			logging.info('Downloading...')
			if not os.path.isdir(self.__Download_Path):
				os.mkdir(self.__Download_Path)
			request.urlretrieve(self.__Agent, self.__Download_File)
			with open(self.__Download_File, 'rb') as ff:
				down_md5 = md5sum(ff.read())
			if s_md5.split()[0].decode() == down_md5.hexdigest():
				logging.info('Install the package.now!')
				self.__Install(self.__Download_File, self.__Download_Path)
				return logging.info('Update finish.')
			else:
				return logging.warning('Download warning! please try to Download of yourself.')

		except error.HTTPError:
			return logging.error("Can't download the package.please check the Url.")

	def __Install(self, x: str, ds: str):
		try:
			logging.info('unzip....plz wait.')
			f = ZipFile(x, mode='r')
			f.extractall(ds)
			logging.info('Starting.Install Thread!')
			self.__ChangeFile(*self.__SelectIp())
			if not os.path.isdir(self.Install_Path):
				logging.info('Copying to %s'%self.Install_Path)
				shutil.move(os.path.join(self.__Download_Path,'agent'),self.Install_Path)
			elif Agent.TestPort(1988):
				win32serviceutil.
			else:
				logging.info('Backup the old fold')
				shutil.move(self.Install_Path,os.path.join(self.Install_Path,'_%s'%time.strftime('%Y-%m-%d')))
				logging.info('Updating...')
				shutil.move(os.path.join(self.__Download_Path, 'agent'), self.Install_Path)

			logging.info('Download the md5.txt file')
			request.urlretrieve(self.AgentMd5, r'C:\falcon_agent\agent\md5.txt')
			return
		except error.HTTPError:
			logging.error('MD5 File Download error!')
			return
		except Exception:
			return



def SendVersion():
	hsname, version = '', 1
	try:
		with open(r'C:\windows\system32\7roadyw\agent\cfg.json') as cfg:
			load = json.loads(cfg.read())
			hsname = load['hostname']
			version = load['version']
	except FileNotFoundError:
		logging.error('Not file cfg.json!')
	url = 'http://127.0.0.1:1988/v1/push'
	parms = [
		{
			"metric": "agent.version",
			"endpoint": hsname,
			"timestamp": int(time.time()),
			"step": 300,
			"value": version,
			"counterType": "GAUGE",
			"tags": ""
		},
	]
	req = requests.post(url, json=json.dumps(parms))
	if req.text.strip() == 'success':
		return logging.info('Push Version Successful.')
	else:
		return logging.warning('Push Version Fail.')


def Check():
	agent = Agent()
	md5file = None
	try:
		with request.urlopen(agent.AgentMd5) as f:
			md5file = f.read()
			server_md5 = md5sum(md5file).hexdigest()
		file = os.path.join(agent.Install_Path,'md5.txt')
		if os.path.exists(file):
			with open(file, 'rb') as fd:
				file_md5 = md5sum(fd.read()).hexdigest()
			if file_md5 == server_md5:
				return logging.info("Same file don't use Update...exit. ")
	except error.HTTPError:
		logging.error("Can not connect %s the Url." % agent.AgentMd5)
	t = Thread(target=agent.Download_Package, args=(md5file,), name='Download')
	t.start()
	t.join()


if __name__ == '__main__':
	Check()
	n = 0
	while n < 5:
		Agent.TestPort(1988)
		SendVersion()
		break


