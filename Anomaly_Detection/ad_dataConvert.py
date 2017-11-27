import requests
import json
import pandas as pd
import consts
# configuration
from ad_configParser import getConfig
cfg = getConfig()

############################
def loadJsonData(node_id, s_date, e_date, cfg):
    query = "?nodeId={}&startDate={}&endDate={}".format(node_id, s_date, e_date)
    url = cfg['API']['url_get_train_data']

    resp = requests.get(url + query)
    dataset = json.loads(resp.text)
    if dataset['rtnCode']['code'] == '0001':
        dataset = None
    else:
        attr = list(consts.FACTOR_INFO['FACTORS'].keys())
        ind = []
        ind.append(consts.FACTOR_INFO['INDEX'])
        dataset = pd.DataFrame(dataset['rtnData'], columns=attr+ind)
        dataset[ind[0]] = pd.to_datetime(dataset[ind[0]], format='%Y-%m-%d %H:%M:%S.%f')
        for factor in attr:
            dataset[factor] = dataset[factor].apply(pd.to_numeric, errors='ignore')

        dataset = dataset.set_index(ind[0])

    return dataset
############################

def loadPatternInfo(id):
    url = cfg['API']['url_get_pattern_info'] + "?id={}".format(id)
    resp = requests.get(url)
    dataset = json.loads(resp.text)

    if dataset['rtnCode']['code'] == '0001':
        dataset = None
    else:
        dataset = dataset['rtnData']

    return dataset

############################
def loadPatternData(id):
    url = cfg['API']['url_get_pattern_data'] + id
    resp = requests.get(url)
    dataset = json.loads(resp.text)

    if dataset['rtnCode']['code'] == '0001':
        dataset = None
    else:
        dataset = dataset['rtnData']

    return dataset


def processResamplingAndMissingValue(dataset, def_val, t_interval, output):
    dataset = dataset.resample(str(t_interval)+'T').mean()
    dataset = dataset.fillna(def_val)
    dataset = dataset.reset_index()
    output.put(dataset)


def extractAttribute(dataset, attr):
    data = dataset[attr]
    return data


if __name__ == "__main__":
    # dataset = loadJsonData('0002.00000039', '2017-10-08T00:00:00Z', '2017-11-07T02:00:00Z', cfg)
    dataset = loadPatternData('master')
    print(dataset)