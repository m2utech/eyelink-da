# coding: utf-8
# Cluster Analysis for Eyelink using clustering algorithm

# ### required library ###
from socketIO_client import SocketIO
from multiprocessing import Process, Queue, freeze_support
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import logging
from datetime import datetime

# import common_modules
from common import es_api
from common import es_query
from common import converter
from config import efsl_config as config
from consts import consts
from common import util

logger = logging.getLogger(config.logger_name)
DA_INDEX = config.es_index
DataId = config.CA_opt['id']
DataIndex = config.CA_opt['index']
TimeUnit = config.CA_opt['timeUnit']
MV_method = config.mv_method


def main(esIndex, docType, sDate, eDate, tInterval, nCluster):
    daTime = utils.getToday(True, consts.DATETIME)
    logger.debug("[CA] create time range by time interval ...")
    dateRange = getDateRange(sDate, eDate, tInterval)
    logger.debug("[CA] get trainning dataset by multiprocessing")
    dataset = getDataset(sDate, eDate, esIndex, docType)

    if dataset.empty:
        logger.warn("[CA] There is no target dataset... skipping analysis")
    else:
        logger.debug("[CA] start cluster analysis by multiprocessing")
        masterDict, detailDict = startAnalysis(dataset, dateRange, tInterval, nCluster)

        logger.debug("[CA] save cluster analysis result ....")
        saveResult(masterDict, detailDict, daTime, dateRange, sDate, eDate, tInterval, esIndex, docType)
        sendAlarm(daTime)


def sendAlarm(daTime):
    logger.debug("[CA] send Alarm message for analysis completion")
    sendData = {}
    sendData['timestamp'] = utils.getToday(True, consts.DATETIME)
    sendData['applicationType'] = config.alarm_info['CA']['appType']
    sendData['agentId'] = config.alarm_info['CA']['agentId']
    sendData['alarmType'] = config.alarm_info['CA']['alarmType']
    sendData['alarmTypeName'] = config.alarm_info['CA']['alarmTypeName']
    sendData['message'] = 'Cluster analysis is completed [requested time: {}]'.format(daTime)
    socketIO = SocketIO(config.alarm_info['host'], config.alarm_info['port'])
    socketIO.emit('receiveAlarmData', sendData)
    socketIO.wait(seconds=1)


def getDateRange(sDate, eDate, tInterval):
    s_dt = datetime.strptime(sDate.replace('T', ' ').replace('Z', ''), consts.PY_DATETIME)
    e_dt = datetime.strptime(eDate.replace('T', ' ').replace('Z', ''), consts.PY_DATETIME)
    dateRange = []
    for dt in utils.datetime_range(s_dt, e_dt, {TimeUnit: tInterval}):
        dateRange.append(dt)
    dateRange = pd.DataFrame(dateRange, columns=[DataIndex])
    return dateRange


def getDataset(sDate, eDate, esIndex, docType):
    idxList = utils.getIndexDateList(esIndex + '-', sDate, eDate, consts.DATE)
    body = es_query.getCorecodeDataByRange(sDate, eDate)
    dataset = pd.DataFrame()
    for idx in idxList:
        logger.debug("[CA] get dataset about index [{}]".format(idx))
        data = es_api.getCorecodeData(idx, docType, body, DataIndex)
        dataset = dataset.append(data)
    dataset = dataset.sort_index()
    return dataset


def startAnalysis(dataset, dateRange, tInterval, nCluster):
    procs, factorList = [], []
    masterQ, detailQ = {}, {}
    masterDict, detailDict = {}, {}

    for factor_name in config.CA_opt['factors']:
        logger.debug("[CA] Cluster analysis about factor [{}]".format(factor_name))
        targetData = dataset[[DataId, factor_name]]
        masterQ[factor_name], detailQ[factor_name] = Queue(), Queue()
        factorList.append(factor_name)

        procs.append(Process(target=clusterAnalysis,
            args=(targetData, dateRange, factor_name, tInterval, nCluster, masterQ[factor_name], detailQ[factor_name])))

    for p in procs:
        p.start()

    for col_name in factorList:
        masterDict[col_name] = masterQ[col_name].get()
        detailDict[col_name] = detailQ[col_name].get()
        masterQ[col_name].close()
        detailQ[col_name].close()
    for proc in procs:
        proc.join()

    return masterDict, detailDict


def clusterAnalysis(dataset, dateRange, factor, tInterval, nCluster, masterQ, detailQ):
    dataset = converter.efsl_preprocessing(dataset, dateRange, DataId, DataIndex, factor, tInterval, TimeUnit, MV_method)
    
    clusterer = KMeans(nCluster)
    learnData = clusterer.fit(dataset)
    clusted_df = pd.DataFrame(learnData.cluster_centers_)
    clusted_df = clusted_df.T

    for i in clusted_df.columns:
        clusted_df = clusted_df.rename(columns={i: "cluster_{:02}".format(i)})

    clusted_df = clusted_df.apply(lambda x: x.astype(float) if np.allclose(x, x.astype(float)) else x)
    clusted_df = clusted_df.round(4)

    labels_df = pd.DataFrame(learnData.labels_)

    assignList, detailList = {}, {}
    for i in clusted_df.columns:
        assignList[i] = []

    for i in labels_df.index:
        cn = labels_df.iloc[i][0]
        assignList["cluster_{:02}".format(cn)].append(dataset.index[i])

    for i in clusted_df.columns:
        detailList[i] = clusted_df[i].tolist()

    masterQ.put(assignList)
    detailQ.put(detailList)


def saveResult(masterDict, detailDict, daTime, dateRange, sDate, eDate, tInterval, esIndex, docType):
    timeIndex = dateRange[DataIndex].astype(str).tolist()
    timeIndex = [dt.replace(' ', 'T') + 'Z' for dt in timeIndex]

    masterDict['da_time'], detailDict['da_time'] = daTime, daTime
    masterDict['start_date'], detailDict['start_date'] = sDate, sDate
    masterDict['end_date'], detailDict['end_date'] = eDate, eDate
    masterDict['time_interval'], detailDict['time_interval'] = tInterval, tInterval
    detailDict['event_time'] = timeIndex

    es_api.insertDataById(DA_INDEX[esIndex][docType]['master']['INDEX'],
        DA_INDEX[esIndex][docType]['master']['TYPE'], daTime, masterDict)
    es_api.insertDataById(DA_INDEX[esIndex][docType]['detail']['INDEX'],
        DA_INDEX[esIndex][docType]['detail']['TYPE'], daTime, detailDict)

    logger.debug("[CA] ### Completed cluster analysis [save ID : {}] ###".format(daTime))


if __name__ == '__main__':
    freeze_support()
    from common.logger import getStreamLogger
    logger = getStreamLogger()
    main('corecode', 'corecode', '2018-01-09T00:00:00Z', '2018-01-10T00:00:00Z', 5, 10)