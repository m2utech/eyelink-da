import logging
import logging.handlers
import consts


def getCaLogger():
    logger = logging.getLogger(consts.LOGGER_NAME['CA'])
    formatter = logging.Formatter(consts.LOG_FORMAT)
    fileMaxByte = consts.FILE_MAX_BYTE    # 100MB
    fileHandler = logging.handlers.RotatingFileHandler(consts.PATH['DAEMON_LOG'], maxBytes=fileMaxByte, backupCount=10)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    # streamHandler = logging.StreamHandler()
    # streamHandler.setFormatter(formatter)
    # logger.addHandler(streamHandler)
    logger.setLevel(logging.DEBUG)

    return logger


def getSchedulerLogger():
    logger = logging.getLogger(consts.LOGGER_NAME['SCHE'])
    formatter = logging.Formatter(consts.LOG_FORMAT)
    fileMaxByte = consts.FILE_MAX_BYTE     # 100MB
    fileHandler = logging.handlers.RotatingFileHandler(consts.PATH['SCHE_LOG'], maxBytes=fileMaxByte, backupCount=10)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.DEBUG)

    return logger


if __name__ == '__main__':
    logger = getCaLogger()
    logger.debug("debugging level message")
    logger.info("info level message")
    logger.warn("warning level message")
    logger.error("error level message")
    logger.critical("cretical error message")
