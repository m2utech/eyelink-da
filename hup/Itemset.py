class Itemset(object):
    """docstring for Itemset"""
    
    itemset = []
    utility = 0

    def __init__(self, itemset):
        self.itemset = itemset

    #    * Get the exact utility of this itemset
    #    * @return the exat utility
    def getExactUtility(self):
        return self.utility

    #    * Increase the utility of this itemset.
    #    * @param utility the amount of utility to be added (int).
    def increaseUtility(self, utility):
        self.utility += utility

    def get(self, pos):
        return self.itemset[pos]

    def size(self):
        return len(self.itemset)


if __name__ == '__main__':
    pass
    # Itemset([3,4,5])