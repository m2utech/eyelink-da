from database.Item import Item
from database.Sequence import Sequence

from collections import deque
from common.LinkedList import LinkedList

class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

class Encoder(object):
    Dict = None
    InvDict= None

    def __init__(self):
        self.Dict = list()
        # self.InvDict = hashabledict()
        self.InvDict = dict()

    def addEntry(self, entry):
        key = deque()
        for i in entry:
            if type(i) == int:
                key.append(i)
            else:
                key.append(i.val)
        id = self.getId(tuple(key))
        if id == None:
            self.Dict.append(tuple(key))
            id = len(self.Dict) - 1
            self.InvDict[tuple(key)] = id
        return id

    def getEntry(self, id):
        return self.Dict[id]

    def getId(self, entry):
        id = self.InvDict.get(entry)
        return id

    def getIdorAdd(self, entry):
        entry = tuple(entry)
        return self.addEntry(entry)

    def encode(self, seq):
        if (seq == None) or (len(seq.getItems()) == 0):
            return seq

        encoded = Sequence(seq.getId())
        seqSize = len(seq.getItems())
        i = 0
        while i < seqSize:
            candidate = seq.getItems()[i:seqSize]
            # candidate = seq.getItems()[i : seqSize]
            idFound = None
            while ((idFound == None) and (len(candidate) > 0)):
                key = deque()
                for element in candidate:
                    key.append(element.val)
                idFound = self.getId(tuple(key))
                if idFound != None:
                    encoded.addItem(Item(idFound))
                    i += len(candidate) - 1
                elif len(candidate) == 1:
                    idFound = self.addEntry(tuple(key))
                    encoded.addItem(Item(idFound))
                else:
                    candidate.pop()
            i += 1
        return encoded

    def decode(self, seq):
        if (seq == None) or (len(seq.getItems()) == 0):
            return seq
        decoded = Sequence(seq.getId())
        for encodedItem in seq.getItems():
            itemset = self.getEntry(encodedItem.val)
            if (itemset != None):
                for decodedItem in itemset:
                    decoded.addItem(decodedItem)
            else:
                print("Could not find item: {}".format(encodedItem.val))

        return decoded


if __name__ == '__main__':
    en = Encoder()

    p1 = deque()
    p1.append(Item(42))
    p1.append(Item(43))
    p2 = deque()
    p2.append(Item(42))
    p3 = deque()
    p3.append(Item(42))
    p3.append(Item(43))
    p3.append(Item(44))
    print(p1)
    print(p2)
    print(p3)

    seq1 = Sequence(-1)
    seq1.addItem(Item(42))
    seq1.addItem(Item(43))
    seq1.addItem(Item(44))
    seq1.addItem(Item(45))
    print(seq1)

    en.addEntry(p1)
    en.addEntry(p2)
    en.addEntry(p3)

    encoded = en.encode(seq1)
    print(seq1)
    print(encoded)
    print(en.decode(encoded))
