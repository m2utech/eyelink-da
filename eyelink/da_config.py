# #### LOGGING ####
log_format = '%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)s) %(message)s'
file_max_byte = 1024 * 1024 * 100
backup_count = 10
logger_name = {
    "efmm": "efmm_log"
}

file_path = {
    "efmm_log": "/home/Toven/eyelink-da/logs/efmm.log",
    "efmm_pid": "/home/Toven/eyelink-da/pid/efmm.pid",
    "efmm_sche_pid": "/home/Toven/eyelink-da/pid/efmmScheduler.pid"
}

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

es_url = 'http://m2u-parstream.eastus.cloudapp.azure.com:9200'

# ### interpolation method for missing value ###
mv_method = 'linear'    # Option : 'linear', 'time', 'index', 'values', 'nearest', 'zero'


AD_opt = {
    'time_interval': '30S', # 30 seconds
    'range_sec': 30,
    'index': 'dtSensed',
    'factors': ['cid', 'availability', 'overall_oee', 'performance', 'quality'],
    'masterID': 'master',
    'n_cluster': 30,
    'cid': 'all',
    'top_k': 3,
    'slide_len': 2,                             # 1m
    'win_len': 120,                             # 1h
    'match_len': 110,                           # 55m
    'value_range': [0.0, 1.0],                  # range of occurrence 
    'match_rate_threshold': 95.0,               # range of value [min, max]
    'cpSchedule': {'cycle': 9, 'range': 24},    # sched opt for create pattern
    'pmSchedule': {'cycle': '*/2', 'range': 60} # sched opt for pattern matching
}

CA_opt = {
    'index': 'measure_time',
    'timeUnit': 'minutes',      # seconds, minutes, hours ...
    'cid': 'all',               # all cids
    'n_cluster': 5,
    'daily': {'cycle': 9, 'range': 1, 'interval': 1},   # 09:00, 1 day, 1 minute
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


efmm_index = {
    'notching': {
        'oee': {'INDEX': 'efmm_notching_oee', 'TYPE': 'oee'},
        'status': {'INDEX': 'efmm_notching_status', 'TYPE': 'status'}
    },
    'stacking': {
        'oee': {'INDEX': 'efmm_stacking_oee', 'TYPE': 'oee'},
        'status': {'INDEX': 'efmm_stacking_status', 'TYPE': 'status'}
    }
}

da_index = {
    'notching': {
        'oee': {
            'PD': {'INDEX': 'efmm_notching_oee_pattern_data', 'TYPE': 'pattern_data'},
            'PI': {'INDEX': 'efmm_notching_oee_pattern_info', 'TYPE': 'pattern_info'},
            'PM': {'INDEX': 'efmm_notching_oee_pattern_matching', 'TYPE': 'pattern_matching'}
        },
        'status': {
            'master': {'INDEX': 'efmm_notching_status_clustering_master', 'TYPE': 'master'},
            'detail': {'INDEX': 'efmm_notching_status_clustering_detail', 'TYPE': 'detail'}
        }
    },
    'stacking': {
        'oee': {
            'PD': {'INDEX': 'efmm_stacking_oee_pattern_data', 'TYPE': 'pattern_data'},
            'PI': {'INDEX': 'efmm_stacking_oee_pattern_info', 'TYPE': 'pattern_info'},
            'PM': {'INDEX': 'efmm_stacking_oee_pattern_matching', 'TYPE': 'pattern_matching'}
        },
        'status': {
            'master': {'INDEX': 'efmm_stacking_status_clustering_master', 'TYPE': 'master'},
            'detail': {'INDEX': 'efmm_stacking_status_clustering_detail', 'TYPE': 'detail'}
        }
    }

}
