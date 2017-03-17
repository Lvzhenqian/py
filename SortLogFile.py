from sys import argv
from re import split


def FiletoSort(x):
	dic = {}

	def StrtoInt(x):
		if x == '' or x == '\n':
			return 0
		new = x.strip(' %\n\t\r')
		for string in new:
			if string not in '0123456789.' or x == '':
				return new
		return float(new)

	for file in x:
		with open(file) as f:
			for i in f:
				key = i.replace('\n', '||' + file + '\n')
				sp = i.split('||')
				dic[key] = {'time': sp[1],
				            'site': sp[2],
				            'lost': int(sp[3].split(':')[-1].strip('%')),
				            'min': StrtoInt(sp[4].split(':')[-1]),
				            'avg': StrtoInt(sp[5].split(':')[-1]),
				            'mix': StrtoInt(sp[6].split(':')[-1])}
	return dic


def Name(x):
	ret = {}
	with open(x) as fd:
		for line in fd:
			value, key, *_ = split(r'\*.* (\w.*)_\d.*', line)
			ret[key] = value
	return ret


if __name__ == '__main__':
	SortList = FiletoSort(argv[2:])
	NameDict = Name(argv[1])
	# s2 = sorted(SortList, key=lambda x: (SortList[x]['lost'],SortList[x]['avg']))
	# with open('./OutPut.txt', 'w') as f:
	# 	for line in s2:
	# 		f.write(line)
	ret = {}
	for k, v in SortList.items():
		site = v['site'].split('_')[0]
		key = k.replace('|',NameDict[site]+'|',1)
		if v['lost'] != 0:
			continue
		if site not in ret.keys() or ret[site][1] > v['avg']:
			ret[site] = (key, v['avg'])
		else:
			continue
	with open('./SortFile.log', 'w') as fd:
		for k, v in ret.items():
			fd.write(v[0])
