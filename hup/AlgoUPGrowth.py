from __future__ import print_function
import time
import traceback
import operator
import psutil
from UPTree import UPTree
from Item import Item

class AlgoUPGrowth(object):
    def __init__(self):
        #  variable for statistics
        self.maxMemory = 0       # the maximum memory usage
        self.startTimestamp = 0  # the time the algorithm started
        self.endTimestamp = 0    # the time the algorithm terminated
        self.huiCount = 0        # the number of HUIs generated
        self.phuisCount = int()  # the number of PHUIs generated

        #  map for minimum node utility during DLU(Decreasing Local Unpromizing items) strategy
        self.mapMinimumItemUtility = {}

        #  writer to write the output file
        self.writer = None

        #  Structure to store the potential HUIs
        self.phuis = list()
        # phuis = ArrayList()

        #  To activate debug mode
        self.DEBUG = True

    # 	 * Method to run the algorithm
    # 	 * @param input path to an input file
    # 	 * @param output  path for writing the output file
    # 	 * @param minUtility  the minimum utility threshold
    # TODO : IOException
    def runAlgorithm(self, inputFile, outputFile, minUtility):
        self.maxMemory = 0
        self.startTimestamp = time.time()
        print("startTimestamp : ", self.startTimestamp)

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
                        twu = transactionUtility if (twu is None) else twu + transactionUtility
                        # mapItemToTWU.update({item : twu})
                        mapItemToTWU[item] = twu
        except:
            traceback.print_exc()

        try:
            tree = UPTree()
            # print(tree.hasMoreThanOnePath)
            # print(tree.headerList)
            # print(tree.mapItemLastNode)
            # print(tree.mapItemNodes)
            # print(tree.root)
            # print(tree.root.childs)
            # print(tree.root.count)
            # print(tree.root.itemID)
            # print(tree.root.nodeLink)
            # print(tree.root.nodeUtility)
            # print(tree.root.parent)
            # print("==========")

            with open(inputFile, 'r') as input:
                for line in input:
                    split = line.rstrip().split(":")
                    items = split[0].split(" ")
                    utilityValues = split[2].split(" ")
                    remainingUtility = 0
                    revisedTransaction = []

                    for i in range(len(items)):
                        itm = int(items[i])
                        utility = int(utilityValues[i])
                        if mapItemToTWU[itm] >= minUtility:
                            element = Item(itm, utility)
                            revisedTransaction.append(element)
                            remainingUtility += utility
                            if itm in self.mapMinimumItemUtility:
                                minItemUtil = self.mapMinimumItemUtility[itm]
                            else:
                                minItemUtil = None

                            if minItemUtil is None or minItemUtil >= utility:
                                self.mapMinimumItemUtility[itm] = utility
                            element = None

                    # print("split : ", split)
                    # print("items : ", items)
                    # print("utilityValues : ", utilityValues)
                    # print("remainingUtility : ", remainingUtility)
                    # print(self.mapMinimumItemUtility)
                    
                    sortedTWU = sorted(mapItemToTWU.items(), key=operator.itemgetter(1), reverse=True)
                    sortedRevisedTransaction = []
                    for key, val in sortedTWU:
                        for x in revisedTransaction:
                            if key == x.name:
                                sortedRevisedTransaction.append(x)

                    # print(vars(sortedRevisedTransaction[0]))
                    tree.addTransaction(sortedRevisedTransaction, remainingUtility)

                # print("mapItemToTWU : ", mapItemToTWU)
                tree.createHeaderList(mapItemToTWU)
                # print("mapItemToTWU : ", mapItemToTWU)
                # print("==== tree ====")
                # print("hasMoreThanOnePath : ", tree.hasMoreThanOnePath)
                # print("headerList : ", tree.headerList)
                # strPrint = {}
                # for key, obj in tree.mapItemLastNode.items():
                #     strPrint[key] = "(i={} count={} nu={})".format(obj.itemID, obj.count, obj.nodeUtility)
                # print("mapItemLastNode : ", strPrint)



            # check the memory usage
                self.checkMemory()

                if self.DEBUG:
                    print("===== Global Tree =====")
                    print("mapITEM-TWU : {}".format(mapItemToTWU))
                    print("mapITEM-MINUTILTY : {}".format(self.mapMinimumItemUtility))
                    print(tree.toString())

                self.upgrowth(tree, minUtility, [])
                self.checkMemory()
        except:
            traceback.print_exc()

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



    def upgrowth(self, tree, minUtility, prefix):
        print("@@@ upgrowth @@@")
        for i in range(len(tree.headerList)-1, 0, -1):
            item = tree.headerList[i]
            print("item : ", item)

            localTree = self.createLocalTree(minUtility, tree, item)
            if self.DEBUG:
                ##################################
                # 오늘은 여기 까지 ~~~ 2018.01.31 #
                ##################################


                # print("LOCAL TREE for projection by:" + ("" if (prefix == None) else Arrays.toString(prefix) + ",") + item + "\n" + localTree.__str__())
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
            


    def createLocalTree(self, minUtility, tree, item):
        prefixPaths = []
        path = tree.mapItemNodes[item]
        # print("path : ", vars(path))
        # print("parent : ", vars(path.parent))

        itemPathUtility = {}

        while path is not None:
            # get the Node Utility of the item
            nodeutility = path.nodeUtility
            if path.parent.itemID is not -1:
                prefixPath = []
                prefixPath.append(path)

                parentnode = path.parent
                while parentnode.itemID is not -1:
                    prefixPath.append(parentnode)

                    if parentnode.itemID in itemPathUtility:
                        pu = itemPathUtility[parentnode.itemID]
                        pu = pu + nodeutility
                    else:
                        pu = nodeutility

                    itemPathUtility[parentnode.itemID] = pu
                    parentnode = parentnode.parent
                    # //end of while loop
                # add the path to the list of prefixpaths
                prefixPaths.append(prefixPath)
            # // end of if
            # we will look for the next prefixpath
            path = path.nodeLink
        # // end of while loop
        
        if self.DEBUG:
            print("===== PrefixPaths =====")
            for pfp in prefixPaths:
                for node in pfp:
                    print("   " + node.toString())
                print("   ----")

        # Calculate the utility of each item in the prefixpath
        localTree = UPTree()
        # for each prefixpath
        for prefixPath in prefixPaths:
            pathCount = prefixPath[0].count
            # print("pathCount : ", pathCount)
            pathUtility = prefixPath[0].nodeUtility
            # print("pathUtility : ", pathUtility)
            localPath = []
            
            for j in range(1, len(prefixPath)):
                itemValue = 0
                node = prefixPath[j]

                if itemPathUtility[node.itemID] >= minUtility:
                    localPath.append(node.itemID)
                else:
                    ######### mapMi~~ value 체크 필요함
                    minItemUtility = self.mapMinimumItemUtility[node.itemID]
                    itemValue = minItemUtility * pathCount
                    # //end of if-else
                pathUtility = pathUtility - itemValue
            # // end of for loop
            if self.DEBUG:
                print("   path utility after DGU,DGN,DLU: {}".format(pathUtility))

            sortedIPU = sorted(itemPathUtility.items(), key=operator.itemgetter(1), reverse=True)
            sortedLocalPath = []
            for key, val in sortedIPU:
                for x in localPath:
                    if key == x:
                        sortedLocalPath.append(x)

            localTree.addLocalTransaction(sortedLocalPath, pathUtility, self.mapMinimumItemUtility, pathCount)
        # //end of for loop

        localTree.createHeaderList(itemPathUtility)
        return localTree




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

    def checkMemory(self):
        currentMemory = psutil.virtual_memory().used / 1024 / 1024
        print("currentMemory : ", currentMemory)
        if currentMemory > self.maxMemory:
            self.maxMemory = currentMemory


    # def printStats(self):
    #     """ generated source for method printStats """
    #     print("=============  UP-GROWTH ALGORITHM - STATS =============")
    #     print(" PHUIs (candidates) count: " + self.phuisCount)
    #     print(" Total time ~ " + (self.endTimestamp - self.startTimestamp) + " ms")
    #     print(" Memory ~ " + self.maxMemory + " MB")
    #     print(" HUIs count : " + self.huiCount)
    #     print("===================================================")

