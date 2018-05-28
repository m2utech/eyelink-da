import logging
import logging.handlers

log_format = '[%(levelname)s][%(filename)s:%(lineno)s] %(message)s'

def getStreamLogger():
    logger = logging.getLogger('stream_log')
    formatter = logging.Formatter(log_format)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    logger.setLevel(logging.DEBUG)
    return logger