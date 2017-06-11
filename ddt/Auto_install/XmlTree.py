from xml.etree import cElementTree
from shutil import move as mv
import time,os


class ET(cElementTree.TreeBuilder):
	def comment(self, data):
		self.start(cElementTree.Comment, {})
		self.data(data)
		self.end(cElementTree.Comment)


def Tree(file: str) -> cElementTree.parse:
	backup = '_'.join((file, time.strftime('%Y-%m-%d')))
	if not os.path.exists(backup):
		mv(file, backup)
	with open(backup, 'r+', encoding='utf8') as f:
		return cElementTree.parse(f, parser=cElementTree.XMLParser(target=ET()))


def TreeWrite(tree: cElementTree.parse, file: str):
	return tree.write(file, encoding='utf-8', xml_declaration=True)
