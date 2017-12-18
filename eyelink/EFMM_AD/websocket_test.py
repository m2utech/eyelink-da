from socketIO_client import SocketIO
import consts
import util
from datetime import datetime

def return_message(arg):
    print('returnData', arg)

timestamp = util.getToday(True, consts.DATETIME) + 'Z'

sendData = {}
sendData['applicationType'] = consts.APP_TYPE
sendData['agentId'] = consts.AGENT_ID
sendData['timestamp'] = timestamp
sendData['alarmType'] = consts.ALARM_TYPE
sendData['alarmTypeName'] = consts.ALARM_TYPE_NAME
sendData['message'] = 'Anomaly expected in {} factor'.format('mPlus OEE')

socketIO = SocketIO('http://m2utech.eastus.cloudapp.azure.com', 5224)

socketIO.emit('receiveAlarmData', sendData)
socketIO.on('returnAlarmData', return_message)
socketIO.wait(seconds=1)

print(sendData)