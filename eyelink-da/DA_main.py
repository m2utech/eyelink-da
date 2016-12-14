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

#pd_sql.execute(sql,pc.conn)
#df = pd_sql.read_sql(sql,pc.conn)

#print(df)
# df = df.T 	#행렬 전치(transpose)
#print(df.axes)
#df.info()
#

#data = pd.read_excel("NODE_RAW_1213_ET_1.xlsx", index_col=0)
data = pd.read_csv("NODE_RAW_1213_ET_1.csv", parse_dates=[2,3])

#print(data['NODE_ID'])
df = pd.DataFrame(data)

print(df.columns.tolist())
df[' EVENT_TIME'] = df[' EVENT_TIME'].dt.date   # key error !!
print(df[' EVENT_TIME'])
df.info()

#df['EVENT_TIME'].date_time.map(lambda x: x.strftime('%Y-%m-%d'))

print(df.pivot_table(index='NODE_ID', columns=' EVENT_TYPE', values='VOLTAGE', aggfunc='first'))


#print(df)


#pd.pivot_table(df, index=["NODE_ID"], values=["VOLTAGE"])