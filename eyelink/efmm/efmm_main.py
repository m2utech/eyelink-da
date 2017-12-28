import socket
from threading import Thread
import logging
import logging.handlers

import common_modules
import da_elasticsearch as efmm_es
import da_query as efmm_query
import da_util as util
import da_config as config
import da_consts as consts

import ad_clustering
import ad_matching
import ca_clustering


NOTCHING_MASTER = None
STACKING_MASTER = None
NOTCHING_CODE = 0
STACKING_CODE = 0
DA_INDEX = config.da_index

logger = logging.getLogger(config.logger_name['efmm'])
threads = []


# Multithreaded Python server : TCP Server Socket Thread Pool
class EfmmSocketThread(object):
    def __init__(self, host, port):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen()
        while True:
            client, address = self.sock.accept()
            logger.debug("New ad-socket thread started for {}:{}".format(address[0], address[1]))
            client.settimeout(consts.CONN_TIMEOUT)
            newthread = Thread(target=self.listen2Client, args=(client, address))
            newthread.start()
            threads.append(newthread)
        for t in threads:
            t.join()

    def listen2Client(self, client, address):
        while True:
            try:
                data = client.recv(consts.BUFFER_SIZE)
                if data:
                    logger.debug("received data from socket: {}".format(data))
                    self.jsonParsing(data)
                    response = data
                    client.send(response)
                else:
                    raise socket.error
            except socket.error:
                client.close()
                return False

    # 소켓 메시지 파싱
    def jsonParsing(self, data):
        global NOTCHING_MASTER
        global STACKING_MASTER
        global NOTCHING_CODE
        global STACKING_CODE

        logger.debug("received message parsing ....")
        dataDecode = data.decode("utf-8")
        json_dict = eval(dataDecode) # dictionary type
        print(json_dict)

        # message set check
        if set(('type', 'esIndex', 'docType', 'sDate', 'eDate', 'tInterval', 'cid', 'nCluster')) <= set(json_dict):
            if 'None' not in json_dict.values():
                esIndex = json_dict['esIndex']
                docType = json_dict['docType']
                sDate = json_dict['sDate']
                eDate = json_dict['eDate']
                tInterval = json_dict['tInterval']
                cid = json_dict['cid']
                nCluster = json_dict['nCluster']
                # check dateformat and convert UTC datetime
                sDate = util.checkDatetime(sDate, consts.DATETIME)
                eDate = util.checkDatetime(eDate, consts.DATETIME)


                ##### Create Patterns #####
                if json_dict["type"] == "pattern":
                    self.loadMasterPattern(esIndex, docType)
                    self.createPattern(esIndex, docType, sDate, eDate, tInterval)
                    self.loadMasterPattern(esIndex, docType)
               
                ##### Pattern Matching #####
                elif json_dict["type"] == "matching":
                    if esIndex == 'notching':
                        if NOTCHING_CODE is 1:
                            self.matchPattern(esIndex, docType, sDate, eDate, tInterval)
                        else:
                            self.loadMasterPattern(esIndex, docType)
                            if NOTCHING_CODE is 1:
                                self.matchPattern(esIndex, docType, sDate, eDate, tInterval)
                            else:
                                new_sDate, new_eDate = util.getStartEndDateByDay(1, True, consts.DATETIME)
                                self.createPattern(esIndex, docType, new_sDate, new_eDate, tInterval)
                                self.loadMasterPattern(esIndex, docType)
                                self.matchPattern(esIndex, docType, sDate, eDate, tInterval)
                    elif esIndex == 'stacking':
                        if STACKING_CODE is 1:
                            self.matchPattern(esIndex, docType, sDate, eDate, tInterval)
                        else:
                            self.loadMasterPattern(esIndex, docType)
                            if STACKING_CODE is 1:
                                self.matchPattern(esIndex, docType, sDate, eDate, tInterval)
                            else:
                                new_sDate, new_eDate = util.getStartEndDateByDay(1, True, consts.DATETIME)
                                self.createPattern(esIndex, docType, new_sDate, new_eDate, tInterval)
                                self.loadMasterPattern(esIndex, docType)
                                self.matchPattern(esIndex, docType, sDate, eDate, tInterval)
                    else:
                        logger.warn("Sensor type is invalid, please check sensor type ...")

                ##### Clustering Analysis #####
                elif json_dict["type"] == "clustering":
                    ca_clustering.main(esIndex, docType, sDate, eDate, tInterval, cid, nCluster)
                else:
                    logger.warn("The type is invalid")
            else:
                logger.warn("Any key has a None value. please check message data")
        else:
            logger.warn("Message format is incorrect")

    def loadMasterPattern(self, esIndex, docType):
        global NOTCHING_MASTER
        global STACKING_MASTER
        global NOTCHING_CODE
        global STACKING_CODE
        query = efmm_query.getDataById(config.AD_opt['masterID'])
        dataset = efmm_es.getDataById(DA_INDEX[esIndex][docType]['PD']['INDEX'],
                                        DA_INDEX[esIndex][docType]['PD']['TYPE'],
                                        query, config.AD_opt['masterID'])
        if dataset is not None:
            logger.debug("reload latest master pattern ....")
            if esIndex == 'notching':
                NOTCHING_MASTER = dataset
                NOTCHING_CODE = 1
            elif esIndex == 'stacking':
                STACKING_MASTER = dataset
                STACKING_CODE = 1
            else:
                logger.warn("Sensor type is invalid, please check sensor type ...")
        else:
            logger.debug("master pattern is None ....")
            if esIndex == 'notching':
                NOTCHING_MASTER = None
                NOTCHING_CODE = 0
            elif esIndex == 'stacking':
                STACKING_MASTER = None
                STACKING_CODE = 0
            else:
                logger.warn("Sensor type is invalid, please check sensor type ...")

    def createPattern(self, esIndex, docType, sDate, eDate, tInterval):
        logger.debug("==== Start pattern generation from [{}] to [{}] ====".format(sDate, eDate))
        if esIndex == 'notching':
            ad_clustering.main(esIndex, docType, sDate, eDate, NOTCHING_MASTER, tInterval)
        elif esIndex == 'stacking':
            ad_clustering.main(esIndex, docType, sDate, eDate, STACKING_MASTER, tInterval)

    def matchPattern(self, esIndex, docType, sDate, eDate, tInterval):
        logger.debug("==== Start pattern matching from [{}] to [{}] ====".format(sDate, eDate))
        if esIndex == 'notching':
            ad_matching.main(esIndex, docType, sDate, eDate, NOTCHING_MASTER, tInterval)
        elif esIndex == 'stacking':
            ad_matching.main(esIndex, docType, sDate, eDate, STACKING_MASTER, tInterval)


######################################
if __name__ == '__main__':
    data = b'{"type": "clustering", "esIndex": "stacking", "docType": "status", "sDate": "2017-12-18T00:00:00", "eDate": "2017-12-18T01:00:00", "tInterval": 5}'
    EfmmSocketThread(consts.LOCAL_HOST, consts.PORT).jsonParsing(data)
