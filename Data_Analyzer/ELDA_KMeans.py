# coding: utf-8
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

# data preprocessing
import ELDA_Preprocessing as elda_pre


#test from sklearn.cross_validation import train_test_split


# csv or text 파일, 구분자','
data = pd.read_csv("../data/busan_tb_node_raw_1215.txt", sep=',', parse_dates=[2,3])
#test df = pd.DataFrame(data)


# 파스트림 연동시를 위해 소문자로..
data.rename(columns = {'NODE_ID' : 'node_id'}, inplace = True)
data.rename(columns = {'EVENT_TYPE' : 'event_type'}, inplace = True)
data.rename(columns = {'MEASURE_TIME' : 'measure_time'}, inplace = True)
data.rename(columns = {'EVENT_TIME' : 'event_time'}, inplace = True)
data.rename(columns = {'VOLTAGE' : 'voltage'}, inplace = True)
data.rename(columns = {'AMPERE' : 'ampere'}, inplace = True)
data.rename(columns = {'POWER_FACTOR' : 'power_factor'}, inplace = True)
data.rename(columns = {'ACTIVE_POWER' : 'active_power'}, inplace = True)
data.rename(columns = {'REACTIVE_POWER' : 'reactive_power'}, inplace = True)
data.rename(columns = {'APPARENT_POWER' : 'apparent_power'}, inplace = True)
data.rename(columns = {'AMOUNT_OF_ACTIVE_POWER' : 'amount_of_active_power'}, inplace = True)

#원하는 데이터 속성만 뽑을때
# RM --> Select Attributes
data = DataFrame(data, columns=['node_id','event_time','voltage'])

'''
pivot table
시간구간별 노드들의 전압값으로 데이터테이블 생성
'''
data = data.pivot_table(index='event_time', columns='node_id', values='voltage')

# 처음-끝 일정사이에 15분 단위로 구분(비어있는 날짜는 자동으로 생성)
data = data.resample('15T').mean()

# 모든 속성이 데이터가 없는 시간대 삭제
data = data.dropna(how='all')

'''
각 속성별 null은 일단 디폴트값으로 처리 (시각화를 위해)
voltage:220, ampere:2, power_factor:0.9, 
'''

# Processing of missing value
# 모듈화 테스트 (ELDA_Preprocessing.py)
#df.voltage = elda_pre.missingValue(df, 'voltage', 200)
data = elda_pre.missingValue(data, 200)

data = DataFrame(data, columns=['0001.00000001','0001.00000002'])



ts = pd.Series(data=data['0001.00000001'], index=data.index)

print(ts)

#ts = ts.cumsum()

ts.plot()
plt.show()


# data Tranpose
#data = data.T

#print(data[:3])

#ts = pd.Series(np.random.randn(500), index=pd.date_range('1/1/2000', periods=500))
#print(ts)

''' 타임시리즈 테스트
import matplotlib
matplotlib.style.use('ggplot')

ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))

ts = ts.cumsum()

ts.plot()
plt.show()
'''

import pdb; pdb.set_trace()  # breakpoint de9aa193 //

plt.plot(data.node_id, data.columns[0:])

#print(data.columns.tolist()) #컬럼 데이터타입 확인
#print(data)


import pdb; pdb.set_trace()  # breakpoint 6d10a28b //




import pdb; pdb.set_trace()  # breakpoint 8ef52259 //


#데이터 확인용 저장
#df3.to_csv('1221_15T_voltage.csv', sep=',', encoding='utf-8')


df3 = df2.T



print (df.voltage)

import pdb; pdb.set_trace()  # breakpoint 9eaf6b04 //

df.voltage = df.voltage.fillna(200)


#ok df3.to_csv('test.csv', sep=',', encoding='utf-8')
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