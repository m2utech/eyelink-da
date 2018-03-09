
class ScoreDistribution(object):
    dict = None

    def __init__(self):
        self.dict = dict()

    def put(self, key, value):
        keys = self.dict.get(value)
        if keys == None:
            keys = list()
        keys.append(key)
        self.dict[value] = keys

    def clear(self):
        self.dict.clear()

    def getBest(self, minThreshold):
        if len(self.dict) == 0:
            return None
        elif len(self.dict) == 1:
            # dict.lastEntry().getValue()
            return sorted(self.dict.items())[-1][1]

        bestVal1 = sorted(self.dict.keys())[-1]    # best value in dict
        bestVal2 = None
        try:
            bestVal2 = self.dict[max(k for k in self.dict if k < bestVal1)]    # second best value in dict
        except ValueError:
            bestVal2 = None

        if (bestVal1 / bestVal2) < minThreshold:
            return None
        else:
            return self.dict.get(bestVal1)

    def getNextBest(self, best):
        try:
            nextBest = self.dict[max(k for k in self.dict if k < best)]
            return self.dict.get(nextBest)
        except ValueError:
            nextBest = None
            return None

