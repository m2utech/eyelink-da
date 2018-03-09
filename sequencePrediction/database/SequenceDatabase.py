from database.Sequence import Sequence
import traceback
from database.Item import Item

class SequenceDatabase(object):
    def __init__(self):
        self.sequences = []

    # def setSequences(self, newSequences):
    #     self.sequences = newSequences
    #
    def getSequences(self):
        return self.sequences

    def size(self):
        return len(self.sequences)

    def clear(self):
        self.sequences.clear()
    #
    # def loadFileCustomFormat(self, filepath, maxCount, minSize, maxSize):
    #     try:
    #         with open(filepath, 'r') as reader:
    #             count = 0
    #             for line in reader.readlines():
    #                 if count < maxCount:
    #                     split = line.split(" ")
    #                     if (len(split) >= minSize) and (len(split) <= maxSize):
    #                         sequence = Sequence(-1)
    def loadFileSPMFFormat(self, path, maxCount, minSize, maxSize):
        myInput = open(path, 'r')
        try:
            count = 0
            for thisLine in myInput.readlines():
                if count >= maxCount:
                    break
                sequence = Sequence(len(self.sequences))
                # tokens = thisLine.strip("\n").split(" ")
                for entier in thisLine.strip("\n").split(" "):
                    if entier == "-1":
                        pass
                    elif entier == "-2":
                        if (sequence.size() >= minSize) and (sequence.size() <= maxSize):
                            self.sequences.append(sequence)
                            count += 1
                    else:
                        val = int(entier)
                        sequence.getItems().append(Item(val))
        except:
            traceback.print_exc()

