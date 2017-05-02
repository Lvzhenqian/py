from .XmlTree import Tree, TreeWrite


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
