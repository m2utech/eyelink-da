# coding: utf-8
# -*- coding : cp949 -*-

def missingValue(data, col_name, value):
	data = data[col_name].fillna(value)
	return data

def missingValue(data, value):
	data = data.fillna(value)
	return data

if __name__ == '__main__':
	pass