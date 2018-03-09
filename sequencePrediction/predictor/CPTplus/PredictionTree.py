from multipledispatch import dispatch
from database.Item import Item

class PredictionTree(object):
    Item = None
    Parent = None
    Children = None

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

    @dispatch(list) # 문제있음!!
    def addChild(self, child):
        newChild = PredictionTree(child)
        self.Children.append(newChild)

    @dispatch(object)
    def addChild(self, child):
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
        return False if found == None else True

    def getChild(self, target):
        for child in self.Children:
            if child.Item.val == target.val:
                return child
        return None

    def getChildren(self):
        return self.Children



