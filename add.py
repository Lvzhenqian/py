from urllib import request, parse
from http import cookiejar
from collections import namedtuple
import re, json, sys


class QYclient:
	"""
	类变量，用于在所有实例都可以使用这个账号与密码
	"""
	__login_user = 'gdddt'
	__login_pwd = 'QY7RoaD@lktWzz7@Q'

	def __init__(self):
		'''
		构造函数，每当实例化时，增加一些属性与生成一个opener()
		'''
		self.__login_request = 'http://www.qycn.com/ajax.request.php?act=26'
		self.__image_url = 'http://www.qycn.com/yzcode.php?name=yz_login&num='
		self.__manage = 'http://dns.qycn.com/index.php'
		self.__domid = {'shenquol.com': 18108, 'ddshenqu.cn': 9794, 'aeonsaga.com': 11283, '7road.net': 7106}
		self.__opener = self.__login_web()

	def __read_file(self, fd) -> iter:
		"""
		处理domain.txt，解析出所需要的格式
		:param fd: 传入文件路径
		:return: 返回，namedtuple所组成的生成器,例子：
		domain(name='s1558.shenquol.com', tellcom='113.107.148.122', unicom='112.90.248.122')
		"""
		with open(fd, 'rt', encoding='utf8') as f:
			namelist, tup = [], []
			dic = namedtuple('domain', ['name', 'tellcom', 'unicom'])
			for line in f:
				if line.startswith(('assist', 's', 'res')):
					namelist.append(line.strip())
				if line[0].isdigit() and not '_' in line:
					tell, uni = line.split()
					tup.append([dic(x, tell, uni) for x in namelist])
					namelist.clear()
		return (j for n in range(len(tup)) for j in tup[n])

	def __login_web(self) -> request.build_opener:
		"""
		登陆函数，手动输入验证码。
		:return: 返回一个处理函数，opener() 用于打开这个站点的所有链接。
		"""
		header = {
			'Content-Type': 'application/x-www-form-urlencoded',
			'Accept': 'application/json, text/javascript, */*',
			'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
			'Host': 'www.qycn.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
			              'Chrome/56.0.2924.76 Safari/537.36',
			'X-Requested-With': 'XMLHttpRequest',
			'Referer': 'http://www.qycn.com/user.php?action=login&goto=http://www.qycn.com/synlogin.php?action=dns',
			'Origin': 'http://www.qycn.com'
		}
		cookie = cookiejar.CookieJar()
		pro = request.HTTPCookieProcessor(cookie)
		opener = request.build_opener(pro)
		opener.addheaders.extend([(k, v) for k, v in header.items()])
		yz_code = opener.open(self.__image_url).read()
		with open('./yz_code.png', 'wb') as f:
			f.write(yz_code)
		yz_login = input('请输入验证码：')
		parms = {
			'username': self.__login_user,
			'password': self.__login_pwd,
			'yz_login': yz_login,
			'save_name': 1
		}
		parm = parse.urlencode(parms)
		request.install_opener(opener)
		req = request.Request(url=self.__login_request, data=parm.encode('ascii'), headers=header)
		resp = opener.open(req).read()
		ret = json.loads(resp.decode())
		print(ret['msg'])
		if ret['flag'] == 1:
			'''
			增加了一个GET链接，下方代码可以获取这个链接的tockenkey.因为没发现用处，先注释掉不使用。
			'''
			opener.open('http://www.qycn.com/synlogin.php?action=dns')
			# tok = opener.open('http://www.qycn.com/synlogin.php?action=dns')
			# cmp = re.compile(r'<.*?><a href=".*\?tokenkey=(.*)" target')
			# for x in tok.read():
			# 	if b'tokenkey' in x:
			# 		mc = cmp.match(x.strip().decode())
			# 		tockenkey = mc.groups()[0]
			# 		break
			return opener.open
		else:
			sys.exit()

	def checker(self, dm: str, address='') -> list:
		"""
		查询函数，用来查询域名或者IP地址的解析记录
		:param dm: 传入域名字符串，可以为空
		:param address: 传入IP地址字符串，可以为空
		:return: 返回namedtuple 列表对象。
		"""
		if dm:
			nt = dm.rsplit('.', 2)
			first, end = nt[0], '.'.join(nt[-2:])
			rex = r'<.*name_(\w+)">(\b%s)<.*?>\s*<.*?>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})<.*?>\s*<.*?>(\w{4})' % dm
		else:
			first = ''
			end = input('请输入将要在那个域名后缀中查询IP地址：')
			rex = r'<.*name_(\w+)">(.*)<.*?>\s*<.*?>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})<.*?>\s*<.*?>(\w{4})'
		data = {'myzone': first, 'myaddress': address, 'mytype': '', 'mypriority': '', 'page_size': '', 'Submit': '查询'}
		domain = 'http://dns.qycn.com/index.php?tp=domrs&domid=%d' % (self.__domid[end])
		querystring = parse.urlencode(data)
		req = request.Request(url=domain, data=querystring.encode('ascii'))
		resp = self.__opener(req).read()

		cmx = re.compile(rex)
		find = cmx.findall(resp.decode())
		if not find:
			return []
		ret = namedtuple('checker', ['id', 'domain', 'address', 'operator'])
		return [ret(*x) for x in find]

	def Add_to_list(self, *, name, address, operator) -> str:
		"""
		增加函数，功能是把域名增加到解析记录里。
		:param name: 传入要解析的域名字符串。
		:param address: 传入对应的IP地址。
		:param operator: 传入解析的线路。【全部线路】【中国联通】这两个其中一个。
		:return: 添加成功返回字符串状态，否则返回False
		"""
		nt = name.rsplit('.', 2)
		first, end = nt[0], '.'.join(nt[-2:])
		mapping = {'全部线路': 10, '中国联通': 2}
		parms = {
			'tp': 'domrs', 'ac': 'adds_a', 'action': 'a', 'domid': self.__domid[end], 'dname': first, 'vdname': first,
			'address': address, 'mtype': mapping[operator], 'mypriority': 10, 'myttl': 3600, 'submit': '新增'}
		query = parse.urlencode(parms)
		reqs = request.Request(self.__manage, data=query.encode('ascii'))
		resp = self.__opener(reqs).read()
		o = re.compile(r'showinfo\(\'(\S+)\',')
		status = o.findall(resp.decode())
		return status.pop() if status else False

	def Delete_domain(self, *, name, domain_id) -> str:
		"""
		删除域名函数
		:param name: 传入将要删除的域名 
		:param domain_id: 传入域名对应的ID
		:return: 返回操作结果字符串。
		"""
		nt = name.rsplit('.', 2)
		first, end = nt[0], '.'.join(nt[-2:])
		p = dict(tp='domrs', ac='ajaxs_del_a', redtp='a', redid=domain_id, domid=self.__domid[end])
		query = parse.urlencode(p)
		reque = request.Request(self.__manage, data=query.encode('ascii'))
		resp = self.__opener(reque).read()
		status = json.loads(resp.decode())
		return status['message']

	def Outprint(self, **kwargs):
		return '[{count:>3}]执行结果：{stat}  域名：{name} 解析到：{address}--{operator}'.format(**kwargs)

	def run(self):
		"""
		自动执行函数，用于自动增加domain.txt文件里的域名
		:return: 返回添加的总结果字符串
		"""
		it = self.__read_file('./domain.txt')
		successful, fail = 0, 0
		for nametp in it:
			telcheck = self.checker(nametp.name, nametp.tellcom)
			if not telcheck:
				telstat = self.Add_to_list(name=nametp.name, address=nametp.tellcom, operator='全部线路')
				if telstat:
					successful += 1
					print(self.Outprint(count=successful, stat=telstat, name=nametp.name, address=nametp.tellcom,
					                    operator='全部线路'))
			else:
				fail += 1

			unichekc = self.checker(nametp.name, nametp.unicom)
			if not unichekc:
				unistat = self.Add_to_list(name=nametp.name, address=nametp.unicom, operator='中国联通')
				if unistat:
					successful += 1
					print(self.Outprint(count=successful, stat=unistat, name=nametp.name, address=nametp.unicom,
					                    operator='中国联通'))
			else:
				fail += 1
		return '成功：{}  失败：{} 总数：{}'.format(successful, fail, successful + fail)


if __name__ == '__main__':
	print('开始登陆群英解析站点')
	client = QYclient()
	while True:
		new = input("请输入将要执行的操作[run|del|add|check|quit]：")
		if new.lower() == 'quit':
			break
		if new.lower() == 'run':
			print(client.run())
		if new.lower() == 'check':
			name = input('【可选】输入要查询的域名：')
			address = input('【可选】输入要查询的IP地址： ')
			req = client.checker(name, address)
			if req:
				for n in req:
					print("----------------------")
					p = '记录ID：{} 域名：{} 解析地址：{} 解析线路：{}'.format(n.id, n.domain, n.address, n.operator)
					print(p)
					print("----------------------")
			else:
				print('没有找到这条DNS记录')
		if new.lower() == 'add':
			rule = {'1': '全部线路', '2': '中国联通'}
			name = input('输入要绑定的域名：')
			address = input('输入域名对应的IP地址： ')
			oper = input('输入解析的线路 [1]全部线路 [2]中国联通： ')
			req = client.Add_to_list(name=name, address=address, operator=rule[oper])
			print("----------------------")
			print('{name} add to list {stat}'.format(name=name, stat=req))
			print("----------------------")
		if new.lower() == 'del':
			name = input('输入要删除的域名： ')
			ck = client.checker(name)
			if ck:
				while ck:
					print("----------------------")
					for n in range(len(ck)):
						print('{} {} {} {}'.format(n, ck[n].id, ck[n].domain, ck[n].address))
					print("----------------------")
					id_n = input("请输入将要删除的解析记录，[quit]退出删除：")
					if id_n.lower() == 'quit':
						break
					stat = client.Delete_domain(domain_id=ck[int(id_n)].id, name=name)
					ck.pop(int(id_n))
					print('删除{}: {}'.format(name, stat))
			else:
				print('没有找到 {} 解析记录'.format(name))
