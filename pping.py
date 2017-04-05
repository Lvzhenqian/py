import os, argparse,socket,struct,select,time


ICMP_ECHO_REQUEST = 8
DEFAULT_TIMEOUT = 2
DEFAULT_COUNT = 4
class Pinger:
	def __init__(self,target_host,count=DEFAULT_COUNT,timeout=DEFAULT_TIMEOUT):
		self.target_host = target_host
		self.count = count
		self.timeout = timeout
	def do_checksum(self,source_string):
		sum = 0
		max_count = (len(source_string) /2)*2
		count = 0
		while count < max_count:
			val = ord(source_string[count +1]) *256 + ord(source_string[count])
			sum += val
			sum &= 0xffffffff
			count += 2
		if max_count<len(source_string):
			sum +=ord(source_string[len(source_string)-1] )
			sum &= 0xffffffff
		sum = (sum >> 16) + (sum &0xffff)
		sum +=(sum >> 16)
		answer = ~sum
		answer &= 0xffff
		answer = answer >> 8 | (answer<<8&0xff00)
		return answer
	def receive_pong(self,sock,ID,timeout):
		time_remaining = timeout
		while True:
			start_time = time.time()
			readable= select.select([sock],[],[],time_remaining)
			time_spent = (time.time() - start_time)
			if readable[0] ==[]:
				return
			time_received = time.time()
			recv_packet,addr = sock.recvfrom(1024)
			icmp_header = recv_packet[20:28]
			type,code,checksum,packet_ID,sequence = struct.unpack("bbHHh",icmp_header)
			if packet_ID == ID:
				bytes_in_double = struct.calcsize("d")
				time_sent = struct.unpack("d",recv_packet[28:28 + bytes_in_double])[0]
				return  time_received - time_sent
			time_remaining -= time_spent
			if time_remaining <= 0:
				return
	def send_ping(self,sock,ID):
		target_addr = socket.gethostbyname(self.target_host)
		my_checksum = 0
		header = struct.pack("bbHHh",ICMP_ECHO_REQUEST,0,my_checksum,ID,1)
		bytes_in_double = struct.calcsize("d")
		data = (192 - bytes_in_double) * "Q"
		data += struct.pack("d",time.time())
		new_data = data.encode()
		my_checksum = self.do_checksum(header+new_data)
		header = struct.pack(
			"bbHHh",ICMP_ECHO_REQUEST,0,socket.htons(my_checksum),ID,1
		)
		packet = header + new_data
		sock.sendto(packet,(target_addr,1))
	def ping_once(self):
		icmp = socket.getprotobyname("icmp")
		try:
			sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,icmp)
		except socket.error as (errno,msg):
			if errno == 1:
				msg += "ICMP messages can only be sent from root user processes"
				raise socket.error(msg)
		except Exception as e:
			print("Exception: {}".format(e))
		my_ID = os.getpid() & 0xFFFF
		self.send_ping(sock,my_ID)
		delay = self.receive_pong(sock,my_ID,self.timeout)
		sock.close()
		return delay
	def ping(self):
		for i in range(self.count):
			print("Ping to {}...".format(self.target_host),end='')
			try:
				delay =  self.ping_once()
			except socket.gaierror as e:
				print("Ping failed.(socket error: {} )".format(e))
				break
			if delay is None:
				print("Ping failed.timeout within {}sec.".format(self.timeout))
			else:
				delay *= 1000
				print("Get Pong in %0.4fms" % delay)
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Python Ping')
	parser.add_argument('--target-host',action='store',dest='target_host',required=True)
	given_args = parser.parse_args()
	target_host = given_args.target_host
	pinger = Pinger(target_host=target_host)
	pinger.ping()