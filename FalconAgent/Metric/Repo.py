from util.config import HOSTNAME, Geloger, IP, VERSION, DEBUG
from Client.HbsClient import Update

repo_log = Geloger(name='Metric.Repo', file='app.log', debug=DEBUG)


def report():
    data = dict(Hostname=HOSTNAME, IP=IP, AgentVersion=str(VERSION), PluginVersion='enable')
    try:
        Update(data)
    except Exception as err:
        repo_log.error(err)
