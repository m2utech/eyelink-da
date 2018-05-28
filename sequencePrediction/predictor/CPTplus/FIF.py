from __future__ import print_function

from abc import ABCMeta, abstractmethod #Abstrace Base Class

class FIF(metaclass=ABCMeta):
    """ generated source for interface FIF """
    @abstractmethod  #FIF 클래스를 상속받는 모든 클래스는 하기 함수를 오버라이딩으로 구현해야 인스턴스 생성이 가능함
    def getItemFrequencies(self, seqs):
        pass

    @abstractmethod
    def findFrequentItemsets(self, seqs, minLength, maxlength, minSup):
        pass


# test code
# if __name__ == '__main__':
#     test = FIF()