import logging
import logging.handlers
import da_config as config


def getEfmmLogger():
    logger = logging.getLogger(config.logger_name['efmm'])
    formatter = logging.Formatter(config.log_format)
    fileMaxByte = config.file_max_byte    # 100MB
    backupCount = 10
    fileHandler = logging.handlers.RotatingFileHandler(config.file_path['efmm_log'], maxBytes=fileMaxByte, backupCount=backupCount)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.DEBUG)
    return logger

# stream logger for local test
def getStreamLogger():
    logger = logging.getLogger(config.logger_name['efmm'])
    formatter = logging.Formatter(config.log_format)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    logger.setLevel(logging.DEBUG)
    return logger