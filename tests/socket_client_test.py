# CLIENT

# -*- coding : cp949 -*-

import socket

# 테스트용 JSON 문자열
jsonString = '{"s_date": "2016-12-08", "e_date": "2016-12-08", "history": [{"date": "2015-03-11", "item": "iPhone"}, {"date": "2016-02-23", "item": "Monitor"}]}'


HOST='127.0.0.1' #localhost

PORT=50007 #서버와 같은 포트사용

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓생성

s.connect((HOST,PORT))

s.send(b'Hello, python') #문자를 보냄

data=s.recv(1024) #서버로 부터 정보를 받음

s.close()

print('Received',repr(data))
