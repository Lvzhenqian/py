from urllib import request, parse
from http import cookiejar
from collections import namedtuple
import re, json


class QYclient:
	__login_user = 'gdddt'
	__login_pwd = 'QY7RoaD@lktWzz7@Q'

	def __init__(self):
		self.__login_request = 'http://www.qycn.com/ajax.request.php?act=26'
		self.__image_url = 'http://www.qycn.com/yzcode.php?name=yz_login&num='
		self.__manage = 'http://dns.qycn.com/index.php'
		self.__domid = {'shenquol.com': 18108, 'ddshenqu.cn': 9794, 'aeonsaga.com': 11283, '7road.net': 7106}
		self.__opener = self.__login_web()

	def __read_file(self, fd) -> iter:
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
			opener.open('http://www.qycn.com/synlogin.php?action=dns')
			# tok = opener.open('http://www.qycn.com/synlogin.php?action=dns')
			# cmp = re.compile(r'<.*?><a href=".*\?tokenkey=(.*)" target')
			# for x in tok.read():
			# 	if b'tokenkey' in x:
			# 		mc = cmp.match(x.strip().decode())
			# 		tockenkey = mc.groups()[0]
			# 		break
			return opener.open
		return False

	def checker(self, dm: str, address='') -> namedtuple:
		first, end = dm.split('.', 1)
		data = {'myzone': first, 'myaddress': address, 'mytype': '', 'mypriority': '', 'page_size': '', 'Submit': '查询'}
		domain = 'http://dns.qycn.com/index.php?tp=domrs&domid=%d' % (self.__domid[end])
		querystring = parse.urlencode(data)
		req = request.Request(url=domain, data=querystring.encode('ascii'))
		resp = self.__opener(req).read()
		rex = r'<.*name_(\w+)">(\b%s)<.*?>\s*<.*?>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})<.*?>\s*<.*?>(\w{4})' % dm
		cmx = re.compile(rex)
		find = cmx.findall(resp.decode())
		if not find:
			return []
		ret = namedtuple('checker', ['id', 'domain', 'address', 'operator'])
		return ret(find)

	def Add_to_list(self, *, name, address, operator) -> str:
		first, end = name.split('.', 1)
		rule = {'全部线路': 10, '中国联通': 2}
		parms = {
			'tp': 'domrs', 'ac': 'adds_a', 'action': 'a', 'domid': self.__domid[end], 'dname': first, 'vdname': first,
			'address': address, 'mtype': rule[operator], 'mypriority': 10, 'myttl': 3600, 'submit': '新增'}
		query = parse.urlencode(parms)
		req = request.Request(self.__manage, data=query.encode('ascii'))
		resp = self.__opener(req).read()
		o = re.compile(r'showinfo\(\'(\S+)\',')
		status = o.findall(resp.decode())
		return status.pop() if status else False

	def Delete_domain(self, *, name, domain_id) -> str:
		first, end = name.split('.', 1)
		p = dict(tp='domrs', ac='ajaxs_del_a', redtp='a', redid=domain_id, domid=self.__domid[end])
		query = parse.urlencode(p)
		req = request.Request(self.__manage, data=query.encode('ascii'))
		resp = self.__opener(req).read()
		status = json.loads(resp.decode())
		return status['message']

	def Outprint(self, **kwargs):
		return '[{count:>3}]执行结果：{stat}  域名：{name} 解析到：{address}--{operator}'.format(**kwargs)

	def run(self):
		it = self.__read_file('./domain.txt')
		successful, fail = 0, 0
		for nametp in it:
			telcheck = self.checker(nametp.name, nametp.tellcom)
			if not telcheck:
				stat = self.Add_to_list(name=nametp.name, address=nametp.tellcom, operator='全部线路')
				if stat:
					successful += 1
					print(self.Outprint(count=successful,
										stat=stat, name=nametp.name,
										address=nametp.tellcom, operator='全部线路'))
				else:
					fail += 1

			unichekc = self.checker(nametp.name, nametp.unicom)
			if not unichekc:

				stat = self.Add_to_list(name=nametp.name, address=nametp.unicom, operator='中国联通')
				if stat:
					successful += 1
					print(self.Outprint(count=successful,
										stat=stat, name=nametp.name,
										address=nametp.unicom, operator='中国联通'))
				else:
					fail += 1
		return '成功：\033[1;32 {} \033[0m  失败：\033[1;31 {} \033[0m 总数：{}'.format(successful, fail, successful + fail)


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
			name = input('输入要查询的域名：')
			address = input('【可选】输入域名对应的IP地址： ')
			req = client.checker(name, address)
			if req:
				p = '记录ID：{}--域名：{}--解析地址：{}--解析线路：{}'.format(req.id, req.domain, req.address, req.operator)
				print(p)
			else:
				print('没有找到这条DNS记录')
		if new.lower() == 'add':
			rule = {'1':'全部线路','2':'中国联通'}
			name = input('输入要绑定的域名：')
			address = input('输入域名对应的IP地址： ')
			oper = input('输入解析的线路 [1]全部线路 [2]中国联通： ')
			req = client.Add_to_list(name=name,address=address,operator=rule[oper])
			print('{name} add to list {stat}'.format(name=name,stat=req))
		if new.lower() == 'del':
			name = input('输入要删除的域名： ')
			ck = client.checker(name)
			if ck:
				stat = client.Delete_domain(domain_id=ck.id,name=name)
				print('删除{}: \033[1;32 {} \033[0m'.format(name,stat))
			else:
				print('没有找到\033[1;31m {} \033[0m解析记录'.format(name))
