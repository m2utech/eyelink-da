# coding: utf-8
from multiprocessing import Process, Queue, freeze_support
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import heapq
import logging

import common_modules
from common import es_api
from common import es_query
from common import converter
from common import learn_utils
from config import efsl_config as config
from consts import consts
from common import util

logger = logging.getLogger(config.logger_name)
DA_INDEX = config.es_index
MASTER_ID = config.AD_opt['masterID']
DataIndex = config.AD_opt['index']
TimeUnit = config.CA_opt['timeUnit']
MV_method = config.mv_method
node_id = config.AD_opt['node_id']
factors = config.AD_opt['factors']



def main(esIndex, docType, sDate, eDate, masterData, tInterval):
    saveID = util.getToday(True, consts.DATE)
    saveID = saveID.replace('Z', '')
    dataset = getDataset(sDate, eDate, esIndex, docType)
    dataset = preprocessing(dataset, tInterval)
    # dataset is empty
    if not bool(dataset):
        logger.warn("[AD] There is no dataset... skipping analysis")
    else:
        if masterData is not None:
            logger.debug("[AD] load pattern info[ID:{}]".format(MASTER_ID))
            query = es_query.getDataById(MASTER_ID)
            masterInfo = es_api.getDataById(DA_INDEX[esIndex][docType]['PI']['INDEX'], DA_INDEX[esIndex][docType]['PI']['TYPE'], query, MASTER_ID)
            logger.debug("[AD] ### Start create pattern ...")
            pData, pInfo, npData, npInfo = createPatternData(dataset, masterData, masterInfo, saveID)
            logger.debug("[AD] Save result of create pattern ...")
            savePatternData(pData, pInfo, npData, npInfo, saveID, True, esIndex, docType)
        else:
            masterInfo = None
            print("masterInfo is None")
            logger.debug("[AD] ### Start create pattern ...")
            pData, pInfo, npData, npInfo = createPatternData(dataset, masterData, masterInfo, saveID)
            logger.debug("[AD] Save result of create pattern ...")
            savePatternData(pData, pInfo, npData, npInfo, saveID, False, esIndex, docType)

def getDataset(sDate, eDate, esIndex, docType):
    idxList = util.getIndexDateList(esIndex+'-', sDate, eDate, consts.DATE)
    body = es_query.getCorecodeTargetDataByRange(node_id, sDate, eDate)
    logger.debug("[AD] INDEX : {} | QUERY: {}".format(idxList, body))
    dataset = pd.DataFrame()
    for idx in idxList:
        logger.debug("[CA] get dataset about index [{}]".format(idx))
        data = es_api.getCorecodeData(idx, docType, body, DataIndex)
        dataset = dataset.append(data)
    dataset = dataset.sort_index()
    return dataset

# def startAnalysis(dataset, masterData, masterInfo, saveID, tInterval):
#     logger.debug("[AD] Dataset preprocessing ...")
#     dataset = preprocessing(dataset, tInterval)
#     procs = []
#     c_pdQ, c_piQ, c_npdQ, c_npiQ = {}, {}, {}, {}
#     pData, pInfo, npData, npInfo = {}, {}, {}, {}

#     for factor_name in factors:
#         c_pdQ[factor_name], c_piQ[factor_name], c_npdQ[factor_name], c_npiQ[factor_name] = Queue(), Queue(), Queue(), Queue()
#         if masterData is not None:
#             procs.append(Process(
#                 target=createPatternData,
#                 args=(dataset[factor_name],
#                       masterData[factor_name],
#                       masterInfo[factor_name],
#                       saveID,
#                       c_pdQ[factor_name],
#                       c_piQ[factor_name],
#                       c_npdQ[factor_name],
#                       c_npiQ[factor_name]
#                       )
#                 )
#             )
#         else:
#             procs.append(Process(
#                 target=createPatternData,
#                 args=(dataset[factor_name],
#                       masterData,
#                       masterInfo,
#                       saveID,
#                       c_pdQ[factor_name],
#                       c_piQ[factor_name],
#                       c_npdQ[factor_name],
#                       c_npiQ[factor_name]
#                       )
#                 )
#             )
#     for p in procs:
#         p.start()
#     for factor_name in factors:
#         pData[factor_name] = c_pdQ[factor_name].get()
#         pInfo[factor_name] = c_piQ[factor_name].get()
#         npData[factor_name] = c_npdQ[factor_name].get()
#         npInfo[factor_name] = c_npiQ[factor_name].get()
#         c_pdQ[factor_name].close()
#         c_piQ[factor_name].close()
#         c_npdQ[factor_name].close()
#         c_npiQ[factor_name].close()
#     for proc in procs:
#         proc.join()

#     return pData, pInfo, npData, npInfo


def preprocessing(dataset, tInterval):
    output, df = {}, {}
    procs = []
    for factor_name in factors:
        output[factor_name] = Queue()
        procs.append(Process(target=converter.sampling,
            args=(dataset[factor_name], tInterval, MV_method, output[factor_name])))
    for p in procs:
        p.start()
    for factor_name in factors:
        df[factor_name] = output[factor_name].get()
        output[factor_name].close()
    for proc in procs:
        proc.join()

    return df


# factor별 multiprocessing
def createPatternData(dataset, masterData, masterInfo, saveID):
    logger.debug("[AD] create pattern for each factors .... ")
    procs = []
    pdQ, piQ, npdQ, npiQ = {}, {}, {}, {}
    pData, pInfo, npData, npInfo = {}, {}, {}, {}

    for col_name in factors:
        pdQ[col_name], piQ[col_name], npdQ[col_name], npiQ[col_name] = Queue(), Queue(), Queue(), Queue()
        if masterData is not None:
            procs.append(Process(
                target=clusteringSegment,
                args=(dataset[col_name], masterData[col_name], masterInfo[col_name], col_name, saveID,
                      pdQ[col_name], piQ[col_name], npdQ[col_name], npiQ[col_name])))
        else:
            procs.append(Process(
                target=clusteringSegment,
                args=(dataset[col_name], masterData, masterInfo, col_name, saveID,
                      pdQ[col_name], piQ[col_name], npdQ[col_name], npiQ[col_name])))

    for p in procs:
        p.start()

    createDatetime = util.getToday(True, consts.DATETIME)
    for col_name in factors:
        pData[col_name] = pdQ[col_name].get()
        pInfo[col_name] = piQ[col_name].get()
        npData[col_name] = npdQ[col_name].get()
        npInfo[col_name] = npiQ[col_name].get()
        pdQ[col_name].close()
        piQ[col_name].close()
        npdQ[col_name].close()
        npiQ[col_name].close()
        pData['createDatetime'] = createDatetime
        pInfo['createDatetime'] = createDatetime
        npData['createDatetime'] = createDatetime
        npInfo['createDatetime'] = createDatetime

    for proc in procs:
        proc.join()

    return pData, pInfo, npData, npInfo


# ##### 속성별 클러스터링 usint K-Means and DTW algorithm #####
def clusteringSegment(dataset, master_data, master_info, col_name, saveID, pdQ, piQ, npdQ, npiQ):
    clusterer = KMeans(n_clusters=config.AD_opt['n_cluster'])
    logger.debug("[AD] extract all segment for [{}] ....".format(col_name))
    segments = extractSegment(dataset, col_name, config.AD_opt['win_len'], config.AD_opt['slide_len'])
    logger.debug("[AD] segment clustering for [{}] ....".format(col_name))
    clusted_segments = clusterer.fit(segments)
    clusted_df = pd.DataFrame(clusted_segments.cluster_centers_)

    for i in range(len(clusted_df.index)):
        clusted_df = clusted_df.rename(index={i: "cluster_{:03}".format(i)})

    logger.debug("[AD] convert to labeled DataFrame for [{}] ....".format(col_name))
    labels_df = pd.DataFrame(clusted_segments.labels_)
    labels_df = labels_df.rename(columns={0: "cluster"})
    segment_df = pd.DataFrame(segments)
    lbl_dataset = pd.concat([segment_df, labels_df], axis=1)

    logger.debug("[AD] compute boundary threshold for [{}] ....".format(col_name))
    min_df, max_df, lower_df, upper_df = computeThreshold(lbl_dataset, config.AD_opt['n_cluster'])
    pd.options.display.float_format = '{:,.4f}'.format
    clusted_df = clusted_df.apply(lambda x: x.astype(float) if np.allclose(x, x.astype(float)) else x)
    min_df = min_df.apply(lambda x: x.astype(float) if np.allclose(x, x.astype(float)) else x)
    max_df = max_df.apply(lambda x: x.astype(float) if np.allclose(x, x.astype(float)) else x)
    lower_df = lower_df.apply(lambda x: x.astype(float) if np.allclose(x, x.astype(float)) else x)
    upper_df = upper_df.apply(lambda x: x.astype(float) if np.allclose(x, x.astype(float)) else x)
    # replace Nan to zero
    clusted_df = clusted_df.fillna(0.0)
    min_df = min_df.fillna(0.0)
    max_df = max_df.fillna(0.0)
    lower_df = lower_df.fillna(0.0)
    upper_df = upper_df.fillna(0.0)

    center_df = clusted_df.T
    fact_pattern = {}
    for col in center_df.columns:
        fact_pattern[col] = {}
        fact_pattern[col]['max_value'] = max_df[col].tolist()
        fact_pattern[col]['upper'] = upper_df[col].tolist()
        fact_pattern[col]['center'] = center_df[col].tolist()
        fact_pattern[col]['lower'] = lower_df[col].tolist()
        fact_pattern[col]['min_value'] = min_df[col].tolist()
        fact_pattern[col]['creationDate'] = saveID

    pdQ.put(fact_pattern)
    logger.debug("[AD] Completed clustering, and then process pattern matching for [{}]".format(col_name))
    info_pattern, new_pattern, new_info = {}, {}, {}
    if master_data is not None:
        master_df = pd.DataFrame()
        for cno in master_data.keys():
            master_df[cno] = pd.Series(master_data[cno]['center']).values

        max_clustNo = int(heapq.nlargest(1,master_df.columns)[0].split('_')[1])
        for clustNo in center_df.columns:
            distance = {}
            for m_clustNo in master_df.columns:
                cur_dist = learn_utils.DTWDistance(center_df[clustNo], master_df[m_clustNo], 1)
                distance[m_clustNo] = cur_dist

            min_dist = heapq.nsmallest(1, distance, key=distance.get)

            match_len = config.AD_opt['match_len']
            valRange = config.AD_opt['value_range']
            percentile = np.sqrt(((valRange[1] - valRange[0])**2)*match_len) / 100.0
            match_rate = 100.0 - (float(distance[min_dist[0]]) / percentile)

            if match_rate > config.AD_opt['match_rate_threshold']:
                info_pattern[clustNo] = {}
                info_pattern[clustNo]["status"] = master_info[min_dist[0]]["status"]
                info_pattern[clustNo]["masterCN"] = min_dist[0]
                info_pattern[clustNo]["createDate"] = saveID
                info_pattern[clustNo]["updateDate"] = saveID

            else:
                max_clustNo += 1
                info_pattern[clustNo] = {}
                info_pattern[clustNo]["status"] = "undefined"
                info_pattern[clustNo]["masterCN"] = "cluster_{:03}".format(max_clustNo)
                info_pattern[clustNo]["createDate"] = saveID
                info_pattern[clustNo]["updateDate"] = saveID
                new_pattern["cluster_{:03}".format(max_clustNo)] = fact_pattern[clustNo]
                new_info["cluster_{:03}".format(max_clustNo)] = {}
                new_info["cluster_{:03}".format(max_clustNo)]["status"] = "undefined"
                new_info["cluster_{:03}".format(max_clustNo)]["masterCN"] = "unknown"
                new_info["cluster_{:03}".format(max_clustNo)]["createDate"] = saveID
                new_info["cluster_{:03}".format(max_clustNo)]["updateDate"] = saveID

        piQ.put(info_pattern)
        npdQ.put(new_pattern)
        npiQ.put(new_info)

    else:
        for clustNo in center_df.columns:
            info_pattern[clustNo] = {}
            info_pattern[clustNo]["status"] = "undefined"
            info_pattern[clustNo]["masterCN"] = "unknown"
            info_pattern[clustNo]["createDate"] = saveID
            info_pattern[clustNo]["updateDate"] = saveID

        piQ.put(info_pattern)
        npdQ.put(new_pattern)
        npiQ.put(new_info)


# ##### 속성별 세그먼트 추출 #####
def extractSegment(dataset, col_name, window_len, slide_len):
    segment = learn_utils.sliding_chunker(dataset, window_len, slide_len)
    logger.debug("[AD] Produced {} waveform {}-segments".format(len(segment), col_name))
    return segment


# ##### boundary threshold 계산 #####
def computeThreshold(dataset, n_cluster):
    min_dict, max_dict, lower_dict, upper_dict = {}, {}, {}, {}
    for cno in range(n_cluster):
        df = dataset[dataset['cluster'] == cno]
        min_list, max_list, lower_list, upper_list = [], [], [], []
        for i in df.columns:
            if i == "cluster": pass
            else:
                min_value = df[i].min()
                min_list.append(min_value)
                lower = np.mean(df[i]) - (np.std(df[i]))
                if lower < 0: lower = 0
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


def savePatternData(pData, pInfo, npData, npInfo, saveID, masterYN, esIndex, docType):
    es_api.insertDataById(DA_INDEX[esIndex][docType]['PD']['INDEX'], DA_INDEX[esIndex][docType]['PD']['TYPE'], saveID, pData)
    es_api.insertDataById(DA_INDEX[esIndex][docType]['PI']['INDEX'], DA_INDEX[esIndex][docType]['PI']['TYPE'], saveID, pInfo)
    if masterYN is False:
        es_api.insertDataById(DA_INDEX[esIndex][docType]['PD']['INDEX'], DA_INDEX[esIndex][docType]['PD']['TYPE'], MASTER_ID, pData)
        es_api.insertDataById(DA_INDEX[esIndex][docType]['PI']['INDEX'], DA_INDEX[esIndex][docType]['PI']['TYPE'], MASTER_ID, pInfo)
    else:
        logger.debug("[AD] insert new pattern clusters to master patterns ....")
        es_api.updateDataById(DA_INDEX[esIndex][docType]['PD']['INDEX'], DA_INDEX[esIndex][docType]['PD']['TYPE'], MASTER_ID, npData)
        es_api.updateDataById(DA_INDEX[esIndex][docType]['PI']['INDEX'], DA_INDEX[esIndex][docType]['PI']['TYPE'], MASTER_ID, npInfo)


#############################
if __name__ == '__main__':
    freeze_support()
    from common.logger import getStreamLogger
    logger = getStreamLogger()
    esIndex = 'notching'
    docType = 'oee'
    sDate = "2018-01-01T00:00:00Z"
    eDate = "2018-01-01T03:00:00Z"

    # query = es_query.getDataById(config.AD_opt['masterID'])
    # masterData = es_api.getDataById(DA_INDEX[esIndex][docType]['PD']['INDEX'], DA_INDEX[esIndex][docType]['PD']['TYPE'], query, config.AD_opt['masterID'])
    # main(esIndex, docType, sDate, eDate, masterData, '30S')

    esIndex = 'stacking'
    query = es_query.getDataById(config.AD_opt['masterID'])
    masterData = es_api.getDataById(DA_INDEX[esIndex][docType]['PD']['INDEX'], DA_INDEX[esIndex][docType]['PD']['TYPE'], query, config.AD_opt['masterID'])
    main(esIndex, docType, sDate, eDate, masterData, '30S')
