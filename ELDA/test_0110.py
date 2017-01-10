# coding: utf-8
### required library ###
import pandas as pd
#import pandas.io.sql as pd_sql
from pandas import DataFrame
import ujson, requests

### required eyelink modules ###
#import elda_parstream_conn as elda_pc
import elda_extract_data as elda_ed
#import elda_read_csv as elda_rc
import elda_preprocessing as elda_pre


### test library ###
import numpy as np
import matplotlib.pyplot as plt

from pandasql import sqldf

###### load json ######
#rawdata = pd.read_json('C:\\test.json', typ='series') #series형태로 로드시
#rawdata = pd.read_json('C:\\test.json') #typ's default -> frame

s_date = '2016-11-16'
e_date = '2016-11-18'

url = "http://m2utech.eastus.cloudapp.azure.com:5223/dashboard/restapi/getTbRawDataByPeriod?startDate={}&endDate={}".format(s_date,e_date)
resp = requests.get(url)
dataset = ujson.loads(resp.text)

##### 원하는 데이터 속성 추출 #####
dataset = DataFrame(dataset['rtnData'], columns=['node_id', 'event_time', 'voltage', 'ampere', 'active_power', 'power_factor'])
#voltage_data['node_id'] = voltage_data['node_id'].astype(str)
#voltage_data = DataFrame(rawdata, columns=['node_id', 'event_time', 'voltage'])

##### 데이터 타입 변환 #####
dataset['voltage'] = dataset['voltage'].convert_objects(convert_numeric=True)
dataset['ampere'] = dataset['ampere'].convert_objects(convert_numeric=True)
dataset['active_power'] = dataset['active_power'].convert_objects(convert_numeric=True)
dataset['power_factor'] = dataset['power_factor'].convert_objects(convert_numeric=True)
dataset['event_time'] = pd.to_datetime(dataset['event_time'], format='%Y-%m-%d %H:%M:%S.%f')

#print(dataset.info())

#print(list(dataset.keys()))

###### 피벗 및 클러스터링 ###############################

##### function (data, index, columns, values, default_value) #####
voltage_data = elda_ed.extract_data(dataset, 'event_time', 'node_id', 'voltage', 200)
ampere_data = elda_ed.extract_data(dataset, 'event_time', 'node_id', 'ampere', 0.5)
active_power_data = elda_ed.extract_data(dataset, 'event_time', 'node_id', 'active_power', 170)
power_factor_data = elda_ed.extract_data(dataset, 'event_time', 'node_id', 'power_factor', 0.9)

ts={}

for i in range(len(voltage_data.columns)):
	ts[voltage_data.columns[i]] = voltage_data.ix[:,i]
	#ts[voltage_data.columns[i]].plot()

#plt.legend(prop={'size':5})
#plt.show()
#ls=[]
col_list = list(voltage_data.columns)
#print(col_list)

ls={}
for i in range(len(voltage_data.columns)):
	ls[str(col_list[i])] = ts[str(voltage_data.columns[i])].tolist()


#print(ls.keys())

from collections import OrderedDict
ls = OrderedDict(sorted(ls.items(), key=lambda x:x[1], reverse=True))
#print("--------------")
#print(ls['0001.00000001'])