

def missingValue(data, col_name, value):
	data = data[col_name].fillna(value)
	return data

def missingValue(data, value):
	data = data.fillna(value)
	return data

def function():
	pass