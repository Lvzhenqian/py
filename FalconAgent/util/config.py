import json, os, logging
PATH = os.path.realpath(__file__)
logging.debug(PATH)
cfg_file = os.path.join(PATH, 'cfg.json')
config = None
try:
	with open(cfg_file) as confile:
		config = json.load(confile)
except Exception as e:
	logging.error(e)

HOSTNAME = config['hostname']
DEBUG = config['debug']
IP = config['ip']
HEARTBEAT = config['heartbeat']
TRANSFER = config['transfer']
HTTP = config['http']
COLLECTOR = config['collector']
IGNORE = config['ignore']
