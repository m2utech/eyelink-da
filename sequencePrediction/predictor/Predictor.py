from abc import ABCMeta, abstractmethod
from multipledispatch import dispatch

class Predictor():
    metaclass = ABCMeta
    TAG = None

    def __init__(self, tag):
        self.__init__()
        self.TAG = tag

    def getTAG(self):
        return self.TAG



    @abstractmethod
    def Train(self, trainingSequences):
        pass

    @abstractmethod
    def Predict(self, target):
        pass

    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def memoryUsage(self):
        pass


# test code
if __name__ == '__main__':
    test = Predictor()
    test.Predict(3)