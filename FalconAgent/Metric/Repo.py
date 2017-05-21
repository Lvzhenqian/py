from ..util.config import *
from ..Client.HbsClient import Update
import time

def report(sleep=60):
	data = dict(Hostname=HOSTNAME,IP=IP,AgentVersion=str(VERSION),PluginVersion=str(PLUGIN.get('version')))
	while True:
		try:
			Update(data)
		except Exception as err:
			logging.error(err)
			continue
		finally:
			time.sleep(sleep)