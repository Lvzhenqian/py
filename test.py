import  requests
from urllib import parse
from contextlib import closing
import progressbar


def download_pack(save_path):
	requests.packages.urllib3.disable_warnings()
	m = ''
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
		with open(save_path, 'wb') as f:
			widgets = ['下载进度: ', progressbar.Percentage(), ' ',
					   progressbar.Bar(marker='#', left='[', right=']'),
					   ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
			pbar = progressbar.ProgressBar(widgets=widgets, maxval=content_size).start()
			for chunk in response.iter_content(chunk_size=chunk_size):
				if chunk:
					f.write(chunk)
					f.flush()
				pbar.update(len(chunk) + 1)
			pbar.finish()