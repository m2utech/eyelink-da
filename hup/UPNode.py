class UPNode(object):
    def __init__(self):
        # String itemName;
        self.itemID = -1
        self.count = 1
        self.parent = None
        # the child nodes of that node
        self.childs = [UPNode]
        self.nodeLink = None

    def getChildWithID(self, name):
        for child in self.childs:
            print(child)

if __name__ == '__main__':
    test = UPNode()
    test.getChildWithID(1)
    # print(test.itemID)