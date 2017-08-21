import logging
import logging.handlers
from config_parser import cfg

def get_running_logger():
	logger = logging.getLogger("ad-running")
	logger.setLevel(logging.INFO)
	# make formatter
	formatter = logging.Formatter('[%(levelname)s|%(asctime)s] > %(message)s')

	# make handler to output Log for stream and file
	fileMaxByte = 1024 * 1024 * 100     # 100MB
	
	fileHandler = logging.handlers.RotatingFileHandler(cfg['DAEMON']['run_log_path'], maxBytes=fileMaxByte, backupCount=10)
	# specify formatter to each handler
	fileHandler.setFormatter(formatter)
	# attach stream and file handler to logger instance
	logger.addHandler(fileHandler)

	return logger


def get_daemon_logger():
	logger = logging.getLogger("ad-daemon")
	logger.setLevel(logging.INFO)
	# make formatter
	formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

	# make handler to output Log for stream and file
	fileMaxByte = 1024 * 1024 * 100     # 100MB
	
	fileHandler = logging.handlers.RotatingFileHandler(cfg['DAEMON']['daemon_path'], maxBytes=fileMaxByte, backupCount=10)
	# specify formatter to each handler
	fileHandler.setFormatter(formatter)
	# attach stream and file handler to logger instance
	logger.addHandler(fileHandler)

	return logger

def get_sche_logger():
	logger = logging.getLogger("ad-scheduler")
	logger.setLevel(logging.INFO)
	# make formatter
	formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

	# make handler to output Log for stream and file
	fileMaxByte = 1024 * 1024 * 100     # 100MB
	
	fileHandler = logging.handlers.RotatingFileHandler(cfg['DAEMON']['scheduler_path'], maxBytes=fileMaxByte, backupCount=10)
	# specify formatter to each handler
	fileHandler.setFormatter(formatter)
	# attach stream and file handler to logger instance
	logger.addHandler(fileHandler)

	return logger