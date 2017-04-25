import requests, json, time,pymysql



class Cleaner:
	def __init__(self):
		self.__graph_api = 'http://127.0.0.1:9966/graph/history'
		self.__portal_api = 'http://127.0.0.1:5050/api/hostclean'

	def Get_metric(self, Stime, Etime, *args):
		head = {'Content-Type': 'application/json'}
		data = {"start": Stime, "end": Etime, "cf": "AVERAGE", "endpoint_counters": list(args)}
		req = requests.post(self.__graph_api, json.dumps(data),headers=head)
		return req.json()

	def CleanHost(self, ip):
		head = {'Content-Type': 'application/x-www-form-urlencoded'}
		data = dict(ipaddr=ip)
		req = requests.get(self.__portal_api, params=data, headers=head)
		return req.json()

if __name__ =='__main__':
	def Get_host_list(ip):
		conn = pymysql.connect(host=ip,user='openfalcon',password='open-falcon@#7road',databases='falcon_portal',port='2433')
		cur = conn.cursor()
		cur.execute('''SELECT hostname FROM host''')
		ret = cur.fetchall()
		cur.close()
		conn.close()
		return ret
	hostlist=Get_host_list('192.168.161.84')