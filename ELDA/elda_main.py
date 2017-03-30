import os
import socket
from threading import Thread
import json
import configparser
import elda_clustering as clustering_main

import logging
import logging.handlers
import time

#configuration
import config_info as config

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):

	def __init__(self, ip, port):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		print("New da-server socket thread started for" + ip + ":" + str(port))

	def json_parsing(data):

		# running time check
		start_time = time.time()
		logger.info("Dataset Loading...")

		dict = json.loads(data.decode("utf-8")) # dictionary type
		start_date = dict['start_date']
		end_date = dict['end_date']
		time_interval = dict['time_interval']
		clustering_main.data_load(start_date, end_date, time_interval)

		running_time = time.time() - start_time
		logger.info("Start-date:{0} | End-date:{1} | Time-interval:{2} >> Running-time:{3:.03f} sec".format(start_date,end_date,time_interval, running_time))

		


	def run(self):
		while True:
			data = conn.recv(2048)
			print("Server received data:", data)
			if not data:	break
			ClientThread.json_parsing(data)
			conn.send(b"analysis success")
			print("anlysis success")


#########################################
# make logger instance

logger = logging.getLogger("Running_Log")
logger.setLevel(logging.INFO)

# make formatter
formatter = logging.Formatter('[%(levelname)s|%(asctime)s] > %(message)s')

# make handler to output Log for stream and file
fileMaxByte = 1024 * 1024 * 100 #100MB
fileHandler = logging.handlers.RotatingFileHandler(config.cfg['run_log_path'], maxBytes=fileMaxByte, backupCount=10)
# specify formatter to each handler
fileHandler.setFormatter(formatter)
# attach stream and file handler to logger instance
logger.addHandler(fileHandler)

#HOST = '192.168.10.27'
#PORT=5225 #포트지정
HOST = config.cfg['host']
PORT = int(config.cfg['port'])

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


if __name__ == '__main__':
	pass