import elasticsearch
from elasticsearch.helpers import scan
import pandas as pd
import logging
import da_config as config
import da_consts as consts

logger = logging.getLogger(config.logger_name['efmm'])
es = elasticsearch.Elasticsearch(config.es_opt['url'])
scroll_time = config.es_opt['scroll_time']
scroll_size = config.es_opt['scroll_size']


def getOeeData(index, docType, body):
    dataset = []
    docs = es.search(index=index, doc_type=docType, body=body, scroll=scroll_time, size=scroll_size)
    scroll_id = docs['_scroll_id']
    while len(docs['hits']['hits']) > 0:
        for item in docs['hits']['hits']:
            for element in item['_source']['data']:
                data = element
                data['cid'] = item['_source']['cid']
                dataset.append(data)
        docs = es.scroll(scroll_id=scroll_id, scroll='1m')
    print("clear_scroll")
    es.clear_scroll(body={'scroll_id': scroll_id})
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
    ind = config.AD_opt['index']
    dataset = pd.DataFrame(dataset)
    dataset[ind] = pd.to_datetime(dataset[ind], format=consts.PY_DATETIME)
    dataset = dataset.set_index(config.AD_opt['index'])
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
    pass