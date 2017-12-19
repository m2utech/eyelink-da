# coding: utf-8
from socketIO_client import SocketIO
from multiprocessing import Process, Queue, freeze_support
import pandas as pd
import numpy as np
import heapq
import logging

import common_modules
import da_elasticsearch as efmm_es
import da_query as efmm_query
import da_converter as efmm_convert
import da_learn_utils as learn_utils

import da_consts as consts
import da_config as config
import da_util as util

DA_INDEX = config.da_index
MASTER_ID = config.da_opt['masterID']
logger = logging.getLogger(config.logger_name['efmm'])


def main(esIndex, docType, sDate, eDate, masterData):
    saveID = eDate
    efmm_index = config.efmm_index[esIndex][docType]['INDEX']
    idxList = util.getIndexDateList(efmm_index+'-', sDate, eDate, consts.DATE)
    body = efmm_query.getOeeDataByRange(sDate, eDate)
    logger.debug("INDEX : {} | QUERY: {}".format(idxList, body))
    dataset = efmm_es.getOeeData(idxList, docType, body)

    if dataset is not None or not dataset.empty:
        if masterData is not None:
            logger.debug("== Dataset preprocessing ...")
            dataset = preprocessing(dataset, eDate)
            logger.debug("== Load pattern info[ID:{}]".format(MASTER_ID))
            query = efmm_query.getDataById(MASTER_ID)
            masterInfo = efmm_es.getDataById(DA_INDEX[esIndex][docType]['PI']['INDEX'], DA_INDEX[esIndex][docType]['PI']['TYPE'], query, MASTER_ID)
            logger.debug("== Start pattern matching ...")
            assign_result = startAnalysis(dataset, masterData, masterInfo, saveID)
            logger.debug("== Save result of pattern matching ...")
            saveMatchingResult(assign_result, saveID, esIndex, docType)
        else:
            logger.warn("master data is None ...")
    else:
        logger.warn("There is no dataset for pattern matching")


def preprocessing(dataset, eDate):
    cid_list = set(dataset['cid'])
    data, output, df = {}, {}, {}
    procs = []
    for cid in cid_list:
        data[cid] = dataset[dataset['cid'] == cid]
        output[cid] = Queue()
        procs.append(Process(target=efmm_convert.targetSampling,
            args=(data[cid], config.da_opt['time_interval'], eDate, output[cid])))
    for p in procs:
        p.start()
    for cid in cid_list:
        df[cid] = output[cid].get()
        output[cid].close()
    for proc in procs:
        proc.join()
    return df


def startAnalysis(dataset, masterData, masterInfo, saveID):
    procs, cid_list = [], []
    resultQ, result = {}, {}
    for cid in dataset.keys():
        resultQ[cid] = Queue()
        cid_list.append(cid)
        procs.append(Process(target=patternMatching,
            args=(dataset[cid], masterData[cid], masterInfo[cid], saveID, resultQ[cid])))
    for p in procs:
        p.start()
    for cid in cid_list:
        result[cid] = resultQ[cid].get()
        resultQ[cid].close()
    for proc in procs:
        proc.join()
    return result


def patternMatching(dataset, master_data, master_info, timestamp, resultQ):
    procs, col_list = [], []
    output, assign_result = {}, {}
    for col_name in dataset.columns:
        output[col_name] = Queue()
        col_list.append(col_name)
        procs.append(Process(target=compareDistance,
            args=(dataset[col_name], master_data[col_name],
                master_info[col_name], col_name, output[col_name])))
    for p in procs:
        p.start()
    for col_name in col_list:
        assign_result[col_name] = output[col_name].get()
        output[col_name].close()

        if assign_result[col_name]['status']['status'] == 'anomaly':
            print("ALARM!!!!!!!")
            sendData = {}
            sendData['applicationType'] = consts.APP_TYPE
            sendData['agentId'] = consts.AGENT_ID
            sendData['timestamp'] = timestamp
            sendData['alarmType'] = consts.ALARM_TYPE
            sendData['alarmTypeName'] = consts.ALARM_TYPE_NAME
            sendData['message'] = 'Anomaly expected in {} factor'.format(col_name)
            socketIO = SocketIO(consts.ALARM_HOST, consts.ALARM_PORT)
            socketIO.emit('receiveAlarmData', sendData)
            print(sendData)
            socketIO.wait(seconds=1)

    for proc in procs:
        proc.join()

    assign_result['timestamp'] = timestamp
    resultQ.put(assign_result)


def compareDistance(test_data, master_data, master_info, col_name, output):
    master_center = pd.DataFrame()
    for cno in master_data.keys():
        master_center[cno] = pd.Series(master_data[cno]['center']).values
    logger.debug("compare distance between patterns of {} ...".format(col_name))
    # max_clustNo = int(heapq.nlargest(1,master_center.columns)[0].split('_')[1])
    distance = {}
    topK = config.da_opt['top_k']
    match_len = config.da_opt['match_len']

    for clust_name in master_center.columns:
        match_data = master_center[clust_name]
        cur_dist = learn_utils.DTWDistance(test_data.tail(match_len), match_data.head(match_len), 1)

        distance[clust_name] = cur_dist

    topK_list = heapq.nsmallest(topK, distance, key=distance.get)
    valRange = config.da_opt['value_range']
    percentile = np.sqrt(((valRange[1] - valRange[0])**2)*match_len) / 100.0

    result = {}
    result["realValue"] = test_data.tail(match_len).tolist()

    for k in range(topK):
        result["top_{}".format(k+1)] = topK_list[k]
        result["top_{}_value".format(k+1)] = master_center[topK_list[k]].tolist()
        result["top_{}_rate".format(k+1)] = 100.0 - (float(distance[topK_list[k]]) / percentile)

    ########### matching rate #############
    # match_rate = 100.0 - (float(distance[topK_list[0]]) / percentile)
    # result = {}
    # result["realValue"] = test_data.tail(match_len).tolist()

    # if match_rate > config.da_opt['match_rate_threshold']:
    #     for k in range(topK):
    #         result["top_{}".format(k+1)] = topK_list[k]
    #         result["top_{}_value".format(k+1)] = master_center[topK_list[k]].tolist()
    #         result["top_{}_rate".format(k+1)] = 100.0 - (float(distance[topK_list[k]]) / percentile)
    # else:
    #     max_clustNo += 1
    #     logger.debug("create new pattern about {} ...".format(col_name))
    #     for k in range(topK):
    #         if k == 0:
    #             result["top_{}".format(k+1)] = "cluster_{:03}".format(max_clustNo)
    #             result["top_{}_value".format(k+1)] = test_data.tolist()
    #             result["top_{}_rate".format(k+1)] = 100.0
    #         else:
    #             result["top_{}".format(k+1)] = topK_list[k-1]
    #             result["top_{}_value".format(k+1)] = master_center[topK_list[k-1]].tolist()
    #             result["top_{}_rate".format(k+1)] = 100.0 - (float(distance[topK_list[k-1]]) / percentile)
    ###########################################


    logger.debug("compare boundary threshould of {} ...".format(col_name))

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
    efmm_es.insertDataById(DA_INDEX[esIndex][docType]['PM']['INDEX'], DA_INDEX[esIndex][docType]['PM']['TYPE'], saveID, assign_result)
    logger.debug("[ID:{}] was saved successfully".format(saveID))


#############################
if __name__ == '__main__':
    freeze_support()
    esIndex = 'notching'
    docType = 'oee'
    sDate = "2017-12-19T01:41:00Z"
    eDate = "2017-12-19T02:41:00Z"
    query = efmm_query.getDataById(config.da_opt['masterID'])
    masterData = efmm_es.getDataById(DA_INDEX[esIndex][docType]['PD']['INDEX'], DA_INDEX[esIndex][docType]['PD']['TYPE'], query, config.da_opt['masterID'])
    main(esIndex, docType, sDate, eDate, masterData)
