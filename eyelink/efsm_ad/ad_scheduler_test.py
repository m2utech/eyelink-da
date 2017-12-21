import sys
from daemon import Daemon
#from ad_configParser import getConfig
#from ad_logger import getSchedulerLogger

#import datetime
#from dateutil.relativedelta import relativedelta

#import socket

#from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.jobstores.base import JobLookupError

# Server infomation for Socket
# cfg = getConfig()
# host = cfg['SERVICE']['host']
# port = int(cfg['SERVICE']['port'])
# node_id = cfg['ATTRIBUTES']['node_id']

# HOST = 'm2u-da.eastus.cloudapp.azure.com'
#logger = logging.getLogger("ad-daemon")
#######################################################
class Scheduler(object):
    def __init__(self):
        self.sched = BackgroundScheduler()
        #self.sched = BlockingScheduler()
        self.sched.start()
        self.job_id=''

    # 클래스가 종료될때, 모든 job들을 종료시켜줍니다.
    def __del__(self):
        self.shutdown()

    # 모든 job들을 종료시켜주는 함수입니다.
    def shutdown(self):
        self.sched.shutdown()

    def job_test(self):
        print("job test~~~ just 10 sec")

    def scheduler(self):
        self.sched.add_job(self.job_test, 'cron', max_instances=5, second='*/10')


class SchedulerDaemon(Daemon):

    def run(self):
        scheduler = Scheduler()
        scheduler.scheduler()

        while True:
            pass


if __name__ == '__main__':
    #logger = getSchedulerLogger()
    daemon = SchedulerDaemon('..\\PID\\ad_scheduler.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            # logger.info("Started Anomaly Detect Scheduler ...")
            daemon.start()
        elif 'stop' == sys.argv[1]:
            # logger.info("Stopped Anomaly Detect Scheduler ...")
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            # logger.info("Restarted Anomaly Detect Scheduler ...")
            daemon.restart()
        else:
            print("unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
