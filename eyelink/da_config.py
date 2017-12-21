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

scheduler_opt = {
    "max_instance": 10,
    "minute": '*/2',
    "hour": 9,          # Local time (every day 09:00)
    "week": 'mon',
    "job_code": {
        '0000': 'pattern',
        '1000': 'matching',
        '2000': 'clustering'
    },
    "time_range_pattern": 24,     #24 hours
    "time_range_matching": 60     #60 minutes --> 55min matching

}

es_url = 'http://m2u-parstream.eastus.cloudapp.azure.com:9200'

# ### interpolation method for missing value ###
mv_method = 'linear'    # Option : 'linear', 'time', 'index', 'values', 'nearest', 'zero'


da_opt = {
    'time_interval': '30S', # 30 seconds
    'range_sec': 30,
    'index': 'dtSensed',
    'factors': ['cid', 'availability', 'overall_oee', 'performance', 'quality'],
    'masterID': 'master',
    'n_cluster': 30,
    'top_k': 3,
    'slide_len': 2,    # 1m
    'win_len': 120,     # 1h
    'match_len': 110,    # 55m
    'value_range': [0.0, 1.0],
    'match_rate_threshold': 95.0    # 95%
}

clustering_opt = {
    'index': 'measure_time',
    'timeUnit': 'minutes',   #seconds, minutes, hours ...
    'n_cluster': 10,
    'byDay': {'range': 1, 'interval': '1T'},    # 1 minute
    'byWeek': {'range': 1, 'interval': '10T'}
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
