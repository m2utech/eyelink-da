# coding: utf-8
# Anomaly detection for Eye-Link using Dinamic Time Wrapping algorithm

# 모듈 및 라이브러리 임포트
import data_convert

#from datetime import date
import datetime
from dateutil.relativedelta import relativedelta

import requests
import numpy as np
#import data_convert
# import learn_utils
from config_parser import cfg
import pandas as pd
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

    print("target data loading ....")
    # target data loading
    dataset = data_convert.json_data_load(node_id, s_time, e_time)
    
    if dataset is None:
        print("There is no dataset")
    else:
        print("data preprocessing ....")
        dataset = data_preprocess(dataset, s_time)
        print("pattern matching ....")
        assign_result = pattern_matching(dataset, pattern_data)

        ######## 결과 업로드 #######
        print("result uploading .......")
        print("save_time: ", e_time)
        print("==============")
        print(assign_result)
        anomaly_pattern_url = cfg['SERVER']['anomaly_pattern_url'] + e_time
        requests.post(anomaly_pattern_url, json=assign_result)
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
def pattern_matching(dataset, pattern_data):

    assign_result = {}

    for col_name in dataset.columns:
        min_dist = float('inf')
        closest_clust = None
        #status = 'Normality'
        
        test_data = dataset[col_name]
        pattern_df = pd.DataFrame.from_records(pattern_data[col_name]['center'])
                
        for clust_name in pattern_df.columns:
            match_data = pattern_df[clust_name]
            cur_dist = DTWDistance(test_data[:110], match_data[:110], 1)
            
            if cur_dist < min_dist:
                #print("min="+ str(min_dist) + ", cur=" + str(cur_dist) + ", cluster=" + str(clust_name))
                min_dist = cur_dist
                closest_clust = clust_name
            #print(col_name + "==> " + closest_clust)
        
    #     if min_dist > 0.7:
    #         status = 'Anomaly'
    #     elif min_dist > 0.3:
    #         status = 'Caution'
    #     else:
    #         status = 'Normality'

        assign_result[col_name] = closest_clust
        #assign_result['{}_status'.format(col_name)] = status
        assign_result['{}_status'.format(col_name)] = min_dist

    #print(assign_result)
    #print(min_dist)
    return assign_result

######### Visualization ##########
# def visualization(dataset, pattern_data, assign_result):
#     plt.figure(figsize=(20,10))
#     i = 1

#     for key, no in assign_result.items():
#         if "_status" in key:
#             pass
#         else:
#             ax = plt.subplot(4,1,i)
            
#             if key == 'ampere': ax.set_ylim([-0.5, 1.2])
#             elif key == 'power_factor': ax.set_ylim([-0.2, 1.2])
#             elif key == 'active_power': ax.set_ylim([-10, 140])
#             else: ax.set_ylim([200, 240])
            
#             plt.plot(dataset[key], label='Original data', c='b')
#             plt.plot(pattern_data[key]['center'][no], label="Prediction pattern", linestyle='dashed', c='r')
#             plt.plot(pattern_data[key]['min_value'][no], label="min-max threshold", c='g', alpha=.3)
#             plt.plot(pattern_data[key]['max_value'][no], c='g', alpha=.3)
#             ax.fill_between(range(120),pattern_data[key]['min_value'][no],pattern_data[key]['max_value'][no], color='green', alpha='0.3')
            
#             plt.ylabel(key)
#             i+=1

#         plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
#     plt.suptitle("{} ~ {}".format(s_time, e_time), fontsize=16)
#     plt.show()
    


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
    # main()