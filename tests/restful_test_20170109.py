import json, requests

s_date = '2016-11-16'
e_date = '2016-11-17'

url = "http://m2utech.eastus.cloudapp.azure.com:5223/dashboard/restapi/getTbRawDataByPeriod?startDate={}&endDate={}".format(s_date,e_date)

uResponse = requests.get(url)

Jresponse = uResponse.text
data = json.loads(Jresponse)
print(data)

