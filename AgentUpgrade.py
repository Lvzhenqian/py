#coding:utf-8
from urllib import request
from urllib import error
from threading import Thread
import socket
import requests
import json
import time
import os
import logging
from hashlib import md5 as md5sum
from zipfile import ZipFile

logging.basicConfig(level=logging.INFO,
                    format='[%(process)s %(processName)s]--[%(threadName)10s]--[%(asctime)s] %(levelname)7s %(message)s',
                    filename='cron.log',
                    filemode='a')


def Install(x: str, ds: str):
	try:
		f = ZipFile(x, mode='r')
		f.extractall(ds)
		Down_md5 = 'http://fe.open-falcon.7road.net:9526/windows/md5.txt'
		request.urlretrieve(Down_md5, r'C:\falcon_agent\agent\md5.txt')
	except error.HTTPError:
		logging.error('MD5 File Download error!')
		return
	except Exception:
		pass
	os.system(os.path.join(ds, 'Agent-install.vbs'))
	return


def SendVersion():
	hsname,version = '',1
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


def Download_Package(s_md5):
	try:
		Down_zip = 'http://fe.open-falcon.7road.net:9526/windows/agent.zip'
		logging.info('Downloading...')
		if not os.path.isdir(r'C:\falcon_agent'):
			os.mkdir(r'C:\falcon_agent')
		request.urlretrieve(Down_zip, r'C:\falcon_agent\agent.zip')
		with open(r'C:\falcon_agent\agent.zip', 'rb') as ff:
			down_md5 = md5sum(ff.read())
		if s_md5.split()[0].decode() == down_md5.hexdigest():
			t = Thread(target=Install,args=(r'C:\falcon_agent\agent.zip', r'C:\falcon_agent'),name='Installing')
			t.start()
			t.join()
		else:
			logging.warning('Download warning! please try to Download of yourself.')
			return
		logging.info('Update finish.')
		return
	except error.HTTPError:
		logging.error("Can't download the package.please check the Url.")


def Check():
	md5file = None
	try:
		with request.urlopen('http://fe.open-falcon.7road.net:9526/windows/md5.txt') as f:
			md5file = f.read()
			server_md5 = md5sum(md5file).hexdigest()
		file = r'C:\windows\system32\7roadyw\agent\md5.txt'
		if os.path.exists(file):
			with open(file, 'rb') as fd:
				file_md5 = md5sum(fd.read()).hexdigest()
			if file_md5 == server_md5:
				return logging.info("Same file don't use Update...exit. ")
	except error.HTTPError:
		logging.error("Can not connect [http://fe.open-falcon.7road.net:9526/windows/md5.txt] the Url.")
	t = Thread(target=Download_Package, args=(md5file,), name='Download')
	t.start()
	t.join()


if __name__ == '__main__':
	Check()
	n = 0
	while n < 5:
		try:
			test = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			test.connect(('127.0.0.1',1988))
			time.sleep(1)
			test.close()
			SendVersion()
			break
		except ConnectionRefusedError:
			logging.error('Cat not connect 1988 port!')
			time.sleep(1)
		n += 1


