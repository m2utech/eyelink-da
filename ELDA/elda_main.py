# coding: utf-8
### required library ###
import pandas as pd
import pandas.io.sql as pd_sql
from pandas import DataFrame
import datetime as dt
from math import sqrt
import json

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
rawdata = pd.read_json('C:\\test.json', typ='frame') #typ's default -> frame

#print(rawdata)

#원하는 데이터 속성 추출 피벗 및 클러스터링 
voltage_data = DataFrame(rawdata, columns=['node_id', 'event_time', 'voltage'])

# function (data, index, columns, values, default_value)
voltage_data = elda_ed.extract_data(voltage_data, 'event_time', 'node_id', 'voltage', 200)

#print(len(voltage_data.columns)) #number of columns

#voltage_data = voltage_data.T

#voltage_data = voltage_data.values.tolist()


#voltage_data = pd.DataFrame(voltage_data.values)
voltage_data = voltage_data.unstack()

print(voltage_data)

print(type(voltage_data))

#import ts_cluster

#ts_cluster.k_means_clust(voltage_data,5,10,4)


#ts={}

#for i in range(len(voltage_data.columns)):
#	ts[i] = voltage_data.ix[:,i]
	#ts[i].plot()

#print(ts)
#plt.legend(prop={'size':5})
#plt.show()

#################################################
#################################################




