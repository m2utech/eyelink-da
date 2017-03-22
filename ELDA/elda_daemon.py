import os
import time
import daemon
import daemon.pidfile

import logging
import logging.handlers

from lockfile.pidlockfile import PIDLockFile
from lockfile import AlreadyLocked

# configuration
import config_info as config


def start_daemon():

	# make logger instance
	#logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger("DA_daemonLog")
	logger.setLevel(logging.INFO)

	# make formatter
	formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

	# make handler to output Log for stream and file
	fileMaxByte = 1024 * 1024 * 100 #100MB
	fileHandler = logging.handlers.RotatingFileHandler(config.cfg['daemon_path'], maxBytes=fileMaxByte, backupCount=10)
	# specify formatter to each handler
	fileHandler.setFormatter(formatter)
	# attach stream and file handler to logger instance
	logger.addHandler(fileHandler)

	pidfile = PIDLockFile(config.cfg['pidfile_path'])
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
			working_directory='/home/Toven/da/elda', umask=0o002,
			pidfile=daemon.pidfile.PIDLockFile('/home/Toven/da/elda_daemon.pid'),
			files_preserve=[fileHandler.stream]
			)

	logger.info("==========================")
	logger.debug("Debug message")
	logger.info("Info message")
	logger.warning("Warning message")
	logger.error("Error message")
	logger.critical("critical debug message")
	logger.info("==========================")


	print("Start daemon for EyeLink in python")

#	daemon_context.open()


	with daemon_context as context:
		while True:
			import elda_main
			#time.sleep(10)



if __name__ == '__main__':
	start_daemon()