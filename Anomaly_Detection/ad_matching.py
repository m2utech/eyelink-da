# coding: utf-8
# Anomaly detection for Eye-Link using Dinamic Time Wrapping algorithm

# 모듈 및 라이브러리 임포트
import data_convert

from datetime import date
import datetime

import requests
import numpy as np

import learn_utils

from config_parser import cfg

import pandas as pd
import matplotlib.pyplot as plt

WINDOW_LEN = 120
################
def main(node_id, s_date, e_date):

    # 1. Pattern dataset loading
    today = date.today().strftime('%Y%m%d')
    timestamp = date.today().strftime('%Y-%m-%d %H:%M')

    global pattern_data
    pattern_data = data_convert.pattern_data_load(today)
    # 전역변수

    # target data loading
    dataset = data_convert.json_data_load(node_id, s_date, e_date)
    
    if dataset is None:
        print("There is no dataset")
    else:
        dataset = data_preprocess(dataset)
        assign_result = pattern_matching(dataset)
        
        ######## 결과 업로드 #######
        # 블라블라블라~
        ############################

#################
def data_preprocess(dataset):

    dataset = dataset.resample('1T').mean()
    dataset = dataset.reset_index()

    s_timestamp = s_date.replace("T"," ")
    s_timestamp = datetime.datetime.strptime(s_timestamp, '%Y-%m-%d %H:%M:%S')
    
    date_list = [s_timestamp + datetime.timedelta(minutes=x) for x in range(0, WINDOW_LEN)]
    date_list = pd.DataFrame(date_list, columns=['event_time'])

    dataset = date_list.set_index('event_time').join(dataset.set_index('event_time'))

    # process missing value
    dataset.voltage = dataset.voltage.fillna(220)
    dataset.ampere = dataset.ampere.fillna(0.5)
    dataset.active_power = dataset.active_power.fillna(110)
    dataset.power_factor = dataset.power_factor.fillna(0.9)

    dataset = dataset.reset_index(drop=True)

    return dataset

################
def pattern_matching(dataset):

    assign_result = {}

    for col_name in dataset.columns:
        min_dist = float('inf')
        closest_clust = None
        
        test_data = dataset[col_name]
        pattern_df = pd.DataFrame.from_records(pattern_data[col_name])
            
        for clust_name in pattern_df.columns:
            match_data = pattern_df[clust_name]
            cur_dist = DTWDistance(test_data[:110], match_data[:110], 1)
            
            if cur_dist < min_dist:
                #print("min="+ str(min_dist) + ", cur=" + str(cur_dist) + ", cluster=" + str(clust_name))
                min_dist = cur_dist
                closest_clust = clust_name
            #print(col_name + "==> " + closest_clust)
            
        
        #assign_result[col_name] = closest_clust
        assign_result[col_name] = closest_clust

    #print(assign_result)
    #print(min_dist)

    ######### Visualization ##########
    plt.figure(figsize=(20,10))
    i = 1
    ylim = []

    for key, no in assign_result.items():
        if key == 'ampere': ylim = [0,1]
        if key == 'voltage': ylim = [0,240]
        if key == 'active_power': ylim = [0,220]
        if key == 'power_factor': ylim = [0,1]


        ax = plt.subplot(4,1,i)
        ax.set_ylim(ylim)
        plt.plot(dataset[key], label='Original data', c='b')
        plt.plot(pattern_data[key][no], label="matching data", c='r')
        plt.ylabel(key)
        plt.legend(loc=0)
        i+=1

    plt.show()

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
    ##############
    node_id = '0002.00000039'
    s_date = '2017-01-13T11:00:00'
    e_date = '2017-01-13T13:00:00'
    ##############
    main(node_id, s_date, e_date)