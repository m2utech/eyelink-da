# coding: utf-8
# Construction of Pattern for Eye-Link using clustering algorithm

# ##### 모듈 및 라이브러리 임포트 #####
from ad_configParser import getConfig
import ad_dataConvert
from ad_matching import DTWDistance

import logging
import requests
import pandas as pd
from sklearn.cluster import KMeans
import learn_utils
import numpy as np
import heapq
import consts
import util

from multiprocessing import Process, Queue, freeze_support

cfg = getConfig()

logger = logging.getLogger("anomalyDetection")


# ##### Main function #####
def main(node_id, s_date, e_date, master_data):
    dataset = preprocessData(node_id, s_date, e_date, cfg)

    if dataset is not None:
        if master_data is not None:
            master_info = ad_dataConvert.loadPatternInfo(consts.ATTR_MASTER_ID)
            total_pattern, info_pattern = createPatternData(dataset, master_data, master_info, cfg)
            savePatternData(total_pattern, info_pattern, cfg, True)
        else:
            logger.debug("master data is None ...")
            master_info = None
            total_pattern, info_pattern = createPatternData(dataset, master_data, master_info, cfg)
            savePatternData(total_pattern, info_pattern, cfg, False)
    else:
        logger.warning("There is no dataset for clustering")


def savePatternData(pattern, pattern_info, cfg, masterYN):
    save_day = util.getToday(True, consts.DATE)
    logger.debug("Uploading result dataset ... [ID : {}]".format(save_day))

    pattern_json = {}
    pattern_json['pattern_data'] = pattern
    pattern_json['pattern_data']['creation_Date'] = save_day

    pattern_info_json = {}
    pattern_info_json['pattern_info'] = pattern_info
    pattern_info_json['pattern_info']['creation_Date'] = save_day

    # #### 데이터 저장 #####
    pattern_url = cfg['API']['url_post_pattern_data']   # 'TEST' #save_day
    requests.post(pattern_url + save_day, json=pattern_json)

    pattern_info_url = cfg['API']['url_post_pattern_info']
    requests.post(pattern_info_url + save_day, json=pattern_info_json)

    if masterYN is False:
        requests.post(pattern_url+consts.ATTR_MASTER_ID, json=pattern_json)
        requests.post(pattern_info_url+consts.ATTR_MASTER_ID, json=pattern_info_json)

    print(pattern_json)
    print(pattern_info_json)


# ##### 초기 데이터 처리 ######
def preprocessData(node_id, s_date, e_date, cfg):
    # 학습데이터 로드
    logger.debug("Trainnig data loading ...")
    dataset = ad_dataConvert.loadJsonData(node_id, s_date, e_date, cfg)

    if dataset is not None:
        # 데이터 전처리(결측치 처리, 구간화, 디폴트값)
        logger.debug("Data preprocessing ...")
        procs = []
        output = {}
        df = pd.DataFrame()
        for key, factor_name in cfg['FACTORS'].items():
            output[factor_name] = Queue()
            procs.append(Process(target=ad_dataConvert.processResamplingAndMissingValue,
                args=(dataset[factor_name], 
                    float(cfg['FACTOR_DEFAULT'][key]), 
                    consts.ATTR_TIME_INTERVAL, 
                    output[factor_name]
                )
            ))

        for p in procs:
            p.start()

        for key, factor_name in cfg['FACTORS'].items():
            if df.empty:
                df = df.append(output[factor_name].get())
            else:
                fact_data = output[factor_name].get()
                df = pd.concat([df, fact_data[factor_name]], axis=1, join_axes=[df.index])
            output[factor_name].close()

        for proc in procs:
            proc.join()

        # event_time 제거 (default index 사용)
        for col in df.columns:
            if 'event_time' in col:
                del df[col]
        return df
    else:
        return None


# ##### 속성별 패턴생성 (multiprocessing) #####
def createPatternData(dataset, master_data, master_info, cfg):
    procs = []
    col_list = []
    p_output = {}
    i_output = {}
    total_pattern = dict()
    info_pattern = dict()

    for col_name in dataset.columns:
        p_output[col_name] = Queue()
        i_output[col_name] = Queue()
        col_list.append(col_name)
        if master_data is not None:
            procs.append(Process(target=clusteringSegment,
                args=(dataset[col_name], master_data[col_name],
                    master_info[col_name], col_name,
                    p_output[col_name], i_output[col_name])))
        else:
            procs.append(Process(target=clusteringSegment,
                args=(dataset[col_name], master_data, master_info,
                    col_name, p_output[col_name], i_output[col_name])))

    for p in procs:
        p.start()

    for col_name in col_list:
        fact_pattern = p_output[col_name].get()
        fact_info = i_output[col_name].get()
        total_pattern[col_name] = fact_pattern
        info_pattern[col_name] = fact_info
        p_output[col_name].close()
        i_output[col_name].close()

    for proc in procs:
        proc.join()

    return total_pattern, info_pattern


# ##### 속성별 클러스터링 usint K-Means and DTW algorithm #####
def clusteringSegment(dataset, master_data, master_info, col_name, p_output, i_output):
    clusterer = KMeans(n_clusters=consts.ATTR_N_CLUSTER)

    logger.debug("extract all segment for [{}]".format(col_name))
    segments = extractSegment(dataset, col_name, consts.ATTR_WIN_LEN, consts.ATTR_SLIDE_LEN)

    logger.debug("Run clustering about segments of [{}]".format(col_name))
    clusted_segments = clusterer.fit(segments)
    clusted_df = pd.DataFrame(clusted_segments.cluster_centers_)

    # index rename
    for i in range(len(clusted_df.index)):
        clusted_df = clusted_df.rename(index={i: "cluster_{}".format(i)})

    logger.debug("Convert to labeled DataFrame for [{}]".format(col_name))
    labels_df = pd.DataFrame(clusted_segments.labels_)
    labels_df = labels_df.rename(columns={0: "cluster"})
    segment_df = pd.DataFrame(segments)
    lbl_dataset = pd.concat([segment_df, labels_df], axis=1)

    logger.debug("Compute boundary threshold ...")
    min_df, max_df, lower_df, upper_df = computeThreshold(lbl_dataset, consts.ATTR_N_CLUSTER)

    pd.options.display.float_format = '{:,.4f}'.format

    clusted_df = clusted_df.apply(lambda x: x.astype(float) if np.allclose(x, x.astype(float)) else x)
    min_df = min_df.apply(lambda x: x.astype(float) if np.allclose(x, x.astype(float)) else x)
    max_df = max_df.apply(lambda x: x.astype(float) if np.allclose(x, x.astype(float)) else x)
    lower_df = lower_df.apply(lambda x: x.astype(float) if np.allclose(x, x.astype(float)) else x)
    upper_df = upper_df.apply(lambda x: x.astype(float) if np.allclose(x, x.astype(float)) else x)

    center_df = clusted_df.T

    fact_pattern = {}

    for col in center_df.columns:
        fact_pattern[col] = {}
        fact_pattern[col]['max_value'] = max_df[col].tolist()
        fact_pattern[col]['upper'] = upper_df[col].tolist()
        fact_pattern[col]['center'] = center_df[col].tolist()
        fact_pattern[col]['lower'] = lower_df[col].tolist()
        fact_pattern[col]['min_value'] = min_df[col].tolist()

    p_output.put(fact_pattern)
    logger.debug("Completed clustering for [{}]".format(col_name))

    # #### matching ####
    logger.debug("pattern matching with master pattern for [{}]".format(col_name))
    meta_pattern = {}  # information about clustered pattern

    if master_data is not None:
        master_df = pd.DataFrame()
        for cno in master_data.keys():
            master_df[cno] = pd.Series(master_data[cno]['center']).values

        for clustNo in center_df.columns:
            distance = {}

            for m_clustNo in master_df.columns:
                cur_dist = DTWDistance(center_df[clustNo], master_df[m_clustNo], 1)
                distance[m_clustNo] = cur_dist

            max_dist = heapq.nlargest(1, distance, key=distance.get)
            min_dist = heapq.nsmallest(1, distance, key=distance.get)

            percentile = float(distance[max_dist[0]]) / 100.0
            match_rate = 100.0 - (float(distance[min_dist[0]]) / percentile)

            if match_rate > 90.0:
                meta_pattern[clustNo] = master_info[min_dist[0]]
            else:
                meta_pattern[clustNo] = "undefined"

        i_output.put(meta_pattern)

    else:
        for clustNo in center_df.columns:
            meta_pattern[clustNo] = "undefined"
        i_output.put(meta_pattern)


# ##### 속성별 세그먼트 추출 #####
def extractSegment(dataset, col_name, window_len, slide_len):
    segment = learn_utils.sliding_chunker(dataset, window_len, slide_len)
    logger.debug("Produced {} waveform {}-segments".format(len(segment), col_name))
    return segment


# ##### boundary threshold 계산 #####
def computeThreshold(dataset, n_cluster):
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
            if i == "cluster":
                pass
            else:
                min_value = df[i].min()
                min_list.append(min_value)
                lower = np.mean(df[i]) - (np.std(df[i]))
                lower_list.append(lower)
                max_value = df[i].max()
                max_list.append(max_value)
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


# ##### 스크립트 직접 실행 시 #####
if __name__ == '__main__':
    freeze_support()

    from ad_logger import getAdLogger
    logger = getAdLogger()

    url = cfg['API']['url_get_pattern_data'] + consts.ATTR_MASTER_ID
    resp = requests.get(url)
    import json
    dataset = json.loads(resp.text)

    if dataset['rtnCode']['code'] == '0000':
        logger.debug("reload master pattern")
        master_data = dataset['rtnData']['pattern_data']
    else:
        master_data = None

    main('0002.00000039', '2017-10-23T00:00:00', '2017-10-24T02:00:00', master_data)