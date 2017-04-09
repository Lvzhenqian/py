from datetime import datetime
import time
n = 0
while n < 100000000:
	try:
		data = datetime.now()
		print(data.timestamp(),end=' ')
		print(data.strftime('%Y-%m-%d %H:%M:%S'))
		time.sleep(1)
	except KeyboardInterrupt:
		break
