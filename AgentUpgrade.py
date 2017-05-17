# coding:utf-8
from urllib import request, parse, error
from subprocess import Popen, PIPE, DEVNULL, STARTUPINFO, STARTF_USESHOWWINDOW
from threading import Thread
from platform import machine, release
from shutil import move, rmtree
import socket, requests, json, time, os, logging, win32serviceutil
from hashlib import md5 as md5sum
from zipfile import ZipFile


class Agent:
    Install_Path = r'c:\7roadyw\agent'

    def __init__(self):
        self.__ip = 'http://ip.7road.net'
        self.__zk_ip = 'http://yw.7road-inc.com:8081/queryAssetsByIpJson'
        self.__Agent = 'http://fe.open-falcon.7road.net:9526/windows/agent.zip'
        self.AgentMd5 = 'http://fe.open-falcon.7road.net:9526/windows/md5.txt'
        self.__AgentManage = 'http://fe.open-falcon.7road.net:9526/windows/AgentUpgrade.exe'
        self.__Manage_Path = os.path.join(r'c:\7roadyw', 'AgentUpgrade.exe')
        self.__Download_Path = r'C:\falcon_agent'
        self.__Download_File = r'C:\falcon_agent\agent.zip'
        self.__Backup_Path = self.Install_Path + '_%s' % time.strftime('%Y-%m-%d')

    def __ChangeFile(self, ip, x):
        try:
            with open(x, mode='rt', encoding='utf8') as r:
                dit = r.read()
            fdit = json.loads(dit)
            fdit['hostname'] = ip
            logging.info('Change hostname=%s ' % ip)
            wf = os.path.join(self.__Download_Path, r'agent\cfg.json')
            logging.info('write to source file!')
            with open(wf, mode='wt', encoding='utf8') as w:
                wbody = json.dumps(fdit)
                w.write(wbody)
            logging.info('ChangeFile successful.')
            return True
        except FileNotFoundError:
            logging.error('Not File!')
            return False
        except FileExistsError:
            logging.error('Not File!')
            return False

    @classmethod
    def TestPort(cls, port: int):
        try:
            test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test.connect(('127.0.0.1', port))
            time.sleep(1)
            test.close()
            return True
        except ConnectionRefusedError:
            logging.error('Cat not connect %s port!' % port)
            return False

    def __SelectIp(self):
        logging.info('Select IP for cfg.json')
        try:
            internet = request.urlopen(self.__ip).read().split()
            net, we = internet[0].decode(), internet[1]
            parms = {
                'ips': net,
                'props': 'ip1'
            }
            url = parse.urlencode(parms)
            req = request.urlopen(self.__zk_ip + '?' + url).read().decode()
            resp = json.loads(req)
            if resp['code'] == 0:
                zk_res, status = resp['data'][0][net]['ip1'], resp['code']
                if we == '中国'.encode():
                    return zk_res, os.path.join(self.__Download_Path, 'agent\cfg.json')
                else:
                    return zk_res, os.path.join(self.__Download_Path, 'agent\hwcfg.json')
            else:
                return net, os.path.join(self.__Download_Path, 'agent\cfg.json')
        except error.HTTPError:
            hsn = socket.gethostname()
            return socket.gethostbyname(hsn), os.path.join(self.__Download_Path, 'agent\cfg.json')

    def Download_Package(self, s_md5):
        try:
            if not os.path.isdir(self.__Download_Path):
                os.mkdir(self.__Download_Path)
            logging.info('Download Package.')
            agent = request.urlopen(self.__Agent).read()
            with open(self.__Download_File,'wb') as f:
                f.write(agent)
            logging.info('Download AgentManage.')
            manage = request.urlopen(self.__AgentManage).read()
            with open(os.path.join(self.__Download_Path,'AgentUpgrade.exe'), 'wb') as f:
                f.write(manage)
            with open(self.__Download_File, 'rb') as ff:
                down_md5 = md5sum(ff.read())
            if s_md5.split()[0].decode() == down_md5.hexdigest():
                logging.info('Install the package.now!')
                install_status = self.__Install(self.__Download_File, self.__Download_Path)
                rmtree(self.__Download_Path)
                if not install_status:
                    return False
                return logging.info('Update finish.')
            else:
                return logging.warning('Download warning! please try to Download of yourself.')

        except error.HTTPError:
            return logging.error("Can't download the package.please check the Url.")

    def __Install(self, x: str, ds: str):
        Manage_Download = os.path.join(self.__Download_Path, 'AgentUpgrade.exe')


        def AddService():
            logging.info('Add To System service.')
            os.system(r'{server} install FalconAgent {exe}'.format(
                server=os.path.join(
                    self.Install_Path, 'nssm64.exe') if machine() == 'AMD64' else os.path.join(
                    self.Install_Path, 'nssm32.exe'),
                exe=os.path.join(self.Install_Path, 'windows-agent.exe')
            ))
            time.sleep(2)
            try:
                win32serviceutil.StartService('falconagent')
            except Exception as e:
                logging.error(e)
            return True

        try:
            logging.info('unzip....plz wait.')
            f = ZipFile(x, mode='r')
            f.extractall(ds)
            logging.info('Starting.Install Thread!')
            ip, addr = self.__SelectIp()
            Change = self.__ChangeFile(ip, addr)
            if not Change:
                logging.error("Change File Error!")
                return False

            if not os.path.isdir(self.Install_Path):
                logging.info('Copying to %s' % self.Install_Path)
                move(os.path.join(self.__Download_Path, 'agent'), self.Install_Path)
                move(Manage_Download, self.__Manage_Path)
                AddService()
            elif Agent.TestPort(1988):
                try:
                    logging.info('Stop service...')
                    win32serviceutil.StopService('falconagent')
                    time.sleep(3)
                    if not os.path.exists(self.__Backup_Path):
                        logging.info('Backup File to {}'.format(self.__Backup_Path))
                        move(self.Install_Path, self.__Backup_Path)
                    logging.info('Updating...')
                    move(os.path.join(self.__Download_Path, 'agent'), self.Install_Path)
                    if not os.path.exists(self.__Manage_Path):
                        move(Manage_Download, self.__Manage_Path)
                    logging.info('starting service...')
                    win32serviceutil.StartService('falconagent')
                except Exception as e:
                    logging.error(e)


            else:
                logging.info('Backup File to {}'.format(self.__Backup_Path))
                try:
                    if not os.path.exists(self.__Backup_Path):
                        logging.info('Backup File to {}'.format(self.__Backup_Path))
                        move(self.Install_Path, self.__Backup_Path)
                    logging.info('Updating...')
                    move(os.path.join(self.__Download_Path, 'agent'), self.Install_Path)
                    if not os.path.exists(self.__Manage_Path):
                        move(Manage_Download, self.__Manage_Path)
                    AddService()
                except Exception as e:
                    logging.error(e)

            logging.info('Download the md5.txt file')
            request.urlretrieve(self.AgentMd5, os.path.join(self.Install_Path, 'md5.txt'))
            return True
        except error.HTTPError:
            return logging.error('MD5 File Download error!')
        except Exception:
            return

    @classmethod
    def Tasks(cls, name: str):
        # 去除pyinstaller 编译后的黑框
        si = STARTUPINFO()
        si.dwFlags |= STARTF_USESHOWWINDOW
        # check tasks
        if release() == '2003Server':
            req = Popen('schtasks /Query', shell=True,
                        stdin=DEVNULL, stdout=PIPE, stderr=DEVNULL,
                        startupinfo=si, env=os.environ)
            for i in req.stdout:
                if name.encode() in i:
                    return logging.info('Exists Task: {}'.format(i.split()[0].decode()))
            code = os.system(os.path.join(Agent().Install_Path, '2003.bat'))
            if code != 0:
                logging.error(
                    r'please use the 2003.bat File to Install the task.On:[{}\2003.bat]'.format(cls.Install_Path))
            return logging.info('Server 2003 Tasks install Successful')
        else:
            req = Popen('cmd /c chcp 437 & schtasks /Query /TN {}'.format(name),
                        shell=True, stdin=DEVNULL, stdout=PIPE, stderr=DEVNULL,
                        universal_newlines=True, startupinfo=si, env=os.environ)
            for i in req.stdout:
                if name in i:
                    return logging.info('Exists Task: {}'.format(i.split()[0]))
            ret = Popen(
                r'schtasks /create /sc minute /mo 5 /tn "{name}" /tr "{PATH}"'.format(
                    name=name,
                    PATH=Agent().__Manage_Path),
                shell=True, stdout=PIPE, stderr=DEVNULL, stdin=DEVNULL, universal_newlines=True, startupinfo=si,
                env=os.environ
            ).stdout
            return logging.info(ret.read())


class PlugManage:
    def __init__(self):
        self.path = os.path.join(Agent.Install_Path, 'plugin')

    @staticmethod
    def Plugin(x: str):
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

    def PushVaule(self, parmlist: list):
        if not parmlist:
            return logging.error('Not Any Metric Push Please try again!')
        url = 'http://127.0.0.1:1988/v1/push'
        req = requests.post(url, data=json.dumps(parmlist))
        if req.text.strip() == 'success':
            return logging.info('Push {} Metric Successful.'.format(len(parmlist)))
        else:
            return logging.warning('Push All Fail.')

    def Start(self):
        if not os.path.exists(self.path):
            return logging.error('Not {} this Plugin Folder.Push exit!'.format(self.path))
        parms = []
        files = [os.path.join(self.path, x) for x in os.listdir(self.path) if x.endswith('.py')]
        for file in files:
            try:
                data = self.Plugin(file)
            except AttributeError:
                data = False
            if data:
                logging.info("Starting...Add [{}] Plugin in the metric list.".format(os.path.basename(file)))
                if isinstance(data, dict):
                    parms.append(data)
                elif isinstance(data, list):
                    parms.extend(data)
            else:
                logging.error("Error,Can't include the [{}] Plugin.".format(os.path.basename(file)))
        logging.info("Starting..Push the metric list")
        if parms:
            self.PushVaule(parms)
        return


def Check():
    agent = Agent()
    md5file = None
    try:
        with request.urlopen(agent.AgentMd5) as f:
            md5file = f.read()
            server_md5 = md5sum(md5file).hexdigest()
        file = os.path.join(agent.Install_Path, 'md5.txt')
        if os.path.exists(file):
            with open(file, 'rb') as fd:
                file_md5 = md5sum(fd.read()).hexdigest()
            if file_md5 == server_md5:
                return logging.info("Same file don't use Update...exit. ")
    except error.HTTPError:
        logging.error("Can not connect %s the Url." % agent.AgentMd5)
    t = Thread(target=agent.Download_Package, args=(md5file,), name='Download')
    t.start()
    t.join()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s --[%(process)s %(processName)s]--[%(threadName)10s]--[%(levelname)7s]: %('
                               'message)s',
                        filename='cron.log',
                        filemode='a')
    logging.info('Start')
    logging.info('Start Checking')
    Check()
    logging.info('End Checking')
    logging.info('Start TaskCheck')
    Agent.Tasks('FalconAgent')
    logging.info('End TaskCheck')
    logging.info('Start Send Metric')
    n = 0
    while n < 5:
        if Agent.TestPort(1988):
            PlugManage().Start()
            break
        n += 1
    logging.info('End Send Metric')
    logging.info('End.\r\n')
