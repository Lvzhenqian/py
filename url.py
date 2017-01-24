from urllib import request
from urllib import parse

url = 'http://192.168.19.20:1234/auth/login'
head = {
    'User-Agent':r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ',
    'Referer':r'http://192.168.19.20:1234/',
    'Content-Type':'application/json',
    'Connection':'keep-alive'
}

data = {'name':'root','password':'abcde'}
data = parse.urlencode(data).encode('ascii')
req = request.Request(url,data)
page = request.urlopen(req).read()

print(page)
