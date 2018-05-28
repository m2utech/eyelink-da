import sys
import logging
import logging.handlers
import config as config
import traceback
from datetime import datetime, timedelta
import elasticsearch
from time import sleep
import pytz


DATETIME = "%Y-%m-%d %H:%M:%S"
DATE = "%Y-%m-%d"
TIME = "%H:%M:%S"
UTC_DT = "%Y-%m-%dT%H:%M:%S"

logger = None
LOOP = False
HOST = 'http://localhost:9200'
TYPE = 'corecode'
es = elasticsearch.Elasticsearch(HOST)
class DataSimulator(object):
    def __init__(self):
        self.datafilepath = sys.argv[2]
        self.nodeId = sys.argv[3]
        self.initialDataInDays = int(0 if sys.argv[4] == None else sys.argv[4])
        self.startDatetimeToSkip = (datetime.now() if sys.argv[5] == None else datetime.strptime(sys.argv[5], DATETIME))

        self.printInfo()

        self.notMatchedCount = 0
        self.matchedCount = 0
        self.curDate = None

        self.initialDateProcessed = False
        self.processedDays = 0

        self.cur_datetime = datetime.now()
        self.prev_month_datetime = (self.cur_datetime - timedelta(days = self.initialDataInDays))
        # print(self.prev_month_datetime)
        self.needNewMapping = True

        # for i in range(3):
        self.readFile()

    def printInfo(self):
        print('=========================================================')
        print('== Data File Path        : {}'.format(self.datafilepath))
        print('== Node ID               : {}'.format(self.nodeId))
        print('== Initial Data In Days  : {}'.format(self.initialDataInDays))
        print('== Start Datetime        : {}'.format(self.startDatetimeToSkip))
        print('=========================================================')

    def readFile(self):

        try:
            with open(self.datafilepath, 'r') as reader:
                for line in reader.readlines():

                    self.matchedCount += 1

                    # self.cur_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cur_datetime = datetime.now()
                    data_arr = line.strip("\n").split(',')
                    event_date = data_arr[3].split(' ')[0]

                    print("####################")
                    print("orginal event_date_time: {}".format(data_arr[3]))

                    if self.curDate == None:
                        self.curDate = event_date
                    if self.curDate != event_date:
                        print("Changing date. curDate: {}, event_date: {}".format(self.curDate, event_date))
                        self.processedDays += 1
                        self.prev_month_datetime = self.prev_month_datetime + timedelta(days=1)
                        self.curDate = event_date

                        if self.processedDays >= self.initialDataInDays:
                            self.initialDateProcessed = True

                        print('=========== {} days passed ============'.format(self.processedDays))

                        self.needNewMapping = True

                    cur_kor_datetime = self.prev_month_datetime.strftime(DATE) + " " + self.cur_datetime.strftime(TIME)

                    data_arr[3] = cur_kor_datetime.split(' ')[0] + 'T' + data_arr[3].split(' ')[1]

                    curDateTime = datetime.strptime(cur_kor_datetime, DATETIME)
                    nextEventDateTime = datetime.strptime(data_arr[3].replace('T', ' '), DATETIME)
                    data_arr[3] = data_arr[3].split('T')[0] + 'T' + nextEventDateTime.strftime(TIME)

                    print("cur_datetime: {}".format(curDateTime.strftime(DATETIME)))
                    print("nextEventDateTime: {}".format(nextEventDateTime.strftime(DATETIME)))
                    print("data_arr[3]: {}".format(data_arr[3]))

                    diffSeconds = (nextEventDateTime - cur_datetime).total_seconds()
                    print("diffSeconds: {}".format(round(diffSeconds)))

                    # if (self.processedDays >= self.initialDataInDays) and ((nextEventDateTime - self.startDatetimeToSkip).total_seconds() > 0):
                    #     print("-------------------------")
                    #     print("Processing data : {}".format(line))
                    #     print("Processing DateTime : {} {}, Next Event DateTime : {}, diffeSeconds : {}".format(event_date, data_arr[3].split('T')[1], nextEventDateTime, diffSeconds))


                    # 로컬 시간을 UTC 시간으로 변경
                    data_arr[3] = self.getDateLocal2UTC(data_arr[3], UTC_DT)

                    if (self.startDatetimeToSkip == None) or (((nextEventDateTime - self.startDatetimeToSkip).total_seconds()) > 0):
                        index = 'corecode-' + cur_kor_datetime.split(' ')[0].replace('-', '.')
                        print("index: {}".format(index))
                        test = self.makeData(index, TYPE, data_arr)

                        if self.needNewMapping:
                            if not es.indices.exists(index):
                                indexSettings = self.indexSetting()
                                es.indices.create(index=index, body=indexSettings)
                            else:
                                print("exist!!!!!!!!!!!!!!!!!!!!!!!!!!")

                            self.needNewMapping = False

                        if diffSeconds <= 0:
                            sleep(0)
                            self.insertData(index, TYPE, data_arr)

                        elif diffSeconds > 0:
                            print("waiting {} seconds .....".format(diffSeconds))
                            sleep(diffSeconds)
                            self.insertData(index, TYPE, data_arr)
                    else:
                        continue

        except IOError:
            traceback.print_exc()

    def insertData(self, index, doc_type, linedata):
        print("Inserting data - index: {}, data : {}".format(index, linedata))
        insertdata = self.makeData(index, doc_type, linedata)
        es.index(index=index, doc_type=doc_type, body=insertdata)

    def makeData(self, index, doc_type, data):
        insertData = {
            "node_id": data[0],
            "event_type": data[1],
            "measure_time": data[2],
            "event_time": data[3],
            "voltage": float(data[4]) if data[4] is not '' else 0,
            "ampere": float(data[5]) if data[5] is not '' else 0,
            "power_factor": float(data[6]) if data[6] is not '' else 0,
            "active_power": float(data[7]) if data[7] is not '' else 0,
            "reactive_power": float(data[8]) if data[8] is not '' else 0,
            "apparent_power": float(data[9]) if data[9] is not '' else 0,
            "amount_of_active_power": float(data[10]) if data[10] is not '' else 0,
            "als_level": int(data[11]) if data[11] is not '' else 0,
            "dimming_level": int(data[12]) if data[12] is not '' else 0,
            "vibration_x": int(data[13]) if data[13] is not '' else 0,
            "vibration_y": int(data[14]) if data[14] is not '' else 0,
            "vibration_z": int(data[15]) if data[15] is not '' else 0,
            "vibration_max": int(data[16]) if data[16] is not '' else 0,
            "noise_origin_decibel": float(data[17]) if data[17] is not '' else 0,
            "noise_origin_frequency": int(data[18]) if data[18] is not '' else 0,
            "noise_decibel": float(data[19]) if data[19] is not '' else 0,
            "noise_frequency": int(data[20]) if data[20] is not '' else 0,
            "gps_longitude": float(data[21]) if data[21] is not '' else 0,
            "gps_latitude": float(data[21]) if data[22] is not '' else 0,
            "gps_altitude": float(data[23]) if data[23] is not '' else 0,
            "gps_satellite_count": int(data[24]) if data[24] is not '' else 0,
            "status_als": int(data[25]) if data[25] is not '' else 0,
            "status_gps": int(data[26]) if data[26] is not '' else 0,
            "status_noise": int(data[27]) if data[27] is not '' else 0,
            "status_vibration": int(data[28]) if data[28] is not '' else 0,
            "status_power_meter": int(data[29]) if data[29] is not '' else 0,
            "status_emergency_led_active": int(data[30]) if data[30] is not '' else 0,
            "status_self_diagnostics_led_active": int(data[31]) if data[31] is not '' else 0,
            "status_active_mode": int(data[32]) if data[32] is not '' else 0,
            "status_led_on_off_type": int(data[33]) if data[33] is not '' else 0,
            "reboot_time": data[34] if data[34] is not '' else 'NULL',
            "event_remain": int(data[35]) if data[35] is not '' else 0
        }
        return insertData


    def getDateLocal2UTC(self, strDate, fm):
        strDate = datetime.strptime(strDate, fm)
        local_tz = pytz.timezone('Asia/Seoul')
        utc_dt = local_tz.localize(strDate).astimezone(pytz.UTC)
        utc_dt = utc_dt.strftime(fm) + 'Z'
        print("utc_dt : {}".format(utc_dt))
        return utc_dt

    def indexSetting(self):
        indexSettings = {
            "settings": {
                "index": {"max_result_window": 100000},
                "index.mapping.total_fields.limit": 100000
            },
            "mappings": {
                "corecode": {
                    "properties": {
                        "node_id": {"type": "text", "index": "true"},
                        "event_type": {"type": "text", "index": "true"},
                        "measure_time": {"type": "text"},
                        "event_time": {"type": "date"},
                        "voltage": {"type": "double"},
                        "ampere": {"type": "double"},
                        "power_factor": {"type": "double"},
                        "active_power": {"type": "double"},
                        "reactive_power": {"type": "double"},
                        "apparent_power": {"type": "double"},
                        "amount_of_active_power": {"type": "double"},
                        "als_level": {"type": "integer"},
                        "dimming_level": {"type": "integer"},
                        "vibration_x": {"type": "integer"},
                        "vibration_y": {"type": "integer"},
                        "vibration_z": {"type": "integer"},
                        "vibration_max": {"type": "integer"},
                        "noise_origin_decibel": {"type": "double"},
                        "noise_origin_frequency": {"type": "integer"},
                        "noise_decibel": {"type": "double"},
                        "noise_frequency": {"type": "integer"},
                        "gps_longitude": {"type": "double"},
                        "gps_latitude": {"type": "double"},
                        "gps_altitude": {"type": "double"},
                        "node_geo": {"type": "geo_point"},
                        "gps_satellite_count": {"type": "integer"},
                        "status_als": {"type": "integer"},
                        "status_gps": {"type": "integer"},
                        "status_noise": {"type": "integer"},
                        "status_vibration": {"type": "integer"},
                        "status_power_meter": {"type": "integer"},
                        "status_emergency_led_active": {"type": "integer"},
                        "status_self_diagnostics_led_active": {"type": "integer"},
                        "status_active_mode": {"type": "integer"},
                        "status_led_on_off_type": {"type": "integer"},
                        "reboot_time": {"type": "text"},
                        "event_remain": {"type": "integer"},
                        "failfirmwareupdate": {"type": "integer"}
                    }
                }
            }
        }
        return indexSettings




def printUsage():
    print('Usage : $ python[version] DataSimulator.py [data source file path] [node id] {days for initial data} {insert start datetime}')
    print('\t  []: required, {}: optional')
    print("Ex.   : $ python3.5 DataSimulator.py ./source.csv B009 30 '2018-01-01 09:00:00'")

def getLogger():
    logger = logging.getLogger(config.logger_name)
    formatter = logging.Formatter(config.log_format)
    fileMaxByte = config.file_max_byte
    backupCount = config.backup_count
    fileHandler = logging.handlers.RotatingFileHandler(config.log_path, maxBytes=fileMaxByte, backupCount=backupCount)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.DEBUG)
    return logger


if __name__ == '__main__':
    logger = getLogger()
    sys.argv = [None] * 6
    sys.argv[0] = 'python3.5'
    sys.argv[1] = 'DataSimulator.py'
    sys.argv[2] = './busan_tb_node_raw_180516_TTA.csv'
    sys.argv[3] = '0'
    sys.argv[4] = '0'
    sys.argv[5] = '2018-05-28 00:00:00'
    # sys.argv[5] = None
    if (sys.argv[2] == None) or (sys.argv[3] == None):
        printUsage()
        sys.exit()

    while True:
        datasimulator = DataSimulator()
        sys.argv[5] = datetime.now().strftime(DATETIME)


