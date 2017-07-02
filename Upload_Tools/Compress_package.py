
from zipfile import ZipFile
import os
import shutil
import subprocess


def unzip(zipfile, path, encoding='gbk'):
	with ZipFile(zipfile, 'r') as myzip:
		for name in myzip.namelist():
			filename = name.encode('cp437').decode(encoding)
			pathname = os.path.join(path, os.path.dirname(filename))
			if not os.path.exists(pathname) and pathname != "":
				os.makedirs(pathname)
			data = myzip.read(name)
			file = os.path.join(path, filename)
			if not os.path.exists(file):
				with open(file, 'wb') as f:
					f.write(data)


def zip_dir(dirname, zippath, mode='w'):
	with ZipFile(zippath, mode=mode) as myzip:
		if os.path.isfile(dirname):
			files = dirname
			myzip.write(files)
			return
		else:
			files = [os.path.join(root, name) for root, dirs, files in os.walk(dirname) for name in files]
			for file in files:
				myzip.write(file)


class work:
	def __init__(self, path, agent,oa):
		self.fix = subprocess.STARTUPINFO()
		self.fix.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		self.workpath = path
		os.chdir(self.workpath)
		self.package = os.path.join(self.workpath, 'package')
		os.mkdir('./dandantang')
		self.dir = os.path.join(self.workpath, 'dandantang')
		self.fileck = 'FileCheck_MD5.exe'

	def keyfile(self, path):
		resp = requests.get('http://113.107.167.212/GenerateKey?expire=86400')
		t = resp.text
		with open(os.path.join(path, 'key.txt'), 'wt') as f:
			stat, key = t.decode().split('=')
			if stat == 'success':
				f.write(key)

	def sql(self, path):
		'''
        生成执行sql的批处理文件
        :param path:
        :return:
        '''
		sqlfiles = [os.path.basename(i) for i in os.listdir(path) if i.endswith('.sql')]
		s = '''
@echo off 
cd /d D:\server-new\dandantang 
sqlcmd -S 127.0.0.1,2433 -i {sql} -E -r0 2>db-error.log 1>db.log 
set "paths=D:\server-new\dandantang\db-error.log" 
for %%a in ("%paths%") do ( 
    if "%%~za" equ "0" ( 
        echo success > end.log 
        ) else ( 
        echo fail > end.log 
    )  
) 
exit 
'''.format(sql=','.join(sqlfiles))
		bat = os.path.join(path, 'sql.bat')
		with open(bat, 'wt') as f:
			f.write(s)

	def IIS_CONFIG_UPDATE(self, path, flag='all'):
		dic = {
			'all': '''
@echo off  
cd /d D:\dandantang\Flash 
update.exe 
cd /d D:\dandantang\Request\CreateAllXml 
CreateAllXml.exe 
iisreset -restart 
exit
    ''',
			'baxi': '''
@echo off 
cd /d D:\dandantang\Flash 
update.exe 
cd /d D:\dandantang\Request\CreateAllXml 
CreateAllXml.exe
cd /d D:\dandantang\Resource\Flash
create.bat 
iisreset -restart 
exit 
    ''',
			'guonei': '''
@echo off  
cd /d D:\dandantang\Flash 
update.exe
UpdateFileName.exe 
cd /d D:\dandantang\Resource\Flash 
update.exe
UpdateFileName.exe 
cd /d D:\dandantang\Request\XmlCreate 
CreateAllXml.exe 
iisreset -restart 
exit
    '''}
		with open('config_update.bat', 'wt') as f:
			f.write(dic[flag])

	def File_Update_kill(self, path):
		'''
        停服覆盖文件脚本生成
        :param path:
        :return:
        '''
		s = '''
@echo off 
echo 删除进程 
TASKKILL /F /IM Road.Service.exe  
TASKKILL /F /IM Fighting.Service.exe 
TASKKILL /F /IM Center.Service.exe 
REM  File Update Start 
echo. 
echo Setp1 File Update Start!!!!!! 
echo. 
echo. 
echo Begin To Update Files,Please Wait...... 
echo -------------------------------------------------------- 
d:\ddt_tool\FileBack.exe d:\dandantang D:\server-new\dandantang\dandantang D:\server-bak\ -u 
echo. 
echo. 
echo File Update Finish!!!!!! 
echo. 
echo================================ 
echo. 
REM Check File 
echo Setp2 Check File 
echo. 
echo File Check start!!!!!! 
echo. 
echo. 
d:\ddt_tool\FileCheck_MD5.exe -check d:\dandantang -k d:\server-new\dandantang\dandantang.key 
echo. 
echo File Check Finish!!!!!! 
echo. 
echo================================ 
echo 
echo Setp 3 Update The configure File 
iisreset -restart
'''
		with open('file_update.bat', 'wt') as f:
			f.write(s)

	def File_Update_NotKill(self, path):
		s = '''
@echo off 
REM  File Update Start 
echo. 
echo Setp1 File Update Start!!!!!! 
echo. 
echo. 
echo Begin To Update Files,Please Wait...... 
echo -------------------------------------------------------- 
d:\ddt_tool\FileBack.exe d:\dandantang D:\server-new\dandantang\dandantang D:\server-bak\ -u 
echo. 
echo. 
echo File Update Finish!!!!!! 
echo. 
echo================================ 
echo. 
REM Check File 
echo Setp2 Check File 
echo. 
echo File Check start!!!!!! 
echo. 
echo. 
d:\ddt_tool\FileCheck_MD5.exe -check d:\dandantang -k d:\server-new\dandantang\dandantang.key 
echo. 
echo File Check Finish!!!!!! 
echo. 
echo================================ 
echo 
echo Setp 3 Update The configure File 
iisreset -restart
'''
		with open('file_update.bat', 'wt') as f:
			f.write(s)

	def __Compress(self, which):
		Compress_Path = os.path.join(self.dir, which)
		if os.path.exists(Compress_Path):
			os.chdir(Compress_Path)
			shutil.copy2(os.path.join(self.package, 'readme.txt'), Compress_Path)
			zip_dir('./dandantang', './dandantang.zip')
			zip_dir('./readme.txt', './dandantang.zip', mode='a')

	def ___check_key(self, source, dst_path):
		###创建dandantang.key文件
		md5key = os.path.join(dst_path, 'dandantang.key')
		p = subprocess.Popen(args=[self.fileck, '-create', source, '-k', md5key], shell=True,
							 stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.DEVNULL,
							 universal_newlines=True, startupinfo=self.fix, env=os.environ)
		ret = p.stdout.read()
		if ret.split()[1] != 'successed':
			return False
		c = subprocess.Popen(args=[self.fileck, '-check', source, '-k', md5key], shell=True,
							 stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.DEVNULL,
							 universal_newlines=True, startupinfo=self.fix, env=os.environ)
		check_ret = c.stdout.read()
		if check_ret.split()[1] != 'success':
			return False

	def DB_Make_Package(self):
		copypath = os.path.join(self.dir, r'db/dandantang/dandantang')
		os.makedirs(copypath)
		s_dir = [os.path.join(self.package, i) for i in ('Center', 'Create_Npc', 'sql')]
		compress_path = os.path.join(self.dir, r'db/dandantang')
		if not s_dir:
			return False
		for p in s_dir:
			if os.path.exists(p):
				shutil.copy2(p, copypath)
			if p.endswith('sql'):
				for sqlfile in os.listdir(p):
					shutil.copy2(sqlfile, compress_path)
				self.sql(compress_path)
		self.___check_key(copypath, compress_path)
		if os.path.exists(os.path.join(copypath, 'Center')):
			self.keyfile(os.path.join(copypath, 'Center'))
		return compress_path

	def FS_Make_Package(self):
		copypath = os.path.join(self.dir, r'fs/dandantang/dandantang')
		os.makedirs(copypath)
		s_dir = [os.path.join(self.package, i) for i in ('Center', 'AreaRankServer', 'FightServer', 'sql')]
		compress_path = os.path.join(self.dir, r'fs/dandantang')
		if not s_dir:
			return False
		for p in s_dir:
			if os.path.exists(p):
				shutil.copy2(p, copypath)
			if p.endswith('FightServer'):
				shutil.copy2(p, copypath)
				for n in range(1, 5):
					ds = os.path.join(copypath, str(n) + 'v' + str(n))
					shutil.copy2(p, ds)
			if p.endswith('sql'):
				for sqlfile in os.listdir(p):
					shutil.copy2(sqlfile, compress_path)
				self.sql(compress_path)
		self.___check_key(copypath, compress_path)
		return compress_path

	def IIS_Make_Package(self, *, online=False, tp='all'):
		copypath = os.path.join(self.dir, r'iis/dandantang/dandantang')
		os.makedirs(copypath)
		s_dir = [os.path.join(self.package, i) for i in ('Flash', 'AreaRankServer', 'Request', 'Resource')]
		compress_path = os.path.join(self.dir, r'iis/dandantang')
		if not s_dir:
			return False
		for p in s_dir:
			if os.path.exists(p):
				shutil.copy2(p, copypath)
		if online:
			self.File_Update_NotKill(compress_path)
		else:
			self.File_Update_kill(compress_path)
		self.IIS_CONFIG_UPDATE(compress_path, tp)
		self.___check_key(copypath, compress_path)
		return compress_path

	def GS_Make_Package(self):
		copypath = os.path.join(self.dir, r'gs/dandantang/dandantang')
		os.makedirs(copypath)
		s_dir = [os.path.join(self.package, i) for i in ('FightServer', 'AreaRankServer', 'Server', 'Server1')]
		compress_path = os.path.join(self.dir, r'gs/dandantang')
		if not s_dir:
			return False
		for p in s_dir:
			if os.path.exists(p):
				shutil.copy2(p, copypath)
			if p.endswith('Server') or p.endswith('Server1'):
				shutil.copy2(p, os.path.join(copypath, 'Server1'))
				shutil.copy2(p, os.path.join(copypath, 'Server2'))
		self.___check_key(copypath, compress_path)
		return compress_path

	def GSIIS_Make_Package(self, *, online=False, tp='all'):
		copypath = os.path.join(self.dir, r'gsiis/dandantang/dandantang')
		os.makedirs(copypath)
		s_dir = [os.path.join(self.package, i) for i in
				 ('Flash', 'AreaRankServer', 'Request', 'Resource', 'FightServer',
				  'Server', 'Server1')]
		compress_path = os.path.join(self.dir, r'gsiis/dandantang')
		if not s_dir:
			return False
		for p in s_dir:
			if os.path.exists(p):
				shutil.copy2(p, copypath)
			if p.endswith('Server') or p.endswith('Server1'):
				shutil.copy2(p, os.path.join(copypath, 'Server1'))
				shutil.copy2(p, os.path.join(copypath, 'Server2'))
		if online:
			self.File_Update_NotKill(compress_path)
		else:
			self.File_Update_kill(compress_path)
		self.IIS_CONFIG_UPDATE(compress_path, tp)
		self.___check_key(copypath, compress_path)
		return compress_path

	def runner(self):
		self.DB_Make_Package()
		self.FS_Make_Package()
		self.GSIIS_Make_Package()
		for ps in os.listdir(self.dir):
			cpath = os.path.realpath(ps)
			self.__Compress(cpath)



