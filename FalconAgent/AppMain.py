from util import thread
from util.config import *
from AutoUpdate import Install
from urllib import request
import time

Geloger(name='main', file='app.log', debug=DEBUG)


def service():
    logging.debug('开启API服务!')
    thread.APIthread()
    logging.debug('开始作业：{}'.format(thread.Jobs.get_jobs()))
    thread.Jobs.start()
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        thread.Jobs.shutdown()
        logging.debug('主进程退出！')


def main():
    m = Install.Upgrade()
    if not os.path.exists(m.Install_Path) or os.path.exists(m.AgentMd5):
        with request.urlopen(m.AgentMd5) as f:
            md5file = f.read()
        return m.Download_And_Install(md5file)
    else:
        service()


if __name__ == '__main__':
    # main()

    service()
