import json
 
# 테스트용 JSON 문자열
jsonString = '{"name": "강진수", "id": 152352, "history": [{"date": "2015-03-11", "item": "iPhone"}, {"date": "2016-02-23", "item": "Monitor"}]}'
 
# JSON 디코딩
dict = json.loads(jsonString)
 
# Dictionary 데이타 체크
print(dict['name'])
for h in dict['history']:
    print(h['date'], h['item'])
