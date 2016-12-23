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

# 모든 속성 이용시..
data.rename(columns = {'ALS_LEVEL' : 'als_level'}, inplace = True)
data.rename(columns = {'DIMMING_LEVEL' : 'dimming_level'}, inplace = True)
data.rename(columns = {'VIBRATION_X' : 'vibration_x'}, inplace = True)
data.rename(columns = {'VIBRATION_Y' : 'vibration_y'}, inplace = True)
data.rename(columns = {'VIBRATION_Z' : 'vibration_z'}, inplace = True)
data.rename(columns = {'VIBRATION_MAX' : 'vibration_max'}, inplace = True)
data.rename(columns = {'NOISE_ORIGIN_DECIBEL' : 'noise_origin_decibel'}, inplace = True)
data.rename(columns = {'NOISE_ORIGIN_FREQUENCY' : 'noise_orgin_frequency'}, inplace = True)
data.rename(columns = {'NOISE_DECIBEL' : 'nosie_decibel'}, inplace = True)
data.rename(columns = {'NOISE_FREQUENCY' : 'noise_frequency'}, inplace = True)
data.rename(columns = {'GPS_LONGITUDE' : 'gps_longtude'}, inplace = True)
data.rename(columns = {'GPS_LATITUDE' : 'gpsi_latitude'}, inplace = True)
data.rename(columns = {'GPS_ALTITUDE' : 'gps_altitude'}, inplace = True)
data.rename(columns = {'GPS_SATELLITE_COUNT' : 'gps_stellite_count'}, inplace = True)
data.rename(columns = {'STATUS_ALS' : 'status_als'}, inplace = True)
data.rename(columns = {'STATUS_GPS' : 'status_gps'}, inplace = True)
data.rename(columns = {'STATUS_NOISE' : 'status_noise'}, inplace = True)
data.rename(columns = {'STATUS_VIBRATION' : 'status_vibration'}, inplace = True)
data.rename(columns = {'STATUS_POWER_METER' : 'status_power_meter'}, inplace = True)
data.rename(columns = {'STATUS_EMERGENCY_LED_ACTIVE' : 'status_fmergency_led_active'}, inplace = True)
data.rename(columns = {'STATUS_SELF_DIAGNOSTICS_LED_ACTIVE' : 'status_self_diagnostics_led_active'}, inplace = True)
data.rename(columns = {'STATUS_ACTIVE_MODE' : 'status_active_mode'}, inplace = True)
data.rename(columns = {'STATUS_LED_ON_OFF_TYPE' : 'status_led_on_off_type'}, inplace = True)
data.rename(columns = {'REBOOT_TIME' : 'reboot_time'}, inplace = True)
data.rename(columns = {'EVENT_REMAIN' : 'event_remain'}, inplace = True)
data.rename(columns = {'FAILFIRMWAREUPDATE' : 'failfirmwareupdate'}, inplace = True)


# 데이터 타입 정의 
# (DtypeWarning: Columns (xx) have mixed types.  방지



#원하는 데이터 속성만 뽑을때
# RM --> Select Attributes
data = DataFrame(data, columns=['node_id','event_time','voltage'])

# 시간구간별 노드들의 전압값으로 데이터테이블 생성
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

data = elda_pre.missingValue(data, 200)
#df.voltage = elda_pre.missingValue(df, 'voltage', 200)


# data Tranpose
#
#데이터 확인용 저장
#data.to_csv('1223_15T_voltage.csv', sep=',', encoding='utf-8')


#시계열 테스트
#data = DataFrame(data, columns=['0001.00000001','0001.00000002'])
data = DataFrame(data, columns=data.columns)

ts = pd.Series(data=data['0001.00000001'], index=data.index)
ts1 = pd.Series(data=data['0001.00000002'], index=data.index)

#print(ts)

#ts = ts.cumsum()

ts.plot()
ts1.plot()
plt.show()


"""
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
"""

"""
#print(df.columns.tolist()) #컬럼 데이터타입 확인
df.info()

#df.event_time = (df.event_time - df.event_time.min()) / np.timedelta64(1,'D')

#df.event_time=df.event_time.astype(object).astype(str)

print(df.event_time)

df.info()

"""
""" #
df_train, df_test = train_test_split(df, train_size=0.6)
cluster = KMeans(n_clusters=8, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1)
cluster.fit(df_train)
result = cluster.predict(df_test)

print(result)
"""