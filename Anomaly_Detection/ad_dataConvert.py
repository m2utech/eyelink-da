import requests
import json
import pandas as pd
# configuration
from ad_configParser import getConfig
cfg = getConfig()

############################
def loadJsonData(node_id, s_date, e_date, cfg):
    
    #nowtime = datetime.datetime.now()
    #nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    ##### load JSON #####
    url = cfg['API']['url_get_train_data'] + "?nodeId={}&startDate={}&endDate={}".format(node_id, s_date, e_date)
    #print(url)

    resp = requests.get(url)
    dataset = json.loads(resp.text)
    #if not dataset['rtnCode']['code'] == '0001':
    if dataset['rtnCode']['code'] == '0001':
        dataset = None
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

def loadPatternInfo(id):
    url = cfg['API']['url_get_pattern_info'] + "?id={}".format(id)
    resp = requests.get(url)
    dataset = json.loads(resp.text)

    if dataset['rtnCode']['code'] == '0001':
        dataset = None
    else:
        dataset = dataset['rtnData']['pattern_info']

    return dataset

############################
def loadPatternData(id):
    url = cfg['API']['url_get_pattern_data'] + id
    resp = requests.get(url)
    dataset = json.loads(resp.text)

    if dataset['rtnCode']['code'] == '0001':
        dataset = None
    else:
        dataset = dataset['rtnData']['pattern_data']

    return dataset

############################

def processResamplingAndMissingValue(dataset, def_val, t_interval, output):
    # 처음-끝 일정사이에 15분 단위로 구분(비어있는 날짜는 자동으로 생성)
    dataset = dataset.resample(str(t_interval)+'T').mean()
    dataset = dataset.fillna(def_val)
    dataset = dataset.reset_index()
    # proc = os.getpid()
    # print('process by process id: {}'.format(proc))
    output.put(dataset)

def extractAttribute(dataset, attr):
    data = dataset[attr]
    return data


###############################################