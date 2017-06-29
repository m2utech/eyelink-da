# CLIENT
# coding: utf-8
# coding: cp949

import socket

#HOST = 'm2u-da.eastus.cloudapp.azure.com'
#HOST = 'DataAnalyzer'
PORT=5229 #포트지정
#HOST='192.168.10.27' #localhost
HOST = 'localhost'
#PORT=5225 #서버와 같은 포트사용


s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓생성
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.connect((HOST,PORT))
print("start test...")
s.send(b'{"node_id": "0002.00000039", "start_date": "2017-01-22", "end_date": "2017-01-31", "time_interval": 15}') #문자를 보냄

data = s.recv(2048) #서버로 부터 정보를 받음

#print(data)

s.close()

print('Received',repr(data))
