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
                        "dtTransmitted": {"gte": sDate, "lt": eDate}
                    }
                }
            }
        }
    }
    return body


def getStatusDataByRange(sDate, eDate, cid):
    body = {}
    if cid == "all" or cid == "All" or cid == "ALL":
        body = {
            "size": 1000,
            "_source": ["cid", "data"],
            "sort": {"dtTransmitted": "asc"},
            "query": {
                "bool": {
                    "must": {"term": {"sensorType": "motor"}},
                    "filter": {
                        "range": {
                            "dtTransmitted": {"gte": sDate, "lt": eDate}
                        }
                    }
                }
            }
        }
    else:
        body = {
            "size": 100000,
            "_source": ["cid", "data"],
            "sort": {"dtTransmitted": "asc"},
            "query": {
                "bool": {
                    "must": [
                        {"term": {"sensorType": "motor"}},
                        {"term": {"cid": cid}}
                    ],
                    "filter": {
                        "range": {
                            "dtTransmitted": {"gte": sDate, "lt": eDate}
                        }
                    }
                }
            }
        }

    return body


# EFSL raw data
def getCorecodeDataByRange(sDate, eDate):
    body = {
        "_source": ["event_time", "active_power", "ampere", "power_factor", "voltage", "node_id"],
        "sort": {"event_time": {"order": "asc"}},
        "query": {
            "bool": {
                "must": {"match": {"event_type": "1"}},
                "filter": {
                    "range": {
                        "event_time": {"gte": sDate, "lt": eDate}
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