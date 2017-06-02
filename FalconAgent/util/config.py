import json
import logging
import os
import sys

SCRIPTPATH = r'D:\FalconAgent'
#SCRIPTPATH = os.path.dirname(os.path.realpath(sys.executable))
cfg_file = os.path.join(SCRIPTPATH, 'cfg.json')
print(cfg_file)
logging.debug(cfg_file)
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
INSTALL = config.get('InstallPath')
PLUGIN = os.path.join(SCRIPTPATH, 'plugin')

if DEBUG:
    logging.basicConfig(filename='app-dbg.log', level=logging.DEBUG, filemode='a',
                        format='%(asctime)s --[%(threadName)10s]--[%(levelname)7s]: %(message)s')
else:
    logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a',
                        format='%(asctime)s --[%(threadName)10s]--[%(levelname)7s]: %(message)s')
