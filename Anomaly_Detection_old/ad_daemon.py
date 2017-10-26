import sys
from daemon import Daemon
# import logging
# import logging.handlers
import ad_logger as adLogging
from config_parser import cfg


class Start_daemon(object):
    def run(self):
        while True:
            import ad_main


class adDaemon(Daemon):
    def run(self):
        startdaemon = Start_daemon()
        startdaemon.run()


if __name__ == '__main__':
    # pidfile_path = '/home/Toven/da/ad_daemon.pid'
    # daemon = adDaemon(pidfile_path)
    logger = adLogging.get_daemon_logger()
    
    daemon = adDaemon(cfg['DAEMON']['ad_pid_path'])
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
