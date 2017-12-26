import sys
import common_modules

from da_daemon import Daemon
from da_logger import getEfmmLogger
import socket
import da_util as util
import da_consts as consts
import da_config as config

from apscheduler.schedulers.background import BackgroundScheduler

### DA socket server
host = consts.HOST
port = consts.PORT

### scheduler option
maxInstances = config.sched_opt['max_instances']
trigger = config.sched_opt['trigger']
job_code = config.sched_opt['job_code']

cp_opt = config.AD_opt['cpScheduler']
pm_opt = config.AD_opt['pmScheduler']
ad_tInterval = config.AD_opt['time_interval']
ad_cid = config.AD_opt['cid']
ad_n_cluster = config.AD_opt['n_cluster']

ca_daily = config.CA_opt['daily']
ca_weekly = config.CA_opt['weekly']
ca_cid = config.CA_opt['cid']
ca_n_cluster = config.CA_opt['n_cluster']


class Scheduler(object):
    def __init__(self):
        self.sched = BackgroundScheduler()
        self.sched.start()

    def __del__(self):  # shutdown all jobs
        self.shutdown()

    def shutdown(self):
        self.sched.shutdown()

    def job_notching_CP(self):
        logger.debug("== start CreatePatterns for Notching OEE ==")
        sDate, eDate = util.getStartEndDateByHour(cp_opt['range'], False, consts.DATETIMEZERO)
        self.sendData("0000", "notching", "oee", sDate, eDate, ad_tInterval, ad_cid, ad_n_cluster)

    def job_notching_PM(self):
        logger.debug("== start PatternMatching for Notching OEE ==")
        sDate, eDate = util.getStartEndDateByMinute(pm_opt['range'], False, consts.DATETIMEZERO)
        self.sendData("1000", "notching", "oee", sDate, eDate, ad_tInterval, ad_cid, ad_n_cluster)

    def job_stacking_CP(self):
        logger.debug("== start CreatePatterns for Stacking OEE ==")
        sDate, eDate = util.getStartEndDateByHour(cp_opt['range'], False, consts.DATETIMEZERO)
        self.sendData("0000", "stacking", "oee", sDate, eDate, ad_tInterval, ad_cid, ad_n_cluster)

    def job_stacking_PM(self):
        logger.debug("== start PatternMatching for Stacking OEE ==")
        sDate, eDate = util.getStartEndDateByMinute(pm_opt['range'], False, consts.DATETIMEZERO)
        self.sendData("1000", "stacking", "oee", sDate, eDate, ad_tInterval, ad_cid, ad_n_cluster)

    def job_stacking_CA_day(self):
        logger.debug("== start Daily CA for Stacking STATUS ==")
        sDate, eDate = util.getTimeRangeByDay(ca_daily['range'], consts.DATETIMEZERO)
        self.sendData("2000", "stacking", "status", sDate, eDate, ca_daily['interval'], ca_cid, ca_n_cluster)

    def job_stacking_CA_week(self):
        logger.debug("== start Weekly CA for Stacking STATUS ==")
        sDate, eDate = util.getTimeRangeByDay(ca_weekly['range'], consts.DATETIMEZERO)
        self.sendData("2000", "stacking", "status", sDate, eDate, ca_weekly['interval'], ca_cid, ca_n_cluster)

    def sendData(self, jobcode, esIndex, docType, sDate, eDate, tInterval, cid, nCluster):
        sendData = {
            "type": job_code[jobcode],
            "esIndex": esIndex,
            "docType": docType,
            "sDate": sDate,
            "eDate": eDate,
            "tInterval": tInterval,
            "cid": cid,
            "nCluster": nCluster
        }
        logger.debug("sendData == {}".format(sendData))
        sendData = str(sendData).encode()
        self.sendMessage(sendData)

    def sendMessage(self, sendData):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(sendData)
        s.close()

    # ##### SCHEDULER #####
    def scheduler(self):
        self.sched.add_job(self.job_notching_CP, trigger, max_instances=maxInstances, hour=cp_opt['cycle'])
        self.sched.add_job(self.job_stacking_CP, trigger, max_instances=maxInstances, hour=cp_opt['cycle'])
        self.sched.add_job(self.job_notching_PM, trigger, max_instances=maxInstances, minute=pm_opt['cycle'])
        self.sched.add_job(self.job_stacking_PM, trigger, max_instances=maxInstances, minute=pm_opt['cycle'])
        self.sched.add_job(self.job_stacking_CA_day, trigger, max_instances=maxInstances, hour=ca_daily['cycle'])
        self.sched.add_job(self.job_stacking_CA_week, trigger, max_instances=maxInstances, day_of_week=ca_weekly['cycle'], hour=ca_daily['cycle'])


class SchedulerDaemon(Daemon):
    def run(self):
        scheduler = Scheduler()
        scheduler.scheduler()
        while True:
            pass


if __name__ == '__main__':
    logger = getEfmmLogger()
    print(config.file_path["efmm_sche_pid"])
    daemon = SchedulerDaemon(config.file_path["efmm_sche_pid"])

    if len(sys.argv) == 2:
        if "start" == sys.argv[1]:
            logger.info("Started Cluster Analysis Scheduler ...")
            daemon.start()
        elif "stop" == sys.argv[1]:
            logger.info("Stopped Cluster Analysis Scheduler ...")
            daemon.stop()
        elif "restart" == sys.argv[1]:
            logger.info("Restarted Cluster Analysis Scheduler ...")
            daemon.restart()
        else:
            print("unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
