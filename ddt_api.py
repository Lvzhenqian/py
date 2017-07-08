import sys
from urllib.request import urlopen
from urllib import parse
up = parse.urlparse(sys.argv[1])
querystring = parse.urlencode(parse.parse_qsl(up.query))
url = 'http://yw.7road-inc.com:8081/updateGameAreaBySid?{}'.format(querystring)
o = urlopen(url)
w = o.read().decode()
with open(r'C:\smallLinux\home\combine_log\url.log', 'wt', encoding='utf-8') as f:
	f.write('请求的URL：{}'.format(url))
	f.write('respone:' + w + '\r\n')
