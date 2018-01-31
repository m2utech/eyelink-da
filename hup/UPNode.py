class UPNode(object):
    def __init__(self):
        # String itemName;
        self.itemID = -1
        self.count = 1
        self.nodeUtility = 0
        self.parent = None
        # the child nodes of that node
        self.childs = []
        self.nodeLink = None


    def getChildWithID(self, name):
        for child in self.childs:
            if child.itemID == name:
                return child
        # print("return None")
        return None

    def toString(self):
        return "(i={} count={} nu={})".format(self.itemID, self.count, self.nodeUtility)

if __name__ == '__main__':
    test = UPNode()
    test.getChildWithID(1)
    # print(test.itemID)