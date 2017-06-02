from util.config import *
from Client.HbsClient import Update


def report():
    data = dict(Hostname=HOSTNAME, IP=IP, AgentVersion=str(VERSION), PluginVersion='enable')
    try:
        Update(data)
    except Exception as err:
        logging.error(err)
