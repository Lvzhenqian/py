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

HOSTNAME = config.get('hostname')
DEBUG = config.get('debug')
IP = config.get('ip')
HEARTBEAT = config.get('heartbeat')
TRANSFER = config.get('transfer')
HTTP = config.get('http')
COLLECTOR = config.get('collector')
IGNORE = config.get('ignore')
VERSION = config.get('version')
PLUGIN = config.get('Plugin')
