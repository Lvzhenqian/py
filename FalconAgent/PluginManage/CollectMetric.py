from ..util.log import *
from ..Client.TransClient import UpdateMetric


def __executive(x):
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


def run(file):
	parms = []
	try:
		data = __executive(file)
	except AttributeError:
		data = False
	if data:
		logging.info("Starting...Add [{}] Plugin in the metric list.".format(os.path.basename(file)))
		if isinstance(data, dict):
			parms.append(data)
		elif isinstance(data, list):
			parms.extend(data)
	else:
		logging.error("错误！无法读取[{}] 这个插件.".format(os.path.basename(file)))
	rep = UpdateMetric(data)
	if rep:
		logging.info("上传{f}成功！状态：{stat}".format(f=os.path.basename(file), stat=rep))
