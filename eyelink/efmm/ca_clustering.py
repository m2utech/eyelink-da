# coding: utf-8
# Cluster Analysis for Eyelink using clustering algorithm

# ### required library ###
from multiprocessing import Process, Queue, freeze_support
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import heapq
import logging
from datetime import datetime

import common_modules
import da_elasticsearch as efmm_es
import da_query as efmm_query
import da_converter as efmm_convert
import da_learn_utils as learn_utils
import da_config as config
import da_consts as consts
import da_util as util

DA_INDEX = config.da_index
logger = logging.getLogger(config.logger_name['efmm'])

def main(esIndex, docType, sDate, eDate, tInterval):
    daTime = util.getToday(True, consts.DATETIME)
    timeUnit = config.clustering_opt['timeUnit']

    logger.debug("create time range by time interval ...")
    dateRange = getDateRange(sDate, eDate, timeUnit, tInterval)
    logger.debug("get trainning dataset by multiprocessing")
    dataset = getDataset(sDate, eDate, esIndex, docType)

    if (dataset is None) or (dataset.empty):
        logger.warn("There is no target dataset... skipping analysis")
    else:
        logger.debug("start cluster analysis by multiprocessing")
        masterDict, detailDict = startAnalysis(dataset, dateRange, timeUnit, tInterval)

        logger.debug("save cluster analysis result ....")
        saveResult(masterDict, detailDict, daTime, dateRange, sDate, eDate, tInterval, esIndex, docType)


def getDateRange(sDate, eDate, timeUnit, tInterval):
    s_dt = datetime.strptime(sDate.replace('T', ' ').replace('Z', ''), consts.PY_DATETIME)
    e_dt = datetime.strptime(eDate.replace('T', ' ').replace('Z', ''), consts.PY_DATETIME)
    dateRange = []
    for dt in util.datetime_range(s_dt, e_dt, {timeUnit: tInterval}):
        dateRange.append(dt)
    dateRange = pd.DataFrame(dateRange, columns=[config.clustering_opt['index']])
    return dateRange


def getDataset(sDate, eDate, esIndex, docType):
    efmm_index = config.efmm_index[esIndex][docType]['INDEX']
    idxList = util.getIndexDateList(efmm_index+'-', sDate, eDate, consts.DATE)
    body = efmm_query.getStatusDataByRange(sDate, eDate)
    procs = []
    dataQ = {}
    dataset = pd.DataFrame()
    for idx in idxList:
        logger.debug("get dataset about index [{}]".format(idx))
        dataQ[idx] = Queue()
        procs.append(Process(target=efmm_es.getStatusData, args=(idx, docType, body, dataQ[idx])))
    for p in procs:
        p.start()

    for idx in idxList:
        dataset = dataset.append(dataQ[idx].get())
        dataQ[idx].close()
    for proc in procs:
        proc.join()
    return dataset


def startAnalysis(dataset, dateRange, timeUnit, tInterval):
    dataset = preprocessing(dataset, dateRange, timeUnit, tInterval)
    procs, cid_list = [], []
    masterQ, detailQ = {}, {}
    masterDict, detailDict = {}, {}

    for cid in dataset.keys():
        logger.debug("Cluster analysis about cid [{}]".format(cid))
        masterQ[cid], detailQ[cid] = Queue(), Queue()
        cid_list.append(cid)
        procs.append(Process(target=clusterAnalysis,
            args=(dataset[cid], masterQ[cid], detailQ[cid])))

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
    logger.debug("=== dataset preprocessing ===")
    cid_list = set(dataset['cid'])
    logger.debug("cid list ==> {}".format(cid_list))
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


def clusterAnalysis(dataset, masterQ, detailQ):
    clusterer = KMeans(config.clustering_opt['n_cluster'])
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
    timeIndex = dateRange[config.clustering_opt['index']].astype(str).tolist()
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

    logger.debug("==== completed cluster analysis [save ID : {}] ====".format(daTime))


if __name__ == '__main__':
    freeze_support()
    from da_logger import getStreamLogger
    logger = getStreamLogger()
    main('stacking', 'status', '2017-12-14T00:00:00Z', '2017-12-21T00:00:00Z', 30)