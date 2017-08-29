import sys
from daemon import Daemon
import logging
import logging.handlers
import config_info as config

import socket

import datetime
from dateutil.relativedelta import relativedelta
from apscheduler.schedulers.blocking import BlockingScheduler


# Server infomation for Socket
HOST = config.cfg['host']
PORT = int(config.cfg['port'])
#HOST = 'm2u-da.eastus.cloudapp.azure.com'

#######################################################
def job_cron_day():
	logger.info("===== Start data analysis for one day =====")

	today = datetime.datetime.today()
	startDate = (today - relativedelta(days=1)).strftime('%Y-%m-%dT%H:%M:00')
	endDate = today.strftime('%Y-%m-%dT%H:%M:00')

	sendDate = '{"start_date":"'+ startDate + '", "end_date":"' + endDate + '", "time_interval":15}'
	sendDate = sendDate.encode()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓생성
	s.connect((HOST,PORT))
	s.send(sendDate) 
#	s.send(b'{"start_date": "2017-02-03", "end_date": "2017-02-03", "time_interval": 15}') #문자를 보냄
	data = s.recv(512) #서버로 부터 정보를 받음
	s.close()
	print('Received',repr(data))


def job_cron_week():
	logger.info("===== Start data analysis for one week =====")
	
	today = datetime.datetime.today()
	startDate = (today - relativedelta(weeks=1)).strftime('%Y-%m-%dT%H:00:00')
	endDate = today.strftime('%Y-%m-%dT%H:00:00')

	sendDate = '{"start_date":"'+ startDate + '", "end_date":"' + endDate + '", "time_interval":60}'
	sendDate = sendDate.encode()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓생성
	s.connect((HOST,PORT))
	s.send(sendDate) 
	#s.send(b'{"start_date": "2017-02-07", "end_date": "2017-02-07", "time_interval": 60}') #문자를 보냄
	data = s.recv(512) #서버로 부터 정보를 받음
	s.close()
	print('Received',repr(data))


def job_cron_month():
	logger.info("===== Start data analysis for one month =====")

	today = datetime.datetime.today()
	startDate = (today - relativedelta(months=1)).strftime('%Y-%m-%dT00:00:00')
	endDate = today.strftime('%Y-%m-%dT00:00:00')

	sendDate = '{"start_date":"'+ startDate + '", "end_date":"' + endDate + '", "time_interval":60}'
	sendDate = sendDate.encode()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓생성
	s.connect((HOST,PORT))
	s.send(sendDate) 
	#s.send(b'{"start_date": "2017-02-07", "end_date": "2017-02-07", "time_interval": 60}') #문자를 보냄
	data = s.recv(512) #서버로 부터 정보를 받음
	s.close()
	print('Received',repr(data))


class Start_scheduler(object):

	def run(self):
		logger.info("ELDA Scheduler start...")
		while True:
			sched = BlockingScheduler()

			sched.add_job(job_cron_day, 'cron', max_instances=10, hour=0)
			sched.add_job(job_cron_week, 'cron', max_instances=10, day_of_week='mon', hour=0, minute=10)
			sched.add_job(job_cron_month, 'cron', max_instances=10, day=1, hour=1)
			sched.start()


class SchedulerDaemon(Daemon):
	def run(self):
		startdaemon = Start_scheduler()
		startdaemon.run()
		


if __name__ == '__main__':
	# make logger instance
	logger = logging.getLogger("Scheduler_Log")
	logger.setLevel(logging.INFO)

	# make formatter
	formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

	# make handler to output Log for stream and file
	fileMaxByte = 1024 * 1024 * 100 #100MB
	fileHandler = logging.handlers.RotatingFileHandler(config.cfg['apscheduler_path'], maxBytes=fileMaxByte, backupCount=10)
	# specify formatter to each handler
	fileHandler.setFormatter(formatter)
	# attach stream and file handler to logger instance
	logger.addHandler(fileHandler)

	daemon = SchedulerDaemon(config.cfg['schePID_path'])

	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print("unknown command")
			sys.exit(2)
		sys.exit(0)
	else:
		print("usage: %s start|stop|restart" % sys.argv[0])
		sys.exit(2)
	#######################################################