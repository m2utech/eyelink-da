from __future__ import print_function
import time
import traceback
import operator
import psutil
from upTree import UPTree
from item import Item
from itemset import Itemset

class AlgoUPGrowth(object):
    def __init__(self):
        #  variable for statistics
        self.maxMemory = 0       # the maximum memory usage
        self.startTimestamp = 0  # the time the algorithm started
        self.endTimestamp = 0    # the time the algorithm terminated
        self.huiCount = 0        # the number of HUIs generated
        self.phuisCount = int()  # the number of PHUIs generated
        #  map for minimum node utility during DLU(Decreasing Local Unpromizing items) strategy
        self.mapMinimumItemUtility = None
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
    def runAlgorithm(self, inputFile, outputFile, minUtility):
        self.maxMemory = 0
        self.startTimestamp = time.time()*1000
        print("startTimestamp : ", self.startTimestamp)

        mapItemToTWU = {}
        try:
            print("@@@InputFile open")
            with open(inputFile, 'r') as input:
                for line in input.readlines():
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

        #  map for minimum node utility during DLU(Decreasing Local Unpromizing items) strategy
        self.mapMinimumItemUtility = {}
        
        try:
            print("@@@ Create Tree")
            tree = UPTree()
            with open(inputFile, 'r') as input:
                for line in input.readlines():
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

                    sortedTWU = sorted(mapItemToTWU.items(), key=operator.itemgetter(1), reverse=True)
                    sortedRevisedTransaction = []
                    for key, val in sortedTWU:
                        for x in revisedTransaction:
                            if key == x.name:
                                sortedRevisedTransaction.append(x)

                    print("### add transaction")
                    tree.addTransaction(sortedRevisedTransaction, remainingUtility)

                print("### create header list")
                tree.createHeaderList( mapItemToTWU)

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

        #########################
        ## Tree 생성 문제 없음 ##

        self.phuisCount = len(self.phuis)

        # ##### TODO: 정렬 데이터 확인 필요 #######
        # for x in self.phuis:
        #     print(x.itemset, len(x.itemset))
        self.phuis.sort(key=lambda s: len(s.itemset))
        # for x in self.phuis:
        #     print(x.itemset, len(x.itemset))

        try:
            with open(inputFile, 'r') as input:
                for line in input.readlines():
                    split = line.rstrip().split(":")
                    items = split[0].split(" ")
                    utilityValues = split[2].split(" ")
                    revisedTransaction = []

                    for i in range(len(items)):
                        item = int(items[i])
                        utility = int(utilityValues[i])
                        element = Item(item, utility)
                        if mapItemToTWU[itm] >= minUtility:
                            revisedTransaction.append(element)

                    revisedTransaction.sort(key=lambda s: s.name)

                    ##########################################
                    # TODO : 잘 처리해야함@@@@@
                    for itemset in self.phuis:
                        if itemset.size() > len(revisedTransaction):
                            break
                        self.updateExactUtility(revisedTransaction, itemset)

        except:
            traceback.print_exc()

        try:
            with open(outputFile, 'w') as output:
                for itemset in self.phuis:
                    if itemset.getExactUtility() >= minUtility:
                        str_output = self.writeOut(itemset)
                        # output.write(str_output)
                        print(str_output)
                        output.writelines(str_output + '\n')
        except:
            traceback.print_exc()



        self.checkMemory()

        self.endTimestamp = time.time()*1000
        print("endTimestamp : ", self.startTimestamp)

        self.phuis.clear()
        self.mapMinimumItemUtility = None


    def upgrowth(self, tree, minUtility, prefix):
        # print("@@@ upgrowth @@@")
        for i in range(len(tree.headerList)-1, -1, -1):
            item = tree.headerList[i]
            # print("item : ", item)

            localTree = self.createLocalTree(minUtility, tree, item)

            if self.DEBUG:
                print("LOCAL TREE for projection by: {}{}".format("" if prefix is None else str(prefix)+", ", item))
                print(localTree.toString())

            # ===== CALCULATE SUM OF ITEM NODE UTILITY =====
            # take node from bottom of header table
            pathCPB = tree.mapItemNodes[item]
            pathCPBUtility = 0
            while pathCPB is not None:
                pathCPBUtility += pathCPB.nodeUtility
                pathCPB = pathCPB.nodeLink

            # if path utility of 'item' in header table is greater than minUtility
            # then 'item' is a PHUI (Potential high utility itemset)
            if pathCPBUtility >= minUtility:
                length = len(prefix)
                newPrefix = [None] * (length+1)
                # print(newPrefix)
                # newPrefix = []
                newPrefix[0:length] = prefix[0:]
                # print(newPrefix)
                newPrefix[length] = item
                # print(newPrefix)

                self.savePHUI(newPrefix)

                # // Make a recursive call to the UPGrowth procedure to explore
                # // other itemsets that are extensions of the current PHUI
                if len(localTree.headerList) > 0:
                    self.upgrowth(localTree, minUtility, newPrefix)



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
            print("\n\n===== PrefixPaths =====")
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


    def savePHUI(self, itemset):
        """ generated source for method savePHUI """
        itemsetObj = Itemset(itemset)
        # print(itemset)
        itemset.sort()
        self.phuis.append(itemsetObj)


    def updateExactUtility(self, transaction, itemset):
        utility = 0
        # print(vars(itemset))
        for i in range(itemset.size()):
            itemI = itemset.get(i)
            # print("itemI: ", itemI)
            for j in range(len(transaction)):
                itemJ = transaction[j]
                # print(itemJ.name, itemI)
                if itemJ.name == itemI:
                    # print("Equal!!!")
                    utility += itemJ.utility
                    # print(utility)
                    break
                elif itemJ.name > itemI:
                    # print('greater then')
                    return
        itemset.increaseUtility(utility)

    """
    # Write a HUI to the output file
    # @param HUI
    # @param utility
    """
    def writeOut(self, HUI):
        self.huiCount += 1

        str_list = []
        for i in range(HUI.size()):
            str_list.append(HUI.get(i))
            str_list.append(' ')
        str_list.append("#UTIL: ")
        str_list.append(HUI.getExactUtility())
        return ''.join(map(str, str_list))



    def checkMemory(self):
        # unit : MB
        currentMemory = psutil.virtual_memory().used / 1024 / 1024 / 1024
        print("currentMemory : ", currentMemory)
        if currentMemory > self.maxMemory:
            self.maxMemory = currentMemory


    def printStats(self):
        """ generated source for method printStats """
        print("=============  UP-GROWTH ALGORITHM - STATS =============")
        print(" PHUIs (candidates) count: {}".format(self.phuisCount))
        print(" Total time ~ {} ms".format(int(round(self.endTimestamp - self.startTimestamp))))
        print(" Memory ~ {} MB".format(self.maxMemory))
        print(" HUIs count : {}".format(self.huiCount))
        print("===================================================")

