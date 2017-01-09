# coding: utf-8
### required library ###
import pandas as pd
#import pandas.io.sql as pd_sql
from pandas import DataFrame
#import datetime as dt
#from math import sqrt
import json, requests

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

s_date = '2016-12-11'
e_date = '2016-12-12'

url = "http://m2utech.eastus.cloudapp.azure.com:5223/dashboard/restapi/getTbRawDataByPeriod?startDate={}&endDate={}".format(s_date,e_date)
resp = requests.get(url=url)
rawdata = json.loads(resp.text)

testdata = DataFrame(rawdata['rtnData'])
print(testdata)
import pdb; pdb.set_trace()  # breakpoint 962cdf6a //

#print(list(rawdata.keys()))

#원하는 데이터 속성 추출 피벗 및 클러스터링 
voltage_data = DataFrame(rawdata['rtnData'], columns=['node_id', 'event_time', 'voltage'])
#voltage_data['node_id'] = voltage_data['node_id'].astype(str)
#voltage_data = DataFrame(rawdata, columns=['node_id', 'event_time', 'voltage'])

voltage_data['event_time'] = pd.to_datetime(voltage_data['event_time'], format='%Y-%m-%d %H:%M:%S.%f')
#####################################

##### function (data, index, columns, values, default_value) #####
voltage_data = elda_ed.extract_data(voltage_data, 'event_time', 'node_id', 'voltage', 200)

#print(len(voltage_data.columns)) #number of columns

#voltage_data = voltage_data.T

#voltage_data = voltage_data.values.tolist()


#voltage_data = pd.DataFrame(voltage_data.values)
#voltage_data = voltage_data.unstack()
#print(voltage_data.columns)

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


import ts_cluster

centroids = ts_cluster.k_means_clust(ls,4,100,4)
#centroids = ts_cluster.k_means_clust(list(ls.values()),5,10,4)

for i in centroids:
    plt.plot(i)

plt.show()

"""#####################################

import pdb; pdb.set_trace()  # breakpoint 78eb40fe //

print(ls["0001.00000001"])

#print(ts['0001.00000001'])

import pdb; pdb.set_trace()  # breakpoint 03543948 //


ls["0001.00000001"] = ts[str(voltage_data.columns[2])].tolist()
import pdb; pdb.set_trace()  # breakpoint f8b5cef2 //

print(ls['test'])

import pdb; pdb.set_trace()  # breakpoint 371e9a88 //


for i in range(len(voltage_data.columns)):
	i = 0

print(ts[str(voltage_data.columns[2])])
print(type(ts[str(voltage_data.columns[4])]))

print(ts[str(voltage_data.columns[2])].tolist())
print(type(ts[str(voltage_data.columns[2])].tolist()))



ls = {}
for i in range(len(voltage_data.columns)):
#	ls["{0}".format(i)] = voltage_data.columns[i]
	ls['{}'.format(voltage_data.columns[i])] = i

print(ls) # dict type

ts={}

for i in range(len(voltage_data.columns)):

	ts[voltage_data.columns[i]] = voltage_data.ix[:,i]
	ts[voltage_data.columns[i]].plot()

	#ts[i].plot()
ls = ts['0001.00000001'].tolist()
print(ls)

import pdb; pdb.set_trace()  # breakpoint 744ad164 //

for i in voltage_data.columns:
	df = voltage_data[i].values.tolist()
#	print(voltage_data.index.values)

print(df)


print(voltage_data)

print(type(voltage_data))

print(voltage_data.ix[:,1])
print(voltage_data.columns[2])

######### convert to series data ########
ts={}

for i in range(len(voltage_data.columns)):

	ts[voltage_data.columns[i]] = voltage_data.ix[:,i]
	ts[voltage_data.columns[i]].plot()


print(ts[str(voltage_data.columns[2])])
print(type(ts[str(voltage_data.columns[4])]))

print(ts[str(voltage_data.columns[2])].tolist())
print(type(ts[str(voltage_data.columns[2])].tolist()))

import pdb; pdb.set_trace()  # breakpoint 302f1be0 //

plt.legend(prop={'size':5})
plt.show()
import pdb; pdb.set_trace()  # breakpoint bf6ed4da //

#print(ts)
import ts_cluster

centroids = ts_cluster.k_means_clust(ts,5,10,4)

for i in centroids:
    plt.plot(i)

plt.show()


#ts={}

#for i in range(len(voltage_data.columns)):
#	ts[i] = voltage_data.ix[:,i]
	#ts[i].plot()

#print(ts)
#plt.legend(prop={'size':5})
#plt.show()

#################################################
#################################################


"""

