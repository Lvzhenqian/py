from urllib import request, parse
from http import cookiejar
import re, json,sys


class Qy:
    __login_user = 'gdddt'
    __login_pwd = 'QY7RoaD@lktWzz7@Q'

    def __init__(self):
        self.__ajax_req = 'http://www.qycn.com/ajax.request.php?act=26'
        self.__image_url = 'http://www.qycn.com/yzcode.php?name=yz_login&num='

    def __read_conf(self, file: str) -> dict:
        pass

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
        parm = parse.urldefrag(parms)
        request.install_opener(opener)
        req = request.Request(url=self.__ajax_req, data=parm.encode('ascii'), headers=header)
        resp = opener.open(req)
        ret = json.loads(resp.read())['flag']
        if ret == 1:
            tok = opener.open('http://www.qycn.com/synlogin.php?action=dns')
            cmp = re.compile(r'<.*?><a href=".*\?tokenkey=(.*)" target')
            for x in tok.read():
                if b'tokenkey' in x:
                    mc = cmp.match(x.strip().decode())
                    tockenkey = mc.groups()[0]
                    break
            return opener
        return False

    def checker(self, dm, address=''):
        opener = self.__login_web()
        first, end = dm.split('.', 1)
        domid = {
            'shenquol.com': 18108,
            'ddshenqu.cn': 9794,
            'aeonsaga.com': 11283,
            '7road.net': 7106
        }
        data = {
            'myzone': first,
            'myaddress': address,
            'mytype': '',
            'mypriority': '',
            'page_size': '',
            'Submit': '查询'
        }
        domain = 'http://dns.qycn.com/index.php?tp=domls&domid=%d' % (domid[end])
        querystring = parse.urlencode(data)
        req = request.Request(url=domain,data=querystring.encode('ascii'))
        resp = opener.open(req)
        rex = r'(\w+\.shenquol.com)<.*?>\s*<.*?>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})<.*?>\s*<.*?>(\w{4})'
        cmx = re.compile(rex)
        lst = cmx.findall(resp.decode())
        if len(lst) == 2:
            print('{}\r\n{}'.format(*lst))
            sys.exit()
        elif not lst:
            pass
        else:
            pass

    def Add_to_list(self,dm,address,operator):
        pass
