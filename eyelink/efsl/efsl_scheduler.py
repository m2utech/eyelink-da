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

ca_daily = config.CA_opt['daily']
ca_weekly = config.CA_opt['weekly']
ca_n_cluster = config.CA_opt['n_cluster']

cp_opt = config.AD_opt['cpSchedule']
pm_opt = config.AD_opt['pmSchedule']
ad_tInterval = config.AD_opt['time_interval']
ad_cid = config.AD_opt['cid']
ad_n_cluster = config.AD_opt['n_cluster']


ca_cid = config.CA_opt['cid']


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
        # self.sched.add_job(self.job_notching_CP, trigger, max_instances=maxInstances, hour=cp_opt['cycle'])
        # self.sched.add_job(self.job_stacking_CP, trigger, max_instances=maxInstances, hour=cp_opt['cycle'])
        # self.sched.add_job(self.job_notching_PM, trigger, max_instances=maxInstances, minute=pm_opt['cycle'])
        # self.sched.add_job(self.job_stacking_PM, trigger, max_instances=maxInstances, minute=pm_opt['cycle'])

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
        logger.debug("== start Daily CA for {} ...".format(product['productName']))
        sDate, eDate = util.getTimeRangeByDay(ca_daily['range'], consts.DATETIMEZERO)
        self.sendData("2000", "corecode", "corecode", sDate, eDate, ca_daily['interval'], ca_n_cluster)

    def job_CA_weekly(self):
        logger.debug("== start Weekly CA for {} ...".format(product['productName']))
        sDate, eDate = util.getTimeRangeByDay(ca_weekly['range'], consts.DATETIMEZERO)
        self.sendData("2000", "corecode", "corecode", sDate, eDate, ca_weekly['interval'], ca_n_cluster)

    # def job_notching_CP(self):
    #     logger.debug("== start CreatePatterns for Notching OEE ==")
    #     sDate, eDate = util.getStartEndDateByHour(cp_opt['range'], False, consts.DATETIMEZERO)
    #     self.sendData("0000", "notching", "oee", sDate, eDate, ad_tInterval, ad_cid, ad_n_cluster)

    # def job_notching_PM(self):
    #     logger.debug("== start PatternMatching for Notching OEE ==")
    #     sDate, eDate = util.getStartEndDateByMinute(pm_opt['range'], False, consts.DATETIMEZERO)
    #     self.sendData("1000", "notching", "oee", sDate, eDate, ad_tInterval, ad_cid, ad_n_cluster)

    # def job_stacking_CP(self):
    #     logger.debug("== start CreatePatterns for Stacking OEE ==")
    #     sDate, eDate = util.getStartEndDateByHour(cp_opt['range'], False, consts.DATETIMEZERO)
    #     self.sendData("0000", "stacking", "oee", sDate, eDate, ad_tInterval, ad_cid, ad_n_cluster)

    # def job_stacking_PM(self):
    #     logger.debug("== start PatternMatching for Stacking OEE ==")
    #     sDate, eDate = util.getStartEndDateByMinute(pm_opt['range'], False, consts.DATETIMEZERO)
    #     self.sendData("1000", "stacking", "oee", sDate, eDate, ad_tInterval, ad_cid, ad_n_cluster)


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
