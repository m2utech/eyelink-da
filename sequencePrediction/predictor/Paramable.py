from multipledispatch import dispatch
from predictor.profile.Profile import Profile

###########################
import logging
logger = logging.getLogger('stream_log')
###########################

class Paramable(object):
    parameters = None

    def __init__(self):
        self.parameters = {}

    def setParameter(self, params):
        if ((params != None) and (len(params) > 0) and (":" in params)):
            paramsStr = params.split(" ")
            for param in paramsStr:
                # logger.debug(param)
                keyValue = param.split(":")
                self.parameters[keyValue[0]] = keyValue[1]
            logger.debug(self.parameters)

    def paramDouble(self, name):
        value = self.parameters.get(name)

        if value != None:
            return float(self.parameters.get(name))
        else:
            return self.Profile.paramDouble(name)


    def paramDoubleOrDefault(self, paramName, defaultValue):
        param = self.paramDouble(paramName)
        return param if param != None else defaultValue


    def paramInt(self, name):
        value = self.parameters.get(name)
        if value != None:
            return int(self.parameters.get(name))
        else:
            return self.Profile.paramInt(name)

    def paramIntOrDefault(self, paramName, defaultValue):
        param = self.paramInt(paramName)
        return param if param != None else defaultValue


    def paramFloat(self, name):
        value = self.parameters.get(name)
        if value != None:
            return float(self.parameters.get(name))
        else:
            return self.Profile.paramFloat(name)

    def paramFloatOrDefault(self, paramName, defaultValue):
        param = self.paramFloat(paramName)
        return param if param != None else defaultValue

    def paramBool(self, name):
        value = self.parameters.get(name)

        if value != None:
            return True if (self.parameters.get(name)).lower() in "true" else False
        else:
            return self.Profile.paramBool(name)

    def paramBoolOrDefault(self, paramName, defaultValue):
        param = self.paramBool(paramName)
        return param if param != None else defaultValue


if __name__ == "__main__":
    a = "CCF:true CBS:true CCFmin:1 CCFmax:6 CCFsup:2 splitMethod:0 splitLength:4 minPredictionRatio:1.0 noiseRatio:1.0"
    print(a)
    Paramable().setParameter(a)