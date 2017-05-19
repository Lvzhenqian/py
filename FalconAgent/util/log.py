from .config import *


def get_logger(logger_name='[FalconService]', path=None):

    logger = logging.getLogger(logger_name)
    handler = logging.FileHandler(os.path.join(path, "Agent.log"))
    if path is None:
        path = r'c:\\'
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if config.DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.DEBUG)

    return logger


def init_log(path=None):
    if config.DEBUG:
        logging.basicConfig(filename=os.path.join(path, 'init.log'),level=logging.DEBUG, format='%(asctime)s %('
                                                                                                'filename)-12s %('
                                                                                                'levelname)-8s %('
                                                                                                'message)s')
    else:
        logging.basicConfig(filename=os.path.join(path, 'init.log'),level=logging.INFO, format='%(asctime)s %('
                                                                                               'filename)-12s %('
                                                                                               'levelname)-8s %('
                                                                                               'message)s')
