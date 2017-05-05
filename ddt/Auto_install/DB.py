#coding:utf8
from .XmlTree import Tree, TreeWrite
from subprocess import run, PIPE
from platform import release


class InstallDB:
	def server_2003(self):
		pass

	def server_2008(self):
		Framework_prc = run('ServerManagerCmd -i NET-Framework -a', shell=True, stdout=PIPE,stderr=PIPE)
		stat = Framework_prc.stdout.split(b'\r\n')[-2]
		#print(stat.decode('utf8'))
		sql_prc = run()



	def run(self):
		rule = {'7': self.server_2008, '2003Server': self.server_2003}
		return rule[release()]()

class AutoDB:
	def __init__(self):
		self.__Center_File = r'D:\dandantang\Center\Center.Service.exe.config'
		self.__key = r'D:\dandantang\Center\key.txt'

	def __Center_File(self, AreaID, constring='', countdb=''):
		tree = Tree(self.__Center_File)
		root = tree.getroot()
		for add in root.findall('appSettings/add'):
			if add.attrib['key'] == 'AreaID':
				add.attrib['value'] = AreaID
			if add.attrib['key'] == 'conString' and constring != '':
				add.attrib['value'] = constring
			if add.attrib['key'] == 'countDb' and countdb != '':
				add.attrib['value'] = countdb
		TreeWrite(tree, self.__Center_File)

	def __Key_File(self, key):
		with open(self.__key, 'w') as f:
			f.write(key)
