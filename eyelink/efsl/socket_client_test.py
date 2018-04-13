# CLIENT
# coding: utf-8
import socket

host = 'm2u-da.eastus.cloudapp.azure.com'
#HOST = 'DataAnalyzer'
port = 5225     # 포트지정

def sendData(jobcode, esIndex, docType, sDate, eDate, tInterval, nCluster):
    sendData = {
        "type": jobcode,
        "esIndex": esIndex,
        "docType": docType,
        "sDate": sDate,
        "eDate": eDate,
        "tInterval": tInterval,
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
    sendData('clustering', 'corecode', 'corecode', '2018-04-10T15:00:00', '2018-04-11T14:00:00', 30, 5)