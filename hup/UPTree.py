from __future__ import print_function


class UPTree(object):
    #  List of items in the header table
    headerList = None

    #  flag that indicate if the tree has more than one path
    hasMoreThanOnePath = False

    #  List of pairs (item, Utility) of the header table
    mapItemNodes = HashMap()

    #  root of the tree
    root = UPNode()

    #  null node
    #  Map that indicates the last node for each item using the node links
    #  key: item value: an fp tree node (added by Philippe)
    mapItemLastNode = HashMap()

    def __init__(self):
        """ generated source for method __init__ """

    # 
    # 	 * Method for adding a transaction to the up-tree (for the initial
    # 	 * construction of the UP-Tree).
    # 	 * 
    # 	 * @param transaction    reorganised transaction
    # 	 * @param RTU   reorganised transaction utility
    # 	 
    def addTransaction(self, transaction, RTU):
        """ generated source for method addTransaction """
        currentNode = self.root
        i = 0
        RemainingUtility = 0
        size = len(transaction)
        #  For each item in the transaction
        while i < size:
            k = i + 1
            while k < len(transaction):
                #  remaining utility is calculated as sum of utilities of all
                #  itms behind currnt one
                RemainingUtility += transaction.get(k).getUtility()
                k += 1
            item = transaction.get(i).__name__
            #  int itm=Integer.parseInt(item);
            #  look if there is a node already in the FP-Tree
            child = currentNode.getChildWithID(item)
            if child == None:
                nodeUtility = (RTU - RemainingUtility)
                #  Nodeutility=  previous + (RTU - utility of
                #  descendent items)
                RemainingUtility = 0
                #  reset RemainingUtility for next item
                #  there is no node, we create a new one
                currentNode = insertNewNode(currentNode, item, nodeUtility)
            else:
                #  there is a node already, we update it
                currentNU = child.nodeUtility
                #  current node utility
                #  Nodeutility=  previous + (RTU - utility of
                #  descendent items)
                nodeUtility = currentNU + (RTU - RemainingUtility)
                RemainingUtility = 0
                #  reset RemainingUtility for next item
                child.count += 1
                child.nodeUtility = nodeUtility
                currentNode = child
            i += 1

    # 
    # 	 * Add a transaction to the UP-Tree (for a local UP-Tree)
    # 	 * @param localPath the path to be inserted
    # 	 * @param pathUtility the path utility
    # 	 * @param pathCount the path count
    # 	 * @param mapMinimumItemUtility the map storing minimum item utility
    # 	 
    def addLocalTransaction(self, localPath, pathUtility, mapMinimumItemUtility, pathCount):
        """ generated source for method addLocalTransaction """
        currentlocalNode = self.root
        i = 0
        RemainingUtility = 0
        size = len(localPath)
        #  For each item in the transaction
        while i < size:
            k = i + 1
            while k < len(localPath):
                search = localPath.get(k)
                #  remaining utility is calculated as sum of utilities of all
                #  items behind current one
                RemainingUtility += mapMinimumItemUtility.get(search) * pathCount
                k += 1
            item = localPath.get(i)
            #  look if there is a node already in the UP-Tree
            child = currentlocalNode.getChildWithID(item)
            if child == None:
                nodeUtility = (pathUtility - RemainingUtility)
                #  Nodeutility=  previous + (RTU - utility of
                #  descendent items)
                RemainingUtility = 0
                #  reset RU for next item
                #  there is no node, we create a new one
                currentlocalNode = insertNewNode(currentlocalNode, item, nodeUtility)
            else:
                #  there is a node already, we update it
                currentNU = child.nodeUtility
                #  current node utility
                #  Nodeutility=  previous + (RTU - utility of
                #  descendent items)
                nodeUtility = currentNU + (pathUtility - RemainingUtility)
                RemainingUtility = 0
                child.count += 1
                child.nodeUtility = nodeUtility
                currentlocalNode = child
            i += 1

    # 
    # 	 * Insert a new node in the UP-Tree as child of a parent node
    # 	 * @param currentlocalNode the parent node
    # 	 * @param item the item in the new node
    # 	 * @param nodeUtility the node utility of the new node
    # 	 * @return the new node
    # 	 
    def insertNewNode(self, currentlocalNode, item, nodeUtility):
        """ generated source for method insertNewNode """
        #  create the new node
        newNode = UPNode()
        newNode.itemID = item
        newNode.nodeUtility = nodeUtility
        newNode.count = 1
        newNode.parent = currentlocalNode
        #  we link the new node to its parrent
        currentlocalNode.childs.add(newNode)
        #  check if more than one path
        if not self.hasMoreThanOnePath and len(currentlocalNode.childs) > 1:
            self.hasMoreThanOnePath = True
        #  We update the header table.
        #  We check if there is already a node with this id in the
        #  header table
        localheadernode = self.mapItemNodes.get(item)
        if localheadernode == None:
            #  there is not
            self.mapItemNodes.put(item, newNode)
            self.mapItemLastNode.put(item, newNode)
        else:
            #  there is
            #  we find the last node with this id.
            #  get the latest node in the tree with this item
            lastNode = self.mapItemLastNode.get(item)
            #  we add the new node to the node link of the last node
            lastNode.nodeLink = newNode
            #  Finally, we set the new node as the last node
            self.mapItemLastNode.put(item, newNode)
        #  we return this node as the current node for the next loop
        #  iteration
        return newNode

    # 
    # 	 * Method for creating the list of items in the header table, in descending
    # 	 * order of TWU or path utility.
    # 	 * 
    # 	 * @param mapItemToEstimatedUtility
    # 	 *            the Utilities of each item (key: item value: TWU or path
    # 	 *            utility)
    # 	 
    def createHeaderList(self, mapItemToEstimatedUtility):
        """ generated source for method createHeaderList """
        #  create an array to store the header list with
        #  all the items stored in the map received as parameter
        self.headerList = ArrayList(self.mapItemNodes.keySet())
        #  sort the header table by decreasing order of utility
        Collections.sort(self.headerList, Comparator())

    @overloaded
    def __str__(self):
        """ generated source for method toString """
        output = ""
        output += "HEADER TABLE: " + self.mapItemNodes + " \n"
        output += "hasMoreThanOnePath: " + self.hasMoreThanOnePath + " \n"
        return output + self.toString("", self.root)

    @toString.register(object, str, UPNode)
    def __str___0(self, indent, node):
        """ generated source for method toString_0 """
        output = indent + node.__str__() + "\n"
        childsOutput = ""
        for child in node.childs:
            childsOutput += self.toString(indent + " ", child)
        return output + childsOutput

