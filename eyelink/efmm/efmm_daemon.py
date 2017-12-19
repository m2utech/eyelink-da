import sys
import common_modules

from da_daemon import Daemon
from da_logger import getEfmmLogger
import da_config as config
import da_consts as consts
import efmm_main


class StartDaemon(object):
    def run(self):
        while True:
            efmm_main.EfmmSocketThread(consts.HOST, consts.PORT).listen()


class EfmmDaemon(Daemon):
    def run(self):
        startDaemon = StartDaemon()
        startDaemon.run()


if __name__ == '__main__':
    logger = getEfmmLogger()
    print(config.file_path['efmm_pid'])
    daemon = EfmmDaemon(config.file_path['efmm_pid'])

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
