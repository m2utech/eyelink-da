from sequencePrediction.database.Sequence import Sequence
from sequencePrediction.database.Item import Item
from sequencePrediction.predictor.profile.Profile import Profile
import traceback

class SequenceDatabase(object):

    def __init__(self):
        self.sequences = []

    def setSequences(self, newSequences):
        self.sequences = newSequences

    def getSequences(self):
        return self.sequences

    def size(self):
        return len(self.sequences)

    def clear(self):
        self.sequences.clear()

    def loadFileDefaultFormat(self, filepath, maxCount, minSize, maxSize):
        try:
            with open(filepath, 'r') as reader:
                count = 0
                for line in reader.readlines():
                    if count < maxCount:
                        split = line.strip("\n").split(" ")
                        if (len(split) >= minSize) and (len(split) <= maxSize):
                            sequence = Sequence(-1)
                            alreadySeen = set()
                            lastValue = -1
                            for value in split:
                                intVal = int(value)
                                if Profile.paramInt(self,"removeDuplicatesMethod") == 2:
                                    if alreadySeen.__contains__(intVal): continue
                                    else: alreadySeen.add(intVal)
                                elif Profile.paramInt(self,"removeDuplicatesMethod") == 1:
                                    if lastValue == intVal: continue
                                    lastValue = intVal
                                item = Item(int(intVal))
                                sequence.addItem(item)
                            self.sequences.append(sequence)
                            count += 1
        except IOError:
            traceback.print_exc()


    """ # Load the sequences for a MSNBC file """
    def loadFileMSNBCFormat(self, filepath, maxCount, minSize, maxSize):
        try:
            with open(filepath, 'r') as reader:
                count = 0
                for line in reader.readlines():
                    if count < maxCount:
                        split = line.strip("\n").split(" ")
                        if (len(split) >= minSize) and (len(split) <= maxSize):
                            sequence = Sequence(-1)
                            alreadySeen = set()
                            lastValue = -1
                            for value in split:
                                intVal = int(value)
                                if Profile.paramInt(self,"removeDuplicatesMethod") == 2:
                                    if alreadySeen.__contains__(intVal): continue
                                    else: alreadySeen.add(intVal)
                                elif Profile.paramInt(self,"removeDuplicatesMethod") == 1:
                                    if lastValue == intVal: continue
                                    lastValue = intVal
                                item = Item(int(intVal))
                                sequence.addItem(item)
                            self.sequences.append(sequence)
                            count += 1
        except IOError:
            traceback.print_exc()


    def loadFileBMSFormat(self, filepath, maxCount, minSize, maxSize):
        try:
            with open(filepath, 'r') as reader:
                lastId = 0
                count = 0
                sequence = None
                for line in reader.readlines():
                    if count < maxCount:
                        split = line.strip("\n").split(" ")
                        id = int(split[0])
                        val = int(split[1])
                        if lastId != id:
                            if (lastId != 0) and (sequence.size() >= minSize) and (sequence.size() <= maxSize):
                                self.sequences.append(sequence)
                                count += 1
                            sequence = Sequence(id)
                            lastId = id
                        item = Item(val)
                        sequence.addItem(item)
        except IOError:
            traceback.print_exc()

    def loadFileCustomFormat(self, filepath, maxCount, minSize, maxSize):
        try:
            with open(filepath, 'r') as reader:
                count = 0
                for line in reader.readlines():
                    if count < maxCount:
                        split = line.strip("\n").split(" ")
                        if (len(split) >= minSize) and (len(split) <= maxSize):
                            sequence = Sequence(-1)
                            for value in split:
                                item = Item(int(value))
                                if item.val.__eq__(-1) == False:
                                    sequence.addItem(item)

                            self.sequences.append(sequence)
                            count += 1
        except IOError:
            traceback.print_exc()




    ''' # Load the sequences for a FIFA (World cup) log file
        # see: http://ita.ee.lbl.gov/html/contrib/WorldCup.html '''
    def loadFileFIFAFormat(self, filepath, maxCount, minSize, maxSize):
        try:
            with open(filepath, 'r') as reader:
                count = 0
                for line in reader.readlines():
                    if count < maxCount:
                        split = line.strip("\n").split(" ")
                        if (len(split) >= minSize) and (len(split) <= maxSize):
                            sequence = Sequence(-1)

                            alreadySeen = set()
                            lastValue = -1

                            for value in split:
                                intVal = int(value)
                                if Profile.paramInt(self,"removeDuplicatesMethod") == 2:
                                    if alreadySeen.__contains__(intVal):
                                        continue
                                    else:
                                        alreadySeen.add(intVal)
                                elif Profile.paramInt(self,"removeDuplicatesMethod")== 1:
                                    if lastValue == intVal:
                                        continue
                                    lastValue = intVal

                                item = Item(int(intVal))
                                sequence.addItem(item)

                            self.sequences.append(sequence)
                            count += 1
        except IOError:
            traceback.print_exc()




    def loadFileLargeTextFormatAsCharacter(self, filepath, maxCount, minSize, maxSize):
        try:
            with open(filepath, 'r') as reader:
                count = 0
                for line in reader.readlines():
                    if maxCount == count:
                        break

                    if (len(split) >= minSize) and (len(split) <= maxSize):
                        sequence = Sequence(-1)

                        for k in range(len(line)):
                            value = line[k]
                            sequence.addItem(Item(value))

                        self.sequences.append(sequence)
                        count += 1
        except IOError:
            traceback.print_exc()


    def loadFileLargeTextFormatAsWords(self, filepath, maxCount, minSize, maxSize, doNotAllowSentenceToContinueOnNextLine):
        try:
            with open(filepath, 'r') as reader:
                seqCount = 0
                lastWordID = 1

                mapWordToID = dict()
                sequence = Sequence(-1)

                for line in reader.readlines():
                    if maxCount == seqCount:
                        break

                    modifiedLine = []
                    for i in range(len(line)):
                        currentChar = line[i]
                        if (currentChar.isalpha()) or (currentChar=='.') or (currentChar=='?') or (currentChar==':') or (currentChar==" "):
                            modifiedLine.append(currentChar)

                    modifiedLine = ''.join(str(e) for e in modifiedLine)
                    split = modifiedLine.strip("\n").split(" ")
                    for i in range(len(split)):
                        token = split[i]
                        containsPunctuation = (token.__contains__(".")) or (token.__contains__("?") or (token.__contains__(":")))

                        if containsPunctuation:
                            seqCount += 1
                            if containsPunctuation or (i == len(split)-1) and (doNotAllowSentenceToContinueOnNextLine):
                                token = token[0:len(token)-1]
                            itemID = mapWordToID.get(token)
                            if itemID == None:
                                itemID = lastWordID + 1
                                mapWordToID[token] = itemID
                            sequence.addItem(Item(itemID))
                            if (len(sequence) >= minSize) and (len(sequence) <= maxSize):
                                self.sequences.append(sequence)
                            sequence = Sequence(-1)
                        else:
                            itemID = mapWordToID.get(token)
                            if itemID == None:
                                itemID = lastWordID + 1
                                mapWordToID[token] = itemID
                            sequence.addItem(Item(itemID))
        except IOError:
            traceback.print_exc()


    def loadFileSignLanguage(self, filepath, maxCount, minSize, maxSize):
        try:
            with open(filepath, 'r') as reader:
                oldUtterance = "-1"
                sequence = None
                count = 0
                alreadySeen = set()
                id = 0
                lastValue = -1

                for line in reader.readlines():
                    if (len(line) >= 1) and (line[0] != '#'):
                        tokens = line.strip("\n").split(" ")
                        currentUtterance = tokens[0]
                        if not currentUtterance.__eq__(oldUtterance):
                            if sequence != None:
                                if (sequence.size() >= minSize) and (sequence.size() <= maxSize):
                                    self.sequences.append(sequence)
                                    count += 1
                            sequence = Sequence(id)
                            id += 1
                            alreadySeen = set()
                            oldUtterance = currentUtterance

                        for j in range(1, len(tokens)):
                            character = int(tokens[j])
                            if (character == -11) or (character == -12):
                                continue
                            if Profile.paramInt("removeDuplicatesMethod") == 2:
                                if alreadySeen.__contains__(character):
                                    continue
                                else:
                                    alreadySeen.add(character)
                            elif Profile.paramInt("removeDuplicatesMethod") == 1:
                                if lastValue == character:
                                    continue
                                lastValue = character
                            sequence.getItems().append(Item(character))

                    if maxCount == count:
                        break

                if (sequence.size() >= minSize) and (sequence.size() <= maxSize):
                    self.sequences.append(sequence)
        except IOError:
            traceback.print_exc()



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
        except IOError:
            traceback.print_exc()

