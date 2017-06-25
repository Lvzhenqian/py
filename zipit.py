from zipfile import ZipFile
import os


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
