import time
from apscheduler.schedulers.blocking import BlockingScheduler
#from apscheduler.schedulers.background import BackgroundScheduler
import socket

import configparser


def job_cron_day():
	#HOST = 'm2u-da.eastus.cloudapp.azure.com'
	HOST = 'dataanalyzer'
	PORT = 5225
	print("Start data analysis for day")
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓생성
	s.connect((HOST,PORT))
	s.send(b'{"start_date": "2017-02-03", "end_date": "2017-02-03", "time_interval": 15}') #문자를 보냄
	data = s.recv(128) #서버로 부터 정보를 받음
	s.close()
	print('Received',repr(data))

def job_cron_week():
	#HOST = 'm2u-da.eastus.cloudapp.azure.com'
	HOST = 'dataanalyzer'
	PORT = 5225
	print("Start data analysis for week")
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓생성
	s.connect((HOST,PORT))
	s.send(b'{"start_date": "2017-02-07", "end_date": "2017-02-07", "time_interval": 60}') #문자를 보냄
	data = s.recv(128) #서버로 부터 정보를 받음
	s.close()
	print('Received',repr(data))

# 전역변수로 처리 필요
config = configparser.ConfigParser()
config.read('../config.cfg')
cfg_server = config['SERVER_INFO']
cfg_default = config['DEFAULT_INFO']


sched = BlockingScheduler()
# Schedules job_function to be run on the third Friday
# of June, July, August, November and December at 00:00, 01:00, 02:00 and 03:00
#sched.add_job(job_function, 'cron', day_of_week='mon-fri', minute='*/1')
sched.add_job(job_cron_day, 'cron', max_instances=10, minute=0)
sched.add_job(job_cron_week, 'cron', max_instances=10, day_of_week='mon-fri', hour='*/3')

sched.start()