import numpy as np
from database.Item import Item
from database.Sequence import Sequence
from predictor.CPTplus.Bitvector import Bitvector

class CPTHelper(object):
    predictor = None
    encoder = None

    def __init__(self, predictor):
        self.predictor = predictor

    def setEncoded(self, encoder):
        self.encoder = encoder

    def getSequenceFromId(self, id):
        if self.encoder == None:
            print("Encoded needs to be set in CPTHelperEncoded")

        items = []
        curNode = self.predictor.LT.get(id)
        items.append(curNode)
        while (curNode.Parent != None) and (curNode.Parent != self.predictor.Root):
            curNode = curNode.Parent
            items.append(curNode.Item)

        items.sort(reverse=True)

        sequence = self.encoder.decode(Sequence(id, items))

        return np.asarray(sequence.getItems())

    def getCommonPrefix(self, A, B):
        if (len(A) < 1) or (len(B) < 1):
            return None

        prefix = list()
        i = 0
        while (i < len(A)) and (i < len(B)):
            if A[i] == B[i]:
                prefix.append(A[i])
            else:
                return prefix
            i += 1
        return prefix


    def keepLastItems(self, sequence, length):
        if sequence.size() <= length:
            return sequence

        result = Sequence(sequence.getId(), sequence.getItems()[sequence.size() - length : sequence.size()])
        return result

    def removeUnseenItems(self, seq):
        target = Sequence(seq)
        threshold = 0
        selectedItems = list()
        for item in target.getItems():
            if (self.predictor.II.get(item.val) != None) and (self.predictor.II.get(item.val).cardinality() >= threshold):
                selectedItems.append(item)

        target.getItems().clear()
        target.getItems().extend(selectedItems)
        return target

    def getSimilarSequencesIds(self, sequence):
        if len(sequence == 0):
            return Bitvector()
        intersection = None
        for i in range(len(sequence)):
            if intersection == None:
                intersection = self.predictor.II.get(sequence[i].val).clone()
            else:
                other = self.predictor.II.get(sequence[i].val)
                if other != None:
                    intersection.And(self.predictor.II.get(sequence[i].val))

        return intersection

