import os
import daemon
import daemon.pidfile

import logging
import logging.handlers

from lockfile.pidlockfile import PIDLockFile
from lockfile import AlreadyLocked

import configparser


# 전역변수로 처리 필요
config = configparser.ConfigParser()
config.read('../config.cfg')
cfg_server = config['SERVER_INFO']
cfg_default = config['DEFAULT_INFO']


def start_daemon():

	daemon_context = daemon.DaemonContext(
		working_directory='./', umask=0o002, pidfile=PIDLockFile('/home/Toven/da/elda_daemon.pid'))

	# make logger instance
	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger("DA_daemonLog")
	# logger.setLevel(logging.DEBUG)

	# make formatter
	formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

	# make handler to output Log for stream and file
	fileMaxByte = 1024 * 1024 * 100 #100MB
	fileHandler = logging.handlers.RotatingFileHandler('./testlog.log', maxBytes=fileMaxByte, backupCount=10)
	# specify formatter to each handler
	fileHandler.setFormatter(formatter)
	# attach stream and file handler to logger instance
	logger.addHandler(fileHandler)

	daemon_context.filesPreserve = [fileHandler.stream]


	pidfile = PIDLockFile(cfg_default['pidfile_path'])
	try:
		pidfile.acquire()
	except AlreadyLocked:
		try:
			os.kill(pidfile.read_pid(), 0)
			print('Process already running!')
			exit(1)
		except OSError:  #No process with locked PID
			pidfile.break_lock()


	print("Start daemon for EyeLink in python")

	daemon_context.open()


	with daemon_context:
		while True:
			import elda_main
			import apscheduler_test_0320
			logger.info("==========================")
			logger.debug("Debug message")
			logger.info("Info message")
			logger.warn("Warning message")
			logger.error("Error message")
			logger.critical("critical debug message")
			logger.info("==========================")



if __name__ == '__main__':
	start_daemon()