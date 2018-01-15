# #### LOGGING ####
log_format = '%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)s) %(message)s'
file_max_byte = 1024 * 1024 * 100
backup_count = 10
logger_name = "efsl_log"    ###
logging_level = "DEBUG"     ### CRITCAL, ERROR, WARNING, INFO, DEBUG, NOTSET
log_file = "/home/Toven/eyelink-da/logs/efsl.log"
pid_file = "/home/Toven/eyelink-da/pid/efsl.pid"
sched_pid_file = "/home/Toven/eyelink-da/pid/efslScheduler.pid"

# used
sched_opt = {
    "max_instances": 10,
    "trigger": "cron",          # e.g. 'date', 'interval', 'cron'
    "CP_cycle": 9,              # 09:00 every day
    "CP_range": 24,             # 24 hours
    "PM_cycle": '*/2',          # every 2 minutes
    "PM_range": 60,             # 60 minutes
    "job_code": {
        '0000': 'pattern',
        '1000': 'matching',
        '2000': 'clustering'
    }
}

##### Elasticsearch API #####
es_opt = {
    'url': 'http://m2u-parstream.eastus.cloudapp.azure.com:9200',
    'scroll_time': '3m',
    'scroll_size': 10000
}

# ### interpolation method for missing value ###
mv_method = 'linear'    # Option : 'linear', 'time', 'index', 'values', 'nearest', 'zero'

AD_opt = {
    'node_id': 'B_009',     ###
    'time_interval': 1,     ### 1 minute
    'range_sec': 30,
    'index': 'event_time',  ###
    'factors': ['ampere', 'active_power', 'power_factor', 'voltage'],
    'masterID': 'master',   ###
    'n_cluster': 50,        ### 50
    'top_k': 3,
    'slide_len': 2,                             # 1m
    'win_len': 120,                             # 1h
    'match_len': 110,                           # 55m
    'value_range': [0.0, 1.0],                  # range of occurrence 
    'match_rate_threshold': 95.0,               # range of value [min, max]
    'timeUnit': 'minutes',      # seconds, minutes, hours ...
    'sched_cp': {'cycle': 0, 'range': 26},    ### sched opt for create pattern
    'sched_pm': {'cycle': '*/2', 'range': 120} ### sched opt for pattern matching
}

### used
##### option info for Clustering Analysis
CA_opt = {
    'id': 'node_id',
    'index': 'event_time',
    'factors': ['ampere', 'active_power', 'power_factor', 'voltage'],
    'timeUnit': 'minutes',      # seconds, minutes, hours ...
    'n_cluster': 5,
    # CA scheduler
    'daily': {'cycle': 0, 'range': 1, 'interval': 1},   # 09:00, 1 day, 1 minute
    'weekly': {'cycle': 'mon', 'range': 7, 'interval': 15}  # monday, 7 days, 10 minutes
}

# ### ALARM MESSAGE ###
alarm_info = {
    'host': 'http://m2utech.eastus.cloudapp.azure.com',
    'port': 5224,
    'AD': {
        'appType': 'CA',
        'agentId': 'TEST',
        'alarmType': 'CA',
        'alarmTypeName': 'CLUSTER_ANALYSIS'
    },
    'CA': {
        'appType': 'AD',
        'agentId': 'TEST',
        'alarmType': 'AD',
        'alarmTypeName': 'ANOMALY_DETECTION'
    }
}

#used
es_index = {
    'corecode': {
        'corecode': {
            'master': {'INDEX': 'efsl_clustering_master', 'TYPE': 'master'},
            'detail': {'INDEX': 'efsl_clustering_detail', 'TYPE': 'detail'},
            'PD': {'INDEX': 'efsl_pattern_data', 'TYPE': 'pattern_data'},
            'PI': {'INDEX': 'efsl_pattern_info', 'TYPE': 'pattern_info'},
            'PM': {'INDEX': 'efsl_pattern_matching', 'TYPE': 'pattern_matching'}
        }
    }
}
