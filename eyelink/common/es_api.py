import elasticsearch
from elasticsearch.helpers import scan
import pandas as pd
import logging
import common_modules
from config import config
from consts import consts

logger = logging.getLogger(config.logger_name['efmm'])
es = elasticsearch.Elasticsearch(config.es_opt['url'], timeout=300)
scroll_time = config.es_opt['scroll_time']
scroll_size = config.es_opt['scroll_size']


def getOeeData(index, docType, body):
    dataset = []
    scroller = scan(es, body, index=index, doc_type=docType, scroll=scroll_time, size=scroll_size)
    for doc in scroller:
        for element in doc['_source']['data']:
            data = element
            data['cid'] = doc['_source']['cid']
            dataset.append(data)
    dataset = dataConvert(dataset)
    return dataset


def getStatusData(index, docType, body):
    dataset = []
    scroller = scan(es, body, index=index, doc_type=docType, scroll=scroll_time, size=scroll_size)
    for doc in scroller:
        for element in doc['_source']['data']:
            data = element
            data['cid'] = doc['_source']['cid']
            dataset.append(data)
    dataset = statusDataConvert(dataset)
    return dataset


def dataConvert(dataset):
    if not dataset:
        dataset = None
    else:
        ind = config.AD_opt['index']
        dataset = pd.DataFrame(dataset)
        dataset[ind] = pd.to_datetime(dataset[ind], format=consts.PY_DATETIME)
        dataset = dataset.set_index(ind)
    return dataset


def statusDataConvert(dataset):
    if not dataset:
        dataset = None
    else:
        ind = config.CA_opt['index']
        dataset = pd.DataFrame(dataset)
        dataset[ind] = pd.to_datetime(dataset[ind], format=consts.PY_DATETIME)
        dataset = dataset.set_index(ind)
    return dataset


def getDataById(index, docType, body, masterId):
    check = es.exists_source(index=index, doc_type=docType, id=masterId)
    if check is True:
        doc = es.search(index=index, doc_type=docType, body=body)
        doc = doc['hits']['hits'][0]['_source']
        return doc
    else:
        doc = None
        logger.warn("dataset does not exist")
        return doc


def insertDataById(index, docType, sid, body):
    check = es.exists_source(index=index, doc_type=docType, id=sid)
    if check is False:
        es.index(index=index, doc_type=docType, id=sid, body=body)
        logger.info("data inserted successfully")
    else:
        logger.info("The same ID already exists.")


def updateDataById(index, docType, sid, body):
    check = es.exists_source(index=index, doc_type=docType, id=sid)
    if check is True:
        updateBody = {"doc": body}
        es.update(index=index, doc_type=docType, id=sid, body=updateBody)
        logger.info("data updated successfully")
    else:
        logger.info("The ID does not exists.")


if __name__ == '__main__':
    import util as util
    import es_query as efmm_query
    esIndex = 'notching'
    docType = 'oee'
    sDate = "2017-12-26T00:00:00Z"
    eDate = "2017-12-27T00:00:00Z"
    efmm_index = config.efmm_index[esIndex][docType]['INDEX']
    idxList = util.getIndexDateList(efmm_index+'-', sDate, eDate, consts.DATE)
    body = efmm_query.getOeeDataByRange(sDate, eDate)
    logger.debug("[AD] INDEX : {} | QUERY: {}".format(idxList, body))
    dataset = getOeeData(idxList, docType, body)
    print(dataset)
