# coding: utf-8
# Anomaly detection for Eye-Link using Dinamic Time Wrapping algorithm

# 모듈 및 라이브러리 임포트
import data_convert
import time
#from datetime import date
import datetime
from dateutil.relativedelta import relativedelta
from socketIO_client import SocketIO

import requests
import numpy as np
#import data_convert
# import learn_utils
from config_parser import cfg
import pandas as pd
import logging

#from sklearn.cluster import KMeans
#import matplotlib.pyplot as plt

node_id = cfg['DA']['node_id']
window_len = int(cfg['DA']['window_len'])
slide_len = int(cfg['DA']['slide_len'])
time_interval = int(cfg['DA']['time_interval'])
v_default = float(cfg['DA']['v_default'])
a_default = float(cfg['DA']['a_default'])
ap_default = float(cfg['DA']['ap_default'])
pf_default = float(cfg['DA']['pf_default'])
n_cluster = int(cfg['DA']['n_cluster'])


logger = logging.getLogger("ad-daemon")

#today = datetime.datetime.today()
#pattern_id = today.strftime('%Y-%m-%d')
#s_time = (today - relativedelta(minutes=110)).strftime('%Y-%m-%dT%H:%M:00')
#save_time = today.strftime('%Y-%m-%dT%H:%M:00')



def main(node_id, s_time, e_time, pattern_data):

    ## Pattern data loading
    #print("pattern data loading ....")

    # 1. Pattern dataset loading
    # 전역변수
#    global pattern_data
    #pattern_data = data_convert.pattern_data_load(pattern_id)

    logger.info("target data loading ....")
    # target data loading
    dataset = data_convert.json_data_load(node_id, s_time, e_time)

    if dataset is None:
        logger.info("There is no dataset")
    else:
        logger.info("data preprocessing ....")
        dataset = data_preprocess(dataset, s_time)
        logger.info("pattern matching start ....")

        assign_result = pattern_matching(dataset, pattern_data, e_time)

        assign_json = {}
        assign_json['analysis'] = assign_result

        #logger.info("assign_result ====> {}".format(assign_result))
        ######## 결과 업로드 #######
        logger.info("result uploading .......")
        #print("==============")
        #print(assign_result)
        #try:
        anomaly_pattern_url = cfg['SERVER']['anomaly_pattern_url'] + e_time
        logger.info("save_info: {}".format(anomaly_pattern_url))
        requests.post(anomaly_pattern_url, json=assign_json)
        #except requests.exceptions.ConnectionError as e:
        #    logger.info(e)
        ############################
        #visualization(dataset,pattern_data,assign_result)

#################
def data_preprocess(dataset, s_time):

    dataset = dataset.resample(str(time_interval)+'T').mean()
    dataset = dataset.reset_index()

    s_timestamp = s_time.replace("T"," ")
    s_timestamp = datetime.datetime.strptime(s_timestamp, '%Y-%m-%d %H:%M:00')

    #base = datetime.datetime.today()
    date_list = [s_timestamp + datetime.timedelta(minutes=x) for x in range(0, window_len-10)]
    date_list = pd.DataFrame(date_list, columns=['event_time'])

    dataset = date_list.set_index('event_time').join(dataset.set_index('event_time'))

    # process missing value
    dataset.voltage = dataset.voltage.fillna(v_default)
    dataset.ampere = dataset.ampere.fillna(a_default)
    dataset.active_power = dataset.active_power.fillna(ap_default)
    dataset.power_factor = dataset.power_factor.fillna(pf_default)

    dataset = dataset.reset_index(drop=True)

    return dataset

################
def pattern_matching(dataset, pattern_data, timestamp):
    # pattern_info loading
    today = datetime.datetime.today()
    today = today.strftime('%Y-%m-%d')
    pattern_info = data_convert.pattern_info_load(today)

    assign_result = {}

    for col_name in dataset.columns:
            
        t1_dist = float('inf')
        t2_dist = float('inf')
        t3_dist = float('inf')
        t1_clust = None
        t2_clust = None
        t3_clust = None
        #status = 'Normality'

        test_data = dataset[col_name]
        pattern_df = pd.DataFrame.from_records(pattern_data[col_name]['center'])

        max_dist = []

        for clust_name in pattern_df.columns:
            match_data = pattern_df[clust_name]
            cur_dist = DTWDistance(test_data[:110], match_data[:110], 1)

            ######## matching rate ########
            max_dist.append(cur_dist)
            ###############################
            if cur_dist < t1_dist:
                t3_dist = t2_dist
                t2_dist = t1_dist
                t1_dist = cur_dist

                t3_clust = t2_clust
                t2_clust = t1_clust
                t1_clust = clust_name

            elif cur_dist < t2_dist:
                t3_dist = t2_dist
                t2_dist = cur_dist
                t3_clust = t2_clust
                t2_clust = clust_name

            elif cur_dist < t3_dist:
                t3_dist = cur_dist
                t3_clust = clust_name
            else:
                continue
        
        # 매칭율
        max_dist = max(max_dist)
        percentile = max_dist / 100.0
        t1_rate = t1_dist / percentile
        t2_rate = t2_dist / percentile
        t3_rate = t3_dist / percentile
        ############################
        assign_result[col_name] = t1_clust
        assign_result['{}_rate'.format(col_name)] = 100.0 - t1_rate
        assign_result['{}_2'.format(col_name)] = t2_clust
        assign_result['{}_2_rate'.format(col_name)] = 100.0 - t2_rate
        assign_result['{}_3'.format(col_name)] = t3_clust
        assign_result['{}_3_rate'.format(col_name)] = 100.0 - t3_rate

        ###### 비교 ######
        lower_df = pd.DataFrame.from_records(pattern_data[col_name]['lower'])[t1_clust][:110]
        upper_df = pd.DataFrame.from_records(pattern_data[col_name]['upper'])[t1_clust][:110]
        min_df = pd.DataFrame.from_records(pattern_data[col_name]['min_value'])[t1_clust][:110]
        max_df = pd.DataFrame.from_records(pattern_data[col_name]['max_value'])[t1_clust][:110]

        anomaly_code = []
        caution_code = []

        for ind in range(len(test_data)):
            if (test_data[ind] >= lower_df[ind]) and (test_data[ind] <= upper_df[ind]):
                anomaly_code.append(-1)
                caution_code.append(-1)
            else:
                if (test_data[ind] <= max_df[ind]) and (test_data[ind] >= min_df[ind]):
                    anomaly_code.append(-1)
                    caution_code.append(test_data[ind])
                else:
                    anomaly_code.append(test_data[ind])
                    caution_code.append(-1)

        ######################
        # 상태정보에 따라 알람 메시지 저장 예정
        ######################
        assign_result['{}_status'.format(col_name)] = pattern_info[col_name][t1_clust]
        ############# 추후에 넣자 #####
        assign_result['{}_anomaly_pt'.format(col_name)] = anomaly_code
        assign_result['{}_caution_pt'.format(col_name)] = caution_code

        if assign_result['{}_status'.format(col_name)] == 'anomaly':
            sendData = {}
            sendData['applicationType'] = 'ELAGENT/DA'
            sendData['agentId'] = ''
            sendData['timestamp'] = timestamp
            sendData['alarmType'] = 'BATCH_ANOMALY'
            sendData['alarmTypeName'] = 'BATCH_ANOMALY'
            sendData['message'] = 'Anomaly expected in {} factor'.format(col_name)

            socketIO = SocketIO('http://m2utech.eastus.cloudapp.azure.com', 5223)
            socketIO.emit('receiveAlarmData', sendData)
        else:
            continue
        
    assign_result['timestamp'] = timestamp

    # print(assign_result)
    # print(min_dist)
    return assign_result


#####################################
## Dinamic Time Wrapping Algorithm ##
#####################################
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
    pass
    # main(node_id, s_time, e_time, pattern_data)