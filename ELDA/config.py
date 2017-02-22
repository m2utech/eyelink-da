import ConfigParser

import sys  #모듈을 실행할 때 설정파일과 섹션을 입력으로 받아들이기 위해 sys를 임포트

section = sys.argv[1]  # 띄어쓰기를 구분으로 입력된 문자열의 두 번째 인자를 섹션으로

conf_file = sys.argv[2]  # 마찬가지로 문자열의 세번 째 인자를 설정파일 네임으로


config = ConfigParser.ConfigParser()  # ConfigParser모듈의 객체를 넣을 변수를 config라고 만들었어요.

config.read(conf_file)  # 그리고 위에서 입력받은 conf_file(설정파일 이름)을 파라미터에 넣어 파일을 읽어들여요. 

 

sns_id = config.get(section, 'id')   # 이제 위에서 입력받은 section(섹션)에서 원하는 옵션(여기에서는 id)을 가져오게 됩니다.

sns_passwd = config.get(section, 'passwd') # 위와 마찬가지!
