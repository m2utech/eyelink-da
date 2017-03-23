import os
import time
from datetime import datetime, timedelta

import daemon
import daemon.pidfile

import logging
import logging.handlers
from logging import getLogger

from lockfile.pidlockfile import PIDLockFile
from lockfile import AlreadyLocked

# configuration
import config_info as config

from apscheduler.schedulers.blocking import BlockingScheduler
#from apscheduler.schedulers.background import BackgroundScheduler
import socket

#######################################################
# make logger instance
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Scheduler_Log")
logger.setLevel(logging.DEBUG)
LOGFILE = config.cfg['apscheduler_path']
LOGSIZE = 1024*100
LOGBACKUP_COUNT = 5

if not logger.handlers:
	loghandler = logging.handlers.RotatingFileHandler(LOGFILE, 
		maxBytes=LOGSIZE, backupCount=LOGBACKUP_COUNT)
	formatter = logging.Formatter('[%(asctime)s|%(name)s-%(levelname)s] >> %(message)s')
	loghandler.setFormatter(formatter)
	logger.addHandler(loghandler)

aps_logger = getLogger(__name__)
aps_logger = logger
#######################################################
# Server infomation for Socket
import config_info as config
HOST = config.cfg['host']
PORT = int(config.cfg['port'])
#HOST = 'm2u-da.eastus.cloudapp.azure.com'

#######################################################
def job_cron_day():
	logger.info("==========================")
	logger.debug("Start data analysis for one day")
	logger.info("==========================")

	today = datetime.now()
	minusDay = timedelta(days=122)
	startDate = today - minusDay
	endDate = startDate

	sendDate = '{"start_date":"'+ startDate.strftime('%Y-%m-%d') + '", "end_date":"' + endDate.strftime('%Y-%m-%d') + '", "time_interval":15}'
	sendDate = sendDate.encode()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓생성
	s.connect((HOST,PORT))
	s.send(sendDate) 
#	s.send(b'{"start_date": "2017-02-03", "end_date": "2017-02-03", "time_interval": 15}') #문자를 보냄
	data = s.recv(2048) #서버로 부터 정보를 받음
	s.close()
	print('Received',repr(data))


def job_cron_week():
	logger.info("==========================")
	logger.debug("Start data analysis for one week")
	logger.info("==========================")

	today = datetime.now()
	minusDay = timedelta(days=123)
	oneWeek = timedelta(days=6)
	endDate = today - minusDay
	startDate = endDate - oneWeek

	sendDate = '{"start_date":"'+ startDate.strftime('%Y-%m-%d') + '", "end_date":"' + endDate.strftime('%Y-%m-%d') + '", "time_interval":15}'
	sendDate = sendDate.encode()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓생성
	s.connect((HOST,PORT))
	s.send(sendDate) 
	#s.send(b'{"start_date": "2017-02-07", "end_date": "2017-02-07", "time_interval": 60}') #문자를 보냄
	data = s.recv(2048) #서버로 부터 정보를 받음
	s.close()
	print('Received',repr(data))


def start_daemon():

	pidfile = PIDLockFile(config.cfg['schePID_path'])
	try:
		pidfile.acquire()
	except AlreadyLocked:
		try:
			os.kill(pidfile.read_pid(), 0)
			print('Process already running!')
			exit(1)
		except OSError:  #No process with locked PID
			pidfile.break_lock()


	sched = BlockingScheduler()
	# Schedules job_function to be run on the third Friday
	# of June, July, August, November and December at 00:00, 01:00, 02:00 and 03:00
	#sched.add_job(job_function, 'cron', day_of_week='mon-fri', minute='*/1')
	sched.add_job(job_cron_day, 'cron', max_instances=10, hour='*/3')
	sched.add_job(job_cron_week, 'cron', max_instances=10, hour=0)

	sched.start()

	print("Start daemon for EyeLink in python")


with daemon.DaemonContext():
	start_daemon()