import requests
import json
import pandas as pd
import consts


def loadJsonData(sDate, eDate):
    query = "?startDate={}&endDate={}".format(sDate, eDate)
    url = consts.API['LOAD_DATA']
    resp = requests.get(url + query)
    dataset = json.loads(resp.text)
    if dataset['rtnCode']['code'] == '0001':
        dataset = None
    else:
        nodeId = [consts.FACTOR_INFO['NODE_ID']]
        attr = list(consts.FACTOR_INFO['FACTORS'].keys())
        ind = [consts.FACTOR_INFO['INDEX']]
        dataset = pd.DataFrame(dataset['rtnData'], columns=nodeId+attr+ind)
        dataset[ind[0]] = pd.to_datetime(dataset[ind[0]], format='%Y-%m-%d %H:%M:%S.%f')
        for factor in attr:
            dataset[factor] = dataset[factor].apply(pd.to_numeric, errors='ignore')

        dataset = dataset.set_index(ind[0])

    return dataset


def preprocessing(data, col, factor, val, tInterval):
    data = data.pivot_table(index=data.index, columns=col, values=factor)
    data = data.resample(str(tInterval)+'T').mean()
    data = data.fillna(val)
    data = data.reset_index()
    return data


##################
if __name__ == '__main__':
    # pass
    dataset = loadJsonData('2017-11-23T00:00:00', '2017-11-23T01:00:00')
    print(dataset)
