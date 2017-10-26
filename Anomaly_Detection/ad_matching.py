# coding: utf-8
# Anomaly detection for Eye-Link using Dinamic Time Wrapping algorithm

# 모듈 및 라이브러리 임포트
import ad_dataConvert
# from datetime import date
import datetime
from socketIO_client import SocketIO
import heapq
import consts

import requests
import numpy as np
from ad_configParser import getConfig
import pandas as pd
import logging

from multiprocessing import Process, Queue, freeze_support

logger = logging.getLogger("anomalyDetection")
cfg = getConfig()


def main(node_id, s_time, e_time, master_data):
    logger.debug("target data loading ....")
    # target data loading
    dataset = ad_dataConvert.loadJsonData(node_id, s_time, e_time, cfg)

    if dataset is not None:
        if master_data is not None:
            logger.debug("data preprocessing ....")
            dataset = preprocessData(dataset, s_time, cfg)
            logger.debug("master info data loading...")
            master_info = ad_dataConvert.loadPatternInfo(consts.ATTR_MASTER_ID)
            logger.debug("pattern matching start ....")
            assign_result = patternMatching(dataset, master_data, master_info, e_time, cfg)
            saveMatchingResult(assign_result, e_time, cfg)
        else:
            logger.warning("master data is None ...")
    else:
        logger.warning("There is no dataset for pattern matching")


def saveMatchingResult(assign_result, e_time, cfg):
    assign_json = {}
    assign_json['da_result'] = assign_result

    logger.debug("result uploading .......")

    anomaly_pattern_url = cfg['API']['url_post_anomaly_pattern'] + e_time
    logger.debug("save_info: {}".format(anomaly_pattern_url))
    requests.post(anomaly_pattern_url, json=assign_json)


# ##### 초기 데이터 처리 ######
def preprocessData(dataset, s_time, cfg):

    t_interval = consts.ATTR_TIME_INTERVAL
    window_len = consts.ATTR_WIN_LEN

    dataset = dataset.resample(str(t_interval)+'T').mean()
    dataset = dataset.reset_index()

    s_timestamp = s_time.replace("T", " ")
    s_timestamp = datetime.datetime.strptime(s_timestamp, '%Y-%m-%d %H:%M:00')

    date_list = [s_timestamp + datetime.timedelta(minutes=x) for x in range(0, window_len-10)]
    date_list = pd.DataFrame(date_list, columns=['event_time'])

    dataset = date_list.set_index('event_time').join(dataset.set_index('event_time'))

    for key, factor_name in cfg['FACTORS'].items():
        dataset[factor_name] = dataset[factor_name].fillna(float(cfg['FACTOR_DEFAULT'][key]))

    dataset = dataset.reset_index(drop=True)

    return dataset


################
def patternMatching(dataset, master_data, master_info, timestamp, cfg):
    procs = []
    col_list = []
    output = {}
    logger.debug("start multiprocessing for pattern matching")

    for col_name in dataset.columns:
        output[col_name] = Queue()
        col_list.append(col_name)

        procs.append(Process(target=compareDistance,
            args=(dataset[col_name], master_data[col_name], 
                master_info[col_name], col_name, output[col_name], cfg)))

    for p in procs:
        p.start()

    assign_result = {}

    for col_name in col_list:
        assign_result[col_name] = output[col_name].get()
        output[col_name].close()

        if assign_result[col_name]['status'] == 'anomaly':
            sendData = {}
            sendData['applicationType'] = consts.APP_TYPE
            sendData['agentId'] = consts.AGENT_ID
            sendData['timestamp'] = timestamp
            sendData['alarmType'] = consts.ALARM_TYPE
            sendData['alarmTypeName'] = consts.ALARM_TYPE_NAME
            sendData['message'] = 'Anomaly expected in {} factor'.format(col_name)

            socketIO = SocketIO(cfg['SERVICE']['alarm_host'], int(cfg['SERVICE']['alarm_port']))
            socketIO.emit('receiveAlarmData', sendData)
        else:
            continue

    for proc in procs:
        proc.join()

    assign_result['timestamp'] = timestamp

    return assign_result


def compareDistance(test_data, master_data, master_info, col_name, output, cfg):
    master_center = pd.DataFrame()
    for cno in master_data.keys():
        master_center[cno] = pd.Series(master_data[cno]['center']).values

    logger.debug("compare distance ...")

    distance = {}

    topK = consts.ATTR_TOP_K

    for clust_name in master_center.columns:
        match_data = master_center[clust_name]
        cur_dist = DTWDistance(test_data[:110], match_data[:110], 1)
        distance[clust_name] = cur_dist

    max_dist = heapq.nlargest(1, distance, key=distance.get)
    topK_list = heapq.nsmallest(topK, distance, key=distance.get)

    percentile = float(distance[max_dist[0]]) / 100.0

    result = {}

    for k in range(topK):
        result["top_{}".format(k+1)] = topK_list[k]
        result["top_{}_rate".format(k+1)] = 100.0 - (float(distance[topK_list[k]]) / percentile)

    logger.debug("compare boundary threshould ...")

    master_lower = pd.Series(master_data[topK_list[0]]['lower'][:110])
    master_upper = pd.Series(master_data[topK_list[0]]['upper'][:110])
    master_min = pd.Series(master_data[topK_list[0]]['min_value'][:110])
    master_max = pd.Series(master_data[topK_list[0]]['max_value'][:110])
    # master_lower = pd.DataFrame.from_dict(master_data[topK_list[0]]['lower'][:110])
    # master_upper = pd.DataFrame.from_dict(master_data[topK_list[0]]['upper'][:110])
    # master_min = pd.DataFrame.from_dict(master_data[topK_list[0]]['min_value'][:110])
    # master_max = pd.DataFrame.from_dict(master_data[topK_list[0]]['max_value'][:110])

    anomaly_code = []
    caution_code = []

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


###################################
# Dinamic Time Wrapping Algorithm #
###################################
def DTWDistance(s1, s2, w):

    DTW = {}

    if w:
        w = max(w, abs(len(s1)-len(s2)))

        for i in range(-1, len(s1)):
            for j in range(-1, len(s2)):
                DTW[(i, j)] = float('inf')

    else:
        for i in range(len(s1)):
            DTW[(i, -1)] = float('inf')
        for i in range(len(s2)):
            DTW[(-1, i)] = float('inf')

    DTW[(-1, -1)] = 0

    for i in range(len(s1)):
        if w:
            for j in range(max(0, i-w), min(len(s2), i+w)):
                dist = float((s1[i] - s2[j]))**2
                DTW[(i, j)] = dist + min(DTW[(i-1, j)], DTW[(i, j-1)], DTW[(i-1, j-1)])
        else:
            for j in range(len(s2)):
                dist = (s1[i]-s2[j])**2
                DTW[(i, j)] = dist + min(DTW[(i-1, j)], DTW[(i, j-1)], DTW[(i-1, j-1)])

    return np.sqrt(DTW[len(s1)-1, len(s2)-1])
#####################################


if __name__ == '__main__':
    freeze_support()

    from ad_logger import getAdLogger
    logger = getAdLogger()

    master_id = consts.ATTR_MASTER_ID
    url = cfg['API']['url_get_pattern_data'] + master_id
    resp = requests.get(url)
    import json
    dataset = json.loads(resp.text)

    if dataset['rtnCode']['code'] == '0000':
        logger.debug("reload master pattern")
        master_data = dataset['rtnData']['pattern_data']
    else:
        master_data = None

    main('0002.00000039', '2017-10-10T00:00:00', '2017-10-20T02:00:00', master_data)
    # main(node_id, s_time, e_time, pattern_data)
