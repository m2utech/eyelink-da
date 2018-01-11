import sys
import common_modules
from common.daemon import Daemon
from common.logger import getLogger
from config import efsl_config as config
from consts import consts
import efsl_main

log_name = config.logger_name
log_file = config.log_file
pid_file = config.pid_file
log_format = config.log_format
file_size = config.file_max_byte
backup_cnt = config.backup_count
log_level = config.logging_level
product = consts.PRODUCTS['efsl']


class StartDaemon(object):
    def run(self):
        while True:
            efsl_main.SocketThread(product['host'], product['port']).listen()


class LoadDaemon(Daemon):
    def run(self):
        startDaemon = StartDaemon()
        startDaemon.run()


if __name__ == '__main__':
    logger = getLogger(log_name, log_file, log_format, file_size, backup_cnt, log_level)
    print(pid_file)
    daemon = LoadDaemon(pid_file)

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            logger.info("Started daemon for {} ...".format(product['productName']))
            daemon.start()
        elif 'stop' == sys.argv[1]:
            logger.info("Stopped daemon for {} ...".format(product['productName']))
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            logger.info("Restarted daemon for {} ...".format(product['productName']))
            daemon.restart()
        else:
            print("unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
