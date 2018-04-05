# #### DATEFORMAT ####
DATE = '%Y-%m-%d'
DATETIME = '%Y-%m-%dT%H:%M:%S'
DATETIMEZERO = '%Y-%m-%dT%H:%M:00'
PY_DATETIME = '%Y-%m-%d %H:%M:%S'
LOCAL_TIMEZONE = 'Asia/Seoul'

# #### SOCKET INFO ####
BUFFER_SIZE = 256
CONN_TIMEOUT = 60
HOST = 'DataAnalyzer'
PORT = 5224
LOCAL_HOST = 'localhost'


# efsl
PRODUCTS = {
    'efsl': {
        'productName': 'EFSL',
        'host': 'localhost',
        'port': 52251
    },
    'efmm': {
        'productName': 'EFMM',
        'host': 'localhost',
        'port': 52241
    }
}
