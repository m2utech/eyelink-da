# from bitsets import bitset
from multipledispatch import dispatch
import traceback
#
# class BitSet:
#     def __init__(self):
        # self.sizeIsSticky = False
        # self.words = list(0)
        # self.wordsInUse = 0


class Bitvector(object):

    @dispatch()
    def __init__(self):
        self.bitset = set()
        self.cardinality = 0

    @dispatch(set, int)
    def __init__(self, bitSet, cardinality):
        self.bitset = bitSet
        self.cardinality = cardinality

    def AND(self, bitvector2):
        self.bitset = self.bitset & bitvector2.bitset
        self.cardinality = -1

    def clone(self):
        try:
            return Bitvector(self.bitset.copy(), self.cardinality)
        except:
            traceback.print_exc()
        return None

    def __copy__(self):
        return Bitvector(self.bitset, self.cardinality)

    def size(self):
        return len(self.bitset)

    def nextSetBit(self, i):
        try:
            next = [x for x in list(self.bitset) if x >= i]
            if not next:
                return -1
            else:
                return min(next)
        except:
            traceback.print_exc()

    # def cardinality(self):
    #     if self.cardinality == -1:
    #         self.cardinality = self.bitset.cardinality()
    #     return self.cardinality

    # cardinality(self) has error about 'int' object is not callable
    def getCardinality(self):
        if self.cardinality == -1:
            self.cardinality = len(self.bitset)
        return self.cardinality

    def setBit(self, i):
        if (i in self.bitset) == False:
            self.bitset.add(i)
            self.cardinality += 1

    def __repr__(self):
        return "{}  cardinality : {}".format(self.bitset, self.cardinality)

