from apscheduler.schedulers.blocking import BlockingScheduler
import socket

import time

HOST = 'm2u-da.eastus.cloudapp.azure.com'
PORT = 5225


def job_function():
	print("Start data analysis")
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓생성
	s.connect((HOST,PORT))
	s.send(b'{"start_date": "2017-02-03", "end_date": "2017-02-04", "time_interval": 30}') #문자를 보냄
	data = s.recv(1024) #서버로 부터 정보를 받음
	s.close()
	print('Received',repr(data))


sched = BlockingScheduler()
# Schedules job_function to be run on the third Friday
# of June, July, August, November and December at 00:00, 01:00, 02:00 and 03:00
sched.add_job(job_function, 'cron', day_of_week='mon-fri', second='*/60')

sched.start()