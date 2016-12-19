import os
import sys
import time
import pandas as pd
import pandas.io.sql as pd_sql
from pandas import DataFrame

# Parstream_conn.py
import Parstream_conn as pc


#cur = pc.conn.cursor()

#sql = "SELECT als_level, dimming_level FROM tb_node_raw where event_time = '2016-11-30 22:31:12'"
#sql = "SELECT event_type, als_level, dimming_level FROM tb_node_raw where event_time = '2016-11-30 22:31:12'"
#cur.execute(sql)
#result = cur.fetchall()

# tuple object를 값으로 가져올 수 없기에 각각 분리
#for each in result:
#	x = each[0]
#	y = each[1]

#	print(list(chain(x)))
#	y = str(''.join(x))
#	z = int(y)
#	print(x,y)

#print(type(each[1]))
sql = "SELECT * FROM tb_node_raw where event_type = 1"
pd_sql.execute(sql,pc.conn)
df = pd_sql.read_sql(sql,pc.conn)

print(df)
# df = df.T 	#행렬 전치(transpose)
#print(df.axes)
#df.info()
#

#data = pd.read_excel("NODE_RAW_1213_ET_1.xlsx", index_col=0)
#data = pd.read_csv("NODE_RAW_1215_ET_1.csv", parse_dates=[2,3])
'''
data = pd.read_csv("../data/NODE_RAW_1215_ET_1.csv", parse_dates=[2,3])

#print(data['NODE_ID'])
df = pd.DataFrame(data)

print(df.columns.tolist()) #컬럼 데이터타입 확인

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
#pd.pivot_table(df, index=["NODE_ID"], values=["VOLTAGE"])