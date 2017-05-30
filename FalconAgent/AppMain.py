from .util.thread import Jobs
from .util.log import *
from .util.config import SCRIPTPATH


def main():
	init_log(SCRIPTPATH)
	logging.info('开始作业：{}'.format(Jobs.get_job()))
	Jobs.start()
	try:
		while True:
			pass
	except (KeyboardInterrupt, SystemExit):
		Jobs.shutdown()
		logging.info('主进程退出！')


if __name__ == '__main__':
	main()
