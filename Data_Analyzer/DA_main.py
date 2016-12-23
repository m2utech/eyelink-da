# coding: utf-8
import pandas as pd
import pandas.io.sql as pd_sql
from pandas import DataFrame

import numpy as np
import matplotlib.pyplot as plt
# Parstream_conn.py
import Parstream_conn as pc

"""
# Connection 클래스 이용  (datatype으로 인해 pandas 대체)
cur = pc.conn.cursor()
sql = "SELECT event_type, als_level, dimming_level FROM tb_node_raw where event_time = '2016-11-30 22:31:12'"
cur.execute(sql)
result = cur.fetchall()
"""
"""
# pandas 이용
sql = "SELECT event_time, voltage FROM tb_node_raw where event_type = 1"
pd_sql.execute(sql,pc.conn)
data = pd_sql.read_sql(sql,pc.conn)

df_list = data.values.tolist()
print(data)
"""
"""
# csv파일 열기
df = pd.read_csv("../data/NODE_RAW_1215_ET_1.csv", parse_dates=[2,3])

#원하는 데이터 속성만 뽑을때
#df = DataFrame(df, columns=['NODE_ID','EVENT_TIME','VOLTAGE'])

# 파스트림 연동시를 위해 소문자로..
df.rename(columns = {'NODE_ID' : 'node_id'}, inplace = True)
df.rename(columns = {'EVENT_TYPE' : 'event_type'}, inplace = True)
df.rename(columns = {'MEASURE_TIME' : 'measure_time'}, inplace = True)
df.rename(columns = {'EVENT_TIME' : 'event_time'}, inplace = True)
df.rename(columns = {'VOLTAGE' : 'voltage'}, inplace = True)
df.rename(columns = {'AMPERE' : 'ampere'}, inplace = True)
df.rename(columns = {'POWER_FACTOR' : 'power_factor'}, inplace = True)
df.rename(columns = {'ACTIVE_POWER' : 'active_power'}, inplace = True)
df.rename(columns = {'REACTIVE_POWER' : 'reactive_power'}, inplace = True)
df.rename(columns = {'APPARENT_POWER' : 'apparent_power'}, inplace = True)
df.rename(columns = {'AMOUNT_OF_ACTIVE_POWER' : 'amount_of_active_power'}, inplace = True)

print(df.columns.tolist()) #컬럼 데이터타입 확인
"""




#days = data['EVENT_TIME']
#print(days[0:2])
#data = data.T
#print(data)


#plt.plot_date(x=df['event_time'],y=df['voltage'])
'''
df = df.T 	#행렬 전치(transpose)
print(df)
print(df.axes)
#df.info()
#
'''
#data = pd.read_csv("NODE_RAW_1215_ET_1.csv", parse_dates=[2,3])


data = pd.read_csv("../data/NODE_RAW_1215_ET_1.csv", parse_dates=[2,3])

#print(data['NODE_ID'])
df = pd.DataFrame(data)

print(df.columns.tolist()) #컬럼 데이터타입 확인

#data = pd.read_excel("NODE_RAW_1213_ET_1.xlsx", index_col=0)
#df[' EVENT_TIME'] = df[' EVENT_TIME'].dt.date   # key error !!
#print(df[' EVENT_TIME'])
df.info()

#df['EVENT_TIME'].date_time.map(lambda x: x.strftime('%Y-%m-%d'))

#print(df['VOLTAGE'])
#print(df.pivot_table(index='EVENT_TIME', columns='NODE_ID', values='VOLTAGE', aggfunc='first'))
df1 = df.pivot_table(index=['EVENT_TIME'], columns='NODE_ID', values=['ACTIVE_POWER', 'POWER_FACTOR'])

df2 = df1.resample('15T').mean()
#df2 = df1.groupby(df1.TimeGroup(freq='10Min')).aggregate(numpy.sum)
df3 = df2.T
print(df3)
df3.to_csv('test.csv', sep=',', encoding='utf-8')
#df2 = df1.T
#print(df2)

#print(df)


#pd.pivot_table(df, index=["NODE_ID"], values=["VOLTAGE"])