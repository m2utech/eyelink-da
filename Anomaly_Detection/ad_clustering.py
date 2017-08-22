# coding: utf-8
# Construction of Pattern for Eye-Link using clustering algorithm

# 모듈 및 라이브러리 임포트
from config_parser import cfg
import data_convert
import learn_utils

import datetime
from dateutil.relativedelta import relativedelta
import requests
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np

# 1. Dataset loading
# 1.1 Condition of target dataset

##########################
# configration information
node_id = cfg['DA']['node_id']
window_len = int(cfg['DA']['window_len'])
slide_len = int(cfg['DA']['slide_len'])
time_interval = int(cfg['DA']['time_interval'])
v_default = float(cfg['DA']['v_default'])
a_default = float(cfg['DA']['a_default'])
ap_default = float(cfg['DA']['ap_default'])
pf_default = float(cfg['DA']['pf_default'])
n_cluster = int(cfg['DA']['n_cluster'])
#n_cluster = 5
today = datetime.datetime.today()
s_date = (today - relativedelta(months=1)).strftime('%Y-%m-%d')
e_date = today.strftime('%Y-%m-%d')
save_day = today.strftime('%Y-%m-%d')
#save_day = today.strftime('%Y-%m-%dT%H:%M:%S')


######################
# 속성별 세그먼트 추출
def extract_segment(dataset, col_name):
    segment = learn_utils.sliding_chunker(dataset, window_len, slide_len)
    print("Produced %d waveform {}-segments".format(col_name) % len(segment))
    return segment


#####################
# min, max value 계산
def compute_min_max(dataset):
    min_dict = dict()
    max_dict = dict()
    lower_dict = dict()
    upper_dict = dict()

    for cno in range(n_cluster):
        df = dataset[dataset['cluster'] == cno]
        min_list = []
        max_list = []
        lower_list = []
        upper_list = []

        for i in df.columns:
            if i == 'cluster':
                pass
            else:
                min_value = df[i].min()
                min_list.append(min_value)
                # lower_bound
                lower = np.mean(df[i]) - np.std(df[i])
                lower_list.append(lower)

                max_value = df[i].max()
                max_list.append(max_value)
                # upper_bound
                upper = np.mean(df[i]) + np.std(df[i])
                upper_list.append(upper)

        min_dict["cluster_{}".format(cno)] = min_list
        max_dict["cluster_{}".format(cno)] = max_list
        lower_dict["cluster_{}".format(cno)] = lower_list
        upper_dict["cluster_{}".format(cno)] = upper_list

    min_df = pd.DataFrame(min_dict)
    max_df = pd.DataFrame(max_dict)
    lower_df = pd.DataFrame(lower_dict)
    upper_df = pd.DataFrame(upper_dict)

    return min_df, max_df, lower_df, upper_df


###############
# main function
def main(node_id, s_date, e_date):

    print("data loading .......")

    # 학습데이터 로드
    dataset = data_convert.json_data_load(node_id, s_date, e_date)

    print("data preprocessing .......")
    # 데이터 전처리(결측치 처리, 구간화, 디폴트값)

    # 미싱벨류 처리
    voltage_data = data_convert.resample_missingValue(dataset['voltage'], v_default, time_interval)
    ampere_data = data_convert.resample_missingValue(dataset['ampere'], a_default, time_interval)
    active_power_data = data_convert.resample_missingValue(dataset['active_power'], ap_default, time_interval)
    power_factor_data = data_convert.resample_missingValue(dataset['power_factor'], pf_default, time_interval)

    # 각 데이터를 하나로 merge
    dataset = pd.concat([voltage_data, ampere_data.ampere, active_power_data.active_power, power_factor_data.power_factor], axis=1, join_axes=[voltage_data.index])

    # event_time 제거 (default index 사용)
    for col in dataset.columns:
        if 'event_time' in col:
            del dataset[col]

    # # Data Analysis
    clusterer = KMeans(n_clusters=n_cluster)
    total_pattern = {}

    for col_name in dataset.columns:
        print("extracting segment for {}".format(col_name))
        segments = extract_segment(dataset[col_name], col_name)

        print("Clustering of {} segments....".format(col_name))
        clusted_segments = clusterer.fit(segments)
        clusted_df = pd.DataFrame(clusted_segments.cluster_centers_)

        # index rename
        for i in range(len(clusted_df.index)):
            clusted_df = clusted_df.rename(index={i: 'cluster_{}'.format(i)})

        print("Create segment and label dataset")
        labels_df = pd.DataFrame(clusted_segments.labels_)
        labels_df = labels_df.rename(columns={0: "cluster"})

        segment_df = pd.DataFrame(segments)

        lbl_dataset = pd.concat([segment_df, labels_df], axis=1)

        min_df, max_df, lower_df, upper_df = compute_min_max(lbl_dataset)

        #소수점 4자리로 정리
        # clusted_df = clusted_df.applymap(lambda x: str(int(x)) if abs(x-int(x)) < 1e-6 else str(round(x,4)))
        # min_df = min_df.applymap(lambda x: str(int(x)) if abs(x-int(x)) < 1e-6 else str(round(x,4)))
        # max_df = max_df.applymap(lambda x: str(int(x)) if abs(x-int(x)) < 1e-6 else str(round(x,4)))
        
        # clusted_df = clusted_df.convert_objects(convert_numeric=True)
        # min_df = min_df.convert_objects(convert_numeric=True)
        # max_df = max_df.convert_objects(convert_numeric=True)

        pd.options.display.float_format = '{:,.4f}'.format

        clusted_df = clusted_df.apply(lambda x: x.astype(float) if np.allclose(x, x.astype(float)) else x)
        min_df = min_df.apply(lambda x: x.astype(float) if np.allclose(x, x.astype(float)) else x)
        max_df = max_df.apply(lambda x: x.astype(float) if np.allclose(x, x.astype(float)) else x)
        lower_df = lower_df.apply(lambda x: x.astype(float) if np.allclose(x, x.astype(float)) else x)
        upper_df = upper_df.apply(lambda x: x.astype(float) if np.allclose(x, x.astype(float)) else x)

        total_pattern[col_name] = {}
        total_pattern[col_name]["center"] = clusted_df.T.to_dict(orient='list')
        total_pattern[col_name]["min_value"] = min_df.to_dict(orient='list')
        total_pattern[col_name]["max_value"] = max_df.to_dict(orient='list')
        total_pattern[col_name]["lower"] = lower_df.to_dict(orient='list')
        total_pattern[col_name]["upper"] = upper_df.to_dict(orient='list')
        
        # end for loop

    result_json = {}
    result_json['pattern_data'] = total_pattern
    # print(result_json)

    print("result uploading .......")
    print(e_date)
    # upload json data (업로드 테스트 완료)
    upload_url = cfg['SERVER']['pattern_upload_url'] + save_day
    requests.post(upload_url, json=result_json)

    print("Completed ~~~~ ^0^")

    return result_json


if __name__ == '__main__':
    # import socket_client_test
    main('0002.00000039', '2017-08-20', '2017-08-20')
