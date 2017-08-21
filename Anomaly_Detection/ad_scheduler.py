import sys
from daemon import Daemon
from config_parser import cfg
import ad_logger as adLogging

import datetime
from dateutil.relativedelta import relativedelta

import socket

#from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError

# Server infomation for Socket
host = cfg['SERVER']['host']
port = int(cfg['SERVER']['port'])
node_id = cfg['DA']['node_id']
# HOST = 'm2u-da.eastus.cloudapp.azure.com'

#######################################################
class Scheduler(object):
	def __init__(self):
		self.sched = BackgroundScheduler()
		self.sched.start()
		self.job_id=''

	# 클래스가 종료될때, 모든 job들을 종료시켜줍니다.
	def __del__(self):
		self.shutdown()

	# 모든 job들을 종료시켜주는 함수입니다.
	def shutdown(self):
		self.sched.shutdown()

	def job_construct_patterns(self):
		logger.info("Start construction of pattern dataset")
		todays = datetime.datetime.today()
		s_date = (todays - relativedelta(months=1)).strftime('%Y-%m-%d')
		e_date = todays.strftime('%Y-%m-%d')
		sendDate = '{"type":"pattern","node_id":"' + node_id + '", "s_date":"' + s_date + '", "e_date":"' + e_date + '"}'
		sendDate = sendDate.encode()
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 소켓생성
		s.connect((host,port))
		s.send(sendDate)
		# print("send data : ", sendDate)
		data = s.recv(1024)  # 서버로 부터 정보를 받음
		s.close()
		print('Received', repr(data))


	def job_pattern_matching(self):
		logger.info("Start pattern matching")
		todays = datetime.datetime.today()
		s_time = (todays - relativedelta(minutes=110)).strftime('%Y-%m-%dT%H:%M:00')
		e_time = todays.strftime('%Y-%m-%dT%H:%M:00')
		sendDate = '{"type":"matching", "node_id":"' + node_id + '", "s_time":"' + s_time + '", "e_time":"' + e_time + '"}'
		sendDate = sendDate.encode()
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 소켓생성
		s.connect((host, port))
		s.send(sendDate)
		logger.info("sendDate: ", sendDate)
		data = s.recv(1024)  # 서버로 부터 정보를 받음
		s.close()
		print('Received', repr(data))


	def job_test(self):
		logger.info("job test~~~ just 10 sec")

	def scheduler(self):
		logger.info("Anomaly Detect Scheduler start...")
		self.sched.add_job(self.job_pattern_matching, 'cron', max_instances=5, minute='*/10')
		self.sched.add_job(self.job_construct_patterns, 'cron', max_instances=5, hour=0)
		#self.sched.add_job(self.job_test, 'cron', max_instances=5, second='*/10')



class SchedulerDaemon(Daemon):

	def run(self):
		scheduler = Scheduler()
		scheduler.scheduler()

		while True:
			pass


if __name__ == '__main__':
	logger = adLogging.get_sche_logger()
	daemon = SchedulerDaemon(cfg['DAEMON']['sche_pid_path'])
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
