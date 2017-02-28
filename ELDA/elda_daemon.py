import daemon
import daemon.pidfile
import lockfile
import logging
import logging.handlers

import time
import configparser

from elda_main import socket_server

# 전역변수로 처리 필요
config = configparser.ConfigParser()
config.read('../config.cfg')
cfg_server = config['SERVER_INFO']
cfg_default = config['DEFAULT_INFO']


def start_daemon():

	logger = logging.getLogger("DaemonLog")
	logger.setLevel(logging.INFO)
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	handler = logging.FileHandler(cfg_default['logging_path'])
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	daemon_context = daemon.DaemonContext(
		working_directory='/home/Toven/da/elda',
        umask=0o002,
        pidfile=daemon.pidfile.PIDLockFile(cfg_default['pidfile_path'),
        files_preserve=[handler.stream]
	)

	print("Start daemon for EyeLink in python")

	with daemon_context as context:
		while True:
			socket_server()
			logger.debug("Debug message")
			logger.info("Info message")
			logger.warn("Warning message")
			logger.error("Error message")
			time.sleep(10)

if __name__ == '__main__':
	start_daemon()