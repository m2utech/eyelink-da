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
    save_day = util.getToday(True, consts.DATE)

    if (dataset is None) or (dataset.empty):
        logger.warning("There is no dataset for clustering")
    else:
        if master_data is not None:
            master_info = ad_dataConvert.loadPatternInfo(consts.ATTR_MASTER_ID)
            pData, pInfo, npData, npInfo = createPatternData(dataset, master_data, master_info, save_day, cfg)
            savePatternData(pData, pInfo, npData, npInfo, save_day, cfg, True)
            logger.debug("Completed create pattern dataset [ID : {}]".format(save_day))
        else:
            logger.debug("master data is None ...")
            master_info = None
            pData, pInfo, npData, npInfo = createPatternData(dataset, master_data, master_info, save_day, cfg)
            savePatternData(pData, pInfo, npData, npInfo, save_day, cfg, False)
            logger.debug("Completed create pattern dataset [ID : {}]".format(save_day))

        


def savePatternData(pattern, pattern_info, newPattern, newPattern_info, save_day, cfg, masterYN):
    creationDate = util.getToday(True, consts.DATETIME)
    logger.debug("Uploading result dataset ... [ID : {}]".format(save_day))

    pattern_json = {}
    pattern_json['pattern_data'] = pattern
    pattern_json['pattern_data']['createDate'] = creationDate

    pattern_info_json = {}
    pattern_info_json['pattern_info'] = pattern_info
    pattern_info_json['pattern_info']['createDate'] = creationDate


    #### 데이터 저장 #####
    pattern_url = cfg['API']['url_post_pattern_data']   # 'TEST' #save_day
    requests.post(pattern_url + save_day, json=pattern_json)

    pattern_info_url = cfg['API']['url_post_pattern_info']
    requests.post(pattern_info_url + save_day, json=pattern_info_json)

    if masterYN is False:
        print("master save")
        requests.post(pattern_url+consts.ATTR_MASTER_ID, json=pattern_json)
        requests.post(pattern_info_url+consts.ATTR_MASTER_ID, json=pattern_info_json)
    else:
        logger.debug("inserted new pattern data : {}".format(newPattern_info))
        url_pd_update = cfg['API']['url_update_pattern_data'].format(consts.ATTR_MASTER_ID)
        url_pi_update = cfg['API']['url_update_pattern_info'].format(consts.ATTR_MASTER_ID)
        requests.post(url_pd_update, json=newPattern)
        requests.post(url_pi_update, json=newPattern_info)




# ##### 초기 데이터 처리 ######
def preprocessData(node_id, s_date, e_date, cfg):
    # 학습데이터 로드
    logger.debug("Trainnig data loading ...")
    dataset = ad_dataConvert.loadJsonData(node_id, s_date, e_date, cfg)

    if dataset is not None:
        # 데이터 전처리(결측치 처리, 구간화, 디폴트값)
        logger.debug("Data preprocessing using multiprocessing ...")
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
def createPatternData(dataset, master_data, master_info, save_day, cfg):
    procs, col_list = [], []
    pdQ, piQ, npdQ, npiQ = {}, {}, {}, {}
    # pattern data, pattern info, new pattern data, new pattern info
    pData, pInfo, npData, npInfo = {}, {}, {}, {}
    logger.debug("create pattern data for each factors using multiprocessing ...")
    for col_name in dataset.columns:
        pdQ[col_name], piQ[col_name], npdQ[col_name], npiQ[col_name] = Queue(), Queue(), Queue(), Queue()
        col_list.append(col_name)

        if master_data is not None:
            procs.append(Process(target=clusteringSegment,
                args=(dataset[col_name], master_data[col_name],
                    master_info[col_name], col_name, save_day,
                    pdQ[col_name], piQ[col_name], npdQ[col_name], npiQ[col_name])))
        else:
            procs.append(Process(target=clusteringSegment,
                args=(dataset[col_name], master_data,
                    master_info, col_name, save_day,
                    pdQ[col_name], piQ[col_name], npdQ[col_name], npiQ[col_name])))

    for p in procs:
        p.start()

    for col_name in col_list:
        # fact_pattern = pdQ[col_name].get()
        # fact_info = piQ[col_name].get()
        # new_pattern = npdQ[col_name].get()
        # new_info = npiQ[col_name].get()

        pData[col_name] = pdQ[col_name].get()
        pInfo[col_name] = piQ[col_name].get()
        npData[col_name] = npdQ[col_name].get()
        npInfo[col_name] = npiQ[col_name].get()

        pdQ[col_name].close()
        piQ[col_name].close()
        npdQ[col_name].close()
        npiQ[col_name].close()

    for proc in procs:
        proc.join()

    return pData, pInfo, npData, npInfo


# ##### 속성별 클러스터링 usint K-Means and DTW algorithm #####
def clusteringSegment(dataset, master_data, master_info, col_name, save_day, pdQ, piQ, npdQ, npiQ):
    clusterer = KMeans(n_clusters=consts.ATTR_N_CLUSTER)

    logger.debug("extract all segment for [{}]".format(col_name))
    segments = extractSegment(dataset, col_name, consts.ATTR_WIN_LEN, consts.ATTR_SLIDE_LEN)

    logger.debug("Run clustering about segments of [{}]".format(col_name))
    clusted_segments = clusterer.fit(segments)
    clusted_df = pd.DataFrame(clusted_segments.cluster_centers_)

    # index rename
    for i in range(len(clusted_df.index)):
        clusted_df = clusted_df.rename(index={i: "cluster_{:03}".format(i)})

    logger.debug("Convert to labeled DataFrame for [{}]".format(col_name))
    labels_df = pd.DataFrame(clusted_segments.labels_)
    labels_df = labels_df.rename(columns={0: "cluster"})
    segment_df = pd.DataFrame(segments)
    lbl_dataset = pd.concat([segment_df, labels_df], axis=1)

    logger.debug("Compute boundary threshold for [{}]".format(col_name))
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
        fact_pattern[col]['creationDate'] = save_day

    pdQ.put(fact_pattern)
    logger.debug("Completed clustering for [{}]".format(col_name))

    # #### matching ####
    logger.debug("pattern matching with master pattern for [{}]".format(col_name))
    info_pattern = {}  # information about clustered pattern
    new_pattern = {}
    new_info = {}

    if master_data is not None:
        master_df = pd.DataFrame()
        for cno in master_data.keys():
            master_df[cno] = pd.Series(master_data[cno]['center']).values

        max_clustNo = int(heapq.nlargest(1,master_df.columns)[0].split('_')[1])

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
                info_pattern[clustNo] = {}
                info_pattern[clustNo]["status"] = master_info[min_dist[0]]["status"]
                info_pattern[clustNo]["masterCN"] = min_dist[0]
                info_pattern[clustNo]["createDate"] = save_day
                info_pattern[clustNo]["updateDate"] = save_day

            else:
                info_pattern[clustNo] = {}
                info_pattern[clustNo]["status"] = "undefined"
                info_pattern[clustNo]["masterCN"] = "unknown"
                info_pattern[clustNo]["createDate"] = save_day
                info_pattern[clustNo]["updateDate"] = save_day

                max_clustNo += 1
                new_pattern["cluster_{:03}".format(max_clustNo)] = fact_pattern[clustNo]
                new_info["cluster_{:03}".format(max_clustNo)] = {}
                new_info["cluster_{:03}".format(max_clustNo)]["status"] = "undefined"
                new_info["cluster_{:03}".format(max_clustNo)]["masterCN"] = "unknown"
                new_info["cluster_{:03}".format(max_clustNo)]["createDate"] = save_day
                new_info["cluster_{:03}".format(max_clustNo)]["updateDate"] = save_day
                #new_pattern[col_name]["cluster_{:03}".format(max_clustNo)] = "test"

        piQ.put(info_pattern)
        npdQ.put(new_pattern)
        npiQ.put(new_info)

    else:
        for clustNo in center_df.columns:
            info_pattern[clustNo] = {}
            info_pattern[clustNo]["status"] = "undefined"
            info_pattern[clustNo]["masterCN"] = "unknown"
            info_pattern[clustNo]["createDate"] = save_day
            info_pattern[clustNo]["updateDate"] = save_day

        piQ.put(info_pattern)
        npdQ.put(new_pattern)
        npiQ.put(new_info)


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
                if lower < 0 : lower = 0
                lower_list.append(lower)
                max_value = df[i].max()
                max_list.append(max_value)
                upper = np.mean(df[i]) + np.std(df[i])
                upper_list.append(upper)

        min_dict["cluster_{:03}".format(cno)] = min_list
        max_dict["cluster_{:03}".format(cno)] = max_list
        lower_dict["cluster_{:03}".format(cno)] = lower_list
        upper_dict["cluster_{:03}".format(cno)] = upper_list

    min_df = pd.DataFrame(min_dict)
    max_df = pd.DataFrame(max_dict)
    lower_df = pd.DataFrame(lower_dict)
    upper_df = pd.DataFrame(upper_dict)

    return min_df, max_df, lower_df, upper_df


# ##### 스크립트 직접 실행 시 #####
if __name__ == '__main__':
    freeze_support()

    # from ad_logger import getAdLogger
    # logger = getAdLogger()

    url = cfg['API']['url_get_pattern_data'] + consts.ATTR_MASTER_ID
    print(url)
    resp = requests.get(url)
    import json
    dataset = json.loads(resp.text)
    
    if dataset['rtnCode']['code'] == '0000':
        logger.debug("reload master pattern")
        master_data = dataset['rtnData']['pattern_data']
        print("there is data")
    else:
        master_data = None

    main('0002.00000039', '2017-10-08T00:00:00Z', '2017-11-07T02:00:00Z', master_data)