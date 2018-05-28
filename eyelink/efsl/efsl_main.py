import socket
from threading import Thread
import daemon

import insertPkgPath
import logging
import logging.handlers
from common import es_api
from common import es_query
from config import efsl_config as config
from consts import consts
from common import util

import ad_clustering
import ad_matching
import ca_clustering


MASTER = None
CODE = 0
DA_INDEX = config.es_index


# Multithreaded Python server : TCP Server Socket Thread Pool
class server_forever(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))

    def listen(self):
        logger.info("Started main socket server for efsl ...")
        self.server.listen(1)
        while True:
            client, address = self.server.accept()
            logger.debug("New ad-socket thread started for {}:{}".format(address[0], address[1]))

            newthread = Thread(target=self.listen2Client, args=[client])
            newthread.daemon = True
            newthread.start()


    def listen2Client(self, client):
        # while True:
        try:
            data = client.recv(consts.BUFFER_SIZE)
            if data:
                response = data
                client.send(response)
                client.close()
                logger.debug("received data from socket: {}".format(data))
                self.jsonParsing(data)
            else:
                raise socket.error
        except socket.error:
            client.close()
            return False

    # 소켓 메시지 파싱
    def jsonParsing(self, data):
        global MASTER, CODE

        logger.debug("received message parsing ....")
        dataDecode = data.decode("utf-8")
        json_dict = eval(dataDecode) # dictionary type
        logger.debug("Received message =>  {}".format(json_dict))

        # message set check
        if {'type', 'esIndex', 'docType', 'sDate', 'eDate', 'tInterval', 'nCluster'} <= set(json_dict):

            if 'None' not in json_dict.values():
                esIndex = json_dict['esIndex']
                docType = json_dict['docType']
                sDate = json_dict['sDate']
                eDate = json_dict['eDate']
                tInterval = json_dict['tInterval']
                nCluster = json_dict['nCluster']
                # check dateformat and convert UTC datetime
                sDate = util.checkDatetime(sDate, consts.DATETIME)
                eDate = util.checkDatetime(eDate, consts.DATETIME)

                logger.debug("Check dateformat and convert UTC time => [sDate: {}, eDate: {}]".format(sDate, eDate))

                ##### Create Patterns #####
                if json_dict["type"] == "pattern":
                    self.loadMasterPattern(esIndex, docType)
                    self.createPattern(esIndex, docType, sDate, eDate, tInterval)
                    self.loadMasterPattern(esIndex, docType)
                ##### Pattern Matching #####
                elif json_dict["type"] == "matching":
                    if esIndex == 'corecode':
                        if CODE is 1:
                            self.matchPattern(esIndex, docType, sDate, eDate, tInterval)
                        else:
                            self.loadMasterPattern(esIndex, docType)
                            if CODE is 1:
                                self.matchPattern(esIndex, docType, sDate, eDate, tInterval)
                            else:
                                new_sDate, new_eDate = utils.getStartEndDateByDay(1, True, consts.DATETIME)
                                self.createPattern(esIndex, docType, new_sDate, new_eDate, tInterval)
                                self.loadMasterPattern(esIndex, docType)
                                self.matchPattern(esIndex, docType, sDate, eDate, tInterval)
                    else:
                        logger.warn("index type is invalid, please check index type ...")
                ##### Clustering Analysis #####
                elif json_dict["type"] == "clustering":
                    ca_clustering.main(esIndex, docType, sDate, eDate, tInterval, nCluster)
                else:
                    logger.warn("The type is invalid")
            else:
                logger.warn("Any key has a None value. please check message data")
        else:
            logger.warn("Message format is incorrect")


    def loadMasterPattern(self, esIndex, docType):
        global MASTER, CODE
        query = es_query.getDataById(config.AD_opt['masterID'])
        dataset = es_api.getDataById(DA_INDEX[esIndex][docType]['PD']['INDEX'],
                                     DA_INDEX[esIndex][docType]['PD']['TYPE'],
                                     query, config.AD_opt['masterID'])
        if dataset is not None:
            logger.debug("reload latest master pattern ....")
            if esIndex == 'corecode':
                MASTER = dataset
                CODE = 1
            else:
                logger.warn("index type is invalid, please check index type ...")
        else:
            logger.debug("master pattern is None ....")
            if esIndex == 'corecode':
                MASTER = None
                CODE = 0
            else:
                logger.warn("index type is invalid, please check index type ...")


    def createPattern(self, esIndex, docType, sDate, eDate, tInterval):
        logger.debug("==== Start pattern generation from [{}] to [{}] ====".format(sDate, eDate))
        ad_clustering.main(esIndex, docType, sDate, eDate, MASTER, tInterval)

    def matchPattern(self, esIndex, docType, sDate, eDate, tInterval):
        logger.debug("==== Start pattern matching from [{}] to [{}] ====".format(sDate, eDate))
        ad_matching.main(esIndex, docType, sDate, eDate, MASTER, tInterval)


######################################
if __name__ == '__main__':
    product = consts.PRODUCTS['efsl']
    ### logging info ###
    LOG = config.log_opt
    logger = logging.getLogger(LOG["name"])
    formatter = logging.Formatter(LOG["format"])
    fileHandler = logging.handlers.RotatingFileHandler(LOG["file"], maxBytes=LOG["fileSize"],
                                                       backupCount=LOG["backupCnt"])
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.getLevelName(LOG["level"]))

    context = daemon.DaemonContext()
    log_fileno = fileHandler.stream.fileno()
    context.files_preserve = [log_fileno]
    with context:
        server_forever(product['host'], product['port']).listen()