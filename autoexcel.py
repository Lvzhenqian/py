# coding:utf-8
import csv
from collections import namedtuple


class convert:
	def __init__(self, iplist, csvfile):
		self.iplist = iplist
		self.csv = csvfile
		self.name = None

	def __ReadIPlist(self):
		dic = {}
		with open(self.iplist,'rt') as fd:
			for i in fd:
				first,*_ = i.split()


	def __ReadCsv(self):
		with open(self.csv) as f:
			f_csv = csv.reader(f)
			_ = next(f_csv)
			data = namedtuple('data', ['name', 'more', 'master'])
			while True:
				try:
					i = next(f_csv)
					yield data(i[11], i[14], i[15])
				except StopIteration:
					break

	def getsite(self):
		rule = {
			"百度": 'baidu_{:0>4}_cgdb'.format,
			"7road官网": '7road_{:0>4}_cgdb'.format,
			"多玩": 'duowan_{:0>4}_cgdb'.format,
			"7k7k": '7k7k_{:0>4}_cgdb'.format,
			"开心": 'kxwang_{:0>4}_cgdb'.format,
			"奇虎": 'qihu360_{:0>4}_cgdb'.format,
			"上海淘米": 'taomi_{:0>4}_cgdb'.format,
			"4399": '4399_{:0>4}_cgdb'.format
		}
		site = []
		fill = lambda st: ''.join([x for x in st.split('-')[0] if x in '0123456789'])
		excel = self.__ReadCsv()
		add = lambda x: site.append(x) if x not in site else x
		for lines in excel:
			for ne in lines.more.split('、'):
				n = fill(ne)
				if lines.name:
					self.name = lines.name
				if '7road' in self.name or '官网' in self.name:
					add(rule["7road官网"](n))
				if '360' in self.name or '奇虎' in self.name:
					add(rule["奇虎"](n))
				if 'kx' in self.name or '开心' in self.name:
					add(rule["开心"](n))
				if 'taomi' in self.name or '淘米' in self.name:
					add(rule["上海淘米"](n))
				add(rule[self.name](n))
		return site


s = convert(csvfile=r'.\test.csv', iplist=None)
for site in s.getsite():
	print(site)
