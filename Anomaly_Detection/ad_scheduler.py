import sys
from daemon import Daemon
from ad_configParser import getConfig
from ad_logger import getSchedulerLogger
import socket
import consts
import util

from apscheduler.schedulers.background import BackgroundScheduler

# Server infomation for Socket
cfg = getConfig()
host = consts.HOST
port = consts.PORT


class Scheduler(object):
    def __init__(self):
        self.sched = BackgroundScheduler()
        self.sched.start()

    # 클래스가 종료될때, 모든 job들을 종료시켜줍니다.
    def __del__(self):
        self.shutdown()

    # 모든 job들을 종료시켜주는 함수입니다.
    def shutdown(self):
        self.sched.shutdown()

    def job_createPatterns(self):
        logger.debug("Start construction of pattern dataset")
        # local time
        s_date, e_date = util.getStartEndDateByHour(consts.TIME_RANGE['HOUR'], False, consts.DATETIMEZERO)
        sendData = {
            "type": consts.JOB_CODE["0000"],
            "node_id": consts.ATTR_NODE_ID,
            "s_date": s_date,
            "e_date": e_date
            }
        sendData = str(sendData).encode()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 소켓생성
        s.connect((host, port))
        s.send(sendData)
        s.close()

    def job_matchingPatterns(self):
        logger.debug("Start pattern matching")
        # local time
        s_date, e_date = util.getStartEndDateByMinute(consts.TIME_RANGE['MINUTE'], False, consts.DATETIMEZERO)
        sendData = {
            "type": consts.JOB_CODE["1000"],
            "node_id": consts.ATTR_NODE_ID,
            "s_date": s_date,
            "e_date": e_date}
        sendData = str(sendData).encode()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 소켓생성
        s.connect((host, port))
        s.send(sendData)
        s.close()

    def scheduler(self):
        self.sched.add_job(
            self.job_matchingPatterns, "cron",
            max_instances=consts.SCHE_MAX_INSTANCE,
            minute=consts.SCHE_MINUTE
        )
        self.sched.add_job(
            self.job_createPatterns, "cron",
            max_instances=consts.SCHE_MAX_INSTANCE,
            hour=consts.SCHE_HOUR
        )


class SchedulerDaemon(Daemon):

    def run(self):
        scheduler = Scheduler()
        scheduler.scheduler()

        while True:
            pass


if __name__ == "__main__":
    logger = getSchedulerLogger()
    daemon = SchedulerDaemon(cfg["FILE_PATH"]["path_scheduler_pid"])

    if len(sys.argv) == 2:
        if "start" == sys.argv[1]:
            logger.info("Started Anomaly Detect Scheduler ...")
            daemon.start()
        elif "stop" == sys.argv[1]:
            logger.info("Stopped Anomaly Detect Scheduler ...")
            daemon.stop()
        elif "restart" == sys.argv[1]:
            logger.info("Restarted Anomaly Detect Scheduler ...")
            daemon.restart()
        else:
            print("unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
