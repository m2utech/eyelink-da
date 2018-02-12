#!/usr/bin/env python
from __future__ import print_function
from algoUPGrowth import AlgoUPGrowth


def main(dirPath):
    """ generated source for method main """
    inputFile = fileToPath(dirPath, "BMS_Utility.txt")
    outputFile = "./output.txt"
    min_utility = 1000

    algo = AlgoUPGrowth()
    algo.runAlgorithm(inputFile, outputFile, min_utility)
    algo.printStats()

def fileToPath(dirPath, filename):
    """ generated source for method fileToPath """
    url = os.path.join(dirPath, filename)
    print(url)
    return url
    # return java.net.URLDecoder.decode(url.getPath(), "UTF-8")


if __name__ == '__main__':
    import os
    dirPath = os.path.dirname(os.path.abspath(__file__))
    main(dirPath)