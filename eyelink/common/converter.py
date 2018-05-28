import pandas as pd
from consts import consts
from config import config
from datetime import datetime
from dateutil.relativedelta import relativedelta

# efsl
def sampling(dataset, tInterval, mv_method, output):
    if isinstance(tInterval, int):
        tInterval = str(tInterval) + 'T'
    dataset = dataset.resample(tInterval).mean()
    dataset = dataset.interpolate(method=mv_method).bfill().ffill()
    output.put(dataset)

### efsl pm
def samplingForPM(dataset, tInterval, eDate, DataIndex, mv_method, match_len, output):
    if isinstance(tInterval, int):
        tInterval = str(tInterval) + 'T'
    dataset = dataset.resample(tInterval).mean()
    dataset = dataset.reset_index()
    timestamp = eDate.replace('T', ' ').replace('Z', '')
    timestamp = datetime.strptime(timestamp, consts.PY_DATETIME)
    date_list = [timestamp - relativedelta(minutes=x) for x in range(0, match_len)]
    date_list = sorted(date_list)
    date_list = pd.DataFrame(date_list, columns=[DataIndex])
    dataset = date_list.set_index(DataIndex).join(dataset.set_index(DataIndex))
    dataset = dataset.interpolate(method=mv_method).bfill().ffill()
    dataset = dataset.reset_index(drop=True)
    output.put(dataset)


def targetSampling(dataset, tInterval, eDate, output):
    ind = config.AD_opt['index']
    dataset = dataset.resample(tInterval).mean()
    dataset = dataset.reset_index()
    timestamp = eDate.replace('T', ' ').replace('Z', '')
    timestamp = datetime.strptime(timestamp, consts.PY_DATETIME)
    date_list = [timestamp - relativedelta(seconds=x*config.AD_opt['range_sec']) for x in range(0, config.AD_opt['match_len'])]
    date_list = sorted(date_list)
    date_list = pd.DataFrame(date_list, columns=[ind])

    dataset = date_list.set_index(ind).join(dataset.set_index(ind))

    for factor_name in config.AD_opt['factors']:
        if factor_name is not 'cid':
            # dataset[factor_name] = dataset[factor_name].fillna(0)
            dataset[factor_name] = dataset[factor_name].interpolate(method=config.mv_method).bfill().ffill()

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
    ind = [config.CA_opt['index']]
    dataset = dateRange.set_index(ind).join(dataset.set_index(ind))
    dataset = dataset.interpolate(method=config.mv_method).bfill().ffill()
    dataset = dataset.reset_index()
    del dataset[config.CA_opt['index']]
    output.put(dataset.T)


# ### For EFSL or all
def efsl_preprocessing(dataset, dateRange, dataId, dataIndex, factor, tInterval, timeUnit, mv_method):
    char = ''
    if timeUnit == 'seconds':
        char = 'S'
    elif timeUnit == 'minutes':
        char = 'T'
    elif timeUnit == 'hours':
        char = 'H'
    dataset = dataset.pivot_table(index=dataset.index, columns=dataId, values=factor)
    dataset = dataset.resample(str(tInterval) + char).mean()
    dataset = dataset.reset_index()
    dataset = dateRange.set_index(dataIndex).join(dataset.set_index(dataIndex))
    dataset = dataset.interpolate(method=mv_method).bfill().ffill()
    dataset = dataset.reset_index()
    del dataset[dataIndex]
    return dataset.T


if __name__ == '__main__':
    cid = 200
    sDate = "2017-12-01T09:00:00"
    eDate = "2017-12-01T13:00:00"

    # loadJsonData(esIndex, cid, sDate, eDate)
