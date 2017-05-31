from ..util.config import *
from ..Client.TransClient import UpdateMetric
from ..util.thread import Jobs


class JobsManage:
	def __init__(self, plugin):
		self.PluginPath = plugin

	def __executive(self, x):
		with open(x, 'rt', encoding='utf8') as f:
			code = f.read()
		if 'subprocess' in code and 'STARTF_USESHOWWINDOW' not in code:
			logging.error(
				"""
		[{}] Plugin 
		this Plugin in use subprocess module,
		But it not used [startupinfo] parameters in Popen function.it can't running.
		you need to change (stdin,stdout,stderr) to PIPE or DEVNULL
		add env=os.environ.
	
		example:
			si = subprocess.STARTUPINFO()
			si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
			subprocess.Popen(startupinfo=si,env=os.environ,
			stderr=subprocess.DEVNULL, stdout=subprocess.PIPE, stdin=subprocess.DEVNULL,
			)
	""".format(os.path.basename(x)))
			return False
		ret = {'metric': None}
		exec(code, ret)
		return ret['metric']

	def __push(self, file):
		parms = []
		try:
			data = self.__executive(file)
		except AttributeError:
			data = False
		if data:
			logging.debug("Starting...Add [{}] Plugin in the metric list.".format(os.path.basename(file)))
			if isinstance(data, dict):
				parms.append(data)
			elif isinstance(data, list):
				parms.extend(data)
		else:
			logging.error("错误！无法读取[{}] 这个插件.".format(os.path.basename(file)))
		rep = UpdateMetric(data)
		if rep:
			logging.info("上传{f}成功！状态：{stat}".format(f=os.path.basename(file), stat=rep))

	def make_jobs(self):
		for files in os.listdir(self.PluginPath):
			f_name = os.path.basename(files)
			if f_name.endswith('.py') and f_name[0].isdigit():
				try:
					timer = int(f_name.split("_")[0])
				except ValueError:
					logging.error('''
					无法导入{}此文件
					格式说明：300_ping.py
					'''.format(f_name))
					continue
				Jobs.add_job(func=self.__push, args=(files,), trigger='interval', seconds=timer,id='Plugin_Manage')
		#
		# def run():
		# 	job = JobsManage(PLUGIN)
		# 	runlist = job.make_jobs()
		# 	runlist.start()
