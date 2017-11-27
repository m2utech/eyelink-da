# #### DATEFORMAT ####
DATE = '%Y-%m-%d'
DATETIME = '%Y-%m-%dT%H:%M:%S'
DATETIMEZERO = '%Y-%m-%dT%H:%M:00'
DATETIMEMILLI = '%Y-%m-%dT%H:%M:%S.%f'
LOCAL_TIMEZONE = 'Asia/Seoul'

# #### LOGGING ####
LOGGER_NAME = {
    'CA': 'clusterAnalysis',
    'SCHE': 'scheduler'
}
LOG_FORMAT = '%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)s) %(message)s'
FILE_MAX_BYTE = 1024 * 1024 * 100


# #### SCHEDULER ####
SCHEDULER = {
    'MAX_INSTANCE': 10,
    'HOUR': 0,           # 02:00 every day
    'DAY_OF_WEEK': 'mon',    # every monday
    'DAY': 1
}


# #### Date Range for Data Analysis ####
TIME_RANGE = {
    'DAY': 1,
    'WEEK': 1,
    'MONTH': 1
}

TIME_INTERVAL = {
    'DAY': 15,
    'WEEK': 30,
    'MONTH': 60
}

# #### SOCKET INFO ####
BUFFER_SIZE = 256
HOST = 'DataAnalyzer'
PORT = 5225
LOCAL_HOST = 'localhost'
CONN_TIMEOUT = 60

# #### Application info ####
APP_TYPE = 'DA'
AGENT_ID = ''
ALARM_TYPE = 'BATCH_CLUSTERING'
ALARM_TYPE_NAME = 'BATCH_CLUSTERING'

# #### factor information for AD ####
FACTOR_INFO = {
    'FACTORS': {
        'ampere': 0.5,
        'active_power': 110.0,
        'power_factor': 0.9,
        'voltage': 220.0
        },
    'NODE_ID': 'node_id',
    'INDEX': 'event_time',
    'N_CLUSTER': 5
}

# #### Configuration ####
API = {
    'LOAD_DATA': 'http://m2utech.eastus.cloudapp.azure.com:5223/analysis/restapi/getClusterRawData',
    'UPLOAD_MASTER': 'http://m2utech.eastus.cloudapp.azure.com:5223/analysis/restapi/insertClusterMaster/',
    'UPLOAD_DETAIL': 'http://m2utech.eastus.cloudapp.azure.com:5223/analysis/restapi/insertClusterDetail/'
}
PATH = {
    'DAEMON_PID': '/home/Toven/da/PID/ca_daemon.pid',
    'SCHE_PID': '/home/Toven/da/PID/ca_scheduler.pid',
    'DAEMON_LOG':  '/home/Toven/da/logs/ca_daemon.log',
    'SCHE_LOG': '/home/Toven/da/logs/ca_scheduler.log'
}
