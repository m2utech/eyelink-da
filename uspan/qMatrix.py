import numpy as np


class QMatrix(object):
    """docstring for QMatrix"""
    def __init__(self, nbItem, nbItemset, itemNames, swu):
        self.matrixItemUtility = np.zeros(shape=(nbItem, nbItemset), dtype=int)
        self.matrixItemRemainingUtility = np.zeros(shape=(nbItem, nbItemset), dtype=int)
        self.swu = swu
        self.itemNames = itemNames

    def registerItem(self, itemPos, itemset, utility, remainingUtility):
        self.matrixItemUtility[itemPos][itemset] = utility
        self.matrixItemRemainingUtility[itemPos][itemset] = remainingUtility

    def toString(self):
        output = " MATRIX \n"
        for i in range(len(self.itemNames)):
            output += "\n  item: {}".format(self.itemNames[i])
            for j in range(len(self.matrixItemUtility[i])):
                output += "\t{}[{}]".format(self.matrixItemUtility[i][j],
                                            self.matrixItemRemainingUtility[i][j])
        output += "   swu: {}\n".format(self.swu)
        return output
