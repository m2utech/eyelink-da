import socket
from threading import Thread
import json

# configuration
import config_parser as configuration

import anomaly_main as ad_main

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):

	def __init__(self, ip, port):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		print("New da-server socket thread started for" + ip + ":" + str(port))
		#logger.info("New da-server socket thread started for" + ip + ":" + str(port))

	def run(self):
		while True:
			data = conn.recv(2048)
			print("Server received data:", data)
			if not data:	break
			ClientThread.json_parsing(data)
			conn.send(b"analysis success")
			print("anlysis success")

	def json_parsing(data):

		#logger.info("Dataset Loading...")
		dict = json.loads(data.decode("utf-8")) # dictionary type
		node_id = dict['node_id']
		start_date = dict['start_date']
		end_date = dict['end_date']
		time_interval = dict['time_interval']

		# main module
		ad_main.main(node_id, start_date, end_date, time_interval)


#########################################
# configuration
cfg = configuration.cfg_parser()

HOST = cfg.host
PORT = int(cfg.port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
threads = []

while True:
	s.listen(50)
	print('The da-server is ready to receive')
	(conn, (ip,port)) = s.accept()
	print('accepted connection')

	newthread = ClientThread(ip, port)
	newthread.start()
	threads.append(newthread)

for t in threads:
	t.join()


if __name__ == '__main__':
	pass