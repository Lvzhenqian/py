# coding:utf8
import os
import win32serviceutil
import configparser
from functools import partial
from platform import release
from subprocess import run, PIPE

from .XmlTree import Tree, TreeWrite


class InstallDB:
	def __init__(self):
		self.path = r'd:\sql'
		self.abspath = partial(os.path.join, self.path)
		self.rule = {'7': self.server_2008, '2003Server': self.server_2003}


	def server_2003(self):
		return self.server_2008()

	def server_2008(self):
		Framework_prc = run('ServerManagerCmd -i NET-Framework -a', shell=True, stdout=PIPE, stderr=PIPE)
		for framework in Framework_prc.stdout.splitlines():
			print(framework.decode('utf8'))
		sql_prc = run('start /wait {exec}  /settings {conf} /qb'.format(exec=self.abspath('setup'),
		                                                                conf=self.abspath('setup.ini')))
		if sql_prc.returncode == 0:
			print('SQL server 2005安装完成！')
		sql_chang = run('sqlcmd -S .\sql2005 -d master -i {sql} -E -b'.format(sql=self.abspath('修改端口.sql')),
		                shell=True, stdout=PIPE, stderr=PIPE)
		for i in sql_chang.stdout.splitlines():
			print(i.decode())
		if sql_chang.returncode == 0:
			print('修改端口脚本执行成功！')
		sql_sac = run('"C:\Program Files (x86)\Microsoft SQL Server\90\Shared\sac" in {sac} -S .'.format(
			sac=self.abspath('sac.xml')),shell=True,stdout=PIPE,stderr=PIPE)
		for j in sql_sac.stdout.splitlines():
			print(j.decode('utf8'))
		if sql_sac.returncode == 0:
			print('修改外围配置成功！')
		win32serviceutil.StopService('SQLAGENT$SQL2005')
		win32serviceutil.RestartService('MSSQL$SQL2005')
		win32serviceutil.StartService('SQLAGENT$SQL2005')


	def run(self):
		return self.rule[release()]()


class AutoDB:
	def __init__(self):
		self.__Center_File = r'D:\dandantang\Center\Center.Service.exe.config'
		self.__WCFFile = r'D:\dandantang\Center\WCFFileGet.dll.config'
		self.__Create_npc = r'D:\dandantang\Create_npc\CreatNpcPlayers.exe.config'
		self.config = configparser.ConfigParser()
		self.config.read('./config.ini')
		self.__key = self.config['Config']['startkey']

	def __Center_File(self):
		tree = Tree(self.__Center_File)
		root = tree.getroot()
		for add in root.findall('appSettings/add'):
			if add.attrib['key'] == 'AreaID':
				add.attrib['value'] = self.config['Config']['AreaID']
			if add.attrib['key'] == 'conString':
				add.attrib['value'] = self.config['Config']['conString']
			if add.attrib['key'] == 'countDb':
				add.attrib['value'] = self.config['Config']['countDb']
		TreeWrite(tree, self.__Center_File)

	def __Key_File(self, key):
		with open(self.__key, 'w') as f:
			f.write(key)

	def __WCffile(self):
		tree = Tree(self.__WCFFile)
		tree.find('system.serviceModel/client/endpoint').attrib['address'] = r'http://{IP}:12347/MethodForGame'.format(
			IP=self.config['Config']['IIS_IP']
		)
		TreeWrite(tree,self.__WCFFile)

	def __Create_NPC(self):
		tree = Tree(self.__Create_npc)
		root = tree.getroot()
		for add in root.findall('appSettings/add'):
			if add.attrib['key'] == 'conString':
				add.attrib['value'] = self.config['Config']['conString']
		TreeWrite(tree,self.__Create_npc)