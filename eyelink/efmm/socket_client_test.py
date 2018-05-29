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
    sendData('clustering', 'stacking', 'status', '2018-04-25T00:00:00Z', '2018-04-25T05:00:00Z', 1, 'all',10)