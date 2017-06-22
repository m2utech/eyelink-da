# coding: utf-8
### required library ###
import pandas as pd
#import pandas.io.sql as pd_sql
from pandas import DataFrame
import ujson, requests

### required eyelink modules ###
#import elda_parstream_conn as elda_pc
import elda_extract_data as elda_ed
#import elda_read_csv as elda_rc
import elda_preprocessing as elda_pre


### test library ###
import numpy as np
import matplotlib.pyplot as plt

from pandasql import sqldf

df = DataFrame(np.random.randn(10, 4))
print(df)

tf = DataFrame()
tf['event_time'] = df.index

tf['c0'] = df.loc[:,0]
tf['c1'] = df.loc[:,1]
tf['c2'] = df.loc[:,2]
tf['c3'] = df.loc[:,3]

print("---------")
print(tf)