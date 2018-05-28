# Frequece Itemset Finder (FIF)
from predictor.CPTplus.FIF import FIF
from database.Item import Item
from database.Sequence import Sequence
import common.utils as util
from collections import OrderedDict

class FIFRaw(FIF):
    itemFrequencies = None

    def getItemFrequencies(self, seqs):
        if self.itemFrequencies == None:
            self.itemFrequencies = dict()
        return self.itemFrequencies

    def findFrequentItemsets(self, seqs, minLength, maxlength, minSup):
        self.itemFrequencies = dict()
        frequents = list()
        frequencies = dict()

        if (maxlength <= 1) or (minLength > maxlength):
            return frequents

        for seq in seqs:
            if seq.size() >= minLength:
                for i in range(seq.size()-1):
                    itemset = list()
                    offset = i
                    while ((offset - i) < maxlength) and (offset < seq.size()):
                        itemset.append(seq.get(offset))

                        if len(itemset) >= minLength:
                            # tupleItemset = util.objToTuple(itemset)
                            # print(tupleItemset)
                            support = frequencies.get(tuple(itemset))
                            if support == None:
                                support = 0
                            frequencies[tuple(itemset)] = support + 1
                        offset += 1

                    # intSeq = util.objToInt(seq.get(i))
                    support = self.itemFrequencies.get(seq.get(i))
                    if support == None:
                        support = 0
                    support +=1
                    self.itemFrequencies[seq.get(i)] = support

        for key, value in frequencies.items():
            if value >= minSup:
                frequents.append(key)
        return frequents


if __name__=='__main__':
    training = list()

    seq2 = Sequence(-1)
    seq2.addItem(Item(1))
    seq2.addItem(Item(2))
    seq2.addItem(Item(3))
    seq2.addItem(Item(4))

    training.append(seq2)

    seq3 = Sequence(-1)
    seq3.addItem(Item(1))
    seq3.addItem(Item(2))
    seq3.addItem(Item(3))
    seq3.addItem(Item(4))
    training.append(seq3)

    finder = FIFRaw()
    print(finder.findFrequentItemsets(training,2,4,2))