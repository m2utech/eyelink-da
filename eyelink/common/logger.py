import common_modules
import logging
import logging.handlers
from config import config


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


# efsl
def getLogger(logger_name, log_file, log_format, file_size, backup_cnt, log_level):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(log_format)
    fileHandler = logging.handlers.RotatingFileHandler(log_file, maxBytes=file_size, backupCount=backup_cnt)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.getLevelName(log_level))
    return logger


if __name__ == '__main__':
    pass
    print(config.backup_count)