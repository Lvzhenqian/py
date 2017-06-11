# coding:utf8
import configparser
from .XmlTree import Tree, TreeWrite
from urllib.parse import urlparse


class AutoIIS:
	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config.read('./config.ini')
		self.__Road_config = r'D:\dandantang\Server1\Road.Service.exe.config'
		self.__Flash_config = r'D:\dandantang\Flash\config.xml'
		self.__Flash_web = r'D:\dandantang\Flash\web.config'
		self.__Flash_Default = r'D:\dandantang\Flash\Default.aspx'
		self.__request_config = r'D:\dandantang\Request\web.config'
		self.__fight_config = r'D:\dandantang\FightServer\Fighting.Service.exe.config'
		self.__host = r'C:\Windows\System32\drivers\etc\hosts'
		self.__dst = lambda st, dt: st.replace(urlparse(st).netloc, dt)

	def Road_config(self):
		tree = Tree(self.__Road_config)
		root = tree.getroot()
		for add in root.findall('appSettings/add'):
			if add.attrib['key'] == 'AreaID':
				add.attrib['value'] = self.config['Config']['AreaID']
			if add.attrib['key'] == 'AreaName':
				add.attrib['value'] = self.config['Config']['AreaName']
			if add.attrib['key'] == 'AppName':
				add.attrib['value'] = self.config['Config']['AppName']
		TreeWrite(tree, self.__Road_config)

	def Flash_config(self, Req, parter_id, assist):
		tree = Tree(self.__Flash_config)
		root = tree.getroot()
		req = root.find('config/REQUEST_PATH').attrib['value']
		root.find('config/REQUEST_PATH').attrib['value'] = self.__dst(req, Req)
		root.find('config/PARTER_ID').attrib['value'] = parter_id
		info = root.find('config/PHP').attrib['infoPath']
		root.find('config/PHP').attrib['infoPath'] = self.__dst(info, assist)
		comm = root.find('config/COMMUNITY_FRIEND_LIST_PATH').attrib['value']
		root.find('config/COMMUNITY_FRIEND_LIST_PATH').attrib['value'] = self.__dst(comm, assist)
		interface = root.find('config/COMMUNITY_INTERFACE').attrib['path']
		root.find('config/COMMUNITY_INTERFACE').attrib['path'] = self.__dst(interface, assist)
		TreeWrite(tree, self.__Flash_config)

	def Flash_web(self, login, logout, title):
		tree = Tree(self.__Flash_web)
		root = tree.getroot()
		for add in root.findall('appSettings/add'):
			if add.attrib['key'] == 'LoginUrl':
				add.attrib['value'] = login
			if add.attrib['key'] == 'LoginOnUrl':
				add.attrib['value'] = logout
			if add.attrib['key'] == 'SiteTitle':
				add.attrib['value'] = title
		TreeWrite(tree, self.__Flash_web)

	def Flash_default(self):
		pass

	def Request_config(self, Did, Areaname):
		tree = Tree(self.__request_config)
		root = tree.getroot()
		for add in root.findall('appSettings/add'):
			if add.attrib['key'] == 'DId':
				add.attrib['value'] = Did
			if add.attrib['key'] == 'AreaName':
				add.attrib['value'] = Areaname
		TreeWrite(tree, self.__request_config)

	def host(self, q_name):
		tmp = []
		with open(self.__host, 'r') as fd:
			for lines in fd:
				line = lines.strip('\n')
				if 'quest' in line:
					sn = line.split()[1]
					line.replace(sn, q_name)
				tmp.append(line)
		with open(self.__host, 'w') as wd:
			for l in tmp:
				wd.writelines(l)
