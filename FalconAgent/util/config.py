import json
import logging
import os
import sys

SCRIPTPATH = r'D:\FalconAgent'
# SCRIPTPATH = os.path.dirname(os.path.realpath(sys.executable))
cfg_file = os.path.join(SCRIPTPATH, 'cfg.json')
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


def Geloger(name, file, debug=False):
    leve = logging.DEBUG if debug else logging.INFO
    log = logging.getLogger(name)
    fmt = logging.Formatter('%(asctime)s --[%(threadName)10s]--[%(levelname)7s]: %(message)s')
    fh = logging.FileHandler(file)
    fh.setLevel(leve)
    fh.setFormatter(fmt)

    console = logging.StreamHandler()
    console.setLevel(leve)
    console.setFormatter(fmt)
    log.addHandler(console)
    log.addFilter(fh)
    return log

Geloger(name='util.config', file='app.log', debug=DEBUG)