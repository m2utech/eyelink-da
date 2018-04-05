from multipledispatch import dispatch
from database.Item import Item

class PredictionTree(object):
    # Item = None
    # Parent = None
    # Children = None

    @dispatch()
    def __init__(self):
        self.Item = Item()
        self.Children = []
        self.Parent = None

    @dispatch(object)
    def __init__(self, itemValue):
        self.Item = itemValue
        self.Children = []
        self.Parent = None

    def addChildItem(self, child):
        newChild = PredictionTree(child)
        newChild.Parent = self
        self.Children.append(newChild)

    def addChildLeaf(self, child):
        child.Parent = self
        self.Children.append(child)

    def removeChild(self, child):
        result = []
        for c in self.Children:
            if not c.Item == child:
               result.append(c)
        self.Children = result

    def hasChild(self, target):
        found = self.getChild(target)
        return False if (found == None) else True

    def getChild(self, target):
        for child in self.Children:
            if child.Item.val == target.val:
                return child
        return None

    def getChildren(self):
        return self.Children


# test
if __name__=="__main__":
    test1 = PredictionTree(3)
    test2 = PredictionTree(4)

    test2.addChildLeaf(test1)


