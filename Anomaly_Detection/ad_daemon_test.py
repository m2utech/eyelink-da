import sys, getopt, time, os
import signal
from multiprocessing import Process, Queue, freeze_support
from daemon import Daemon
from ad_logger import getAdLogger
from ad_configParser import getConfig


class JobServer(Process):
	def stopsignal(self, signum):
		self.substoptag = 1

	def __init__(self):
		Process.__init__(self)
		self.substoptag = 0

	def run(self):
		signal.signal(signal.SIGTERM,self.stopsignal)
		print("sub process run")
		while True:
			time.sleep(5)
			if self.substoptag == 1:
				print("exit sub process")
				break;

class AdDaemonMain(Daemon):
	def __init__(self, pidfile):
		self.pidfile = pidfile
		self.procs = []


	def run(self):
		print("Job start")
		proc = [JobServer(), "one Job"]
		self.procs.append(proc)

		proc[0].start()


if __name__ == '__main__':
    logger = getAdLogger()
    cfg = getConfig()
    daemon = AdDaemonMain(cfg['SERVICE']['path_ad_pid'])

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            logger.info("Started Anomaly Detection daemon ...")
            daemon.start()
        elif 'stop' == sys.argv[1]:
            logger.info("Stopped Anomaly Detection daemon ...")
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            logger.info("Restarted Anomaly Detection daemon ...")
            daemon.restart()
        else:
            print("unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
