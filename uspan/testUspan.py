from __future__ import print_function
from algoUSpan import AlgoUSpan


def main(dirPath):
        #  the input database
        input = fileToPath(dirPath, "DataBase_HUSRM.txt")
        #  the path for saving the patterns found
        output = "./output.txt"
        #  the minimum utility threshold
        minutil = 35

        algo = AlgoUSpan()
        #  set the maximum pattern length (optional)
        algo.setMaxPatternLength(4)
        #  run the algorithm
        algo.runAlgorithm(input, output, minutil)
        #  print statistics
        # algo.printStatistics()


def fileToPath(dirPath, filename):
    url = os.path.join(dirPath, filename)
    print(url)
    return url


if __name__ == '__main__':
    import os
    dirPath = os.path.dirname(os.path.abspath(__file__))
    main(dirPath)

