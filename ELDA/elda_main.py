# coding: utf-8
import pandas as pd
import pandas.io.sql as pd_sql
from pandas import DataFrame

import numpy as np
import matplotlib.pyplot as plt

import datetime as dt

from pandasql import sqldf

# eyelink modules
import elda_parstream_conn as elda_pc
import elda_read_csv as elda_rc
import elda_preprocessing as elda_pre
import elda_extract_data as elda_ed

"""
##### Connection 클래스 이용  (datatype으로 인해 pandas 대체) #####
cur = elda_pc.conn.cursor()
sql = "SELECT event_type, als_level, dimming_level FROM tb_node_raw where event_time = '2016-11-30 22:31:12'"
cur.execute(sql)
result = cur.fetchall()
"""
""" ##### pandas 이용 #####
sql = "SELECT event_time, voltage FROM tb_node_raw where event_type = 1"
pd_sql.execute(sql,elda_pc.conn)
data = pd_sql.read_sql(sql,elda_pc.conn)

df_list = data.values.tolist()
print(data)
"""

#------------ 20161226------------------#
##### csv파일 열기 #####
dataset = elda_rc.read_file()	#read_csvfile module


# 원하는 기간 설정: test 11.18 ~ 11.18
targetdata = dataset
targetdata.index = targetdata.event_time

st = dt.datetime(2016,11,18,0,0,0)
en = dt.datetime(2016,12,13,10,30)
targetdata = targetdata.ix[st:en]


#원하는 데이터 속성 추출 피벗 및 클러스터링 
voltage_data = DataFrame(targetdata, columns=['node_id', 'event_time', 'voltage'])
ampere_data = DataFrame(targetdata, columns=['node_id', 'event_time', 'ampere'])
vib_x_data = DataFrame(targetdata, columns=['node_id', 'event_time', 'vibration_x'])
vib_y_data = DataFrame(targetdata, columns=['node_id', 'event_time', 'vibration_y'])
vib_z_data = DataFrame(targetdata, columns=['node_id', 'event_time', 'vibration_z'])

# fun(data, index, columns, values, default_value)
voltage_data = elda_ed.extract_data(voltage_data, 'event_time', 'node_id', 'voltage', 200)
ampere_data = elda_ed.extract_data(ampere_data, 'event_time', 'node_id', 'ampere', 0)
vib_x_data = elda_ed.extract_data(vib_x_data, 'event_time', 'node_id', 'vibration_x', 0)
vib_y_data = elda_ed.extract_data(vib_y_data, 'event_time', 'node_id', 'vibration_y', 0)
vib_z_data = elda_ed.extract_data(vib_z_data, 'event_time', 'node_id', 'vibration_z', 0)



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
