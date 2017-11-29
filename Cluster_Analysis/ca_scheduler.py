import sys
from daemon import Daemon
from ca_logger import getCaLogger
import socket
import consts
import util
from apscheduler.schedulers.background import BackgroundScheduler

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

    def job_day(self):
        logger.info("===== Start cluster analysis for one day =====")
        s_date, e_date = util.getTimeRangeByDay(consts.TIME_RANGE['DAY'], consts.DATETIME)
        sendData = {"s_date": s_date, "e_date": e_date, "tInterval": consts.TIME_INTERVAL['DAY']}
        sendData = str(sendData).encode()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 소켓생성
        s.connect((host, port))
        s.send(sendData)
        s.close()

    def job_week(self):
        logger.info("===== Start cluster analysis for one week =====")
        s_date, e_date = util.getTimeRangeByWeek(consts.TIME_RANGE['WEEK'], consts.DATETIME)
        sendData = {"s_date": s_date, "e_date": e_date, "tInterval": consts.TIME_INTERVAL['WEEK']}
        sendData = str(sendData).encode()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 소켓생성
        s.connect((host, port))
        s.send(sendData)
        s.close()

    def job_month(self):
        logger.info("===== Start cluster analysis for one month =====")
        s_date, e_date = util.getTimeRangeByMonth(consts.TIME_RANGE['MONTH'], consts.DATETIME)
        sendData = {"s_date": s_date, "e_date": e_date, "tInterval": consts.TIME_INTERVAL['MONTH']}
        sendData = str(sendData).encode()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 소켓생성
        s.connect((host, port))
        s.send(sendData)
        s.close()

    def job_test(self):
        logger.info("===== test check 30 minute =====")

    def scheduler(self):
        self.sched.add_job(
            self.job_day, "cron", max_instances=consts.SCHEDULER['MAX_INSTANCE'],
            hour=consts.SCHEDULER['HOUR']
        )
        self.sched.add_job(
            self.job_week, "cron", max_instances=consts.SCHEDULER['MAX_INSTANCE'],
            day_of_week=consts.SCHEDULER['DAY_OF_WEEK']
        )
        self.sched.add_job(
            self.job_month, "cron", max_instances=consts.SCHEDULER['MAX_INSTANCE'],
            day=consts.SCHEDULER['DAY']
        )
        self.sched.add_job(
            self.job_test, "cron", max_instances=consts.SCHEDULER['MAX_INSTANCE'],
            minute=30)


class SchedulerDaemon(Daemon):

    def run(self):
        scheduler = Scheduler()
        scheduler.scheduler()

        while True:
            pass


if __name__ == '__main__':
    logger = getCaLogger()
    print(consts.PATH["SCHE_PID"])
    daemon = SchedulerDaemon(consts.PATH["SCHE_PID"])

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
