import psutil

class MemoryLogger(object):
    def __init__(self):
        self.instance = MemoryLogger()
        self.maxMemory = 0

    def getInstance(self):
        return self.instance

    def getMaxMemory(self):
        return self.maxMemory

    def reset(self):
        self.maxMemory = 0

    def checkMemory(self):
        # unit : MB
        currentMemory = psutil.virtual_memory().used / 1024 / 1024 / 1024
        if currentMemory > self.maxMemory:
            self.maxMemory = currentMemory