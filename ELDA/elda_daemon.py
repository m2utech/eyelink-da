import daemon
import daemon.pidfile
import lockfile
import logging
import logging.handlers

import time

from elda_main import socket_server

def start_daemon():

	logger = logging.getLogger("DaemonLog")
	logger.setLevel(logging.INFO)
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	handler = logging.FileHandler("/home/Toven/da/logs/elda_daemon.log")
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	daemon_context = daemon.DaemonContext(
		working_directory='/home/Toven/da/elda',
        umask=0o002,
        pidfile=daemon.pidfile.PIDLockFile('/home/Toven/da/elda_daemon.pid'),
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