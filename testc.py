import time
with open(r'c:\test.txt','wt',encoding='utf8') as f:
	while True:
		f.writelines(time.strftime('%Y:%m:%d %H:%M:%S')+'\r\n')
		time.sleep(5)
		f.flush()