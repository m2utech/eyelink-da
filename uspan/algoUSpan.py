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
        # self.BUFFERS_SIZE = 2000
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
        # //self.patternBuffer = [None] * self.BUFFERS_SIZE
        self.patternBuffer = []
        self.maxMemory = 0
        self.startTimestamp = time.time()*1000
        print("startTimestamp : ", self.startTimestamp)
        # self.writer = BufferedWriter(FileWriter(output))
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
            traceback.print_exc()
        finally:
            myInput.close()

        self.checkMemory()

        self.uspanFirstTime(self.patternBuffer, 0, database)

        self.checkMemory()


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
                    # row = self.binary_search(qmatrix.itemNames, 5, 0, len(qmatrix.itemNames))
                    pos = np.searchsorted(qmatrix.itemNames, item)
                    row = pos if pos != len(qmatrix.itemNames) and qmatrix.itemNames[pos] == item else -1
                    # Arrays.binarySearch(qmatrix.itemNames, item)
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
                    writeOut(prefix, 1, totalUtility)
                    ################# 2018. 02. 20 ##################

                if totalUtility + totalRemainingUtility >= self.minUtility:
                    if 1 < self.maxPatternLength:
                        uspan(prefix, 1, matrixProjections, 1)
        MemoryLogger.getInstance().checkMemory()

    # class Pair(object):
    #     """ generated source for class Pair """
    #     swu = int()
    #     lastSID = None

    # def uspan(self, prefix, prefixLength, projectedDatabase, itemCount):
    #     """ generated source for method uspan """
    #     if self.DEBUG:
    #         i = 0
    #         while i < prefixLength:
    #             print(prefix[i] + " ", end="")
    #             i += 1
    #         print()
    #         print()
    #     mapItemSWU = HashMap()
    #     for qmatrix in projectedDatabase:
    #         for position in qmatrix.positions:
    #             row = position.row + 1
    #             column = position.column
    #             localSequenceUtility = qmatrix.getLocalSequenceUtility(position)
    #             while len(length):
    #                 item = qmatrix.getItemNames()[row]
    #                 if qmatrix.getItemUtility(row, column) > 0:
    #                     currentSWU = mapItemSWU.get(item)
    #                     if currentSWU == None:
    #                         pair = self.Pair()
    #                         pair.lastSID = qmatrix
    #                         pair.swu = position.utility + localSequenceUtility
    #                         mapItemSWU.put(item, pair)
    #                     elif currentSWU.lastSID != qmatrix:
    #                         currentSWU.lastSID = qmatrix
    #                         currentSWU.swu += position.utility + localSequenceUtility
    #                     else:
    #                         tempSWU = position.utility + localSequenceUtility
    #                         if tempSWU > currentSWU.swu:
    #                             currentSWU.swu = tempSWU
    #                 row += 1
    #     for entry in mapItemSWU.entrySet():
    #         itemSWU = entry.getValue()
    #         if itemSWU.swu >= self.minUtility:
    #             item = entry.getKey()
    #             totalUtility = 0
    #             totalRemainingUtility = 0
    #             matrixProjections = ArrayList()
    #             for qmatrix in projectedDatabase:
    #                 rowItem = Arrays.binarySearch(qmatrix.getItemNames(), item)
    #                 if rowItem >= 0:
    #                     maxUtility = 0
    #                     maxRemainingUtility = 0
    #                     positions = ArrayList()
    #                     for position in qmatrix.positions:
    #                         column = position.column
    #                         newItemUtility = qmatrix.getItemUtility(rowItem, column)
    #                         if newItemUtility > 0:
    #                             newPrefixUtility = position.utility + newItemUtility
    #                             positions.add(MatrixPosition(rowItem, column, newPrefixUtility))
    #                             if newPrefixUtility > maxUtility:
    #                                 maxUtility = newPrefixUtility
    #                                 remaining = qmatrix.getRemainingUtility(rowItem, column)
    #                                 if remaining > 0 and maxRemainingUtility == 0:
    #                                     maxRemainingUtility = remaining
    #                     totalUtility += maxUtility
    #                     totalRemainingUtility += maxRemainingUtility
    #                     projection = QMatrixProjection(qmatrix, positions)
    #                     matrixProjections.add(projection)
    #             prefix[prefixLength] = item
    #             if totalUtility >= self.minUtility:
    #                 writeOut(prefix, prefixLength + 1, totalUtility)
    #             if totalUtility + totalRemainingUtility >= self.minUtility:
    #                 if itemCount + 1 < self.maxPatternLength:
    #                     self.uspan(prefix, prefixLength + 1, matrixProjections, itemCount + 1)
    #     mapItemSWU.clear()
    #     for qmatrix in projectedDatabase:
    #         for position in qmatrix.positions:
    #             localSequenceUtility = qmatrix.getLocalSequenceUtility(position)
    #             row = 0
    #             while len(length):
    #                 item = qmatrix.getItemNames()[row]
    #                 column = position.column + 1
    #                 while len(length):
    #                     if qmatrix.getItemUtility(row, column) > 0:
    #                         currentSWU = mapItemSWU.get(item)
    #                         if currentSWU == None:
    #                             pair = self.Pair()
    #                             pair.lastSID = qmatrix
    #                             pair.swu = position.utility + localSequenceUtility
    #                             mapItemSWU.put(item, pair)
    #                         elif currentSWU.lastSID != qmatrix:
    #                             currentSWU.lastSID = qmatrix
    #                             currentSWU.swu += position.utility + localSequenceUtility
    #                         else:
    #                             tempSWU = position.utility + localSequenceUtility
    #                             if tempSWU > currentSWU.swu:
    #                                 currentSWU.swu = tempSWU
    #                         break
    #                     column += 1
    #                 row += 1
    #     for entry in mapItemSWU.entrySet():
    #         itemSWU = entry.getValue()
    #         if itemSWU.swu >= self.minUtility:
    #             item = entry.getKey()
    #             totalUtility = 0
    #             totalRemainingUtility = 0
    #             matrixProjections = ArrayList()
    #             for qmatrix in projectedDatabase:
    #                 rowItem = Arrays.binarySearch(qmatrix.getItemNames(), item)
    #                 if rowItem >= 0:
    #                     maxUtility = 0
    #                     maxRemainingUtility = 0
    #                     positions = ArrayList()
    #                     for position in qmatrix.positions:
    #                         column = position.column + 1
    #                         while len(length):
    #                             newItemUtility = qmatrix.getItemUtility(rowItem, column)
    #                             if newItemUtility > 0:
    #                                 newPrefixUtility = position.utility + newItemUtility
    #                                 positions.add(MatrixPosition(rowItem, column, newPrefixUtility))
    #                                 if newPrefixUtility > maxUtility:
    #                                     maxUtility = newPrefixUtility
    #                                     remaining = qmatrix.getRemainingUtility(rowItem, column)
    #                                     if remaining > 0 and maxRemainingUtility == 0:
    #                                         maxRemainingUtility = remaining
    #                             column += 1
    #                     totalUtility += maxUtility
    #                     totalRemainingUtility += maxRemainingUtility
    #                     projection = QMatrixProjection(qmatrix, positions)
    #                     matrixProjections.add(projection)
    #             prefix[prefixLength] = -1
    #             prefix[prefixLength + 1] = item
    #             if totalUtility >= self.minUtility:
    #                 writeOut(prefix, prefixLength + 2, totalUtility)
    #             if totalUtility + totalRemainingUtility >= self.minUtility:
    #                 if itemCount + 1 < self.maxPatternLength:
    #                     self.uspan(prefix, prefixLength + 2, matrixProjections, itemCount + 1)
    #     MemoryLogger.getInstance().checkMemory()





    # def writeOut(self, prefix, prefixLength, utility):
    #     """ generated source for method writeOut """
    #     self.patternCount += 1
    #     buffer_ = StringBuilder()
    #     if self.SAVE_RESULT_EASIER_TO_READ_FORMAT == False:
    #         i = 0
    #         while i < prefixLength:
    #             buffer_.append(prefix[i])
    #             buffer_.append(' ')
    #             i += 1
    #         buffer_.append("-1 #UTIL: ")
    #         buffer_.append(utility)
    #     else:
    #         buffer_.append('<')
    #         buffer_.append('(')
    #         i = 0
    #         while i < prefixLength:
    #             if prefix[i] == -1:
    #                 buffer_.append(")(")
    #             else:
    #                 buffer_.append(prefix[i])
    #             i += 1
    #         buffer_.append(")>:")
    #         buffer_.append(utility)
    #     self.writer.write(buffer_.__str__())
    #     self.writer.newLine()
    #     if self.DEBUG:
    #         print(" SAVING : " + buffer_.__str__())
    #         print()
    #         checkIfUtilityOfPatternIsCorrect(prefix, prefixLength, utility)

    # def checkIfUtilityOfPatternIsCorrect(self, prefix, prefixLength, utility):
    #     """ generated source for method checkIfUtilityOfPatternIsCorrect """
    #     calculatedUtility = 0
    #     myInput = BufferedReader(InputStreamReader(FileInputStream(File(self.input))))
    #     try:
    #         thisLine = None
    #         while (thisLine = myInput.readLine()) != None:
    #             if thisLine.isEmpty() == True or thisLine.charAt(0) == '#' or thisLine.charAt(0) == '%' or thisLine.charAt(0) == '@':
    #                 continue 
    #             tokens = thisLine.split(" ")
    #             tokensLength = len(tokens)
    #             sequence = [None] * tokensLength
    #             sequenceUtility = [None] * tokensLength
    #             i = 0
    #             while i < tokensLength:
    #                 currentToken = tokens[i]
    #                 if 0 == len(currentToken):
    #                     i += 1
    #                     continue 
    #                 item = int()
    #                 itemUtility = int()
    #                 if currentToken == "-1":
    #                     item = -1
    #                     itemUtility = 0
    #                 else:
    #                     positionLeftBracketString = currentToken.indexOf('[')
    #                     positionRightBracketString = currentToken.indexOf(']')
    #                     itemString = currentToken.substring(0, positionLeftBracketString)
    #                     item = Integer.parseInt(itemString)
    #                     utilityString = currentToken.substring(positionLeftBracketString + 1, positionRightBracketString)
    #                     itemUtility = Integer.parseInt(utilityString)
    #                 sequence[i] = item
    #                 sequenceUtility[i] = itemUtility
    #                 i += 1
    #             util = tryToMatch(sequence, sequenceUtility, prefix, prefixLength, 0, 0, 0)
    #             calculatedUtility += util
    #     except Exception as e:
    #         e.printStackTrace()
    #     finally:
    #         if myInput != None:
    #             myInput.close()
    #     if calculatedUtility != utility:
    #         print(" ERROR, WRONG UTILITY FOR PATTERN : ", end="")
    #         i = 0
    #         while i < prefixLength:
    #             print(prefix[i], end="")
    #             i += 1
    #         print(" utility is: " + utility + " but should be: " + calculatedUtility)
    #         System.in_.read()

    # def tryToMatch(self, sequence, sequenceUtility, prefix, prefixLength, prefixPos, seqPos, utility):
    #     """ generated source for method tryToMatch """
    #     otherUtilityValues = ArrayList()
    #     posP = prefixPos
    #     posS = seqPos
    #     previousPrefixPos = prefixPos
    #     itemsetUtility = 0
    #     while posP < prefixLength & len(sequence):
    #         if prefix[posP] == -1 and sequence[posS] == -1:
    #             posS += 1
    #             otherUtility = self.tryToMatch(sequence, sequenceUtility, prefix, prefixLength, previousPrefixPos, posS, utility)
    #             otherUtilityValues.add(otherUtility)
    #             posP += 1
    #             utility += itemsetUtility
    #             itemsetUtility = 0
    #             previousPrefixPos = posP
    #         elif prefix[posP] == -1:
    #             while sequence[posS] != -1 and len(sequence):
    #                 posS += 1
    #             otherUtility = self.tryToMatch(sequence, sequenceUtility, prefix, prefixLength, previousPrefixPos, posS, utility)
    #             otherUtilityValues.add(otherUtility)
    #             utility += itemsetUtility
    #             itemsetUtility = 0
    #             previousPrefixPos = posP
    #         elif sequence[posS] == -1:
    #             posP = previousPrefixPos
    #             itemsetUtility = 0
    #             posS += 1
    #         elif prefix[posP] == sequence[posS]:
    #             posP += 1
    #             itemsetUtility += sequenceUtility[posS]
    #             posS += 1
    #             if posP == prefixLength:
    #                 while sequence[posS] != -1 and len(sequence):
    #                     posS += 1
    #                 otherUtility = self.tryToMatch(sequence, sequenceUtility, prefix, prefixLength, previousPrefixPos, posS, utility)
    #                 otherUtilityValues.add(otherUtility)
    #                 utility += itemsetUtility
    #         elif prefix[posP] != sequence[posS]:
    #             posS += 1
    #     max = 0
    #     if posP == prefixLength:
    #         max = utility
    #     for utilValue in otherUtilityValues:
    #         if utilValue > utility:
    #             max = utilValue
    #     return max

    # def printStatistics(self):
    #     """ generated source for method printStatistics """
    #     print("=============  USPAN ALGORITHM v2.14 - STATS ==========")
    #     print(" Total time ~ " + (self.endTimestamp - self.startTimestamp) + " ms")
    #     print(" Max Memory ~ " + MemoryLogger.getInstance().getMaxMemory() + " MB")
    #     print(" High-utility sequential pattern count : " + self.patternCount)
    #     print("========================================================")

    def checkMemory(self):
        # unit : MB
        currentMemory = psutil.virtual_memory().used / 1024 / 1024 / 1024
        print("currentMemory : ", currentMemory)
        if currentMemory > self.maxMemory:
            self.maxMemory = currentMemory

    def setMaxPatternLength(self, maxPatternLength):
        self.maxPatternLength = maxPatternLength

    def binarySearch(self, A, B):
        idx = np.searchsorted(A,B)

        idx2 = np.minimum(len(A) - 1, np.searchsorted(A,B))
        idx1 = np.maximum(0, idx2 - 1)
        idx2_is_better = np.abs(A[idx1] - B) > np.abs(A[idx2] - B)
        np.putmask(idx1, idx2_is_better, idx2)
        return  A[idx1]

    def binary_search(self, a, x, lo=0, hi=None):
        hi = hi if hi is not None else len(a)  # hi defaults to len(a)
        pos = bisect_left(a, x, lo, hi)  # find insertion position
        return (pos if pos != hi and a[pos] == x else -1)  # don't walk off the end
