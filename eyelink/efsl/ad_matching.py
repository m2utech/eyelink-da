# coding: utf-8
from socketIO_client import SocketIO
from multiprocessing import Process, Queue, freeze_support
import pandas as pd
import numpy as np
import heapq
import logging

import insertPkgPath
from common import es_api
from common import es_query
from common import converter
from common import learn_utils
from config import efsl_config as config
from consts import consts
from common import util

logger = logging.getLogger(config.logger_name)
DA_INDEX = config.es_index
MASTER_ID = config.AD_opt['masterID']
DataIndex = config.AD_opt['index']
TimeUnit = config.CA_opt['timeUnit']
MV_method = config.mv_method
topK = config.AD_opt['top_k']
match_len = config.AD_opt['match_len']
valRange = config.AD_opt['value_range']
node_id = config.AD_opt['node_id']
factors = config.AD_opt['factors']

### Alarm Info ###
appType = config.alarm_info['AD']['appType']
agentId = config.alarm_info['AD']['agentId']
alarmType = config.alarm_info['AD']['alarmType']
alarmTypeName = config.alarm_info['AD']['alarmTypeName']
alarm_host = config.alarm_info['host']
alarm_port = config.alarm_info['port']


def main(esIndex, docType, sDate, eDate, masterData, tInterval):
    saveID = util.getToday(True, consts.DATETIMEZERO)
    saveID = saveID.replace('Z', '')
    # saveID = eDate
    dataset = getDataset(sDate, eDate, esIndex, docType)
    print(dataset)

    if (dataset is not None) and (not dataset.empty):
        if masterData is not None:
            logger.debug("[AD] Dataset preprocessing ...")
            dataset = preprocessing(dataset, eDate, tInterval)

            logger.debug("[AD] Load pattern info[ID:{}]".format(MASTER_ID))
            query = es_query.getDataById(MASTER_ID)
            masterInfo = es_api.getDataById(
                                    DA_INDEX[esIndex][docType]['PI']['INDEX'],
                                    DA_INDEX[esIndex][docType]['PI']['TYPE'],
                                    query,
                                    MASTER_ID)
            logger.debug("[AD] ### Start pattern matching ...")
            assign_result = patternMatching(dataset, masterData, masterInfo, saveID)
            logger.debug("[AD] Save result of pattern matching ...")
            saveMatchingResult(assign_result, saveID, esIndex, docType)
        else:
            logger.warn("[AD] master data is None ...")
    else:
        logger.warn("[AD] There is no dataset for pattern matching")


def getDataset(sDate, eDate, esIndex, docType):
    idxList = util.getIndexDateList(esIndex + '-', sDate, eDate, consts.DATE)
    print(idxList)
    body = es_query.getCorecodeTargetDataByRange(node_id, sDate, eDate)
    print(body)
    logger.debug("[AD] INDEX : {} | QUERY: {}".format(idxList, body))
    dataset = pd.DataFrame()
    for idx in idxList:
        logger.debug("[CA] get dataset about index [{}]".format(idx))
        data = es_api.getCorecodeData(idx, docType, body, DataIndex)
        dataset = dataset.append(data)
    dataset = dataset.sort_index()
    return dataset


def preprocessing(dataset, eDate, tInterval):
    output, df = {}, {}
    procs = []
    for factor_name in factors:
        output[factor_name] = Queue()
        procs.append(Process(
            target=converter.samplingForPM,
            args=(dataset[factor_name], tInterval, eDate, DataIndex,
                  MV_method, match_len, output[factor_name])))
    for p in procs:
        p.start()
    for factor_name in factors:
        df[factor_name] = output[factor_name].get()
        output[factor_name].close()
    for proc in procs:
        proc.join()
    return df


def patternMatching(dataset, master_data, master_info, saveID):
    procs = []
    output, assign_result = {}, {}
    for col_name in factors:
        output[col_name] = Queue()
        procs.append(Process(
            target=compareDistance,
            args=(dataset[col_name], master_data[col_name],
                  master_info[col_name], col_name, topK,
                  match_len, valRange[col_name], output[col_name])))
    for p in procs:
        p.start()
    for col_name in factors:
        assign_result[col_name] = output[col_name].get()
        output[col_name].close()

        if assign_result[col_name]['status']['status'] == 'anomaly':
            sendData = {}
            sendData['applicationType'] = appType
            sendData['agentId'] = agentId
            sendData['alarmType'] = alarmType
            sendData['alarmTypeName'] = alarmTypeName
            sendData['timestamp'] = saveID
            sendData['message'] = 'Anomaly expected in {} factor'.format(col_name)
            socketIO = SocketIO(alarm_host, alarm_port)
            socketIO.emit('receiveAlarmData', sendData)
            socketIO.wait(seconds=1)

    for proc in procs:
        proc.join()

    assign_result['timestamp'] = saveID
    return assign_result


def compareDistance(test_data, master_data, master_info, col_name, topK, match_len, valRange, output):
    test_data = pd.Series(test_data[col_name].values)
    master_center = pd.DataFrame()
    for cno in master_data.keys():
        master_center[cno] = pd.Series(master_data[cno]['center']).values
    logger.debug("[AD] compare distance between patterns of {} ...".format(col_name))
    # max_clustNo = int(heapq.nlargest(1,master_center.columns)[0].split('_')[1])
    distance = {}

    for clust_name in master_center.columns:
        match_data = master_center[clust_name]
        cur_dist = learn_utils.DTWDistance(test_data.tail(match_len), match_data.head(match_len), 1)
        distance[clust_name] = cur_dist

    topK_list = heapq.nsmallest(topK, distance, key=distance.get)
    percentile = np.sqrt(((valRange[1] - valRange[0])**2)*match_len) / 100.0

    result = {}
    result["realValue"] = test_data.tail(match_len).tolist()

    for k in range(topK):
        result["top_{}".format(k+1)] = topK_list[k]
        result["top_{}_value".format(k+1)] = master_center[topK_list[k]].tolist()
        result["top_{}_rate".format(k+1)] = 100.0 - (float(distance[topK_list[k]]) / percentile)

    logger.debug("[AD] compare boundary threshould of {} ...".format(col_name))

    master_lower = pd.Series(master_data[topK_list[0]]['lower'][:match_len])
    master_upper = pd.Series(master_data[topK_list[0]]['upper'][:match_len])
    master_min = pd.Series(master_data[topK_list[0]]['min_value'][:match_len])
    master_max = pd.Series(master_data[topK_list[0]]['max_value'][:match_len])

    anomaly_code, caution_code = [], []

    for ind in range(len(test_data)):
        if (test_data[ind] >= master_lower[ind]) & (test_data[ind] <= master_upper[ind]):
            anomaly_code.append(-1)
            caution_code.append(-1)
        else:
            if (test_data[ind] <= master_max[ind]) & (test_data[ind] >= master_min[ind]):
                anomaly_code.append(-1)
                caution_code.append(test_data[ind])
            else:
                anomaly_code.append(test_data[ind])
                caution_code.append(-1)

    result["status"] = master_info[topK_list[0]]
    result["anomaly_pt"] = anomaly_code
    result["caution_pt"] = caution_code
    output.put(result)


def saveMatchingResult(assign_result, saveID, esIndex, docType):
    es_api.insertDataById(DA_INDEX[esIndex][docType]['PM']['INDEX'], DA_INDEX[esIndex][docType]['PM']['TYPE'], saveID, assign_result)
    logger.debug("[AD] [ID:{}] was saved successfully".format(saveID))


#############################
if __name__ == '__main__':
    freeze_support()
    from common.logger import getStreamLogger
    logger = getStreamLogger()

    esIndex = 'corecode'
    docType = 'corecode'
    sDate = "2018-04-12T00:00:00Z"
    eDate = "2018-04-12T02:00:00Z"

    masterID = config.AD_opt['masterID']
    query = es_query.getDataById(masterID)
    masterData = es_api.getDataById(DA_INDEX[esIndex][docType]['PD']['INDEX'], DA_INDEX[esIndex][docType]['PD']['TYPE'], query, masterID)
    main(esIndex, docType, sDate, eDate, masterData, 1)
