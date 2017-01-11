import pandas as pd
from pandas import DataFrame

import elda_preprocessing as elda_pre

def extract_data(targetdata, idx, col, val, def_val, t_interval):

	# 시간구간별 노드들의 전압값으로 데이터테이블 생성
	targetdata = targetdata.pivot_table(index=idx, columns=col, values=val)

	# 처음-끝 일정사이에 15분 단위로 구분(비어있는 날짜는 자동으로 생성)
	targetdata = targetdata.resample(t_interval).mean()

	# missing value process
	targetdata = elda_pre.missingValue(targetdata,def_val)

	return targetdata