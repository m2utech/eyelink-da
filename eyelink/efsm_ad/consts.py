# #### DATEFORMAT ####
DATE = '%Y-%m-%d'
DATETIME = '%Y-%m-%dT%H:%M:%SZ'
DATETIMEZERO = '%Y-%m-%dT%H:%M:00Z'
DATETIMEMILLI = '%Y-%m-%dT%H:%M:%S.%fZ'
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

# #### factor information for AD ####
FACTOR_INFO = {
    'INDEX': 'event_time',
    'FACTORS': {
        'ampere': 0.5,
        'active_power': 110.0,
        'power_factor': 0.9,
        'voltage': 220.0
    },
    'RANGE': {
        'ampere': [0.0, 1.0],
        'active_power': [0.0, 200.0],
        'power_factor': [0.0, 1.0],
        'voltage': [0.0, 240.0]
    }
}

# #### Attributes for anomaly detection ####
ATTR_MASTER_ID = 'master'
ATTR_NODE_ID = '0002.00000039'
ATTR_WIN_LEN = 120
ATTR_SLIDE_LEN = 1
ATTR_TIME_INTERVAL = 1
ATTR_N_CLUSTER = 50
ATTR_TOP_K = 3
