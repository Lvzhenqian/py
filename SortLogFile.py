from sys import argv
def FiletoSort(x):
	dic = {}
	def StrtoInt(x):
		if x == '' or x == '\n':
			return 0
		new = x.strip(' %\n\t\r')
		for i in new:
			if i not in '0123456789.' or x == '':
				return new
		return float(new)
	with open(x) as f:
		for i in f.readlines():
			sp = i.split('||')
			dic[i] = (int(sp[3].split(':')[-1].strip('%')), StrtoInt(sp[4].split(':')[-1]), StrtoInt(sp[5].split(':')[-1]),StrtoInt(sp[6].split(':')[-1]))
	return sorted(dic, key=lambda x: (dic[x][0], dic[x][1]))

if __name__ == '__main__':
	first = argv[1]
	end = argv[2]
	SortList=FiletoSort(first)
	print(len(SortList))
	with open(end,'a') as f:
		for line in SortList:
			f.write(line)