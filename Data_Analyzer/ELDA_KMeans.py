# 데이터 처리
import pandas as pd
import pandas.io.sql as pd_sql
from pandas import DataFrame
#import Parstream_conn as pc
import datetime as dt

import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

#from sklearn.cross_validation import train_test_split


# csv파일 열기
#df = pd.read_csv("../data/NODE_RAW_1215.csv", parse_dates=[2,3])
# text 파일
df = pd.read_csv("../data/busan_tb_node_raw_1215.txt", sep=',', parse_dates=[2,3])
#df = pd.DataFrame(data)


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

#원하는 데이터 속성만 뽑을때
# RM --> Select Attributes
df = DataFrame(df, columns=['node_id','event_time','voltage','ampere'])

# Processing of missing value

#df.event_time = df.event_time.astype(str)
print(df.event_time)
df.info()

df.voltage = df.voltage.fillna(200)

df1 = df.pivot_table(index='event_time', columns='node_id', values='voltage')

df2 = df1.resample('H').mean()
df3 = df2.T

df3.to_csv('test.csv', sep=',', encoding='utf-8')
'''# Data Tranpose
df3 = df2.T
print(df3)
df3.to_csv('test.csv', sep=',', encoding='utf-8')
'''

#print(df1)


#plt.plot(df.event_time,df.voltage)

#plt.show()
#print(df.voltage)
print(df.columns.tolist()) #컬럼 데이터타입 확인
#print(df)

import pdb; pdb.set_trace()  # breakpoint 69f071f9 //


'''


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

'''


#print(df.columns.tolist()) #컬럼 데이터타입 확인
df.info()

#df.event_time = (df.event_time - df.event_time.min()) / np.timedelta64(1,'D')

#df.event_time=df.event_time.astype(object).astype(str)

print(df.event_time)

df.info()
#x, y = make_blobs()	#가우시안 분포 생성
plt.figure(figsize=(12, 12))	#결과화면 사이즈




#plt.show()

''' #
df_train, df_test = train_test_split(df, train_size=0.6)
cluster = KMeans(n_clusters=8, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1)
cluster.fit(df_train)
result = cluster.predict(df_test)

print(result)
'''