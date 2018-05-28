import socket
from threading import Thread

from ad_configParser import getConfig
import logging
import logging.handlers
import consts


cfg = getConfig()

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
            client.settimeout(60)
            Thread(target=self.listen2Client, args=(client,address)).start()

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
    def jsonParsing(self,data):

        print(data)
        print("received json and parsing start ....")

# /// end of class /// #


if __name__ == '__main__':
    AdSocketThread(consts.HOST, consts.PORT).listen()
