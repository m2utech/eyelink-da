# CLIENT
# coding: utf-8
import common_modules
import da_util as util
import da_config as config
import da_consts as consts
import socket

host = 'm2u-da.eastus.cloudapp.azure.com'
#HOST = 'DataAnalyzer'
port = 5224     # 포트지정


class SchedulerTest(object):
    def __init__(self):
        self.host = host
        self.port = port
    def job_notching_CP(self):
        logger.info("== start CreatePatterns for Notching OEE ==")
        sDate, eDate = util.getStartEndDateByHour(config.scheduler_opt['time_range_pattern'], False, consts.DATETIMEZERO)
        self.sendData("0000", "notching", "oee", sDate, eDate, None)

    def job_notching_PM(self):
        logger.info("== start PatternMatching for Notching OEE ==")
        sDate, eDate = util.getStartEndDateByMinute(config.scheduler_opt['time_range_matching'], False, consts.DATETIMEZERO)
        self.sendData("1000", "notching", "oee", sDate, eDate, None)

    def job_stacking_CP(self):
        logger.info("== start CreatePatterns for Stacking OEE ==")
        sDate, eDate = util.getStartEndDateByHour(config.scheduler_opt['time_range_pattern'], False, consts.DATETIMEZERO)
        self.sendData("0000", "stacking", "oee", sDate, eDate, None)

    def job_stacking_PM(self):
        logger.info("== start PatternMatching for Stacking OEE ==")
        sDate, eDate = util.getStartEndDateByMinute(config.scheduler_opt['time_range_matching'], False, consts.DATETIMEZERO)
        self.sendData("1000", "stacking", "oee", sDate, eDate, None)

    def job_stacking_CA_day(self):
        logger.info("== start Daily CA for Stacking STATUS ==")
        sDate, eDate = util.getTimeRangeByDay(config.clustering_opt['byDay']['range'], consts.DATETIMEZERO)
        print(sDate)
        print(eDate)
        self.sendData("2000", "stacking", "status", sDate, eDate, config.clustering_opt['byDay']['interval'])

    def job_stacking_CA_week(self):
        logger.info("== start Weekly CA for Stacking STATUS ==")
        sDate, eDate = util.getTimeRangeByDay(config.clustering_opt['byWeek']['range'], consts.DATETIMEZERO)
        self.sendData("2000", "stacking", "status", sDate, eDate, config.clustering_opt['byWeek']['interval'])


    def sendData(self, jobcode, esIndex, docType, sDate, eDate, tInterval):
        sendData = ''
        if tInterval is not None:
            sendData = {"type": config.scheduler_opt['job_code'][jobcode], "esIndex": esIndex,
                        "docType": docType, "sDate": sDate, "eDate": eDate, "tInterval": tInterval}
        else:
            sendData = {"type": config.scheduler_opt['job_code'][jobcode], "esIndex": esIndex,
                        "docType": docType, "sDate": sDate, "eDate": eDate}
        sendData = str(sendData).encode()
        print(sendData)

        self.sendMessage(sendData)


    def sendMessage(self, sendData):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(sendData)
        print("send")
        s.close()


        #############################


if __name__ == '__main__':
    from da_logger import getStreamLogger
    logger = getStreamLogger()
    schedulerTest = SchedulerTest()
    schedulerTest.job_stacking_CA_week()
    # job_stackingCreatePattern()