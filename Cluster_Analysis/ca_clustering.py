# coding: utf-8
# Cluster Analysis for Eyelink using clustering algorithm

# ### required library ###
from multiprocessing import Process, Queue, freeze_support
from sklearn.cluster import KMeans
import pandas as pd
import requests
import logging
from datetime import datetime, timedelta
# ### import module ###
import consts
import ca_dataConvert
import util

logger = logging.getLogger(consts.LOGGER_NAME['CA'])


def main(sDate, eDate, tInterval):
    nowtime = util.getToday(True, consts.DATETIME)
    sDate = util.checkDatetime(sDate, consts.DATETIME)
    eDate = util.checkDatetime(eDate, consts.DATETIME)
    # print(nowtime, sDate, eDate)

    s_dt = datetime.strptime(sDate.replace('T', ' ').replace('Z', ''), consts.LOCAL_ZERO_TIME)
    e_dt = datetime.strptime(eDate.replace('T', ' ').replace('Z', ''), consts.LOCAL_ZERO_TIME)
    dateRange = []
    for dt in util.datetime_range(s_dt, e_dt, {'minutes': tInterval}):
        dateRange.append(dt)
    dateRange = pd.DataFrame(dateRange, columns=[consts.FACTOR_INFO["INDEX"]])


    logger.debug("trainnig dataset loading ....")
    dataset = ca_dataConvert.loadJsonData(sDate, eDate)
    logger.debug("Clustering by multiprocessing ....")
    procs, factorList = [], []
    indexQ, masterQ, detailQ = {}, {}, {}
    nodeId = consts.FACTOR_INFO['NODE_ID']

    for factor_name, val in consts.FACTOR_INFO['FACTORS'].items():
        targetData = dataset[[nodeId, factor_name]]
        indexQ[factor_name], masterQ[factor_name], detailQ[factor_name] = Queue(), Queue(), Queue()
        factorList.append(factor_name)

        procs.append(Process(target=clusterAnalysis,
            args=(dateRange, targetData, nodeId, factor_name, val, tInterval, masterQ[factor_name], detailQ[factor_name], indexQ[factor_name])))

    for p in procs:
        p.start()

    masterDict, detailDict = {}, {}
    timeIndex = []
    for col_name in factorList:
        masterDict.update(masterQ[col_name].get())
        detailDict.update(detailQ[col_name].get())
        timeIndex = indexQ[col_name].get()
        masterQ[col_name].close()
        detailQ[col_name].close()
        indexQ[col_name].close()
    for proc in procs:
        proc.join()

    timeIndex = [dt.replace(' ', 'T') + 'Z' for dt in timeIndex]

    masterDict['da_time'], detailDict['da_time'] = nowtime, nowtime
    masterDict['start_date'], detailDict['start_date'] = sDate, sDate
    masterDict['end_date'], detailDict['end_date'] = eDate, eDate
    masterDict['time_interval'], detailDict['time_interval'] = tInterval, tInterval
    detailDict['event_time'] = timeIndex
    logger.debug("save clustering result ....")

    saveResult(masterDict, detailDict, nowtime)
    logger.debug("==== completed cluster analysis [save ID : {}] ====".format(nowtime))


def saveResult(masterDict, detailDict, saveId):
    masterJson, detailJson = {}, {}
    masterJson['master_result'] = masterDict
    detailJson['detail_result'] = detailDict

    # print(masterDict)
    # print(detailDict)
    masterApi = consts.API['UPLOAD_MASTER'] + saveId
    detailApi = consts.API['UPLOAD_DETAIL'] + saveId

    requests.post(masterApi, json=masterJson)
    requests.post(detailApi, json=detailJson)


def clusterAnalysis(dateRange, dataset, nodeId, factor, val, tInterval, masterQ, detailQ, indexQ):
    dataset = ca_dataConvert.preprocessing(dateRange, dataset, nodeId, factor, val, tInterval)
    # dataset = dataset.reset_index()
    # dataset = dataset.set_index('node_id')
    timeIndex = dataset[consts.FACTOR_INFO['INDEX']].astype(str).tolist()
    del dataset[consts.FACTOR_INFO['INDEX']]
    dataset = dataset.T

    clusterer = KMeans(consts.FACTOR_INFO['N_CLUSTER'])
    learnData = clusterer.fit(dataset)
    centers_df = pd.DataFrame(learnData.cluster_centers_)
    centers_df = centers_df.T

    for i in centers_df.columns:
        centers_df = centers_df.rename(columns={i: "cluster_{:02}".format(i)})

    labels_df = pd.DataFrame(learnData.labels_)

    assignList, detailList = {}, {}
    assignList[factor], detailList[factor] = {}, {}
    for i in centers_df.columns:
        assignList[factor][i] = []

    for i in labels_df.index:
        cn = labels_df.iloc[i][0]
        assignList[factor]["cluster_{:02}".format(cn)].append(dataset.index[i])

    for i in centers_df.columns:
        detailList[factor][i] = centers_df[i].tolist()

    masterQ.put(assignList)
    detailQ.put(detailList)
    indexQ.put(timeIndex)


####################################
if __name__ == '__main__':
    freeze_support()
    main('2017-11-28T00:00:00', '2017-11-29T00:00:00', 30)
