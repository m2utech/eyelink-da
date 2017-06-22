# To kick off the script, run the following from the python directory:
# PYTHONPATH=`pwd` python elda_daemon.py start

#standard python libs
import time

#third party libs
from daemon import runner

class App():
  def __init__(self):
    self.stdin_path = '/dev/null'
    self.stdout_path = '/dev/tty'
    self.stderr_path = '/dev/tty'
    self.pidfile_path =  '/home/Toven/da/elda_daemon.pid'
    self.pidfile_timeout = 5

  def run(self):
    while True:
      print("tetetettetet")
      time.sleep(10)

app = App()
daemon_runner = runner.DaemonRunner(app)

daemon_runner.do_action()
