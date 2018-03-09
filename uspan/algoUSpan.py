from __future__ import print_function
import time
import traceback
import operator
import psutil
from qMatrix import QMatrix
import numpy as np
from bisect import bisect_left
from matrixPosition import MatrixPosition
from QMatrixProjection import QMatrixProjection


class AlgoUSpan(object):
    def __init__(self):
        self.maxMemory = 0  # the maximum memory usage
        self.startTimestamp = 0  # the time the algorithm started
        self.endTimestamp = 0  # the time the algorithm terminated

        self.patternCount = 0
        self.writer = None
        self.BUFFERS_SIZE = 2000
        self.patternBuffer = None

        #  if true, debugging information will be shown in the console
        self.DEBUG = True
        #  if true, save result to file in a format that is easier to read by humans
        self.SAVE_RESULT_EASIER_TO_READ_FORMAT = False
        #  the minUtility threshold
        self.minUtility = 0
        #  max pattern length
        self.maxPatternLength = 1000
        #  the input file path
        self.input = None


    def runAlgorithm(self, inputFile, output, minUtility):
        self.input = inputFile
        self.patternBuffer = [0] * self.BUFFERS_SIZE
        # self.patternBuffer = []
        self.maxMemory = 0
        self.startTimestamp = time.time()*1000
        print("startTimestamp : ", self.startTimestamp)
        self.writer = open(output, 'w')
        self.minUtility = minUtility

        mapItemToSWU = {}
        consideredItems = []
        #  ==========  FIRST DATABASE SCAN TO IDENTIFY PROMISING ITEMS =========
        #  We scan the database a first time to calculate the SWU of each item.
        sequenceCount = 0

        myInput = open(inputFile, 'r')
        try:
            for line in myInput.readlines():
            #  if the line is a comment, is  empty or is a kind of metadata, skip it
                if (not line) or (line[:1] == '#') or (line[:1] == '%') or (line[:1] == '@'):
                    continue

                tokens = line.split(" ")
                sequenceUtilityString = tokens[len(tokens)-1]
                positionColons = sequenceUtilityString.index(':')
                sequenceUtility = int(sequenceUtilityString[positionColons+1:])

                for i in range(len(tokens)-3):
                    currentToken = tokens[i]
                    if (len(currentToken) != 0) and (currentToken[:1] != '-'):
                        positionLeftBracketString = currentToken.index('[')
                        itemString = currentToken[:positionLeftBracketString]
                        item = int(itemString)

                        if item in consideredItems:
                            print("{} is already considered in the same line input sequence")
                        else:
                            consideredItems.append(item)
                            if item in mapItemToSWU:
                                swu = mapItemToSWU[item]
                                swu = swu + sequenceUtility
                            else:
                                swu = sequenceUtility
                            mapItemToSWU[item] = swu

                consideredItems.clear()
                sequenceCount += 1
        except:
            self.writer.close()
            traceback.print_exc()
        finally:
            myInput.close()

        if self.DEBUG:
            print("INITIAL ITEM COUNT {}".format(len(mapItemToSWU)))
            print("SEQUENCE COUNT = {}".format(sequenceCount))
            print("INITIAL SWU OF ITEMS")
            for key, value in mapItemToSWU.items():
                print("Item: {} swu: {}".format(key, value))

        # # ================  SECOND DATABASE SCAN ===================
        # #  Read the database again to create the QMatrix for each sequence
        database = []

        myInput = open(inputFile, 'r')
        try:

            # //itemBuffer = [0] * self.BUFFERS_SIZE
            # //utilityBuffer = [0] * self.BUFFERS_SIZE
            # //itemsSequenceBuffer = [0] * self.BUFFERS_SIZE

            for line in myInput.readlines():
                itemBuffer = []
                utilityBuffer = []
                itemsSequenceBuffer = []
                #  if the line is a comment, is  empty or is a kind of metadata, skip it
                if (not line) or (line[:1] == '#') or (line[:1] == '%') or (line[:1] == '@'):
                    continue
                # We reset the two following buffer length to zero because we are reading a new sequence
                itemBufferLength = 0
                itemsLength = 0

                tokens = line.split(" ")

                #  get the sequence utility (the last token on the line)
                sequenceUtilityString = tokens[len(tokens) - 1]
                positionColons = sequenceUtilityString.index(':')
                sequenceUtility = int(sequenceUtilityString[positionColons + 1:])

                #  This variable will count the number of itemsets
                nbItemsets = 1
                #  This variable will be used to remember if an itemset contains at least a promising item
                #  (otherwise, the itemset will be empty).
                currentItemsetHasAPromisingItem = False

                #  Copy the current sequence in the sequence buffer.
                #  For each token on the line except the last three tokens
                #  (the -1 -2 and sequence utility).
                for i in range(len(tokens)-3):
                    currentToken = tokens[i]

                    if len(currentToken) == 0:
                        continue

                    #  if the current token is -1
                    if currentToken == "-1":
                        #  It means that it is the end of an itemset.
                        #  So we check if there was a promising item in that itemset
                        if currentItemsetHasAPromisingItem:
                            #  If yes, then we keep the -1, because
                            #  that itemset will not be empty.
                            #  We store the -1 in the respective buffers
                            itemBuffer.append(-1)
                            utilityBuffer.append(-1)
                            # //itemBuffer[itemBufferLength] = -1
                            # //utilityBuffer[itemBufferLength] = -1
                            #  We increase the length of the data stored in the buffers
                            itemBufferLength += 1
                            #  we update the number of itemsets in that sequence that are not empty
                            nbItemsets += 1
                            #  we reset the following variable for the next itemset that
                            #  we will read after this one (if there is one)
                            currentItemsetHasAPromisingItem = False
                    else:
                        #  if  the current token is an item
                        #   We will extract the item from the string:
                        positionLeftBracketString = currentToken.index('[')
                        positionRightBracketString = currentToken.index(']')
                        itemString = currentToken[:positionLeftBracketString]
                        item = int(itemString)
                        #  We also extract the utility from the string:
                        utilityString = currentToken[positionLeftBracketString+1:positionRightBracketString]
                        itemUtility = int(utilityString)

                        #  it the item is promising (its SWU >= minutility), then
                        #  we keep it in the sequence
                        if mapItemToSWU[item] >= minUtility:
                            #  We remember that this itemset contains a promising item
                            currentItemsetHasAPromisingItem = True
                            #  We store the item and its utility in the buffers
                            #  for temporarily storing the sequence
                            itemBuffer.append(item)
                            utilityBuffer.append(itemUtility)
                            # //itemBuffer[itemBufferLength] = item
                            # //utilityBuffer[itemBufferLength] = itemUtility
                            itemBufferLength += 1
                            #  We also put this item in the buffer for all items of this sequence
                            itemsLength += 1
                            # itemsSequenceBuffer[itemsLength] = item
                            itemsSequenceBuffer.append(item)
                        else:
                            #  if the item is not promising, we subtract its utility
                            #  from the sequence utility, and we do not add it to the buffers
                            #  because this item will not be part of a high utility sequential pattern.
                            sequenceUtility -= itemUtility

                if sequenceUtility == 0:
                    continue

                #  If we are in debug mode,
                if self.DEBUG:
                    #  We will show the original sequence
                    print("SEQUENCE BEFORE REMOVING UNPROMISING ITEMS:")
                    print(" " + line)
                    #  We will show the sequence after removing unpromising items
                    print("SEQUENCE AFTER REMOVING UNPROMISING ITEMS:")
                    strItems = ""
                    for i in range(itemBufferLength):
                        strItems += "{}[{}] ".format(itemBuffer[i], utilityBuffer[i])
                    print("{} NEW SEQUENCE UTILITY {}".format(strItems, sequenceUtility))

                itemsSequenceBuffer = list(set(itemsSequenceBuffer))
                itemsSequenceBuffer.sort()

                if self.DEBUG:
                    print("\nLIST OF PROMISING ITEMS IN THAT SEQUENCE:")
                    strISB = ""
                    for i in itemsSequenceBuffer:
                        strISB += "{} ".format(i)
                    print(strISB)

                nbItems = len(itemsSequenceBuffer)

                matrix = QMatrix(nbItems, nbItemsets, itemsSequenceBuffer, sequenceUtility)
                database.append(matrix)
                
                posBuffer = 0
                for itemset in range(nbItemsets):
                    posNames = 0
                    while posBuffer < itemBufferLength:
                        item = itemBuffer[posBuffer]
                        if item == -1:
                            posBuffer += 1
                            break
                        elif item == matrix.itemNames[posNames]:
                            utility = utilityBuffer[posBuffer]
                            sequenceUtility -= utility
                            matrix.registerItem(posNames, itemset, utility, sequenceUtility)
                            posNames += 1
                            posBuffer += 1
                        elif item > matrix.itemNames[posNames]:
                            matrix.registerItem(posNames, itemset, 0, sequenceUtility)
                            posNames += 1
                        else:
                            matrix.registerItem(posNames, itemset, 0, sequenceUtility)
                            posBuffer += 1

                if self.DEBUG:
                    print(matrix.toString())
                    print("\n")

        except:
            self.writer.close()
            traceback.print_exc()
        finally:
            myInput.close()

        self.checkMemory()

        self.uspanFirstTime(self.patternBuffer, 0, database)

        self.checkMemory()

        self.writer.close()

        self.startTimestamp = time.time() * 1000

    #
    # 	 * This is the initial call to the USpan procedure to find all High utility sequential patterns
    # 	 * of length 1. It is optimized for finding patterns of length 1.
    # 	 * To find larger patterns the "uspan" method is then used recursively.
    # 	 * @param prefix  This is the buffer for storing the current prefix. Initially, it is empty.
    # 	 * @param prefixLength The current prefix length. Initially, it is zero.
    # 	 * @param database This is the original sequence database (as a set of QMatrix)
    # 	 * @throws IOException If an error occurs while reading/writting to file.

    def uspanFirstTime(self, prefix, prefixLength, database):
        #  For the first call to USpan, we only need to check I-CONCATENATIONS
        #  =======================  I-CONCATENATIONS  ===========================/
        #  scan the projected database to
        #  calculate the SWU of each item
        mapItemSWU = {}
        for qmatrix in database:
            #  for each row (item) we will update the swu of the corresponding item
            for item in qmatrix.itemNames:
                #  get its swu and update
                if item in mapItemSWU:
                    currentSWU = mapItemSWU[item]
                    mapItemSWU[item] = currentSWU + qmatrix.swu
                else:
                    mapItemSWU[item] = qmatrix.swu

        #  For each item
        for key, value in mapItemSWU.items():
            itemSWU = value
            #  if the item is promising
            if itemSWU >= self.minUtility:
                #  We get the item
                item = key
                #  We initialize two variables for calculating the total utility and remaining utility
                #  of that item
                totalUtility = 0
                totalRemainingUtility = 0
                #  We also initialize a variable to remember the projected qmatrixes of sequences
                #  where this item appears. This will be used for call to the recursive
                #  "uspan" method later.
                matrixProjections = []
                #  For each sequence
                for qmatrix in database:
                    #  if the item appear in that sequence (in that qmatrix)
                    row = self.binarySearch(qmatrix.itemNames, item)
                    if row >= 0:
                        #  create a list to store the positions (itemsets) where this item
                        #  appear in that sequence
                        positions = []
                        #  find the max utility of this item in that sequence
                        #  and the max remaining utility
                        maxUtility = 0
                        maxRemainingUtility = 0
                        #  for each itemset in that sequence
                        ####################################
                        for itemset in range(len(qmatrix.matrixItemRemainingUtility[row])):
                            #  get the utility of the item in that itemset
                            utility = qmatrix.matrixItemUtility[row][itemset]
                            if utility > 0:
                                positions.append(MatrixPosition(row, itemset, utility))
                                if utility > maxUtility:
                                    maxUtility = utility
                                    remaining = qmatrix.matrixItemRemainingUtility[row][itemset]
                                    if remaining > 0 and maxRemainingUtility == 0:
                                        maxRemainingUtility = remaining

                        totalUtility += maxUtility
                        totalRemainingUtility += maxRemainingUtility
                        projection = QMatrixProjection()
                        projection.qMatrixProjection(qmatrix, positions)

                        matrixProjections.append(projection)


                prefix[0] = item
                if totalUtility >= self.minUtility:
                    self.writeOut(prefix, 1, totalUtility)
                    ################# 2018. 02. 20 ##################

                if totalUtility + totalRemainingUtility >= self.minUtility:
                    if 1 < self.maxPatternLength:
                        self.uspan(prefix, 1, matrixProjections, 1)
        self.checkMemory()



    def checkIfUtilityOfPatternIsCorrect(self, prefix, prefixLength, utility):
        calculatedUtility = 0
        myInput = open(self.input, 'r')

        try:
            for thisLine in myInput.readlines():
                #  if the line is a comment, is  empty or is a kind of metadata, skip it
                if (not thisLine) or (thisLine[:1] == '#') or (thisLine[:1] == '%') or (thisLine[:1] == '@'):
                    continue

                tokens = thisLine.split(" ")
                tokensLength = len(tokens) - 3

                sequence = [None] * tokensLength
                sequenceUtility = [None] * tokensLength

                for i in range(tokensLength):
                    currentToken = tokens[i]

                    if(len(currentToken) == 0):
                        continue

                    item = None
                    itemUtility = None

                    if currentToken == "-1":
                        item = -1
                        itemUtility = 0
                    else:
                        positionLeftBracketString = currentToken.index('[')
                        positionRightBracketString = currentToken.index(']')
                        itemString = currentToken[:positionLeftBracketString]
                        item = int(itemString)

                        utilityString = currentToken[positionLeftBracketString+1:positionRightBracketString]
                        itemUtility = int(utilityString)

                    sequence[i] = item
                    sequenceUtility[i] = itemUtility

                util = self.tryToMatch(sequence, sequenceUtility, prefix, prefixLength, 0, 0, 0)
                calculatedUtility += util
        except:
            self.writer.close()
            traceback.print_exc()
        finally:
            myInput.close()

        if calculatedUtility != utility:
            print(" ERROR, WRONG UTILITY FOR PATTERN : ", end="")
            for i in range(prefixLength):
                print(prefix[i], end="")
            print(" utility is: {} but should be: ".format(utility,calculatedUtility))
            input() # like java's system.in.read()


    def tryToMatch(self, sequence, sequenceUtility, prefix, prefixLength, prefixPos, seqPos, utility):
        otherUtilityValues = []
        posP = prefixPos
        posS = seqPos
        previousPrefixPos = prefixPos
        itemsetUtility = 0
        while (posP < prefixLength) & (posS < len(sequence)):
            if prefix[posP] == -1 and sequence[posS] == -1:
                posS += 1
                otherUtility = self.tryToMatch(sequence, sequenceUtility, prefix, prefixLength, previousPrefixPos, posS, utility)
                otherUtilityValues.append(otherUtility)

                posP += 1
                utility += itemsetUtility
                itemsetUtility = 0
                previousPrefixPos = posP

            elif prefix[posP] == -1:
                while (posS < len(sequence)) and (sequence[posS] != -1):
                    posS += 1
                otherUtility = self.tryToMatch(sequence, sequenceUtility, prefix, prefixLength, previousPrefixPos, posS, utility)
                otherUtilityValues.append(otherUtility)
                utility += itemsetUtility
                itemsetUtility = 0
                previousPrefixPos = posP

            elif sequence[posS] == -1:
                posP = previousPrefixPos
                itemsetUtility = 0
                posS += 1

            elif prefix[posP] == sequence[posS]:
                posP += 1
                itemsetUtility += sequenceUtility[posS]
                posS += 1
                if posP == prefixLength:
                    while (posS < len(sequence)) and (sequence[posS] != -1):
                        posS += 1
                    otherUtility = self.tryToMatch(sequence, sequenceUtility, prefix, prefixLength, previousPrefixPos, posS, utility)
                    otherUtilityValues.append(otherUtility)
                    utility += itemsetUtility

            elif prefix[posP] != sequence[posS]:
                posS += 1

        max = 0
        if posP == prefixLength:
            max = utility
        for utilValue in otherUtilityValues:
            if utilValue > utility:
                max = utilValue

        return max
        ### // end of tryToMatch()

    def printStatistics(self):
        print("=================  USPAN ALGORITHM STATS ===============")
        print(" Total time ~ {} ms".format(int(round(self.endTimestamp - self.startTimestamp))))
        print(" Max Memory ~ {} MB".format(self.maxMemory))
        print(" High-utility sequential pattern count : {}".format(self.patternCount))
        print("========================================================")

    def checkMemory(self):
        # unit : MB
        currentMemory = psutil.virtual_memory().used / 1024 / 1024 / 1024
        # print("currentMemory : ", currentMemory)
        if currentMemory > self.maxMemory:
            self.maxMemory = currentMemory

    def setMaxPatternLength(self, maxPatternLength):
        self.maxPatternLength = maxPatternLength

    def binarySearch(self, a, x):
        pos = np.searchsorted(a, x)
        return (pos if pos != len(a) and a[pos] == x else -1)


    def writeOut(self, prefix, prefixLength, utility):
        self.patternCount += 1
        buffer = []
        if(self.SAVE_RESULT_EASIER_TO_READ_FORMAT == False):
            # append each item of the pattern
            for i in range(prefixLength):
                buffer.append(prefix[i])
                buffer.append(" ")

            buffer.append("-1 #UTIL: ")
            buffer.append(utility)
        else:
            buffer.append("<")
            buffer.append("(")
            for i in range(prefixLength):
                if prefix[i] == -1:
                    buffer.append(")(")
                else:
                    buffer.append(prefix[i])
            buffer.append(")>:")
            buffer.append(utility)
        buffer = ''.join(map(str, buffer))

        self.writer.writelines(buffer + '\n')

        if self.DEBUG:
            print("SAVING : {} \n".format(buffer))
            #  check if the calculated utility is correct by reading the file for debugging purpose
            self.checkIfUtilityOfPatternIsCorrect(prefix, prefixLength, utility)






    def uspan(self, prefix, prefixLength, projectedDatabase, itemCount):
        if self.DEBUG:
            for i in range(prefixLength):
                print("{} ".format(prefix[i]), end="")
            print("\n")

        #  =======================  I-CONCATENATIONS  ===========================/
        #  We first try to perform I-Concatenations to grow the pattern larger.
        #  we scan the projected database to calculated the SWU of each item that could
        #  ne concatenated to the prefix
        #  The following map will store for each item, their SWU (key: item value: swu)
        mapItemSWU = {}

        for qmatrix in projectedDatabase:

            for position in qmatrix.positions:
                row = position.row + 1
                column = position.column
                localSequenceUtility = qmatrix.getLocalSequenceUtility(position)

                for row in range(row, len(qmatrix.getItemNames())):
                    item = qmatrix.getItemNames()[row]
                    if qmatrix.getItemUtility(row, column) > 0:
                        currentSWU = mapItemSWU.get(item)
                        if currentSWU == None:
                            ######### TODO: inner class 처리 ###########
                            pair = self.Pair()
                            pair.lastSID = qmatrix
                            pair.swu = position.utility + localSequenceUtility
                            mapItemSWU[item] = pair

                        elif currentSWU.lastSID != qmatrix:
                            currentSWU.lastSID = qmatrix
                            currentSWU.swu += position.utility + localSequenceUtility

                        else:
                            tempSWU = position.utility + localSequenceUtility
                            if tempSWU > currentSWU.swu:
                                currentSWU.swu = tempSWU


        for key, value in mapItemSWU.items():
            itemSWU = value
            if itemSWU.swu >= self.minUtility:
                item = key
                totalUtility = 0
                totalRemainingUtility = 0
                matrixProjections = []
                for qmatrix in projectedDatabase:
                    rowItem = self.binarySearch(qmatrix.getItemNames(), item)

                    if rowItem >= 0:
                        positions = []
                        maxUtility = 0
                        maxRemainingUtility = 0

                        #  for each position of the prefix
                        for position in qmatrix.positions:
                            column = position.column
                            newItemUtility = qmatrix.getItemUtility(int(rowItem), int(column))
                            if newItemUtility > 0:
                                newPrefixUtility = position.utility + newItemUtility
                                positions.append(MatrixPosition(rowItem, column, newPrefixUtility))
                                if newPrefixUtility > maxUtility:
                                    maxUtility = newPrefixUtility
                                    remaining = qmatrix.getRemainingUtility(rowItem, column)
                                    if remaining > 0 and maxRemainingUtility == 0:
                                        maxRemainingUtility = remaining

                        totalUtility += maxUtility
                        totalRemainingUtility += maxRemainingUtility
                        projection = QMatrixProjection()
                        projection.qProjectionMatrix(qmatrix, positions)

                        matrixProjections.append(projection)


                prefix[prefixLength] = item
                if totalUtility >= self.minUtility:
                    self.writeOut(prefix, prefixLength + 1, totalUtility)

                if totalUtility + totalRemainingUtility >= self.minUtility:
                    if itemCount + 1 < self.maxPatternLength:
                        self.uspan(prefix, prefixLength + 1, matrixProjections, itemCount + 1)

        #  =======================  S-CONCATENATIONS  ===========================/
        #  We will next look for S-Concatenations
        #  We first clear the map for calculating the SWU of items to reuse it instead of creating a new one
        mapItemSWU.clear()
        #  Now, we will loop over sequences of the projected database to calculate the local SWU of each item
        #  For each sequence in the projected database

        for qmatrix in projectedDatabase:

            for position in qmatrix.positions:
                localSequenceUtility = qmatrix.getLocalSequenceUtility(position)

                for row in range(len(qmatrix.getItemNames())):
                    item = qmatrix.getItemNames()[row]

                    for column in range(position.column+1,
                                        len(qmatrix.originalMatrix.matrixItemUtility[row])):

                        if qmatrix.getItemUtility(row, column) > 0:
                            currentSWU = mapItemSWU.get(item)
                            if currentSWU == None:
                                ######### TODO: inner class 처리 ###########
                                pair = self.Pair()
                                pair.lastSID = qmatrix
                                pair.swu = position.utility + localSequenceUtility
                                mapItemSWU[item] = pair

                            elif currentSWU.lastSID != qmatrix:
                                currentSWU.lastSID = qmatrix
                                currentSWU.swu += position.utility + localSequenceUtility

                            else:
                                tempSWU = position.utility + localSequenceUtility
                                if tempSWU > currentSWU.swu:
                                    currentSWU.swu = tempSWU
                            #  we don't need to check the other column if we found one column where this item
                            #  appears after the previous item
                            break


        for key, value in mapItemSWU.items():
            itemSWU = value

            if itemSWU.swu >= self.minUtility:
                item = key
                totalUtility = 0
                totalRemainingUtility = 0
                matrixProjections = []

                for qmatrix in projectedDatabase:
                    rowItem = self.binarySearch(qmatrix.getItemNames(), item)

                    if rowItem >= 0:
                        maxUtility = 0
                        maxRemainingUtility = 0
                        positions = []

                        #  for each position of the prefix
                        for position in qmatrix.positions:

                            for column in range(position.column + 1,
                                                len(qmatrix.originalMatrix.matrixItemUtility[rowItem])):
                                newItemUtility = qmatrix.getItemUtility(int(rowItem), int(column))
                                if newItemUtility > 0:
                                    newPrefixUtility = position.utility + newItemUtility
                                    positions.append(MatrixPosition(rowItem, column, newPrefixUtility))
                                    if newPrefixUtility > maxUtility:
                                        maxUtility = newPrefixUtility
                                        remaining = qmatrix.getRemainingUtility(rowItem, column)
                                        if remaining > 0 and maxRemainingUtility == 0:
                                            maxRemainingUtility = remaining

                        totalUtility += maxUtility
                        totalRemainingUtility += maxRemainingUtility

                        projection = QMatrixProjection()
                        projection.qProjectionMatrix(qmatrix, positions)
                        matrixProjections.append(projection)

                prefix[prefixLength] = -1
                prefix[prefixLength + 1] = item

                if totalUtility >= self.minUtility:
                    self.writeOut(prefix, prefixLength + 2, totalUtility)

                if totalUtility + totalRemainingUtility >= self.minUtility:
                    if itemCount + 1 < self.maxPatternLength:
                        self.uspan(prefix, prefixLength + 2, matrixProjections, itemCount + 1)


        self.checkMemory()




    class Pair(object):
        def __init__(self):
            self.swu = 0
            self.lastSID = None

