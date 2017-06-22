# 진행된 사항이 없음(0303)
import configparser

config = configparser.RawConfigParser()
config.read('example.cfg')

cfg_server = config['SERVER_INFO']
cfg_default = config['DEFAULT_INFO']


print(config.sections())

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
        pidfile=daemon.pidfile.PIDLockFile(cfg_default['pidfile_path'],
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
	