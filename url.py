from urllib import request
from urllib import parse

url = 'http://121.10.141.71:8081/api/counters'
head = {'Content-Type':'application/x-www-form-urlencoded'}

data = {'endpoints':'113.107.161.24'}
data = parse.urlencode(data).encode('ascii')
req = request.Request(url,data)
page = request.urlopen(req).read()

print(page)
