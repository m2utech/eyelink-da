import sys
import socket
import common_modules
from common.daemon import Daemon
from common.logger import getLogger
from config import efsl_config as config
from consts import consts
from common import util

from apscheduler.schedulers.background import BackgroundScheduler

### logging info ###
log_name = config.logger_name
log_file = config.log_file
pid_file = config.sched_pid_file
log_format = config.log_format
file_size = config.file_max_byte
backup_cnt = config.backup_count
log_level = config.logging_level
product = consts.PRODUCTS['efsl']

### scheduler option
maxInstances = config.sched_opt['max_instances']
trigger = config.sched_opt['trigger']
job_code = config.sched_opt['job_code']
### Cluster Analysis opt
ca_daily = config.CA_opt['daily']
ca_weekly = config.CA_opt['weekly']
ca_n_cluster = config.CA_opt['n_cluster']
### Anomaly Detection opt
ad_cp_sched = config.AD_opt['sched_cp']
ad_pm_sched = config.AD_opt['sched_pm']
ad_tInterval = config.AD_opt['time_interval']
ad_n_cluster = config.AD_opt['n_cluster']


class Scheduler(object):
    def __init__(self):
        self.sched = BackgroundScheduler()
        self.sched.start()

    def __del__(self):  # shutdown all jobs
        self.shutdown()

    def shutdown(self):
        self.sched.shutdown()

    # ##### SCHEDULER #####
    def scheduler(self):
        self.sched.add_job(self.job_runTest, trigger, max_instances=maxInstances, minute='*/10')
        self.sched.add_job(self.job_CA_daily, trigger, max_instances=maxInstances, hour=ca_daily['cycle'])
        self.sched.add_job(self.job_CA_weekly, trigger, max_instances=maxInstances, day_of_week=ca_weekly['cycle'], hour=ca_daily['cycle'])
        self.sched.add_job(self.job_CP, trigger, max_instances=maxInstances, hour=ad_cp_sched['cycle'])
        self.sched.add_job(self.job_PM, trigger, max_instances=maxInstances, minute=ad_pm_sched['cycle'])

    def sendData(self, jobcode, esIndex, docType, sDate, eDate, tInterval, nCluster):
        sendData = {
            "type": job_code[jobcode], "esIndex": esIndex, "docType": docType,
            "sDate": sDate, "eDate": eDate, "tInterval": tInterval, "nCluster": nCluster}
        logger.debug("sendData : {}".format(sendData))
        sendData = str(sendData).encode()
        self.sendMessage(sendData)

    def sendMessage(self, sendData):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((product['host'], product['port']))
        s.send(sendData)
        s.close()

    # ### job function ###
    def job_runTest(self):
        logger.debug("========== scheduler run test ==========")

    def job_CA_daily(self):
        logger.debug("== start Daily Cluster Analysis for {} ...".format(product['productName']))
        sDate, eDate = util.getTimeRangeByDay(ca_daily['range'], consts.DATETIMEZERO)
        self.sendData("2000", "corecode", "corecode", sDate, eDate, ca_daily['interval'], ca_n_cluster)

    def job_CA_weekly(self):
        logger.debug("== start Weekly Cluster Analysis for {} ...".format(product['productName']))
        sDate, eDate = util.getTimeRangeByDay(ca_weekly['range'], consts.DATETIMEZERO)
        self.sendData("2000", "corecode", "corecode", sDate, eDate, ca_weekly['interval'], ca_n_cluster)

    def job_CP(self):
        logger.debug("========== CP test ==========")
        # logger.debug("== start Create Patterns for {} ...".format(product['productName']))
        # sDate, eDate = util.getStartEndDateByHour(ad_cp_sched['range'], False, consts.DATETIMEZERO)
        # self.sendData("0000", "corecode", "corecode", sDate, eDate, ad_tInterval, ad_n_cluster)

    def job_PM(self):
        logger.debug("========== PM test ==========")
        # logger.debug("== start Pattern Matching for {} ...".format(product['productName']))
        # sDate, eDate = util.getStartEndDateByMinute(ad_pm_sched['range'], False, consts.DATETIMEZERO)
        # self.sendData("1000", "corecode", "corecode", sDate, eDate, ad_tInterval, ad_n_cluster)


class SchedulerDaemon(Daemon):
    def run(self):
        scheduler = Scheduler()
        scheduler.scheduler()
        while True:
            pass


if __name__ == '__main__':
    logger = getLogger(log_name, log_file, log_format, file_size, backup_cnt, log_level)
    print(pid_file)
    daemon = SchedulerDaemon(pid_file)

    if len(sys.argv) == 2:
        if "start" == sys.argv[1]:
            logger.info("Started Scheduler daemon for {} ...".format(product['productName']))
            daemon.start()
        elif "stop" == sys.argv[1]:
            logger.info("Stopped Scheduler daemon for {} ...".format(product['productName']))
            daemon.stop()
        elif "restart" == sys.argv[1]:
            logger.info("Restarted scheduler daemon for {} ...".format(product['productName']))
            daemon.restart()
        else:
            print("unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
