# coding: utf-8
##### required library #####
import pandas as pd
from pandas import DataFrame
import ujson
import json
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
start_date = '2016-12-08'
end_date = '2016-12-09'
time_interval = 15	#15분, W:weekly, D:daily, H:hourly, T:minutely

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
nowtime = datetime.datetime.now()

result_tb = pd.DataFrame()
result_tb['event_time'] = voltage_data.index
result_tb['da_time'] = nowtime
result_tb = result_tb[['da_time','event_time']]

#test = {'da_time': [nowtime]}
#master_tb = pd.DataFrame(test)

#print(master_tb)

master_tb = pd.DataFrame(index=[0])

master_tb['da_time'] = nowtime
master_tb['start_date'] = start_date
master_tb['end_date'] = end_date
master_tb['time_interval'] = time_interval

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
v_centroids, v_assignments = ts_cluster.k_means_clust(v_ls,4,10,4) #data, clus_num, iter, window
## datail result ##
v_result_centroids = pd.DataFrame(v_centroids)
v_result_centroids.reset_index(level=0, inplace=True)
v_result_centroids = v_result_centroids.pivot_table(columns = 'index')
result_tb['c0_voltage'] = v_result_centroids.loc[:,0]
result_tb['c1_voltage'] = v_result_centroids.loc[:,1]
result_tb['c2_voltage'] = v_result_centroids.loc[:,2]
result_tb['c3_voltage'] = v_result_centroids.loc[:,3]
## master result ##
v_assign = ",".join(map(str, list(v_assignments.values())))
v_assign = v_assign.replace(", ",":").replace("'","").replace("[","").replace("]","")
v_assign = v_assign.split(',')
v_assign = pd.DataFrame(v_assign).T
master_tb['c0_voltage'] = v_assign.loc[:,0]
master_tb['c0_voltage'] = v_assign.loc[:,1]
master_tb['c0_voltage'] = v_assign.loc[:,2]
master_tb['c0_voltage'] = v_assign.loc[:,3]


##### ampere #####
a_centroids, a_assignments = ts_cluster.k_means_clust(a_ls,4,10,4)
## datail result ##
a_result_centroids = pd.DataFrame(a_centroids)
a_result_centroids.reset_index(level=0, inplace=True)
a_result_centroids = a_result_centroids.pivot_table(columns = 'index')
result_tb['c0_ampere'] = a_result_centroids.loc[:,0]
result_tb['c1_ampere'] = a_result_centroids.loc[:,1]
result_tb['c2_ampere'] = a_result_centroids.loc[:,2]
result_tb['c3_ampere'] = a_result_centroids.loc[:,3]
## master result ##
a_assign = ",".join(map(str, list(a_assignments.values())))
a_assign = a_assign.replace(", ",":").replace("'","").replace("[","").replace("]","")
a_assign = a_assign.split(',')
a_assign = pd.DataFrame(a_assign).T
master_tb['c0_ampere'] = a_assign.loc[:,0]
master_tb['c0_ampere'] = a_assign.loc[:,1]
master_tb['c0_ampere'] = a_assign.loc[:,2]
master_tb['c0_ampere'] = a_assign.loc[:,3]


##### active power #####
ap_centroids, ap_assignments = ts_cluster.k_means_clust(ap_ls,4,10,4)
## detail result ##
ap_result_centroids = pd.DataFrame(ap_centroids)
ap_result_centroids.reset_index(level=0, inplace=True)
ap_result_centroids = ap_result_centroids.pivot_table(columns = 'index')
result_tb['c0_active_power'] = ap_result_centroids.loc[:,0]
result_tb['c1_active_power'] = ap_result_centroids.loc[:,1]
result_tb['c2_active_power'] = ap_result_centroids.loc[:,2]
result_tb['c3_active_power'] = ap_result_centroids.loc[:,3]
## master result ##
ap_assign = ",".join(map(str, list(ap_assignments.values())))
ap_assign = ap_assign.replace(", ",":").replace("'","").replace("[","").replace("]","")
ap_assign = ap_assign.split(',')
ap_assign = pd.DataFrame(ap_assign).T
master_tb['c0_active_power'] = ap_assign.loc[:,0]
master_tb['c0_active_power'] = ap_assign.loc[:,1]
master_tb['c0_active_power'] = ap_assign.loc[:,2]
master_tb['c0_active_power'] = ap_assign.loc[:,3]


##### power factor #####
pf_centroids, pf_assignments = ts_cluster.k_means_clust(pf_ls,4,10,4)
## detail result ##
pf_result_centroids = pd.DataFrame(pf_centroids)
pf_result_centroids.reset_index(level=0, inplace=True)
pf_result_centroids = pf_result_centroids.pivot_table(columns = 'index')
result_tb['c0_power_factor'] = pf_result_centroids.loc[:,0]
result_tb['c1_power_factor'] = pf_result_centroids.loc[:,1]
result_tb['c2_power_factor'] = pf_result_centroids.loc[:,2]
result_tb['c3_power_factor'] = pf_result_centroids.loc[:,3]
## master result ##
pf_assign = ",".join(map(str, list(pf_assignments.values())))
pf_assign = pf_assign.replace(", ",":").replace("'","").replace("[","").replace("]","")
pf_assign = pf_assign.split(',')
pf_assign = pd.DataFrame(pf_assign).T
master_tb['c0_power_factor'] = pf_assign.loc[:,0]
master_tb['c0_power_factor'] = pf_assign.loc[:,1]
master_tb['c0_power_factor'] = pf_assign.loc[:,2]
master_tb['c0_power_factor'] = pf_assign.loc[:,3]

########### JSON 합치기... ##############
result_json = {}
#result['tb_da_clustering_master'] = master_tb.to_json(orient='values', date_format='iso', date_unit='s')
#result['tb_da_clustering_detail'] = result_tb.to_json(orient='values', date_format='iso', date_unit='s')
#result['tb_da_clustering_master'] = result_tb.to_csv(sep=',', encoding='utf-8', index=False, header=False)

master_json = master_tb.to_json(orient='values', date_format='iso', date_unit='s')
detail_json = result_tb.to_json(orient='values', date_format='iso', date_unit='s')

result_json.tb_da_clustering_master = master_json
result_json.tb_da_clustering_detail = detail_json

print(result_json)

import pdb; pdb.set_trace()  # breakpoint 65ad779e //

#print(json.dumps(result, indent=4))


########### json 저장 ##############
#result_tb.to_json('_tb_da_clustering_detail.json', orient='split', date_format='iso', date_unit='s')
#master_tb.to_json('_tb_da_clustering_master.json', orient='values', date_format='iso', date_unit='s')
####################################

############################
##### save to CSV file #####
today = nowtime.strftime('%Y%m%d%H%M%S')
result_tb.to_csv('tb_da_clustering_detail.'+str(today)+'.csv', sep=',', encoding='utf-8', index=False, header=False)
master_tb.to_csv('tb_da_clustering_master.'+str(today)+'.csv', sep=',', encoding='utf-8', index=False, header=False)


plt.figure(1)

plt.subplot(221)
for i in v_centroids:
    plt.plot(i)
plt.title("Voltage pattern")
#plt.legend(a_centroids, prop={'size':5})

plt.subplot(222)
for i in a_centroids:
    plt.plot(i)
plt.title("Ampere pattern")
#plt.legend(a_centroids, prop={'size':5})

plt.subplot(223)
for i in ap_centroids:
    plt.plot(i)
plt.title("Active power pattern")
#plt.legend(a_centroids, prop={'size':5})

plt.subplot(224)
for i in pf_centroids:
    plt.plot(i)
plt.title("Power factor pattern")
#plt.legend(a_centroids, prop={'size':5})

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

