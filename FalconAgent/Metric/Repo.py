from FalconAgent.util.config import *
from FalconAgent.Client.HbsClient import Update
from FalconAgent.util.thread import Jobs


@Jobs.scheduled_job(trigger='interval', id='HbsRepo', minutes=1)
def report():
	data = dict(Hostname=HOSTNAME, IP=IP, AgentVersion=str(VERSION), PluginVersion='enable')
	try:
		Update(data)
	except Exception as err:
		logging.error(err)
