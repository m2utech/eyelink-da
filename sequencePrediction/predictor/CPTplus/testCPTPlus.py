from __future__ import print_function
import sys

from database.SequenceDatabase import SequenceDatabase
from database.SequenceStatsGenerator import SequenceStatsGenerator
from predictor.CPTplus.CPTPlusPredictor import CPTPlusPredictor
from database.Sequence import Sequence
from database.Item import Item

#### Logging ####
from common.logger import getStreamLogger
logger = getStreamLogger()
#################

# from algoCPTplus import AlgoCPTplus
# from sequencePrediction.database.Item import Item

# from sequencePrediction.database.SequenceDatabase import SequenceDatabase


def main(dirPath):
        #  the input database
        inputPath = fileToPath(dirPath, "contextCPT.txt")
        trainingSet = SequenceDatabase()
        trainingSet.loadFileSPMFFormat(inputPath, sys.maxsize, 0, sys.maxsize)

        print("--- Training sequences ---")
        for sequence in trainingSet.getSequences():
            print(str(sequence))
        print("")

        SequenceStatsGenerator().prinStats(trainingSet, "training sequences ")
        #  Here is a brief description of the parameter used in the above line:
        optionalParameters = "CCF:true CBS:true CCFmin:1 CCFmax:6 CCFsup:2 splitMethod:0 splitLength:4 minPredictionRatio:1.0 noiseRatio:1.0"
        # optionalParameters = {
        #     "CCF": True,        #  CCF:true  --> activate the CCF strategy
        #     "CBS": True,        #  CBS:true -->  activate the CBS strategy
        #     "CCFmin": 1,        #  CCFmin:1 --> indicate that the CCF strategy will not use pattern having less than 1 items
        #     "CCFmax": 6,        #  CCFmax:6 --> indicate that the CCF strategy will not use pattern having more than 6 items
        #     "CCFsup": 2,        #  CCFsup:2 --> indicate that a pattern is frequent for the CCF strategy if it appears in at least 2 sequences
        #     "splitMethod": 0,   #  splitMethod:0 --> 0 : indicate to not split the training sequences    1: indicate to split the sequences
        #     "splitLength": 4,   #  splitLength:4  --> indicate to split sequence to keep only 4 items, if splitting is activated
        #     "minPredictionRatio": 1.0,  #  minPredictionRatio:1.0  -->  the amount of sequences or part of sequences that should match to make a prediction, expressed as a ratio
        #     "noiseRatio": 1.0   #  noiseRatio:1.0  -->   ratio of items to remove in a sequence per level (see paper).
        # }

        ### Train the prediction model
        predictionModel = CPTPlusPredictor("CPT+", optionalParameters)
        predictionModel.Train(trainingSet.getSequences())


        """ Now we will make a prediction We want to predict what would occur after
        the sequence <1, 2> We first create the sequence """
        sequence = Sequence(0)
        sequence.addItem(Item(11))
        sequence.addItem(Item(17))
        sequence.addItem(Item(8))
        sequence.addItem(Item(5))
        sequence.addItem(Item(10))

        logger.debug(sequence)


        """ Then we perform the prediction """
        thePrediction = predictionModel.Predict(sequence)
        print("For the sequence <(1), (2)>, the prediction for the next symbol is: +{}".format(thePrediction))

        """ If we want to see why that prediction was made, we can also ask to see the count table of 
        the prediction algorithm. The count table is a structure that stores the score for each symbols
        for the last prediction that was made. The symbol with the highest score was the prediction."""
        print("To make the prediction, the scores were calculated as follows:")
        counTable = predictionModel.getCountTable()
        for key, value in counTable.items():
            print("symbol {0} \t score: {1}".format(key, value))


def fileToPath(dirPath, filename):
    url = os.path.join(dirPath, filename)
    print(url)
    return url


if __name__ == '__main__':
    import os
    dirPath = os.path.dirname(os.path.abspath(__file__))
    main(dirPath)
