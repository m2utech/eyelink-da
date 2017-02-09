# socket server for data analysis from node.js

# coding: cp949
# coding: utf-8

# default lib of python
import socket
import json

# required lib
import elda_clustering as clustering_main

def json_parsing(data):
	dict = json.loads(data.decode("utf-8")) # dictionary type
	start_date = dict['start_date']
	end_date = dict['end_date']
	time_interval = dict['time_interval']

	clustering_main.data_load(start_date, end_date, time_interval)


def socket_server():
	HOST = '192.168.10.27'
	#HOST = 'http://m2u-da.eastus.cloudapp.azure.com'
	PORT = 5225

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.bind((HOST, PORT))

	s.listen(1) # Wait for connection
	print('The server is ready to receive')

	while 1:
		conn, addr = s.accept() # approve connection
		print('accepted connection')

		data = conn.recv(1024)

		if not data: break

		json_parsing(data)

		conn.send(b"ok") #받은 데이터를 그대로 클라이언트에 전송
		print("completed~~")

	conn.close() # if false

############################
if __name__ == '__main__':
	socket_server()