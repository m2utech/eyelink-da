import sys
from daemon import Daemon
from ca_logger import getCaLogger
import ca_main
import consts


class Start_daemon(object):
    def run(self):
        while True:
            ca_main.CaSocketThread(consts.HOST, consts.PORT).listen()


class CaDaemon(Daemon):
    def run(self):
        startdaemon = Start_daemon()
        startdaemon.run()


if __name__ == '__main__':
    logger = getCaLogger()
    daemon = CaDaemon(consts.PATH['DAEMON_PID'])

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            logger.info("Started Cluster Analysis daemon ...")
            daemon.start()
        elif 'stop' == sys.argv[1]:
            logger.info("Stopped Cluster Analysis daemon ...")
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            logger.info("Restarted Cluster Analysis daemon ...")
            daemon.restart()
        else:
            print("unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
