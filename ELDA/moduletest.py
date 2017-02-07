import pandas as pd
from pandas import DataFrame
import ujson
import json
import requests
from collections import OrderedDict
import datetime


def data_load(s_date, e_date, t_iterval):
	global start_date, end_date, time_interval
	start_date = s_date
	end_date = e_date
	time_interval = t_iterval

	print(start_date)
	print("===========")
	print(end_date)
	print("===========")
	print(time_interval)

####################################
if __name__ == '__main__':
	print("test")
