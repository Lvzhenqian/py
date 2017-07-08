from hashlib import md5 as md5sum
from collections import OrderedDict
from email_get import mail_down
from Compress_package import *
from TransClient import SSHclient
import json


def PushPackage(Spath, Upath, **socket):
    sc = SSHclient(ip=socket['ip'], port=socket['port'], usrname=socket['user'],
                   passwd=socket['passwd'])
    for pk in os.listdir(Spath):
        pck = os.path.realpath(os.path.join(pk, 'dandantang.zip'))
        ps = Upath + '/' + pk
        sc.run('rm -rf {}'.format(ps + '/' + 'dandantang.zip'))
        sc.push(pck, ps + '/' + 'dandantang.zip')


try:
    with open('./config.json', encoding='utf8') as f:
        config = json.loads(f.read())
    agents = OrderedDict(sorted(config['agents'].items(), key=lambda t: len(t[0])))
    while True:
        for l, name in enumerate(agents.keys()):
            context = "{number:>2}. {title}({agent})".format(number=l, title=agents[name]['title'], agent=name)
            print(context)
        choose = lambda iput: list(agents.keys())[int(iput)] if iput.isdigit() else iput if iput in list(agents.keys()) else None
        ag = choose(input('请输入将要打包的代理[quit]： '))
        if not ag:
            print('输入的代理不在列表中，请重新执行！')
            break
        if ag.lower() == 'quit':
            break
        oa_num = input('请输入邮件oa单号：')
        tg = True if ag == 'guoneiddt' else False
        package = mail_down(user=config['name'], pswd=config['password'], oa=oa_num, tag=tg)
        DownloadPath = '.'
        downfile = package.download_pack(DownloadPath)
        if not downfile:
            print('下载出错！！请重试')
            break
        with open(downfile, 'rb') as file:
            fmd5 = md5sum(file.read()).hexdigest()
        if fmd5 == package.Md5:
            os.chdir(os.path.dirname(downfile))
            pkg_path = os.path.join(DownloadPath, 'dandantang')
            if os.path.exists(pkg_path):
                shutil.rmtree(pkg_path)
            unzip(zipfile=downfile, path='./package')
            compress = work(path=DownloadPath, agent=ag, oa=oa_num)
            compress.runner()
            PushPackage(Spath=compress.dir, Upath=agents[ag]['path'], **agents[ag])
        else:
            raise FileExistsError('MD5 ERROR')
except FileNotFoundError:
    pass
except json.JSONDecodeError:
    pass
