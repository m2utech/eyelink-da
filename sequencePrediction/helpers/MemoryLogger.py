import psutil


class MemoryLogger:
    mMemoryUsage = list()

    def __init__(self):
        pass
        # self.mMemoryUsage = list()

    def reset(self):
        self.mMemoryUsage.clear()

    def addUpdate(self):
        self.mMemoryUsage.append(self.getUsedMemory())

    def getUsedMemory(self):
        mb = 1024 * 1024 * 1024
        mem = psutil.virtual_memory()
        # usage = int(psutil.virtual_memory().used / mb)
        usage = int((mem.total - mem.free) / mb)
        return usage

    def getMaxMemory(self):
        mb = 1024 * 1024 * 1024
        usage = int(psutil.virtual_memory().total / mb)
        return usage

    def displayUsage(self):
        max = 0
        output = "Memory history: "
        for i in self.mMemoryUsage:
            output += "{} ".format(i)
            if i > max:
                max = i

        print(output)
        print("Max memory used: {} mb".format(max))