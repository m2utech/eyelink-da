'''
* UP-growth algorithm for High Utility Pattern mining
* Reference source code : SPMF
* Developer : Hyeongsoo Kim
'''
class UPNode(object):

    def __init__(self):
        # String itemName;
        self.itemID = -1
        self.count = 1
        self.nodeUtility = None
        self.parent = None
        # the child nodes of that node
        self.childs = []
        self.nodeLink = None


    def getChildWithID(self, name):
        for child in self.childs:
            if child.itemID == name:
                return child
        # not found, return None
        return None


    def toString(self):
        return "(i={} count={} nu={})".format(self.itemID, self.count, self.nodeUtility)

if __name__ == '__main__':
    test = UPNode()
    test.nodeUtility = 3
    test.getChildWithID(1)
    print(vars(test))