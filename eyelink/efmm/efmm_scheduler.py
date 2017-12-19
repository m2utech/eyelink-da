import sys
import common_modules

from da_daemon import Daemon
from da_logger import getEfmmLogger
import socket
import da_util as util
import da_consts as consts
import da_config as config

from apscheduler.schedulers.background import BackgroundScheduler

host = consts.HOST
port = consts.PORT


class Scheduler(object):
    def __init__(self):
        self.sched = BackgroundScheduler()
        self.sched.start()

    def __del__(self):  # shutdown all jobs
        self.shutdown()

    def shutdown(self):
        self.sched.shutdown()

    def job_notchingCreatePattern(self):
        logger.info("== start createPatterns for Notching OEE ==")
        sDate, eDate = util.getStartEndDateByHour(config.scheduler_opt['time_range_pattern'], False, consts.DATETIMEZERO)
        self.sendMessage("0000", "notching", "oee", sDate, eDate)

    def job_stackingCreatePattern(self):
        logger.info("== start createPatterns for Stacking OEE ==")
        sDate, eDate = util.getStartEndDateByHour(config.scheduler_opt['time_range_pattern'], False, consts.DATETIMEZERO)
        self.sendMessage("0000", "stacking", "oee", sDate, eDate)

    def job_notchingPatternMatching(self):
        logger.info("== start patternMatching for Notching OEE ==")
        sDate, eDate = util.getStartEndDateByMinute(config.scheduler_opt['time_range_matching'], False, consts.DATETIMEZERO)
        self.sendMessage("1000", "notching", "oee", sDate, eDate)

    def job_stackingPatternMatching(self):
        logger.info("== start patternMatching for Stacking OEE ==")
        sDate, eDate = util.getStartEndDateByMinute(config.scheduler_opt['time_range_matching'], False, consts.DATETIMEZERO)
        self.sendMessage("1000", "stacking", "oee", sDate, eDate)

    def sendMessage(self, jobcode, esIndex, docType, sDate, eDate):
        sendData = {"type": config.scheduler_opt['job_code'][jobcode], "esIndex": esIndex,
                    "docType": docType, "sDate": sDate, "eDate": eDate}
        sendData = str(sendData).encode()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(sendData)
        s.close()

    def scheduler(self):
        maxInstances = config.scheduler_opt['max_instance']
        hour = config.scheduler_opt['hour']
        minute = config.scheduler_opt['minute']
        self.sched.add_job(self.job_notchingCreatePattern, "cron", max_instances=maxInstances, hour=hour)
        self.sched.add_job(self.job_stackingCreatePattern, "cron", max_instances=maxInstances, hour=hour)
        self.sched.add_job(self.job_notchingPatternMatching, "cron", max_instances=maxInstances, minute=minute)
        self.sched.add_job(self.job_stackingPatternMatching, "cron", max_instances=maxInstances, minute=minute)


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
