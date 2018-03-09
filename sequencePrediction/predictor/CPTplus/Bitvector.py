# from bitsets import bitset
from multipledispatch import dispatch
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
        self.bitset = self.bitset & bitvector2
        self.cardinality = -1

    def __copy__(self):
        return Bitvector(self.bitset, self.cardinality)

    def size(self):
        return len(self.bitset)

    def nextSetBit(self, i):
        return self.getValue(self.bitset, i)

    def getValue(self, bitset, i):
        listSet = bitset
        sorted(listSet)
        return listSet[i]

    def cardinality(self):
        if self.cardinality == -1:
            self.cardinality = self.bitset.cardinality()
        return self.cardinality

    def setBit(self, i):
        if (i in self.bitset) == False:
            self.bitset.add(i)
            self.cardinality += 1

    def __repr__(self):
        return "{}  cardinality : {}".format(self.bitset, self.cardinality)

