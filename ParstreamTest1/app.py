import os
import sys
import jpype
import jaydebeapi as jp
import pandas as pd
from flask import Flask
from flask import render_template
import json
from bson import json_util
from bson.json_util import dumps


app = Flask(__name__)

# oracle jdbc 파일 경로 및 class 경로 설정
JDBC_DRIVER = 'C:/dev/jdbc-4.2.9.jar'
jar = r'C:/dev/jdbc-4.2.9.jar'
args = '-Djava.class.path=%s' % jar
	
	# parstream 접근
conn = jp.connect('com.parstream.ParstreamDriver',
                  'jdbc:parstream://m2u-parstream.eastus.cloudapp.azure.com:9043/eyelink?user=parstream&password=Rornfldkf!2',
                  JDBC_DRIVER)

cur = conn.cursor()
sql = "SELECT event_time, als_level, dimming_level FROM tb_node_raw where event_type = 17 and month = 11 and day = 30"
dataset = pd.read_sql(sql,conn)

#		json_projects.append(project)
#	json_projects = json.dumps(json_projects, default=json_util.default)
#	conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tbnode")
def tbnode():
	json_projects = []
	for project in dataset:
		print(project)
	return json_projects
	#return render_template("tbnode.html")
    


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
