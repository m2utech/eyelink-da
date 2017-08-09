# coding: utf-8
# Construction of Pattern for Eye-Link using clustering algorithm

# 모듈 및 라이브러리 임포트
import datetime
import requests
import numpy as np
import data_convert
import learn_utils
from config_parser import cfg
import pandas as pd
from sklearn.cluster import KMeans

# 1. Dataset loading
# 1.1 Condition of target dataset

###########################
node_id = '0002.00000039'
s_date = '2017-01-01'
e_date = '2017-01-31'
WINDOW_LEN = 120
###########################


def main(node_id, s_date, e_date):

    print("data loading .......")

    # 학습데이터 로드
    dataset = data_convert.json_data_load(node_id, s_date, e_date)

    print("data preprocessing .......")
    # 데이터 전처리(결측치 처리, 구간화, 디폴트값)

    # 미싱벨류 처리
    # resample_missingValue(data, default_value, t_interval)
    voltage_data = data_convert.resample_missingValue(dataset['voltage'], 220, 1)
    ampere_data = data_convert.resample_missingValue(dataset['ampere'], 0.5, 1)
    active_power_data = data_convert.resample_missingValue(dataset['active_power'], 110, 1)
    power_factor_data = data_convert.resample_missingValue(dataset['power_factor'], 0.9, 1)


    # 각 데이터를 하나로 merge
    dataset = pd.concat([voltage_data, ampere_data.ampere, active_power_data.active_power, power_factor_data.power_factor], axis=1, join_axes=[voltage_data.index])


    # event_time 제거 (default index 사용)
    for col in dataset.columns:
        if 'event_time' in col:
            del dataset[col]


    # ### Extracting segmentsa
    print("extracting segments .......")
    #segments = learn_utils.sliding_chunker(dataset, WINDOW_LEN, 1)
    ## 속성별 세그먼트 추출
    v_seg = learn_utils.sliding_chunker(dataset.voltage, WINDOW_LEN, 1)
    a_seg = learn_utils.sliding_chunker(dataset.ampere, WINDOW_LEN, 1)
    ap_seg = learn_utils.sliding_chunker(dataset.active_power, WINDOW_LEN, 1)
    pf_seg = learn_utils.sliding_chunker(dataset.power_factor, WINDOW_LEN, 1)
    #print("Produced %d waveform segments" % len(segments))
    print("Produced %d waveform v_segments" % len(v_seg))
    print("Produced %d waveform a_segments" % len(a_seg))
    print("Produced %d waveform ap_segments" % len(ap_seg))
    print("Produced %d waveform pf_segments" % len(pf_seg))


    # ### Reshape of segments (dimesional reduction)

    # 차원축소를 위해 np.array로 변환
    #segments = np.array(segments)
    # 속성별
    #v_seg = np.array(v_seg)
    #a_seg = np.array(a_seg)
    #ap_seg = np.array(ap_seg)
    #pf_seg = np.array(pf_seg)


    # 2차원 배열로 차원축소 (복합패턴일경우)
    #multi_segments = segments.reshape(len(segments), -1)

    # ### Clustering using segments
    print("Clustering by segments .......")
    # 클러스터링 객체 생성 (n = 50)
    clusterer = KMeans(n_clusters=120)


    # 클러스터링(학습) 및 데이터 처리를 위해 DataFrame으로 변환

    #clusted_segments = clusterer.fit(multi_segments)
    #clusted_df = pd.DataFrame(clusted_segments.cluster_centers_)

    v_clusted_segments = clusterer.fit(v_seg)
    v_clusted_df = pd.DataFrame(v_clusted_segments.cluster_centers_)

    a_clusted_segments = clusterer.fit(a_seg)
    a_clusted_df = pd.DataFrame(a_clusted_segments.cluster_centers_)

    ap_clusted_segments = clusterer.fit(ap_seg)
    ap_clusted_df = pd.DataFrame(ap_clusted_segments.cluster_centers_)

    pf_clusted_segments = clusterer.fit(pf_seg)
    pf_clusted_df = pd.DataFrame(pf_clusted_segments.cluster_centers_)


    # - index rename (ex. cluster_1...cluster_n)

    #for i in range(len(clusted_df.index)):
    #    clusted_df = clusted_df.rename(index={i:'cluster_{}'.format(i)})

    print("result data processing .......")
    # index rename
    for i in range(len(v_clusted_df.index)):
        v_clusted_df = v_clusted_df.rename(index={i:'cluster_{}'.format(i)})
        a_clusted_df = a_clusted_df.rename(index={i:'cluster_{}'.format(i)})
        ap_clusted_df = ap_clusted_df.rename(index={i:'cluster_{}'.format(i)})
        pf_clusted_df = pf_clusted_df.rename(index={i:'cluster_{}'.format(i)})


    # column rename
    for i in range(len(v_clusted_df.columns)):
        v_clusted_df = v_clusted_df.rename(columns={i:'t_{}'.format(i)})
        a_clusted_df = a_clusted_df.rename(columns={i:'t_{}'.format(i)})
        ap_clusted_df = ap_clusted_df.rename(columns={i:'t_{}'.format(i)})
        pf_clusted_df = pf_clusted_df.rename(columns={i:'t_{}'.format(i)})

    # ### Extract multi-patterns
    # # 속성별 패턴 데이터셋
    # V_cl_pattern = pd.DataFrame()
    # A_cl_pattern = pd.DataFrame()
    # AP_cl_pattern = pd.DataFrame()
    # PF_cl_pattern = pd.DataFrame()

    # v_no = 0
    # a_no = 0
    # ap_no = 0
    # pf_no = 0

    # for x in range(len(clusted_df.columns)):
    #     if (x%4)==0:
    #         col_name = 't_{}'.format(v_no)
    #         V_cl_pattern[col_name] = clusted_df.iloc[:,x]
    #         v_no+=1
    #     if (x%4)==1:
    #         col_name = 't_{}'.format(a_no)
    #         A_cl_pattern[col_name] = clusted_df.iloc[:,x]
    #         a_no+=1
    #     if (x%4)==2:
    #         col_name = 't_{}'.format(ap_no)
    #         AP_cl_pattern[col_name] = clusted_df.iloc[:,x]
    #         ap_no+=1
    #     if (x%4)==3:
    #         col_name = 't_{}'.format(pf_no)
    #         PF_cl_pattern[col_name] = clusted_df.iloc[:,x]
    #         pf_no+=1


    #v_clusted_df.T.to_dict(orient="dict")


    # Create json
    print("Create json format .......")
    total_pattern = {}
    total_pattern['voltage'] = v_clusted_df.T.to_dict(orient='list')
    total_pattern['ampere'] = a_clusted_df.T.to_dict(orient='list')
    total_pattern['active_power'] = ap_clusted_df.T.to_dict(orient='list')
    total_pattern['power_factor'] = pf_clusted_df.T.to_dict(orient='list')

    result_json = {}
    result_json['pattern_data'] = total_pattern
    #print(result_json)

    print("result uploading .......")
    # upload json data (업로드 테스트 완료)
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    
    upload_url = cfg['pattern_upload_url'] + today
    #upload_url = cfg['pattern_update_url'] + today
    r = requests.post(upload_url, json=result_json)

    print("Completed ~~~~ ^0^")

if __name__ == '__main__':
    # import socket_client_test
    main("0002.00000039", '2017-01-01', '2017-01-31')
    #pass
