from __future__ import print_function
import time
import traceback

class AlgoUPGrowth(object):
    #  variable for statistics
    maxMemory = 0       # the maximum memory usage
    startTimestamp = 0  # the time the algorithm started
    endTimestamp = 0    # the time the algorithm terminated
    huiCount = 0        # the number of HUIs generated
    phuisCount = int()  # the number of PHUIs generated

    #  map for minimum node utility during DLU(Decreasing Local Unpromizing items) strategy
    mapMinimumItemUtility = {}

    #  writer to write the output file
    writer = None

    #  Structure to store the potential HUIs
    phuis = list()
    # phuis = ArrayList()

    #  To activate debug mode
    DEBUG = False

    # 	 * Method to run the algorithm
    # 	 * @param input path to an input file
    # 	 * @param output  path for writing the output file
    # 	 * @param minUtility  the minimum utility threshold
    # TODO : IOException
    def runAlgorithm(self, inputFile, outputFile, minUtility):
        self.maxMemory = 0
        self.startTimestamp = time.time()
        print(self.startTimestamp)

        mapItemToTWU = {}

        try:
            with open(inputFile, 'r') as input:
                for line in input:
                    split = line.rstrip().split(":")
                    items = split[0].split(" ")
                    transactionUtility = int(split[1])

                    for i in range(len(items)):
                        item = int(items[i])
                        twu = mapItemToTWU.get(item)
                        twu = transactionUtility if (twu == None) else twu + transactionUtility
                        # mapItemToTWU.update({item : twu})
                        mapItemToTWU[item] = twu
        except:
            traceback.print_exc()

        mapMinimumItemUtility = {}

        try:
            tree = UPTree()
            with open(inputFile, 'r') as input:
                for line in input:
                    split = line.rstrip().split(":")
                    items = split[0].split(" ")
                    utilityValues = split[2].split(" ")

                    for i in range(len(items)):
                        item = int(items[i])
                        twu = mapItemToTWU.get(item)
                        twu = transactionUtility if (twu == None) else twu + transactionUtility
                        # mapItemToTWU.update({item : twu})
                        mapItemToTWU[item] = twu
        except:
            pass


    #     try:
    #         tree = UPTree()
    #         myInput = BufferedReader(InputStreamReader(FileInputStream(File(input))))
    #         while (thisLine = myInput.readLine()) != None:
    #             if thisLine.isEmpty() == True or thisLine.charAt(0) == '#' or thisLine.charAt(0) == '%' or thisLine.charAt(0) == '@':
    #                 continue 
    #             split = thisLine.split(":")
    #             items = split[0].split(" ")
    #             utilityValues = split[2].split(" ")
    #             remainingUtility = 0
    #             revisedTransaction = ArrayList()
    #             i = 0
    #             while len(items):
    #                 itm = Integer.parseInt(items[i])
    #                 utility = Integer.parseInt(utilityValues[i])
    #                 if mapItemToTWU.get(itm) >= minUtility:
    #                     element = Item(itm, utility)
    #                     revisedTransaction.add(element)
    #                     remainingUtility += utility
    #                     minItemUtil = self.mapMinimumItemUtility.get(itm)
    #                     if (minItemUtil == None) or (minItemUtil >= utility):
    #                         self.mapMinimumItemUtility.put(itm, utility)
    #                     element = None
    #                 i += 1
    #             Collections.sort(revisedTransaction, Comparator())
    #             tree.addTransaction(revisedTransaction, remainingUtility)
    #         tree.createHeaderList(mapItemToTWU)
    #         checkMemory()
    #         if self.DEBUG:
    #             print("GLOBAL TREE" + "\nmapITEM-TWU : " + mapItemToTWU + "\nmapITEM-MINUTIL : " + self.mapMinimumItemUtility + "\n" + tree.__str__())
    #         upgrowth(tree, minUtility, [None] * 0)
    #         checkMemory()
    #     except Exception as e:
    #         e.printStackTrace()
    #     finally:
    #         if myInput != None:
    #             myInput.close()
    #     self.phuisCount = len(self.phuis)
    #     Collections.sort(self.phuis, Comparator())
    #     try:
    #         myInput = BufferedReader(InputStreamReader(FileInputStream(File(input))))
    #         while (thisLine = myInput.readLine()) != None:
    #             if thisLine.isEmpty() == True or thisLine.charAt(0) == '#' or thisLine.charAt(0) == '%' or thisLine.charAt(0) == '@':
    #                 continue 
    #             split = thisLine.split(":")
    #             items = split[0].split(" ")
    #             utilityValues = split[2].split(" ")
    #             revisedTransaction = ArrayList()
    #             i = 0
    #             while len(items):
    #                 item = Integer.parseInt(items[i])
    #                 utility = Integer.parseInt(utilityValues[i])
    #                 element = Item(item, utility)
    #                 if mapItemToTWU.get(item) >= minUtility:
    #                     revisedTransaction.add(element)
    #                 i += 1
    #             Collections.sort(revisedTransaction, Comparator())
    #             for itemset in phuis:
    #                 if len(itemset) > len(revisedTransaction):
    #                     break
    #                 updateExactUtility(revisedTransaction, itemset)
    #     except Exception as e:
    #         e.printStackTrace()
    #     for itemset in phuis:
    #         if itemset.getExactUtility() >= minUtility:
    #             writeOut(itemset)
    #     checkMemory()
    #     self.endTimestamp = System.currentTimeMillis()
    #     self.phuis.clear()
    #     self.mapMinimumItemUtility = None
    #     self.writer.close()

    # def compareItemsDesc(self, item1, item2, mapItemEstimatedUtility):
    #     """ generated source for method compareItemsDesc """
    #     compare = mapItemEstimatedUtility.get(item2) - mapItemEstimatedUtility.get(item1)
    #     return item1 - item2 if (compare == 0) else compare

    # def upgrowth(self, tree, minUtility, prefix):
    #     """ generated source for method upgrowth """
    #     i = len(tree.headerList) - 1
    #     while i >= 0:
    #         item = tree.headerList.get(i)
    #         localTree = createLocalTree(minUtility, tree, item)
    #         if self.DEBUG:
    #             print("LOCAL TREE for projection by:" + ("" if (prefix == None) else Arrays.toString(prefix) + ",") + item + "\n" + localTree.__str__())
    #         pathCPB = tree.mapItemNodes.get(item)
    #         pathCPBUtility = 0
    #         while pathCPB != None:
    #             pathCPBUtility += pathCPB.nodeUtility
    #             pathCPB = pathCPB.nodeLink
    #         if pathCPBUtility >= minUtility:
    #             newPrefix = [None] * len(prefix)
    #             System.arraycopy(prefix, 0, newPrefix, 0, )
    #             newPrefix[len(prefix)] = item
    #             savePHUI(newPrefix)
    #             if len(localTree.headerList) > 0:
    #                 self.upgrowth(localTree, minUtility, newPrefix)
    #         i -= 1

    # def createLocalTree(self, minUtility, tree, item):
    #     """ generated source for method createLocalTree """
    #     prefixPaths = ArrayList()
    #     path = tree.mapItemNodes.get(item)
    #     itemPathUtility = HashMap()
    #     while path != None:
    #         nodeutility = path.nodeUtility
    #         if path.parent.itemID != -1:
    #             prefixPath = ArrayList()
    #             prefixPath.add(path)
    #             parentnode = path.parent
    #             while parentnode.itemID != -1:
    #                 prefixPath.add(parentnode)
    #                 pu = itemPathUtility.get(parentnode.itemID)
    #                 pu = nodeutility if (pu == None) else pu + nodeutility
    #                 itemPathUtility.put(parentnode.itemID, pu)
    #                 parentnode = parentnode.parent
    #             prefixPaths.add(prefixPath)
    #         path = path.nodeLink
    #     if self.DEBUG:
    #         print("\n\n\nPREFIXPATHS:")
    #         for prefixPath in prefixPaths:
    #             for node in prefixPath:
    #                 print("    " + node)
    #             print("    --")
    #     localTree = UPTree()
    #     for prefixPath in prefixPaths:
    #         pathCount = prefixPath.get(0).count
    #         pathUtility = prefixPath.get(0).nodeUtility
    #         localPath = ArrayList()
    #         j = 1
    #         while j < len(prefixPath):
    #             itemValue = 0
    #             node = prefixPath.get(j)
    #             if itemPathUtility.get(node.itemID) >= minUtility:
    #                 localPath.add(node.itemID)
    #             else:
    #                 minItemUtility = self.mapMinimumItemUtility.get(node.itemID)
    #                 itemValue = minItemUtility * pathCount
    #             pathUtility = pathUtility - itemValue
    #             j += 1
    #         if self.DEBUG:
    #             print("  path utility after DGU,DGN,DLU: " + pathUtility)
    #         Collections.sort(localPath, Comparator())
    #         localTree.addLocalTransaction(localPath, pathUtility, self.mapMinimumItemUtility, pathCount)
    #     localTree.createHeaderList(itemPathUtility)
    #     return localTree

    # def savePHUI(self, itemset):
    #     """ generated source for method savePHUI """
    #     itemsetObj = Itemset(itemset)
    #     Arrays.sort(itemset)
    #     self.phuis.add(itemsetObj)

    # def updateExactUtility(self, transaction, itemset):
    #     """ generated source for method updateExactUtility """
    #     utility = 0
    #     i = 0
    #     while i < len(itemset):
    #         itemI = itemset.get(i)
    #         j = 0
    #         while j < len(transaction):
    #             itemJ = transaction.get(j)
    #             if itemJ.name == itemI:
    #                 utility += transaction.get(j).utility
    #                 j += 1
    #                 continue 
    #             elif itemJ.name > itemI:
    #                 return
    #             j += 1
    #         return
    #         i += 1
    #     itemset.increaseUtility(utility)

    # def writeOut(self, HUI):
    #     """ generated source for method writeOut """
    #     self.huiCount += 1
    #     buffer_ = StringBuilder()
    #     i = 0
    #     while i < len(HUI):
    #         buffer_.append(HUI.get(i))
    #         buffer_.append(' ')
    #         i += 1
    #     buffer_.append("#UTIL: ")
    #     buffer_.append(HUI.getExactUtility())
    #     self.writer.write(buffer_.__str__())
    #     self.writer.newLine()

    # def checkMemory(self):
    #     """ generated source for method checkMemory """
    #     currentMemory = (Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()) / 1024 / 1024
    #     if currentMemory > self.maxMemory:
    #         self.maxMemory = currentMemory

    # def printStats(self):
    #     """ generated source for method printStats """
    #     print("=============  UP-GROWTH ALGORITHM - STATS =============")
    #     print(" PHUIs (candidates) count: " + self.phuisCount)
    #     print(" Total time ~ " + (self.endTimestamp - self.startTimestamp) + " ms")
    #     print(" Memory ~ " + self.maxMemory + " MB")
    #     print(" HUIs count : " + self.huiCount)
    #     print("===================================================")

