import daemon
import logging
import logging.handlers
import lockfile

from daemon import runner

class App():
	"""docstring for App"""
	def __init__(self):
		self.stdin_path = '/dev/null'
		self.stdout_path = '/dev/tty'
		self.stderr_path = '/dev/tty'
		self.pidfile_path = '/home/Toven/example/m2upidTest.pid'
		self.pidfile_timeout = 5

	def run(self):
		while True:
			#Main code goes here ...
			import test

			#Note that logger level needs to be set to logging.DEBUG before this shows up in the logs 
			logger.debug("Debug message") 
			logger.info("Info message") 
			logger.warn("Warning message")
			logger.error("Error message")

app = App()

# 로거 인스턴스를 만든다
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
# 포매터를 만든다
fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
# 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
#fileHandler = logging.FileHandler('./myLoggerTest.log')
fileMaxByte = 1024 * 1024 * 100 #100MB
fileHandler = logging.handlers.RotatingFileHandler('./m2uLoggerTest.log', maxBytes=fileMaxByte, backupCount=10)
# 각 핸들러에 포매터를 지정한다.
fileHandler.setFormatter(fomatter)
# 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
logger.addHandler(fileHandler)

daemon_runner = runner.DaemonRunner(app)

#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[fileHandler.stream]

try:
	daemon_runner.do_action()
except lockfile.LockTimeout:
	print("error: coodkfdkfk")
