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

import common_modules
from common import es_api as efmm_es
from common import es_query as efmm_query
from common import converter as efmm_convert
from common import learn_utils
from config import config
from consts import consts
from common import util

DA_INDEX = config.da_index
logger = logging.getLogger(config.logger_name['efmm'])


def main(esIndex, docType, sDate, eDate, tInterval, cid, nCluster):
    daTime = util.getToday(True, consts.DATETIME)
    timeUnit = config.CA_opt['timeUnit']

    logger.debug("[CA] create time range by time interval ...")
    dateRange = getDateRange(sDate, eDate, timeUnit, tInterval)
    logger.debug("[CA] get trainning dataset by multiprocessing")
    dataset = getDataset(sDate, eDate, esIndex, docType, cid)
    dataset = dataset.sort_index()
    
    if dataset.empty:
        logger.warn("[CA] There is no target dataset... skipping analysis")
    else:
        logger.debug("[CA] start cluster analysis by multiprocessing")
        masterDict, detailDict = startAnalysis(dataset, dateRange, timeUnit, tInterval, nCluster)

        logger.debug("[CA] save cluster analysis result ....")
        saveResult(masterDict, detailDict, daTime, dateRange, sDate, eDate, tInterval, esIndex, docType)
        sendAlarm(daTime)


def sendAlarm(daTime):
    logger.debug("[CA] send Alarm message for analysis completion")
    sendData = {}
    sendData['timestamp'] = util.getToday(True, consts.DATETIME)
    sendData['applicationType'] = config.alarm_info['CA']['appType']
    sendData['agentId'] = config.alarm_info['CA']['agentId']
    sendData['alarmType'] = config.alarm_info['CA']['alarmType']
    sendData['alarmTypeName'] = config.alarm_info['CA']['alarmTypeName']
    sendData['message'] = 'Cluster analysis is completed [requested time: {}]'.format(daTime)
    socketIO = SocketIO(config.alarm_info['host'], config.alarm_info['port'])
    socketIO.emit('receiveAlarmData', sendData)
    socketIO.wait(seconds=1)


def getDateRange(sDate, eDate, timeUnit, tInterval):
    s_dt = datetime.strptime(sDate.replace('T', ' ').replace('Z', ''), consts.PY_DATETIME)
    e_dt = datetime.strptime(eDate.replace('T', ' ').replace('Z', ''), consts.PY_DATETIME)
    dateRange = []
    for dt in util.datetime_range(s_dt, e_dt, {timeUnit: tInterval}):
        dateRange.append(dt)
    dateRange = pd.DataFrame(dateRange, columns=[config.CA_opt['index']])
    return dateRange


def getDataset(sDate, eDate, esIndex, docType, cid):
    efmm_index = config.efmm_index[esIndex][docType]['INDEX']
    idxList = util.getIndexDateList(efmm_index+'-', sDate, eDate, consts.DATE)
    body = efmm_query.getStatusDataByRange(sDate, eDate, cid)

    dataset = pd.DataFrame()
    for idx in idxList:
        logger.debug("[CA] get dataset about index [{}]".format(idx))
        data = efmm_es.getStatusData(idx, docType, body)
        dataset = dataset.append(data)
    return dataset

def startAnalysis(dataset, dateRange, timeUnit, tInterval, nCluster):
    dataset = preprocessing(dataset, dateRange, timeUnit, tInterval)
    procs, cid_list = [], []
    masterQ, detailQ = {}, {}
    masterDict, detailDict = {}, {}

    for cid in dataset.keys():
        logger.debug("[CA] Cluster analysis about cid [{}]".format(cid))
        masterQ[cid], detailQ[cid] = Queue(), Queue()
        cid_list.append(cid)
        procs.append(Process(target=clusterAnalysis,
            args=(dataset[cid], nCluster, masterQ[cid], detailQ[cid])))

    for p in procs:
        p.start()

    for cid in cid_list:
        masterDict[cid] = masterQ[cid].get()
        detailDict[cid] = detailQ[cid].get()
        masterQ[cid].close()
        detailQ[cid].close()

    for proc in procs:
        proc.join()

    return masterDict, detailDict


def preprocessing(dataset, dateRange, timeUnit, tInterval):
    logger.debug("[CA] preprocessing for dataset")
    cid_list = set(dataset['cid'])
    logger.debug("[CA] cid list : {}".format(cid_list))
    data, output, df = {}, {}, {}
    procs = []
    for cid in cid_list:
        data[cid] = dataset[dataset['cid'] == cid]
        output[cid] = Queue()
        procs.append(Process(target=efmm_convert.preprocessClustering,
            args=(data[cid], dateRange, timeUnit, tInterval, output[cid])))
    for p in procs:
        p.start()
    for cid in cid_list:
        df[cid] = output[cid].get()
        output[cid].close()
    for proc in procs:
        proc.join()
    return df


def clusterAnalysis(dataset, nCluster, masterQ, detailQ):
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
    timeIndex = dateRange[config.CA_opt['index']].astype(str).tolist()
    timeIndex = [dt.replace(' ', 'T') + 'Z' for dt in timeIndex]

    masterDict['da_time'], detailDict['da_time'] = daTime, daTime
    masterDict['start_date'], detailDict['start_date'] = sDate, sDate
    masterDict['end_date'], detailDict['end_date'] = eDate, eDate
    masterDict['time_interval'], detailDict['time_interval'] = tInterval, tInterval
    detailDict['event_time'] = timeIndex
    efmm_es.insertDataById(DA_INDEX[esIndex][docType]['master']['INDEX'],
        DA_INDEX[esIndex][docType]['master']['TYPE'], daTime, masterDict)
    efmm_es.insertDataById(DA_INDEX[esIndex][docType]['detail']['INDEX'],
        DA_INDEX[esIndex][docType]['detail']['TYPE'], daTime, detailDict)

    logger.debug("[CA] ### Completed cluster analysis [save ID : {}] ###".format(daTime))


if __name__ == '__main__':
    freeze_support()
    from common.logger import getStreamLogger
    logger = getStreamLogger()
    print(config.test)
    # main('stacking', 'status', '2017-12-24T23:50:00Z', '2017-12-25T00:00:00Z', 1, 'all', 5)