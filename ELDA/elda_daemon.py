# To kick off the script, run the following from the python directory:
# PYTHONPATH=`pwd` python elda_daemon.py start

#standard python libs
import logging
import time

#third party libs
import daemon
from daemon import runner
from elda_main import socket_server


class App():
  def __init__(self):
    self.stdin_path = '/dev/null'
    self.stdout_path = '/dev/tty'
    self.stderr_path = '/dev/tty'
    self.pidfile_path =  '/home/Toven/da/elda_daemon.pid'
    self.pidfile_timeout = 5

  def run(self):
    while True:
      socket_server()
      logger.debug("Debug message")
      logger.info("Info message")
      logger.warn("Warning message")
      logger.error("Error message")
      time.sleep(10)

app = App()
logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/home/Toven/da/logs/elda_daemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)

#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
