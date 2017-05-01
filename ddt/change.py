from xml.etree import cElementTree
from shutil import move as mv
from urllib.parse import urlparse
import time


class ET(cElementTree.TreeBuilder):
	def comment(self, data):
		self.start(cElementTree.Comment, {})
		self.data(data)
		self.end(cElementTree.Comment)


class change:
	def __init__(self):
		self.__Center_File = r'D:\dandantang\Center\Center.Service.exe.config'
		self.__key = r'D:\dandantang\Center\key.txt'
		self.__Road_config = r'D:\dandantang\Server1\Road.Service.exe.config'
		self.__Flash_config = r'D:\dandantang\Flash\config.xml'
		self.__Flash_web = r'D:\dandantang\Flash\web.config'
		self.__Flash_Default = r'D:\dandantang\Flash\Default.aspx'
		self.__request_config = r'D:\dandantang\Request\web.config'
		self.__host = r'C:\Windows\System32\drivers\etc\hosts'

	def make_tree(self, file: str) -> cElementTree.parse:
		backup = '_'.join((file, time.strftime('%Y-%m-%d')))
		mv(file, backup)
		with open(backup, 'r+') as f:
			tree = cElementTree.parse(f, parser=cElementTree.XMLParser(target=ET()))
		return tree

	def DB_change(self, AreaID, AreaName):
		tree = self.make_tree(self.__Center_File)
		root = tree.getroot()
		for add in root.findall('appSettings/add'):
			if add.attrib['key'] == 'AreaID':
				add.attrib['value'] = AreaID
			if add.attrib['key'] == 'AreaName':
				add.attrib['value'] = AreaName
		tree.write(self.__Center_File, encoding='utf-8', xml_declaration=True)

	def Road_config(self, Appname, AreaID, AreaName):
		tree = self.make_tree(self.__Road_config)
		root = tree.getroot()
		for add in root.findall('appSettings/add'):
			if add.attrib['key'] == 'AreaID':
				add.attrib['value'] = AreaID
			if add.attrib['key'] == 'AreaName':
				add.attrib['value'] = AreaName
			if add.attrib['key'] == 'AppName':
				add.attrib['value'] = Appname
		tree.write(self.__Road_config, encoding='utf-8', xml_declaration=True)

	def Flash_config(self, Req, parter_id, assist):
		dst = lambda st: st.replace(urlparse(st).netloc, assist)
		tree = self.make_tree(self.__Flash_config)
		root = tree.getroot()
		root.find('config/REQUEST_PATH').attrib['value'] = Req
		root.find('config/PARTER_ID').attrib['value'] = parter_id
		info = root.find('config/PHP').attrib['infoPath']
		root.find('config/PHP').attrib['infoPath'] = dst(info)
		comm = root.find('config/COMMUNITY_FRIEND_LIST_PATH').attrib['value']
		root.find('config/COMMUNITY_FRIEND_LIST_PATH').attrib['value'] = dst(comm)
		interface = root.find('config/COMMUNITY_INTERFACE').attrib['path']
		root.find('config/COMMUNITY_INTERFACE').attrib['path'] = dst(interface)
		tree.write(self.__Flash_config, encoding='utf-8', xml_declaration=True)

	def Flash_web(self, login, logout, title):
		tree = self.make_tree(self.__Flash_web)
		root = tree.getroot()
		for add in root.findall('appSettings/add'):
			if add.attrib['key'] == 'LoginUrl':
				add.attrib['value'] = login
			if add.attrib['key'] == 'LoginOnUrl':
				add.attrib['value'] = logout
			if add.attrib['key'] == 'SiteTitle':
				add.attrib['value'] = title
		tree.write(self.__Flash_web, encoding='utf-8', xml_declaration=True)

	def Flash_default(self):
		pass

	def Request_config(self, Did, Areaname):
		tree = self.make_tree(self.__request_config)
		root = tree.getroot()
		for add in root.findall('appSettings/add'):
			if add.attrib['key'] == 'DId':
				add.attrib['value'] = Did
			if add.attrib['key'] == 'AreaName':
				add.attrib['value'] = Areaname
		tree.write(self.__request_config, encoding='utf-8', xml_declaration=True)

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

def main():
	event = change()

	while True:
		print(
			'''
			1. 修改DB服务器 Center.Service.exe.config与key.txt文件
			2. 修改IIS服务器的
			[Server1|Road.Service.exe.config] 
			[Flash|config.xml web.config Default.aspx] 
			[Request|web.config]
			hosts 文件
			'''
		)
		p = int(input('请输入要修改的服务器[1:DB|2:iis]： '))
		if p == 1:
			pass