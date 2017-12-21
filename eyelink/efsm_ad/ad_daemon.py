import sys
from daemon import Daemon
from ad_logger import getAdLogger
from ad_configParser import getConfig
import ad_main
import consts


class StartDaemon(object):
    def run(self):
        while True:
            ad_main.AdSocketThread(consts.HOST, consts.PORT).listen()


class AdDaemon(Daemon):
    def run(self):
        startDaemon = StartDaemon()
        startDaemon.run()


if __name__ == '__main__':
    logger = getAdLogger()
    cfg = getConfig()
    daemon = AdDaemon(cfg['FILE_PATH']['path_ad_pid'])

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
