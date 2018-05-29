from multipledispatch import dispatch
from queue import Queue
import math
import sys
import numpy as np

from database.Item import Item
from database.Sequence import Sequence
from predictor.Paramable import Paramable
from predictor.Predictor import Predictor
from predictor.CPTplus.FIFRaw import FIFRaw
from predictor.CPTplus.CPTHelper import CPTHelper
from predictor.CPTplus.PredictionTree import PredictionTree
from predictor.CPTplus.Encoder import Encoder
from predictor.CPTplus.Bitvector import Bitvector
from predictor.CPTplus.CountTable import CountTable


class CPTPlusPredictor(Predictor):
    # Root = None
    # LT = None
    # II = None
    # helper = None
    # nodeNumber = None
    CCF = False
    CBS = True
    # encoder = None
    # seqEncoding = None
    # parameters = None
    TAG = "CPT+"
    lastCountTable = None

    @dispatch()
    def __init__(self):
        self.Root = PredictionTree()
        self.LT = dict()
        self.II = dict()
        self.nodeNumber = 0

        self.parameters = Paramable()
        self.seqEncoding = False
        self.helper = CPTHelper(self)

    @dispatch(str)
    def __init__(self, tag):
        self.__init__()
        self.TAG = tag

    @dispatch(str, str)
    def __init__(self, tag, params):
        self.__init__(tag)
        self.parameters.setParameter(params)

    def getTAG(self):
        return self.TAG

    def Train(self, trainingSequences):
        self.Root = PredictionTree()
        self.LT = {}
        self.II = {}
        self.encoder = Encoder()
        self.helper.setEncoded(self.encoder)
        self.nodeNumber = 0
        seqId = 0
        curNode = None

        finder = FIFRaw()
        if self.parameters.paramBoolOrDefault("CCF", self.CCF):
            itemsets = finder.findFrequentItemsets(trainingSequences, self.parameters.paramInt("CCFmin"), self.parameters.paramInt("CCFmax"), self.parameters.paramInt("CCFsup"))

            for itemset in itemsets:
                # print(list(itemset))
                self.encoder.addEntry(itemset)

        for seq in trainingSequences:
            if self.parameters.paramInt("splitMethod") > 0:
                seq = self.helper.keepLastItems(seq, self.parameters.paramInt("splitLength"))

            seqCompressed = Sequence(seq)
            seqCompressed = self.encoder.encode(seqCompressed)

            curNode = self.Root

            for itemCompressed in seqCompressed.getItems():
                itemset = self.encoder.getEntry(itemCompressed.val)

                for item in itemset:
                    if (item.val in self.II) ==False:
                        tmpBitset = Bitvector()
                        self.II[item.val] = tmpBitset

                    self.II.get(item.val).setBit(seqId)

                if curNode.hasChild(itemCompressed) == False:
                    curNode.addChildItem(itemCompressed)
                    self.nodeNumber += 1
                    curNode = curNode.getChild(itemCompressed)
                else:
                    curNode = curNode.getChild(itemCompressed)

            self.LT[seqId] = curNode
            seqId += 1

        if self.parameters.paramBoolOrDefault("CBS", self.CBS):
            self.pathCollapse()

        return True

    def Predict(self, target):
        target = self.helper.removeUnseenItems(target)
        ct = None
        ct = self.predictionByActiveNoiseReduction(target)

        predicted = ct.getBestSequence(1)
        self.lastCountTable = ct.getTable()
        return predicted


    def predictionByActiveNoiseReduction(self, target):
        seen = set()
        queue = Queue()  # linked list
        queue.put(target)

        maxPredictionCount = 1 + int(target.size() * self.parameters.paramDouble("minPredictionRatio"))
        predictionCount = 0
        noiseRatio = self.parameters.paramDouble("noiseRatio")
        initialTargetSize = target.size()

        ct = CountTable(self.helper)
        ct.update(np.array(target.getItems()), target.size())

        predicted = ct.getBestSequence(1)
        if predicted.size() > 0:
            predictionCount += 1

        seq = queue.get()
        while (seq != None) and (predictionCount < maxPredictionCount):
            if (seq in seen) == False:
                seen.add(seq)
                noises = self.getNoise(seq, noiseRatio)

                for noise in noises:
                    candidate = seq.clone()

                    for i in range(len(candidate.getItems())):
                        if candidate.getItems()[i] == noise:
                            # candidate.getItems().remove(i)
                            candidate.getItems().pop(i)
                            break

                    if candidate.size() > 1:
                        queue.put(candidate)

                    candidateItems = np.array(candidate.getItems())

                    branches = ct.update(candidateItems, initialTargetSize)

                    if branches > 0:
                        predicted = ct.getBestSequence(1)
                        if predicted.size() > 0:
                            predictionCount += 1

            if queue.empty():
                seq = None
            else:
                seq = queue.get()

        return ct

    # {1 = {0, 2, 3}    cardinality: 3,
    # 2 = {0, 1, 2, 3}    cardinality: 4,
    # 3 = {0, 1, 2, 3}    cardinality: 4,
    # 4 = {0, 1, 2, 3}    cardinality: 4,
    # 5 = {1, 2, 3}    cardinality: 3,
    # 6 = {0}    cardinality: 1,
    # 7 = {3}    cardinality: 1}

    def getNoise(self, target, noiseRatio):
        noiseCount = int(math.floor(target.size() * noiseRatio))
        if noiseCount <= 0:
            minSup = int(sys.maxsize)
            itemVal = -1
            for item in target.getItems():
                if self.II[item.val].getCardinality() < minSup:
                    minSup = self.II[item.val].getCardinality()
                    itemVal = item.val

            noises = []
            noises.append(Item(itemVal))
            return noises
        else:
            ## TODO: sort the items of a sequence by frequency...
            noises = sorted(target.getItems(), key=lambda x: self.II.get(x.val).getCardinality(), reverse=True)
            return noises[(target.size() - noiseCount):target.size()]


    def pathCollapse(self):
        nodeSaved = 0

        for entryKey, entryVal in self.LT.items():
            cur = entryVal
            leaf = cur
            last = None
            itemset = []
            pathLength = 0
            singlePath = True

            if len(cur.getChildren()) == 0:
                while singlePath == True:
                    if (len(cur.getChildren()) > 1) or (cur == None):
                        if pathLength != 1:
                            newId = self.encoder.getIdorAdd(itemset)
                            leaf.Item = Item(newId)
                            leaf.Parent = cur

                            cur.removeChild(last.Item)
                            cur.addChildLeaf(leaf)
                            nodeSaved += pathLength - 1
                        singlePath = False
                    else:
                        curItemset = self.encoder.getEntry(cur.Item.val)
                        tmp = itemset
                        itemset = []
                        itemset.extend(curItemset)
                        itemset.extend(tmp)

                        cur.getChildren().clear()
                        pathLength += 1
                        last = cur
                        cur = cur.Parent

        self.nodeNumber -= nodeSaved


    def size(self):
        return self.nodeNumber


    def memoryUsage(self):
        sizePredictionTree = self.nodeNumber * 3 * 4
        sizeInvertedIndex = float(len(self.II) * (math.ceil(len(self.LT) / 8) + 4))
        sizeLookupTable = len(self.LT) * 2 * 4
        return sizePredictionTree + sizeInvertedIndex + sizeLookupTable


    def getCountTable(self):
        return self.lastCountTable









