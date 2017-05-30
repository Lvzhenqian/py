from ..util.config import *
from ..Client.HbsClient import Update
from ..util.thread import Jobs


@Jobs.scheduled_job(trigger='interval', id='HbsRepo', minutes=1)
def report():
	data = dict(Hostname=HOSTNAME, IP=IP, AgentVersion=str(VERSION), PluginVersion='enable')
	try:
		Update(data)
	except Exception as err:
		logging.error(err)
