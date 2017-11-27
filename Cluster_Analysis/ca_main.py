import socket
from threading import Thread
import ca_clustering
import logging
import consts
import util

logger = logging.getLogger(consts.LOGGER_NAME['CA'])
threads = []


# Multithreaded Python server : TCP Server Socket Thread Pool
class CaSocketThread(object):

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

        logger.debug("start json parsing ....")
        dataDecode = data.decode("utf-8")
        json_dict = eval(dataDecode) # dictionary type
        print(json_dict)
        if set(('sDate', 'eDate', 'tInterval')) <= set(json_dict):
            if 'None' not in json_dict.values():
                sDate = json_dict['sDate']
                eDate = json_dict['eDate']
                tInterval = json_dict['tInterval']
                print(sDate, eDate, tInterval)
                logger.debug("Start clustering analysis")
                ca_clustering.main(sDate, eDate, tInterval)

        else:
            logger.warn("Message format is incorrect")



if __name__ == '__main__':
    # CaSocketThread(consts.LOCAL_HOST, consts.PORT).listen()
    data = b'{"sDate": "2017-11-21T00:00:00", "eDate": "2017-11-22T00:00:00", "tInterval": 15}'
    CaSocketThread(consts.LOCAL_HOST, consts.PORT).jsonParsing(data)