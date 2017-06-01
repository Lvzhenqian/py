from ..AutoUpdate.Install import *
from threading import Thread
from FalconAgent.PluginManage.Manage import JobsManage
from FalconAgent.api.HttpAPI import *
from apscheduler.schedulers.background import BackgroundScheduler

Jobs = BackgroundScheduler()
Plugin = JobsManage(PLUGIN)
Plugin.make_jobs()


@Jobs.scheduled_job(trigger='interval', id='Install', minutes=5)
def InstallThread():
	md5file = None
	ins = Upgrade()
	try:
		with request.urlopen(ins.AgentMd5) as f:
			md5file = f.read()
			server_md5 = md5sum(md5file).hexdigest()
		file = os.path.join(ins.Install_Path, 'md5.txt')
		if os.path.exists(file):
			with open(file, 'rb') as fd:
				file_md5 = md5sum(fd.read()).hexdigest()
			if file_md5 == server_md5:
				return logging.info("Md5验证通过，跳过更新！ ")
	except error.HTTPError:
		logging.error("无法连接到： %s" % ins.AgentMd5)
	t = Thread(target=ins.Download_And_Install, args=(md5file,), name='更新线程', daemon=True)
	logging.info('{}--{}'.format(t.name, t.ident))
	t.start()


def APIthread():
	t = Thread(target=app.run, kwargs=dict(port=1988), name='API接口线程', daemon=True)
	logging.info('{}--{}'.format(t.name, t.ident))
	t.start()
