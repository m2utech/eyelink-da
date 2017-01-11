# coding: utf-8
##### required library #####
import pandas as pd
from pandas import DataFrame
import ujson
import requests
from collections import OrderedDict
import datetime

##### required eyelink modules #####
import elda_extract_data as elda_ed
import ts_cluster
#import elda_read_csv as elda_rc
#import elda_preprocessing as elda_pre
#import elda_parstream_conn as elda_pc

##### test library #####
import matplotlib.pyplot as plt
#import numpy as np
#from pandasql import sqldf

##### 분석 조건 세팅 #####
start_date = '2016-12-07'
end_date = '2016-12-08'
time_interval = '30T'	#15분, W:weekly, D:daily, H:hourly, T:minutely

##### JSON 로드 #####
url = "http://m2utech.eastus.cloudapp.azure.com:5223/dashboard/restapi/getTbRawDataByPeriod?startDate={}&endDate={}".format(start_date,end_date)
resp = requests.get(url)
dataset = ujson.loads(resp.text)

##### 분석할 데이터 속성 추출 #####
dataset = DataFrame(dataset['rtnData'], columns=['node_id', 'event_time', 'voltage', 'ampere', 'active_power', 'power_factor'])

##### 데이터 타입 변환 #####
dataset['voltage'] = dataset['voltage'].convert_objects(convert_numeric=True)
dataset['ampere'] = dataset['ampere'].convert_objects(convert_numeric=True)
dataset['active_power'] = dataset['active_power'].convert_objects(convert_numeric=True)
dataset['power_factor'] = dataset['power_factor'].convert_objects(convert_numeric=True)
dataset['event_time'] = pd.to_datetime(dataset['event_time'], format='%Y-%m-%d %H:%M:%S.%f')

#print(list(dataset.keys()))

################## 피벗 및 클러스터링 ####################
# function (data, index, columns, values, default_value) #
voltage_data = elda_ed.extract_data(dataset, 'event_time', 'node_id', 'voltage', 200, time_interval)
ampere_data = elda_ed.extract_data(dataset, 'event_time', 'node_id', 'ampere', 0.5, time_interval)
active_power_data = elda_ed.extract_data(dataset, 'event_time', 'node_id', 'active_power', 170, time_interval)
power_factor_data = elda_ed.extract_data(dataset, 'event_time', 'node_id', 'power_factor', 0.9, time_interval)

###### 결과 테이블 ######
result_tb = pd.DataFrame()
result_tb['event_time'] = voltage_data.index
result_tb['da_time'] = datetime.datetime.now()

###### time-series format ######
v_ts = {}
a_ts = {}
ap_ts = {}
pf_ts = {}

for i in range(len(voltage_data.columns)):
	v_ts[voltage_data.columns[i]] = voltage_data.ix[:,i]
	a_ts[ampere_data.columns[i]] = ampere_data.ix[:,i]
	ap_ts[active_power_data.columns[i]] = active_power_data.ix[:,i]
	pf_ts[power_factor_data.columns[i]] = power_factor_data.ix[:,i]

##### column list #####
v_col_list = list(voltage_data.columns)
a_col_list = list(ampere_data.columns)
ap_col_list = list(active_power_data.columns)
pf_col_list = list(power_factor_data.columns)

##### Convert dict list for clustering analysis
v_ls = {}
a_ls = {}
ap_ls = {}
pf_ls = {}

for i in range(len(voltage_data.columns)):
	v_ls[str(v_col_list[i])] = v_ts[str(voltage_data.columns[i])].tolist()
	a_ls[str(a_col_list[i])] = a_ts[str(ampere_data.columns[i])].tolist()
	ap_ls[str(ap_col_list[i])] = ap_ts[str(active_power_data.columns[i])].tolist()
	pf_ls[str(pf_col_list[i])] = pf_ts[str(power_factor_data.columns[i])].tolist()

#print(ls.keys())

############# sort list ###############
# from collections import OrderedDict #
v_ls = OrderedDict(sorted(v_ls.items(), key=lambda x:x[1], reverse=True))
a_ls = OrderedDict(sorted(a_ls.items(), key=lambda x:x[1], reverse=True))
ap_ls = OrderedDict(sorted(ap_ls.items(), key=lambda x:x[1], reverse=True))
pf_ls = OrderedDict(sorted(pf_ls.items(), key=lambda x:x[1], reverse=True))


#################### clustering ###################
##### voltage #####
v_centroids = ts_cluster.k_means_clust(v_ls,4,10,4) #data, clus_num, iter, window
v_result_centroids = pd.DataFrame(v_centroids)
v_result_centroids.reset_index(level=0, inplace=True)
v_result_centroids = v_result_centroids.pivot_table(columns = 'index')
result_tb['c0_voltage'] = v_result_centroids.loc[:,0]
result_tb['c1_voltage'] = v_result_centroids.loc[:,1]
result_tb['c2_voltage'] = v_result_centroids.loc[:,2]
result_tb['c3_voltage'] = v_result_centroids.loc[:,3]


##### ampere #####
a_centroids = ts_cluster.k_means_clust(a_ls,4,10,4)
a_result_centroids = pd.DataFrame(a_centroids)
a_result_centroids.reset_index(level=0, inplace=True)
a_result_centroids = a_result_centroids.pivot_table(columns = 'index')
result_tb['c0_ampere'] = a_result_centroids.loc[:,0]
result_tb['c1_ampere'] = a_result_centroids.loc[:,1]
result_tb['c2_ampere'] = a_result_centroids.loc[:,2]
result_tb['c3_ampere'] = a_result_centroids.loc[:,3]

##### active power #####
ap_centroids = ts_cluster.k_means_clust(ap_ls,4,10,4)
ap_result_centroids = pd.DataFrame(ap_centroids)
ap_result_centroids.reset_index(level=0, inplace=True)
ap_result_centroids = ap_result_centroids.pivot_table(columns = 'index')
result_tb['c0_active_power'] = ap_result_centroids.loc[:,0]
result_tb['c1_active_power'] = ap_result_centroids.loc[:,1]
result_tb['c2_active_power'] = ap_result_centroids.loc[:,2]
result_tb['c3_active_power'] = ap_result_centroids.loc[:,3]


##### power factor #####
pf_centroids = ts_cluster.k_means_clust(pf_ls,4,10,4)
pf_result_centroids = pd.DataFrame(pf_centroids)
pf_result_centroids.reset_index(level=0, inplace=True)
pf_result_centroids = pf_result_centroids.pivot_table(columns = 'index')
result_tb['c0_power_factor'] = pf_result_centroids.loc[:,0]
result_tb['c1_power_factor'] = pf_result_centroids.loc[:,1]
result_tb['c2_power_factor'] = pf_result_centroids.loc[:,2]
result_tb['c3_power_factor'] = pf_result_centroids.loc[:,3]

#print(result_tb)

##### save to CSV file #####
today = datetime.datetime.now().strftime('%Y%m%d_%H_%M_%S')
result_tb.to_csv(str(today)+'_result_tb.csv', sep=',', encoding='utf-8', index=False, header=False)

import pdb; pdb.set_trace()  # breakpoint 895c15f6 //

for i in a_centroids:
    plt.plot(i)

plt.legend(a_centroids, prop={'size':5})
plt.show()

"""#####################################
print(ls["0001.00000001"])
#print(ts['0001.00000001'])

ls["0001.00000001"] = ts[str(voltage_data.columns[2])].tolist()

print(ls['test'])

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


plt.legend(prop={'size':5})
plt.show()

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

