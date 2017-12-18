def getOeeDataByRange(sDate, eDate):
    body = {
        "size": 100000,
        "_source": ["data.dtSensed", "cid", "data.availability",
            "data.performance", "data.quality", "data.overall_oee"],
        "sort": {"dtTransmitted": "asc"},
        "query": {
            "bool": {
                "filter": {
                    "range": {
                        "dtTransmitted": {"gte": sDate, "lte": eDate}
                    }
                }
            }
        }
    }
    return body

def getDataById(id):
    body = {
        "query": {
            "term": {"_id": id}
        }
    }
    return body

def insertDataById(index, docType, saveID, body):
    # docs = {
    #     "_index": index,
    #     "_type": docType,
    #     "_id": saveID,
    #     '_source': body
    # }
    docs = []
    for cnt in range(10):
        docs.append({
            '_index': index,
            '_type': docType,
            '_id': 'new_id_' + str(cnt),
            '_source': {
                'state': 'NY'
            }
        })
    return docs

if __name__ == '__main__':
    result = getDataById('test')
    print(result)