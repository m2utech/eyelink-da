#import numpy as np
#import struct
#import matplotlib.pyplot as plt
#import csv
import datetime
import requests
import json
import pandas as pd

# configuration
from config_parser import cfg

############################
def json_data_load(node_id, s_date, e_date):
    
    #nowtime = datetime.datetime.now()
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    ##### load JSON #####
    url = cfg['SERVER']['train_data_url'] + "?nodeId={}&startDate={}&endDate={}".format(node_id, s_date, e_date)
    #print(url)

    resp = requests.get(url)
    dataset = json.loads(resp.text)

    if not dataset['rtnData']:
        dataset = None
        return dataset
        #logger.warning("There is no dataset")
    else:
        attr = ['event_time', 'voltage', 'ampere', 'active_power','power_factor']
        dataset = pd.DataFrame(dataset['rtnData'], columns=attr)
        #dataset = pd.DataFrame(dataset['rtnData'], columns=['event_time', 'voltage'])
        #dataset = pd.DataFrame(dataset['rtnData'])
        dataset['event_time'] = pd.to_datetime(dataset['event_time'], format='%Y-%m-%d %H:%M:%S.%f')
        dataset['voltage'] = dataset['voltage'].apply(pd.to_numeric, errors='ignore')
        dataset['ampere'] = dataset['ampere'].apply(pd.to_numeric, errors='ignore')
        dataset['active_power'] = dataset['active_power'].apply(pd.to_numeric, errors='ignore')
        dataset['power_factor'] = dataset['power_factor'].apply(pd.to_numeric, errors='ignore')
        dataset = dataset.set_index('event_time')  

    return dataset
############################


############################
def pattern_data_load(id):

    ##### load JSON #####
    url = cfg['SERVER']['pattern_dataset_url'] + id
    #print(url)

    resp = requests.get(url)
    dataset = json.loads(resp.text)

    if not dataset['rtnData']:
        print("There is no dataset")
        #logger.warning("There is no dataset")
    else:
        dataset = dataset['rtnData']['pattern_data']
#        dataset = pd.DataFrame.from_records(dataset['rtnData']['pattern_data'])

    return dataset

############################

def resample_missingValue(dataset, def_val, t_interval):
    # 처음-끝 일정사이에 15분 단위로 구분(비어있는 날짜는 자동으로 생성)
    dataset = dataset.resample(str(t_interval)+'T').mean()
    dataset = dataset.fillna(def_val)
    dataset = dataset.reset_index()
    #dataset = dataset[dataset.voltage != 100]
    return dataset


def extract_attribute(dataset, attr):
    data = dataset[attr]
    return data


###############################################