from database.Item import Item
from database.Sequence import Sequence
from helpers.ScoreDistribution import ScoreDistribution

class CountTable(object):
    table = None
    branchVisited = None
    helper = None

    def __init__(self, helper):
        self.table = dict()
        self.branchVisited = set()
        self.helper = helper


    def push(self, key, curSeqLength, fullSeqLength, numberOfSeqSameLength, dist):
        weightLevel = 1.0 / numberOfSeqSameLength
        weightDistance = 1.0 / dist
        curValue = (weightLevel * 1.0) + (1.0) + (weightDistance * 0.0001)

        oldVal = self.table.get(key)
        if oldVal == None:
            self.table[key] = curValue
        else:
            self.table[key] = oldVal * curValue


    def update(self, sequence, initialSequenceSize):

        branchesUsed = 0
        ids = self.helper.getSimilarSequencesIds(sequence)

        # For each sequence similar of the given sequence
        id = ids.nextSetBit(0)
        while id >= 0:
            if id in self.branchVisited:
                id = ids.nextSetBit(id + 1)
                continue

            self.branchVisited.add(id)
            # extracting the sequence from the PredictionTree
            seq = self.helper.getSequenceFromId(id)
            # Generating a set of all the items from sequence
            toAvoid = set()
            for item in sequence:
                toAvoid.add(item)

            # Updating this CountTable with the items {S}
            # Where {S} contains only the items that are in seq after
            # all the items from sequence have appeared at least once
            # Ex:
            # 	sequence: 	A B C
            #   seq: 		X A Y B C E A F
            # 	{S}: 		E F
            max = 99            # used to limit the number of items to push in the count table
            count = 1           # current number of items already pushed
            for item in seq:
                # only enters this if toAvoid is empty
                # it means that all the items of toAvoid have been seen
                if (len(toAvoid) == 0) and (count < max):
                    # calculating the score for this item
                    self.push(item.val, len(sequence), initialSequenceSize, ids.getCardinality(), count)
                    count += 1
                elif item in toAvoid:
                    toAvoid.remove(item)

            # meaning that the count table has been really updated
            if count > 1:
                branchesUsed += 1

            id = ids.nextSetBit(id + 1)

        return branchesUsed


    def getBestSequence(self, count):
        # Iterating through the CountTable to sort the items by score
        sd = ScoreDistribution()
        for itKey, itVal in self.table.items():
            # the following measure of confidence and lift are "simplified" but are exactly the same as in the literature.
            # CONFIDENCE : |X -> Y|
            # LIFT: CONFIDENCE(X -> Y) / (|Y|)
            confidence = itVal
            # 			double support = helper.predictor.II.get(it.getKey()).cardinality();
            # 			double lift = it.getValue() * support;
            # Calculate score based on lift or confidence
            score = confidence
            # Use confidence or lift, depending on Parameter.firstVote
            sd.put(itKey, score)

        # Filling a sequence with the best |count| items
        seq = Sequence(-1)
        bestItems = sd.getBest(1.002)
        # bestItems = sd.getBest(1.00001);
        if (bestItems != None) and (len(bestItems) > 0):
            i = 0
            while (i < count) and (i < len(bestItems)):
                seq.addItem(Item(bestItems[i]))
                i += 1

        return seq

    # 	 * Get the symbols and their scores
    # 	 * @return the internal count table
    def getTable(self):
        return self.table

