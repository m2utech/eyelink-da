# CLIENT
# coding: utf-8
# coding: cp949

import socket
import consts
import util

HOST = 'm2u-da.eastus.cloudapp.azure.com'
#HOST = 'DataAnalyzer'
PORT=5225 #포트지정
#HOST='192.168.10.27' #localhost
#HOST = 'localhost'
#PORT=5225 #서버와 같은 포트사용


s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓생성
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((HOST,PORT))
print("start test...")

s.send(b'{"type":"pattern", "node_id": "B009", "s_date": "2018-04-10T00:00:00Z", "e_date": "2018-04-12T00:00:00Z"}') #문자를 보냄
# s.send(b'{"type":"matching", "node_id": "0002.00000039", "s_date": "2017-11-08T14:00:00Z", "e_date": "2017-11-08T15:50:00Z"}') #문자를 보냄
print("good?")
data = s.recv(256) #서버로 부터 정보를 받음

print(data)

s.close()

print('Received',repr(data))
