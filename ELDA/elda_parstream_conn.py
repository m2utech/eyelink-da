# -*- coding: utf-8-*-

import jpype
import jaydebeapi as jp
import pandas as pd
import pandas.io.sql as pd_sql
import matplotlib

# jdbc 파일 경로 및 class 경로 설정
JDBC_DRIVER = '../drivers/jdbc-4.2.9.jar'

# parstream 접근
conn = jp.connect('com.parstream.ParstreamDriver',
                  'jdbc:parstream://m2u-parstream.eastus.cloudapp.azure.com:9043/eyelink?user=parstream&password=Rornfldkf!2',
                  JDBC_DRIVER)

#conn.close()
