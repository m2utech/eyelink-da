import os
import daemon
import daemon.pidfile

import logging
import logging.handlers

from lockfile.pidlockfile import PIDLockFile
from lockfile import AlreadyLocked

import configparser

'''
# 전역변수로 처리 필요
config = configparser.ConfigParser()
config.read('../config.cfg')
cfg_server = config['SERVER_INFO']
cfg_default = config['DEFAULT_INFO']
'''


def start_daemon():
	# 전역변수로 처리 필요
	config = configparser.ConfigParser()
	config.read('./config.cfg')
	cfg_server = config['SERVER_INFO']
	cfg_default = config['DEFAULT_INFO']
	# make logger instance
	logger = logging.getLogger("DA_daemonLog")
	
	# make formatter
	formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

	# make handler to output Log for stream and file
	fileMaxByte = 1024 * 1024 * 100 #100MB
	fileHandler = logging.handlers.RotatingFileHandler(cfg_default['test_path'], maxBytes=fileMaxByte, backupCount=10)

	# fileHandler = logging.FileHandler(cfg_default['logging_path'])
	streamHandler = logging.StreamHandler()

	# specify formatter to each handler
	fileHandler.setFormatter(formatter)
	streamHandler.setFormatter(formatter)

	# attach stream and file handler to logger instance
	logger.addHandler(fileHandler)
	logger.addHandler(streamHandler)

	pidfile = PIDLockFile(cfg_default['test_pid_path'])
	try:
		pidfile.acquire()
	except AlreadyLocked:
		try:
			os.kill(pidfile.read_pid(), 0)
			print('Process already running!')
			exit(1)
		except OSError:  #No process with locked PID
			pidfile.break_lock()



	daemon_context = daemon.DaemonContext(
		working_directory='/home/Toven/da/elda',
		umask=0o002,
		pidfile=PIDLockFile('/home/Toven/da/elda_daemon.pid'),
	)

	print("Start daemon for EyeLink in python")

	with daemon_context:
		while True:
			logger.setLevel(logging.INFO)
			logger.info("==========================")
			logger.debug("Debug message")
			logger.info("Info message")
			logger.warn("Warning message")
			logger.error("Error message")
			logger.critical("critical debug message")
			logger.info("==========================")

			#import elda_main


if __name__ == '__main__':
	start_daemon()