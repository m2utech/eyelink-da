from __future__ import print_function
from upNode import UPNode
from item import Item
import operator
import collections

class UPTree(object):
    def __init__(self):
        #  List of items in the header table
        self.headerList = None
        #  flag that indicate if the tree has more than one path
        self.hasMoreThanOnePath = False
        #  List of pairs (item, Utility) of the header table
        #  {integer, UPNode}
        self.mapItemNodes = {}
        # self.mapItemNodes = collections.OrderedDict()
        #  root of the tree
        self.root = UPNode()
        #  Map that indicates the last node for each item using the node links
        #  key: item value: an fp tree node (added by Philippe)
        self.mapItemLastNode = {}
        # self.mapItemLastNode = collections.OrderedDict()

    # Method for adding a transaction to the up-tree
    # (for the initial construction of the UP-Tree).
    # @param transaction    reorganised transaction
    # @param RTU   reorganised transaction utility
    def addTransaction(self, transaction, RTU):
        # print("@@@ UPTree - addTransaction")
        currentNode = self.root
        # print("currentNode : ", vars(currentNode))
        i = 0
        RemainingUtility = 0
        size = len(transaction)
        
        for i in range(size):
            for k in range(i+1, size):
                RemainingUtility += transaction[k].getUtility()
            # print("=============")
            # print(vars(self))
            # print("RemainingUtility : ", RemainingUtility)
            item = transaction[i].getName()
            # print("item : ", item)
            child = currentNode.getChildWithID(item)
            # print("child : ", child)

            if child is None:
                nodeUtility = (RTU - RemainingUtility)
                RemainingUtility = 0

                currentNode = self.insertNewNode(currentNode, item, nodeUtility)
                # print("currentNode : ", vars(currentNode))
            else:
                currentNU = child.nodeUtility
                nodeUtility = currentNU + (RTU - RemainingUtility)
                RemainingUtility = 0
                child.count = child.count + 1
                child.nodeUtility = nodeUtility
                currentNode = child
            # print("nodeUtility : ", nodeUtility)


    # # 	 * Add a transaction to the UP-Tree (for a local UP-Tree)
    # # 	 * @param localPath the path to be inserted
    # # 	 * @param pathUtility the path utility
    # # 	 * @param pathCount the path count
    # # 	 * @param mapMinimumItemUtility the map storing minimum item utility
    def addLocalTransaction(self, localPath, pathUtility, mapMinimumItemUtility, pathCount):
        currentlocalNode = self.root
        i = 0
        RemainingUtility = 0
        size = len(localPath)
        # print("size : ", size)
        #  For each item in the transaction
        for i in range(len(localPath)):
            for k in range(i+1, len(localPath)):
                search = localPath[k]
                #  remaining utility is calculated as sum of utilities of all
                #  items behind current one
                RemainingUtility += mapMinimumItemUtility[search] * pathCount
                # //end of for loop
            item = localPath[i]
            
            #  look if there is a node already in the UP-Tree
            child = currentlocalNode.getChildWithID(item)

            if child is None:
                nodeUtility = (pathUtility - RemainingUtility)
                RemainingUtility = 0    #  reset RU for next item

                #  there is no node, we create a new one
                currentlocalNode = self.insertNewNode(currentlocalNode, item, nodeUtility)
            else:
                #  there is a node already, we update it
                currentNU = child.nodeUtility   # current node utility
                nodeUtility = currentNU + (pathUtility - RemainingUtility)
                RemainingUtility = 0
                child.count += 1
                child.nodeUtility = nodeUtility
                currentlocalNode = child
            # // end of if-else
        # // end of for loop

    # # 
    # # 	 * Insert a new node in the UP-Tree as child of a parent node
    # # 	 * @param currentlocalNode the parent node
    # # 	 * @param item the item in the new node
    # # 	 * @param nodeUtility the node utility of the new node
    # # 	 * @return the new node
    # # 	 
    def insertNewNode(self, currentlocalNode, item, nodeUtility):
        # print("@@ UPTree - insertNewNode @@")
        newNode = UPNode()
        newNode.itemID = item
        newNode.nodeUtility = nodeUtility
        newNode.count = 1
        newNode.parent = currentlocalNode

        # print("newNode : ", vars(newNode))
        #  we link the new node to its parrent
        currentlocalNode.childs.append(newNode)

        if not self.hasMoreThanOnePath and len(currentlocalNode.childs) > 1:
            self.hasMoreThanOnePath = True
        ##########
        if item in self.mapItemNodes:
            localheadernode = self.mapItemNodes[item]
            lastNode = self.mapItemLastNode[item]
            lastNode.nodeLink = newNode
            self.mapItemLastNode[item] = newNode
        else:
            self.mapItemNodes[item] = newNode
            self.mapItemLastNode[item] = newNode

        return newNode


    # Method for creating the list of items in the header table, in descending
    # order of TWU or path utility.
    # @param mapItemToEstimatedUtility
    #  the Utilities of each item (key: item value: TWU or path utility)
    def createHeaderList(self, mapItemToEstimatedUtility):
        #  create an array to store the header list with
        #  all the items stored in the map received as parameter
        self.headerList = list(self.mapItemNodes.keys())
        sortedHeaderList = []
        sortedUtility = sorted(mapItemToEstimatedUtility.items(), key=operator.itemgetter(1), reverse=True)
        for key, val in sortedUtility:
            for x in self.headerList:
                if x is key:
                    sortedHeaderList.append(x)
        self.headerList = sortedHeaderList
        # print("headerList : ", self.headerList)


    #     self.headerList = ArrayList(self.mapItemNodes.keySet())
    #     #  sort the header table by decreasing order of utility
    #     Collections.sort(self.headerList, Comparator())

    def toString(self):
        temp = {}
        for key, obj in self.mapItemNodes.items():
            temp[key] = "(i={} count={} nu={})".format(obj.itemID, obj.count, obj.nodeUtility)
        output = "HEADER TABLE : {} \n".format(temp)
        output += "hasMoreThanOnePath : {} \n".format(self.hasMoreThanOnePath)
        return output + self.treeToString("", self.root)

    def treeToString(self, indent, node):
        output = "{}{}\n".format(indent, node.toString())
        childsOutput = ""
        for child in node.childs:
            childsOutput += self.treeToString(indent + "  ", child)
        return output + childsOutput
