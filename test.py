import  requests
from urllib import parse
from contextlib import closing
import progressbar


def download_pack(save_path):
	requests.packages.urllib3.disable_warnings()
	m = 'http://ftpin.7road.com:8080/down?key=40866481db78c463c2d7930d34a2537c203075'
	header = {
		'Content-Type': 'application/x-www-form-urlencoded',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
					  'Chrome/56.0.2924.76 Safari/537.36'
	}
	urlp = parse.urlsplit(m)
	_, keywd = urlp.query.split('=', 1)
	url = 'http://ftpin.7road.com:8080/down'.replace('ftpin.7road.com', urlp.hostname)
	param = {
		'username': 'lv',
		'password': 'angelo_5566!@',
		'key': keywd}
	with closing(requests.request(method='POST', url=url, data=param, headers=header, stream=True)) as response:
		chunk_size = 1024  # 单次请求最大值
		content_size = int(response.headers['content-length'])
		flag = 0 if content_size % chunk_size == 0 else 1
		mxv = (content_size // chunk_size) + flag
		with open(save_path, 'wb') as f:
			widgets = ['下载：', progressbar.Percentage(),progressbar.Bar(marker='#', left='[', right=']'),
					   progressbar.ETA()]
			with progressbar.ProgressBar(widgets=widgets, maxval=mxv) as bar:
				n = 0
				for chunk in response.iter_content(chunk_size=chunk_size):
					if chunk:
						f.write(chunk)
						f.flush()
					bar.update(n)
					n += 1

download_pack(r'd:/1.zip')