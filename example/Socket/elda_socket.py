import socket
from threading import Thread
import json
import configparser
#import elda_clustering as clustering_main


# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):

	def __init__(self, ip, port):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		print("New da-server socket thread started for" + ip + ":" + str(port))


	def json_parsing(data):
		dict = json.loads(data.decode("utf-8")) # dictionary type
		start_date = dict['start_date']
		print(start_date)
		print(type(start_date))
		end_date = dict['end_date']
		print(end_date)
		print(type(end_date))
		time_interval = dict['time_interval']
		print(time_interval)
		print(type(time_interval))
		clustering_main.data_load(start_date, end_date, time_interval)


	def run(self):
		while True:
			data = conn.recv(1024)
			print("Server received data:", data)

			if not data:	break

			ClientThread.json_parsing(data)

			conn.send(b"analysis success")
			print("anlysis success")


config = configparser.ConfigParser()
config.read('../config.cfg')
cfg_server = config['SERVER_INFO']
cfg_default = config['DEFAULT_INFO']

#HOST = '192.168.10.27'
#PORT=5225 #포트지정
HOST = cfg_server['host']
PORT = int(cfg_server['port'])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
threads = []

while True:
	s.listen(50)
	print('The da-server is ready to receive')
	(conn, (ip,port)) = s.accept()
	newthread = ClientThread(ip, port)
	newthread.start()
	threads.append(newthread)

for t in threads:
	t.join()