from urllib import request
from urllib import error
import requests
import json
import time
import os
import logging
from hashlib import md5 as md5sum
from zipfile import ZipFile

logging.basicConfig(level=logging.INFO,
                    format='[%(filename)s:%(process)s]--[%(asctime)s] %(levelname)s %(message)s',
                    filename='cron.log',
                    filemode='a')


def Install(x: str, ds: str):
	try:
		f = ZipFile(x, mode='r')
		f.extractall(ds)
	except Exception:
		pass
	return os.system(ds + 'Agent-install.vbs')



def SendVersion():
	with open(r'C:\\windows\\system32\\7roadyw\\agent\\cfg.json') as cfg:
		try:
			hsname = json.loads(cfg.read())['hostname']
		except error.HTTPError:
			return logging.warning('Push Version Fail.')

	url = 'http://127.0.0.1:1988/v1/push'
	parms = [
		{
			"metric": "agent.version",
			"endpoint": hsname,
			"timestamp": int(time.time()),
			"step": 300,
			"value": 2,
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
	md5file = None
	try:
		with request.urlopen('http://fe.open-falcon.7road.net:9526/windows/md5.txt') as f:
			md5file = f.read()
			server_md5 = md5sum(md5file).hexdigest()
		file = r'C:\\windows\\system32\\7roadyw\\agent\\md5.txt'
		if os.path.exists(file):
			with open(file, 'r') as fd:
				file_md5 = md5sum(fd.read()).hexdigest()
			if file_md5 == server_md5:
				return logging.info("Same file don't use Update...exit. ")
	# now! Updateing...
		logging.info('Downloading...')
		request.urlretrieve('http://fe.open-falcon.7road.net:9526/windows/agent.zip', r'C:\\falcon_agent\\agent.zip')
	except error.HTTPError:

		return
	with open(r'C:\\falcon_agent\\agent.zip', 'rb') as ff:
		down_md5 = md5sum(ff.read())
	if md5file.split()[0].decode() == down_md5.hexdigest():
		Install(r'C:\\falcon_agent\\agent.zip', r'C:\\falcon_agent\\')
	else:
		logging.warning('Download warning! please try to Download of yourself.')
		return
	return logging.info('Update finish.')


if __name__ == '__main__':
	Check()
	SendVersion()
