# #### DATEFORMAT ####
DATE = '%Y-%m-%d'
DATETIME = '%Y-%m-%dT%H:%M:%S'
DATETIMEZERO = '%Y-%m-%dT%H:%M:00'
DATETIMEMILLI = '%Y-%m-%dT%H:%M:%S.%f'
LOCAL_TIMEZONE = 'Asia/Seoul'

# #### LOGGING ####
LOGGER_NAME = {
	'AD': 'anomalyDetection',
	'SCHE': 'scheduler'
}
LOG_FORMAT = '%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)s) %(message)s'
FILE_MAX_BYTE = 1024 * 1024 * 100


# #### SCHEDULER ####
SCHE_MAX_INSTANCE = 10
SCHE_MINUTE = '*/2'     # every 2 minutes
SCHE_HOUR = 2           # 02:00 every day
JOB_CODE = {
    '0000': 'pattern',
    '1000': 'matching'
}


# #### Date Range for Data Analysis ####
TIME_RANGE = {
	'HOUR': 26,
	'MINUTE': 110,
	'DAY': 10
}

# #### SOCKET INFO ####
BUFFER_SIZE = 256
HOST = 'DataAnalyzer'
PORT = 5226
LOCAL_HOST = 'localhost'
CONN_TIMEOUT = 60

# #### Application info ####
APP_TYPE = 'DA'
AGENT_ID = ''
ALARM_TYPE = 'BATCH_ANOMALY'
ALARM_TYPE_NAME = 'BATCH_ANOMALY'


# #### Attributes for anomaly detection ####
ATTR_MASTER_ID = 'master'
ATTR_NODE_ID = '0002.00000039'
ATTR_WIN_LEN = 120
ATTR_SLIDE_LEN = 1
ATTR_TIME_INTERVAL = 1
ATTR_N_CLUSTER = 120
ATTR_TOP_K = 3
