# -*- coding: utf-8-*-

import os
import sys
import jpype
import jaydebeapi as jp
import pandas as pd
import pandas.io.sql as pd_sql
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import json

import seaborn as sns
sns.set(color_codes=True)

# oracle jdbc 파일 경로 및 class 경로 설정
JDBC_DRIVER = 'C:/dev/jdbc-4.2.9.jar'

# parstream 접근
conn = jp.connect('com.parstream.ParstreamDriver',
                  'jdbc:parstream://m2u-parstream.eastus.cloudapp.azure.com:9043/eyelink?user=parstream&password=Rornfldkf!2',
                  JDBC_DRIVER)
cur = conn.cursor()

#Excute SQL
#sql = "SELECT * FROM tb_node_raw where event_type = 17 and month = 11 and day = 30"
sql = "SELECT * FROM tb_node_raw where event_type = 1"

pd_sql.execute(sql,conn)
df = pd_sql.read_sql(sql,conn, index_col = None)
#df = pd_sql.read_sql(sql,conn, pd.to_datetime, index_col = None)
df1 = df.pivot_table(index=['event_type'], columns='node_id', values=['power_factor'])
df2 = df1.resample('15T').mean()

df2.to_csv('test.csv', sep=',', encoding='utf-8')

#df.info()

#print(df)
#df.to_csv('parstream_data.csv', sep=',', encoding='utf-8')
'''
df['event_time'] = pd.to_datetime(df['event_time'])
df.info()
print(df.columns.tolist())

df['event_time'] = df['event_time'].dt.date

#df['event_time'] = df['event_time'].dt.date   # key error !!
print(df['event_time'])
'''


#df.convert_objects(convert_numeric=True)
#pd.set_option('display.max_columns', 80)
#print(df.head(3))


#print(df['als_level'])
#print(df['als_level'].convert_objects(convert_numeric=True))

#print(df.dtypes)

#df.info()

#print(df.head())

#dataset = pd.read_sql(sql,conn)
#dataset.info()
'''
cur.execute(sql)
results = cur.fetchall()

if results:
	for r in results:
		print(r)
'''
"""
json_output = []
json_output = cur.fetchall()
print(json_output)
"""

#dataset = cur.fetchall()

#data = pd_sql.execute(sql,conn)
#df = pd.read_sql(sql,conn)
#df = pd_sql.read_sql(sql,conn)


#dataset['als_level'] = pd.to_numeric(dataset['als_level'], errors='coerce').fillna(0)
#dataset['dimming_level'] = pd.to_numeric(dataset['dimming_level'], errors='coerce').fillna(0)

#json_output = json.dumps(dataset)

#print(json_output)

#dataset.info() #데이터 정보 확인

#sns.lmplot(x="als_level", y="dimming_level", data=dataset);

#plt.show()

#conn.close()
