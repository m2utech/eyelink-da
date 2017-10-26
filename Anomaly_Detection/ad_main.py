import socket
from threading import Thread
import json
import requests

from ad_configParser import getConfig
import ad_clustering
import ad_matching
import logging
import logging.handlers
import consts
import util


MASTER_DATA = None
PATTERN_CODE = 0

logger = logging.getLogger(consts.LOGGER_NAME['AD'])
cfg = getConfig()

threads = []


## Multi-thread ##
class AdSocketThread(object):

    def __init__(self, host, port):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen()
        print('The ad-server is ready to receive')
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
                print("received data from socket: {}".format(data))
                if data:
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
        global MASTER_DATA
        global PATTERN_CODE

        logger.debug("received json and parsing start ....")
        dataDecode = data.decode("utf-8")
        json_dict = eval(dataDecode) # dictionary type
        #json_dict = data

        # message set check
        if set(('type', 'node_id', 's_date', 'e_date')) <= set(json_dict):
            if 'None' not in json_dict.values():
                logger.debug("start anomaly detection")
                node_id = json_dict['node_id']
                # convert UTC datetime
                s_date = util.getLocalStr2Utc(json_dict['s_date'], consts.DATETIMEZERO)
                e_date = util.getLocalStr2Utc(json_dict['e_date'], consts.DATETIMEZERO)
                
                if json_dict["type"] == "pattern":
                    if PATTERN_CODE is 1:
                        self.createPattern(node_id, s_date, e_date)
                    else:
                        self.checkMasterPattern()
                        self.createPattern(node_id, s_date, e_date)

                elif json_dict["type"] == "matching":
                    if PATTERN_CODE is 1:
                        self.matchPattern(node_id, s_date, e_date)
                    else:
                        self.checkMasterPattern()
                        if PATTERN_CODE is 1:
                            self.matchPattern(node_id, s_date, e_date)
                        else:
                            new_s_date, new_e_date = util.getStartEndDateByDay(consts.TIME_RANGE['DAY'], True, consts.DATETIME)
                            self.createPattern(node_id, new_s_date, new_e_date)
                            self.checkMasterPattern()
                            self.matchPattern(node_id, s_date, e_date)
                else:
                    logger.warning("The type is invalid")
            else:
                logger.warn("Any key has a None value. please check message")
        else:
            logger.warn("Message format is incorrect")

    def checkMasterPattern(self):
        global MASTER_DATA
        global PATTERN_CODE
        # master data load..
        url = cfg['API']['url_get_pattern_data'] + consts.ATTR_MASTER_ID
        resp = requests.get(url)
        dataset = json.loads(resp.text)

        if dataset['rtnCode']['code'] == '0000':
            logger.debug("reload master pattern")
            MASTER_DATA = dataset['rtnData']['pattern_data']
            PATTERN_CODE = 1
        else:
            MASTER_DATA = None
            PATTERN_CODE = 0

    # 패턴데이터 생성
    def createPattern(self, node_id, s_date, e_date):
        logger.debug("====== Start creating pattern dataset ======")
        logger.debug("[node-id:{0} | start-date:{1} | end-date:{2}]".format(node_id, s_date, e_date))
        #pattern_dataset = ad_clustering.main(node_id, s_date, e_date)
        ad_clustering.main(node_id, s_date, e_date, MASTER_DATA)
        logger.debug("====== Completed creating pattern dataset ======")

    # 패턴 매칭
    def matchPattern(self, node_id, s_time, e_time):
        logger.debug("====== Start pattern matching ======")
        logger.debug("[node-id:{0} | s_time:{1} | e_time:{2}]".format(node_id, s_time, e_time))
        ad_matching.main(node_id, s_time, e_time, MASTER_DATA)
        logger.debug("====== Completed pattern matching ======")


if __name__ == '__main__':
    AdSocketThread(consts.LOCAL_HOST, consts.PORT).listen()
