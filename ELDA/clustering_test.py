# coding: utf-8
### required library ###
import pandas as pd
import pandas.io.sql as pd_sql
from pandas import DataFrame
import datetime as dt

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

targetdata = targetdata.ix[targetdata.index.min():targetdata.index.max()]

''' ###### 1229일 테스트 예정 #####
targetdata.index = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
print(targetdata.index)

np.linspace(targetdata.index.min(), targetdata.index.max(), len(targetdata.index))

ts1=pd.Series(targetdata.voltage)
ts2=pd.Series(2.2*np.sin(x/3.5+2.4)+3.2)
ts3=pd.Series(0.04*x+3.0)

ts1.plot()
ts2.plot()
ts3.plot()

plt.ylim(-2,10)
plt.legend(['ts1','ts2','ts3'])
plt.show()
'''