import json
import pandas as pd

data = pd.read_json("C:\\test.json")

print(data.info())
import pdb; pdb.set_trace()  # breakpoint cc176a94 //

# 테스트용 Python Dictionary
with open("C:\\test.json") as json_file:
	js = json.load(json_file)
 
# JSON 인코딩
jsonString = json.dumps(js, indent=4)
 
# 문자열 출력
print(jsonString)
print(type(jsonString))   # class str
