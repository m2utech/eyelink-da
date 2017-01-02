# coding: utf-8
### required library ###
import pandas as pd
import pandas.io.sql as pd_sql
from pandas import DataFrame
import datetime as dt
import math

### required eyelink modules ###
import elda_parstream_conn as elda_pc
import elda_extract_data as elda_ed
import elda_read_csv as elda_rc
import elda_preprocessing as elda_pre

### test library ###
import numpy as np
import matplotlib.pyplot as plt

from pandasql import sqldf

import matplotlib.dates as mdates
import time


'''
##### parstream connection using pandas #####
sql = """
SELECT * 
FROM tb_node_raw 
WHERE event_time <= TIMESTAMP'2016-12-13 23:59:59' 
ORDER BY event_time;
"""
targetdata = pd_sql.read_sql(sql,elda_pc.conn,index_col='event_time')
'''

##### csv파일 열기 #####
dataset = elda_rc.read_file()	#read_csvfile module

# 원하는 기간 설정: test 11.18 ~ 11.18
targetdata = dataset
targetdata.index = targetdata.event_time

#st = dt.datetime(2016,11,18,0,0,0)
#en = dt.datetime(2016,12,13,10,30)
#targetdata = targetdata.ix[st:en]

#원하는 데이터 속성 추출 피벗 및 클러스터링 
voltage_data = DataFrame(targetdata, columns=['node_id', 'event_time', 'voltage'])
# function (data, index, columns, values, default_value)
voltage_data = elda_ed.extract_data(voltage_data, 'event_time', 'node_id', 'voltage', 200)

print(len(voltage_data.columns))
ts={}

### divide time series variables
for i in range(len(voltage_data.columns)):
    ts[i] = voltage_data.ix[:,i]
    ts[i].plot()

#plt.legend(prop={'size':5})
#plt.show()



### Calculation of Euclidean distance
def euclid_dist(t1, t2):
    return math.sqrt(sum((t1-t2)**2))

print(euclid_dist(ts[0], ts[1]))


##### Dynamic Time Warping
def DTWDistance(s1, s2):
    DTW = {}
    for i in range(len(s1)):
        DTW[(i, -1)] = np.float('inf')
    for i in range(len(s2)):
        DTW[(-1, i)] = np.float('inf')
    DTW[(-1, -1)] = 0

    for i in range(len(s1)):
        for j in range(len(s2)):
            dist = (s1[i]-s2[j])**2
            DTW[(i, j)] = dist + min(DTW[(i-1, j)], DTW[(i, j-1)], DTW[(i-1, j-1)])
    return math.sqrt(DTW[len(s1)-1, len(s2)-1])

print(DTWDistance(ts[0], ts[1]))

'''
for col_name in voltage_data.columns:
	"ts_"+col_name = voltage_data.ix[:,col_name]
	print("ts_"+col_name)
'''
'''

for  in voltage_data:
	ts{i} = voltage_data.ix[:,i]
	print(ts{i})


ts1 = voltage_data.ix[:,0]
print(ts1)

'''

"""
# 데이터 구간
targetdata = targetdata.ix[targetdata.index.min():targetdata.index.max()]


coord = mdates.date2num(targetdata.index.to_pydatetime())

np.linspace(coord.min(), coord.max(), len(coord))
ts1=pd.Series(targetdata.voltage)

ts1.plot()

plt.ylim(0,250) #y축 min, max
plt.show()
"""
""" # main 내용
ts_ampere = pd.Series(data=ampere_data['0001.00000007'])
ts_ampere.plot()
plt.show()

import pdb; pdb.set_trace()  # breakpoint cbcd1d1d //


ts_x = pd.Series(data=vib_x_data['0001.00000007'])
ts_y = pd.Series(data=vib_y_data['0001.00000007'])
ts_z = pd.Series(data=vib_z_data['0001.00000007'])

ts_x.plot()
ts_y.plot()
ts_z.plot()

plt.show()

# df3.to_csv('test.csv', sep=',', encoding='utf-8')
"""