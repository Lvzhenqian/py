from hashlib import md5 as md5sum
from zipfile import ZipFile
from .email_get import *
import shutil


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


def zip_dir(dirname, zippath):
	with ZipFile(zippath, 'w') as myzip:
		if os.path.isfile(dirname):
			files = dirname
			myzip.write(files)
			return
		else:
			files = [os.path.join(root, name) for root, dirs, files in os.walk(dirname) for name in files]
			for file in files:
				myzip.write(file)


class work:
	def __init__(self, path):
		self.workpath = path
		os.chdir(self.workpath)
		self.package = os.path.join(self.workpath, 'package')
		os.mkdir('./dandantang')
		self.dir = os.path.join(self.workpath, 'dandantang')

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

	def DB_Make_Package(self):
		dirs = os.path.join(self.dir, r'db/dandantang/dandantang')
		os.makedirs(dirs)
		s_dir = [os.path.join(self.package, i) for i in ('Center', 'Create_Npc', 'sql')]
		for p in s_dir:
			if os.path.exists(p):
				shutil.copy2(p, dirs)
			if p.endswith('sql'):
				sqldir = os.path.join(self.dir, r'db/dandantang')
				for sqlfile in os.listdir(p):
					shutil.copy2(sqlfile, sqldir)
				self.sql(sqldir)
				shutil.copy2(os.path.join(self.package, 'readme.txt'), sqldir)
		if os.path.exists(os.path.join(dirs, 'Center')):
			self.keyfile(os.path.join(dirs, 'Center'))





oa_num = input('请输入邮件oa单号：')
package = mail_down(oa=oa_num)
download = r'd:/1.zip'
downfile = package.download_pack(download)

if md5sum(downfile) == package.Md5:
	os.chdir(os.path.dirname(downfile))
	unzip(zipfile=downfile, path='./package')
