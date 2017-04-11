from urllib import request, parse
from http import cookiejar
from collections import namedtuple
import re, json, sys


class Qy:
    __login_user = 'gdddt'
    __login_pwd = 'QY7RoaD@lktWzz7@Q'

    def __init__(self):
        self.__login_request = 'http://www.qycn.com/ajax.request.php?act=26'
        self.__image_url = 'http://www.qycn.com/yzcode.php?name=yz_login&num='
        self.__manage = 'http://dns.qycn.com/index.php'
        self.__domid = {'shenquol.com': 18108, 'ddshenqu.cn': 9794, 'aeonsaga.com': 11283, '7road.net': 7106}

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
        yz_login = input('Input yz code: ')
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
        ret = json.loads(resp.decode())['flag']
        if ret == 1:
            opener.open('http://www.qycn.com/synlogin.php?action=dns')
            # tok = opener.open('http://www.qycn.com/synlogin.php?action=dns')
            # cmp = re.compile(r'<.*?><a href=".*\?tokenkey=(.*)" target')
            # for x in tok.read():
            # 	if b'tokenkey' in x:
            # 		mc = cmp.match(x.strip().decode())
            # 		tockenkey = mc.groups()[0]
            # 		break
            return opener
        return False

    def checker(self, dm, address=''):
        opener = self.__login_web()
        first, end = dm.split('.', 1)

        data = {'myzone': first, 'myaddress': address, 'mytype': '', 'mypriority': '', 'page_size': '', 'Submit': '查询'}
        domain = 'http://dns.qycn.com/index.php?tp=domrs&domid=%d' % (self.__domid[end])
        querystring = parse.urlencode(data)
        req = request.Request(url=domain, data=querystring.encode('ascii'))
        resp = opener.open(req).read()
        rex = r'(\b%s)<.*?>\s*<.*?>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})<.*?>\s*<.*?>(\w{4})' % dm
        cmx = re.compile(rex)
        lst = cmx.findall(resp.decode())
        if len(lst) == 2:
            print('{} It have domain in the nameserver: '.format(dm))
            print('{}\r\n{}'.format(*lst))
            return lst
        elif not lst:
            return []
        else:
            return lst

    def Add_to_list(self, zone, address, operator):
        rule = {'tel':10,'uni':2}
        parms = {
            'tp': 'domrs', 'ac': 'adds_a', 'action': 'a', 'domid': 18108, 'dname': zone, 'vdname': zone,
            'address': address, 'mtype': rule[operator], 'mypriority': 10, 'myttl': 3600, 'submit': '新增'}

    def Delete_domain(self, name):
        first,end = name.split('.',1)
        p = {'tp':'domrs','ac':'ajaxs_del_a','redtp':'a','redid':62191173,'domid':self.__domid[end]}
        parms = {
            'tp': 'domrs', 'domid': 18108, 'type': 'A', 'myzone': first, 'myaddress': '', 'mytype': '', 'mypriority': '',
            'page_size': '', 'cid': ''}

    def run(self):
        pass
