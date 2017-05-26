from ..AutoUpdate.Install import *
from threading import Thread


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
		logging.error("Can not Client %s the Url." % ins.AgentMd5)
	t = Thread(target=ins.Download_And_Install, args=(md5file,), name='更新线程')
	logging.info('{}--{}'.format(t.name, t.ident))
	t.start()
