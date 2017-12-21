import pandas as pd
import da_consts as consts
import da_config as config
from datetime import datetime
from dateutil.relativedelta import relativedelta


def sampling(dataset, tInterval, output):
    dataset = dataset.resample(tInterval).mean()
    dataset = dataset.interpolate(method=config.mv_method)
    output.put(dataset)


def targetSampling(dataset, tInterval, eDate, output):
    ind = config.da_opt['index']
    dataset = dataset.resample(tInterval).mean()
    dataset = dataset.reset_index()
    timestamp = eDate.replace('T', ' ').replace('Z', '')
    timestamp = datetime.strptime(timestamp, consts.PY_DATETIME)
    date_list = [timestamp - relativedelta(seconds=x*config.da_opt['range_sec']) for x in range(0, config.da_opt['match_len'])]
    date_list = sorted(date_list)
    date_list = pd.DataFrame(date_list, columns=[ind])

    dataset = date_list.set_index(ind).join(dataset.set_index(ind))

    for factor_name in config.da_opt['factors']:
        if factor_name is not 'cid':
            # dataset[factor_name] = dataset[factor_name].fillna(0)
            dataset[factor_name] = dataset[factor_name].interpolate(method=config.mv_method)

    dataset = dataset.reset_index(drop=True)
    output.put(dataset)

def preprocessClustering(dataset, dateRange, timeUnit, tInterval, output):
    char = ''
    if timeUnit == 'seconds':
        char = 'S'
    elif timeUnit == 'minutes':
        char = 'T'
    elif timeUnit == 'hours':
        char = 'H'
    dataset = dataset.resample(str(tInterval) + char).mean()
    dataset = dataset.reset_index()
    ind = [config.clustering_opt['index']]
    dataset = dateRange.set_index(ind).join(dataset.set_index(ind))
    dataset = dataset.interpolate(method=config.mv_method)
    dataset = dataset.fillna(dataset.mean(), inplace=True)
    dataset = dataset.reset_index()
    del dataset[config.clustering_opt['index']]
    output.put(dataset.T)


if __name__ == '__main__':
    cid = 200
    sDate = "2017-12-01T09:00:00"
    eDate = "2017-12-01T13:00:00"

    # loadJsonData(esIndex, cid, sDate, eDate)
