import logging
import logging.handlers
from ad_configParser import getConfig
import consts


def getAdLogger():
    cfg = getConfig()

    logger = logging.getLogger(consts.LOGGER_NAME['AD'])
    formatter = logging.Formatter(consts.LOG_FORMAT)
    fileMaxByte = consts.FILE_MAX_BYTE    # 100MB
    fileHandler = logging.handlers.RotatingFileHandler(cfg['FILE_PATH']['path_ad_log'], maxBytes=fileMaxByte, backupCount=10)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    # streamHandler = logging.StreamHandler()
    # streamHandler.setFormatter(formatter)
    # logger.addHandler(streamHandler)
    logger.setLevel(logging.DEBUG)

    return logger


def getSchedulerLogger():
    cfg = getConfig()

    logger = logging.getLogger(consts.LOGGER_NAME['SCHE'])
    formatter = logging.Formatter(consts.LOG_FORMAT)
    fileMaxByte = consts.FILE_MAX_BYTE     # 100MB
    fileHandler = logging.handlers.RotatingFileHandler(cfg['FILE_PATH']['path_scheduler_log'], maxBytes=fileMaxByte, backupCount=10)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.DEBUG)

    return logger


if __name__ == '__main__':
    logger = getAdLogger()
    logger.debug("debugging level message")
    logger.info("info level message")
    logger.warn("warning level message")
    logger.error("error level message")
    logger.critical("cretical error message")
