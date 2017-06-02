# from FalconAgent.util.thread import Jobs
# from FalconAgent.util.config import *
import sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from FalconAgent.util.thread import Jobs

# def main():
# 	logging.debug('开始作业：{}'.format(Jobs.get_job()))
# 	Jobs.start()
# 	try:
# 		while True:
# 			pass
# 	except (KeyboardInterrupt, SystemExit):
# 		Jobs.shutdown()
# 		logging.debug('主进程退出！')
#
#
# if __name__ == '__main__':
# 	main()
