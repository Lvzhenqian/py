from urllib import request
from urllib import parse

url = 'http://121.10.141.71:8081/chart'
head = {
    'Content-Type':'application/x-www-form-urlencoded'
}

data = {'endpoints[]':'113.107.161.24','counters[]':'df.bytes.total/stype=NTFS','graph_type':'h'}
data = parse.urlencode(data).encode('ascii')
req = request.Request(url,data)
page = request.urlopen(req).read()

print(page)
