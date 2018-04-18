import socket
import insertPkgPath
import daemon
import logging
import logging.handlers

from config import efsl_config as config
from consts import consts
from common import util as utils

from apscheduler.schedulers.background import BackgroundScheduler
product = consts.PRODUCTS['efsl']
### logging info ###
LOG = config.log_opt
logger = logging.getLogger(LOG["name"])
formatter = logging.Formatter(LOG["format"])
fileHandler = logging.handlers.RotatingFileHandler(LOG["file"], maxBytes=LOG["fileSize"], backupCount=LOG["backupCnt"])
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.setLevel(logging.getLevelName(LOG["level"]))

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


sched = BackgroundScheduler()

# ##### SCHEDULER #####
def scheduler():
    # sched.add_job(job_runTest, trigger, max_instances=maxInstances, minute='*/5')
    sched.add_job(job_CA_daily, trigger, max_instances=maxInstances, hour=ca_daily['cycle'])
    sched.add_job(job_CA_weekly, trigger, max_instances=maxInstances, day_of_week=ca_weekly['cycle'], hour=ca_daily['cycle'])
    sched.add_job(job_CP, trigger, max_instances=maxInstances, hour=ad_cp_sched['cycle'])
    sched.add_job(job_PM, trigger, max_instances=maxInstances, minute=ad_pm_sched['cycle'])

    context = daemon.DaemonContext()
    log_fileno = fileHandler.stream.fileno()
    context.files_preserve = [log_fileno]
    with context:
        sched.start()
        while True:
            pass

def sendData(jobcode, esIndex, docType, sDate, eDate, tInterval, nCluster):
    sendData = {
        "type": job_code[jobcode], "esIndex": esIndex, "docType": docType,
        "sDate": sDate, "eDate": eDate, "tInterval": tInterval, "nCluster": nCluster}
    logger.debug("sendData : {}".format(sendData))
    sendData = str(sendData).encode()
    sendMessage(sendData)

def sendMessage(sendData):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((product['host'], product['port']))
    s.send(sendData)
    s.close()

# ### job function ###
def job_runTest():
    logger.debug("========== scheduler run test ==========")

def job_CA_daily():
    logger.debug("== start Daily Cluster Analysis for {} ...".format(product['productName']))
    sDate, eDate = utils.getTimeRangeByDay(ca_daily['range'], consts.DATETIMEZERO)
    sendData("2000", "corecode", "corecode", sDate, eDate, ca_daily['interval'], ca_n_cluster)

def job_CA_weekly():
    logger.debug("== start Weekly Cluster Analysis for {} ...".format(product['productName']))
    sDate, eDate = utils.getTimeRangeByDay(ca_weekly['range'], consts.DATETIMEZERO)
    sendData("2000", "corecode", "corecode", sDate, eDate, ca_weekly['interval'], ca_n_cluster)

def job_CP():
    logger.debug("== start Create Patterns for {} ...".format(product['productName']))
    sDate, eDate = utils.getStartEndDateByHour(ad_cp_sched['range'], False, consts.DATETIMEZERO)
    sendData("0000", "corecode", "corecode", sDate, eDate, ad_tInterval, ad_n_cluster)

def job_PM():
    logger.debug("== start Pattern Matching for {} ...".format(product['productName']))
    sDate, eDate = utils.getStartEndDateByMinute(ad_pm_sched['range'], False, consts.DATETIMEZERO)
    print(sDate, eDate)
    sendData("1000", "corecode", "corecode", sDate, eDate, ad_tInterval, ad_n_cluster)


if __name__ == '__main__':
    logger.info("Started Scheduler daemon for {} ...".format(product['productName']))
    scheduler()