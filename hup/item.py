'''
* UP-growth algorithm for High Utility Pattern mining
* Reference source code : SPMF
* Developer : Hyeongsoo Kim
'''
class Item(object):
    name = 0        # item
    utility = 0     # utility of item

    # constructor that takes item name
    def __init__(self, name, utility=None):
        self.name = name
        if utility is None:
            pass
        else:
            self.utility = utility

    # ## method to get node utility
    def getUtility(self):
        return self.utility

    # ## method to set node utility
    def setUtility(self, utility):
        self.utility = utility

    def getName(self):
        return self.name

if __name__ == '__main__':
    # for test
    item = Item(1, 30)
    print(vars(item))