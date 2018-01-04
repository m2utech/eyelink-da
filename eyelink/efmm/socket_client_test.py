# CLIENT
# coding: utf-8
import socket

host = 'm2u-da.eastus.cloudapp.azure.com'
#HOST = 'DataAnalyzer'
port = 5224     # 포트지정

def sendData(jobcode, esIndex, docType, sDate, eDate, tInterval, cid, nCluster):
    sendData = {
        "type": jobcode,
        "esIndex": esIndex,
        "docType": docType,
        "sDate": sDate,
        "eDate": eDate,
        "tInterval": tInterval,
        "cid": cid,
        "nCluster": nCluster
    }
    sendData = str(sendData).encode()
    print(sendData)
    sendMessage(sendData)


def sendMessage(sendData):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(sendData)
    print("send")
    s.close()
#############################


if __name__ == '__main__':
    sendData('pattern', 'notching', 'oee', '2017-12-25T09:00:00', '2017-12-26T09:00:00', '30S', 'all',50)