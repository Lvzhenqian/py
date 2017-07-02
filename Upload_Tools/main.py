from hashlib import md5 as md5sum
from collections import OrderedDict
from .email_get import mail_down
from .Compress_package import *
from .TransClient import PushPackage
import json

try:
	with open('./config.json') as f:
		config = json.loads(f.read())
	agents = OrderedDict(sorted(config['agents'].items(), key=lambda t: len(t[0])))
	while True:
		for l, name in enumerate(agents.keys()):
			context = "{number:>2}. {title}({agent})".format(number=l, title=agents[name]['title'], agent=name)
			print(context)
		choose = lambda iput: list(agents.keys())[int(iput)] if iput.isdigit() else iput
		ag = choose(input('请输入将要打包的代理[quit]： '))
		if ag.lower() == 'quit':
			break
		oa_num = input('请输入邮件oa单号：')
		tg = True if ag == 'guoneiddt' else False
		package = mail_down(user=config['name'], pswd=config['password'], oa=oa_num, tag=tg)
		DownloadPath = '.'
		downfile = package.download_pack(DownloadPath)
		if md5sum(downfile) == package.Md5:
			os.chdir(os.path.dirname(downfile))
			unzip(zipfile=downfile, path='./package')
			compress = work(path=DownloadPath, agent=ag, oa=oa_num)
			compress.runner()
			for pk in os.listdir(compress.dir):
				pck = os.path.realpath(os.path.join(pk, 'dandantang.zip'))
				ps = os.path.join(agents[ag]['path'], pk)
				PushPackage(package=pck, path=ps, **agents[ag])
		else:
			raise FileExistsError('MD5 ERROR')
except FileNotFoundError:
	pass
except json.JSONDecodeError:
	pass
