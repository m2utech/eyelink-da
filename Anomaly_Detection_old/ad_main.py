import socket
from threading import Thread
import json
import datetime
from dateutil.relativedelta import relativedelta
import requests
# import time
from config_parser import cfg
# import ad_logger as adLogging
import ad_clustering
import ad_matching
import data_convert

import logging
import logging.handlers

pattern_dataset = None
# ### status code ###
PATTERN_CODE = 0
#MATCH_CODE = 1

logger = logging.getLogger("ad-daemon")


# ##### class ######
class ClientThread(Thread):

    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        #self.logger = adLogging.get_daemon_logger()
        logger.info("New ad-server socket thread started for" + ip + ":" + str(port))

    # 소켓 메시지 파싱
    def json_parsing(data):

        global pattern_dataset
        global PATTERN_CODE
        global MATCH_CODE
        # running time check
        logger.info("received json and parsing start ....")

        json_dict = json.loads(data.decode("utf-8")) # dictionary type
        #print(json_dict)

        if json_dict["type"] == "pattern":
            PATTERN_CODE = 1;
            node_id = json_dict['node_id']
            s_date = json_dict['s_date']
            e_date = json_dict['e_date']
            ClientThread.create_pattern(node_id, s_date, e_date)

        elif json_dict["type"] == "matching":
            if PATTERN_CODE == 1:
                logger.warning("Now, Pattern dataset is being generated ... wait")
            
            else:
                if pattern_dataset is None:
                    logger.info("Check pattern dataset...")

                    today = datetime.datetime.today()
                    pattern_id = today.strftime('%Y-%m-%d')
                    url = cfg['SERVER']['pattern_dataset_url'] + pattern_id
                    logger.info(url)
                    resp = requests.get(url)
                    dataset = json.loads(resp.text)

                    if dataset['rtnCode']['code'] == '0001':
                        logger.info("There is no loaded pattern dataset...")
                        logger.info("Create pattern dataset...")
                        node_id = json_dict['node_id']
                        s_date = (today - relativedelta(months=1)).strftime('%Y-%m-%d')
                        e_date = today.strftime('%Y-%m-%d')
                        ClientThread.create_pattern(node_id, s_date, e_date)
                       
                        pattern_dataset = data_convert.pattern_data_load(pattern_id)
                        
                        if pattern_dataset is None:
                            logger.info("Target data is None ...")
                        else: 
                            ClientThread.matching_pattern(json_dict)
                    else:
                        pattern_dataset = dataset['rtnData']['pattern_data']
                        ClientThread.matching_pattern(json_dict)

                else:
                    ClientThread.matching_pattern(json_dict)
        else:
            logger.warning("The type is invalid")


    #############
    def create_pattern(node_id, s_date, e_date):
        # 패턴매칭
        global PATTERN_CODE

        logger.info("====== Start creating pattern dataset ======")
        logger.info("[node-id:{0} | start-date:{1} | end-date:{2}]".format(node_id,s_date, e_date))
        #pattern_dataset = ad_clustering.main(node_id, s_date, e_date)
        ad_clustering.main(node_id, s_date, e_date)
        logger.info("====== Completed creating pattern dataset ======")

        PATTERN_CODE = 0
        #MATCH_CODE = 1
    #############

    #############
    def matching_pattern(json_dict):

        node_id = json_dict['node_id']
        s_time = json_dict['s_time']
        e_time = json_dict['e_time']
        logger.info("====== Start pattern matching ======")
        logger.info("[node-id:{0} | s_time:{1} | e_time:{2}]".format(node_id,s_time, e_time))
        ad_matching.main(node_id, s_time, e_time, pattern_dataset)
        logger.info("====== Completed pattern matching ======")

    def run(self):
        while True:
            data = conn.recv(256)
            logger.info("received data from socket: {}".format(data))
            print("received data from socket: {}".format(data))
            if not data:	break
            ClientThread.json_parsing(data)
            #conn.send(b"received analysis success")
# ##### end of class #####


host = cfg['SERVER']['host']
port = int(cfg['SERVER']['port'])
# host = 'DataAnalyzer'
# port = 5228

# logger.info("[%(asctime)s] > before socket")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
threads = []

# logger.info("[%(asctime)s] > after socket")
while True:
    # logger.info("[%(asctime)s] > listen")
    s.listen()
    print('The ad-server is ready to receive')
    # logger.info("connection test")
    (conn, (ip, port)) = s.accept()
    newthread = ClientThread(ip, port)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()


if __name__ == '__main__':
    pass