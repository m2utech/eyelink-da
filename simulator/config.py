# #### LOGGING ####
log_format = '%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)s) %(message)s'
file_max_byte = 1024 * 1024 * 100
backup_count = 5
logger_name = "dataSimulator_log"    ###
logging_level = "DEBUG"     ### CRITCAL, ERROR, WARNING, INFO, DEBUG, NOTSET
log_path = "./dataSimulator.log"