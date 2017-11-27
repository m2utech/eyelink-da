import sys

from daemon import Daemon

import logging
import logging.handlers

# configuration
import config_info as config


class Start_daemon(object):
	
	def run(self):

		logger.info("ELDA daemon start...")
		while True:
			import elda_main


class EldaDaemon(Daemon):
	def run(self):
		startdaemon = Start_daemon()
		startdaemon.run()
		



if __name__ == '__main__':
	# make logger instance
	#logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger("elda_daemonLog")
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



	daemon = EldaDaemon(config.cfg['pidfile_path'])

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