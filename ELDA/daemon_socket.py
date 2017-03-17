import os
import daemon
import daemon.pidfile

import logging
import logging.handlers

from lockfile.pidlockfile import PIDLockFile
from lockfile import AlreadyLocked

import time
import configparser

import socket
from threading import Thread
import json
import configparser
import elda_clustering as clustering_main

#from elda_main import socket_server
#import elda_socket


# 전역변수로 처리 필요
config = configparser.ConfigParser()
config.read('../config.cfg')
cfg_server = config['SERVER_INFO']
cfg_default = config['DEFAULT_INFO']

def ClientThread(Thread):
	while True:
		data = conn.recv(1024)
		print("Server received data:", data)

		if not data:	break

		ClientThread.json_parsing(data)

		conn.send(b"analysis success")
		print("anlysis success")


def socket_forever():
	#HOST = '192.168.10.27'
	#PORT=5225 #포트지정
	HOST = cfg_server['host']
	PORT = int(cfg_server['port'])

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	threads = []

	while True:
		s.listen(10)
		print('The da-server is ready to receive')
		conn, add = s.accept()
		newthread = Thread(target=ClientThread, args=[conn])
		newthread.daemon = True
		newthread.start()
		threads.append(newthread)

	for t in threads:
		t.join()



def start_daemon():

	print("Start daemon for EyeLink in python")

	with daemon.DaemonContext():
		while True:
#			elda_main.run()
			time.sleep(10)

if __name__ == '__main__':
	start_daemon()