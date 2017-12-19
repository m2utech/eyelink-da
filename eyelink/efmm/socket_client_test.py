# CLIENT
# coding: utf-8
import common_modules
import da_util as util
import da_config as config
import da_consts as consts
import socket

HOST = 'm2u-da.eastus.cloudapp.azure.com'
#HOST = 'DataAnalyzer'
PORT=5224 #포트지정

def job_notchingCreatePattern():
    sDate, eDate = util.getStartEndDateByHour(config.scheduler_opt['time_range_pattern'], False, consts.DATETIMEZERO)
    sendMessage("0000", "notching", "oee", sDate, eDate)

def job_stackingCreatePattern():
    sDate, eDate = util.getStartEndDateByHour(config.scheduler_opt['time_range_pattern'], False, consts.DATETIMEZERO)
    sendMessage("0000", "stacking", "oee", sDate, eDate)


def sendMessage(jobcode, esIndex, docType, sDate, eDate):
    sendData = {"type": config.scheduler_opt['job_code'][jobcode], "esIndex": esIndex,
                "docType": docType, "sDate": sDate, "eDate": eDate}
    sendData = str(sendData).encode()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(sendData)
    s.close()


if __name__ == '__main__':
    job_notchingCreatePattern()
    # job_stackingCreatePattern()