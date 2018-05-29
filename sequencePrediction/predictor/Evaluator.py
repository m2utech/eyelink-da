from multipledispatch import dispatch
import time
from queue import Queue
from sequencePrediction.common.LinkedList import LinkedList
from sequencePrediction.database.DatabaseHelper import DatabaseHelper
from sequencePrediction.database.Item import Item
from sequencePrediction.database.Sequence import Sequence
from sequencePrediction.database.SequenceStatsGenerator import SequenceStatsGenerator
from sequencePrediction.helpers.MemoryLogger import MemoryLogger
from sequencePrediction.helpers.StatsLogger import StatsLogger
from sequencePrediction.predictor.profile.Profile import Profile
from sequencePrediction.predictor.profile.ProfileManager import ProfileManager


class Evaluator(object):
    HOLDOUT = 0
    KFOLD = 1
    RANDOMSAMPLING = 2
    startTime = 0.0
    endTime = 0.0

    predictors = None
    stats = None
    experiments = None
    datasets = None
    datasetsMaxCount = None
    # memoryLogger = MemoryLogger()
    # parameters = {}


    def __init__(self, pathToDatasets):
        self.predictors = list()
        self.datasets = list()
        self.datasetMaxCount = list()
        self.database = DatabaseHelper(pathToDatasets)

    def addPredictor(self, predictor):
        self.predictors.append(predictor)

    def addDataset(self, datasetName, maxCount):
        self.datasets.append(datasetName)
        self.datasetMaxCount.append(maxCount)

    def Start(self, samplingType, param, showResults, showDatasetStats, showExecutionStats):
        try:
            statsColumns = list()
            statsColumns.append('Success')
            statsColumns.append('Failure')
            statsColumns.append('No Match')
            statsColumns.append('Too Small')
            statsColumns.append('Overall')
            statsColumns.append('Size (MB)')
            statsColumns.append('Train Time')
            statsColumns.append('Test Time')

            predictorNames = list()
            for predictor in self.predictors:
                predictorNames.append(predictor.getTAG())

            for i in range(len(self.datasets)):
                maxCount = self.datasetMaxCount.__getitem__(i)
                strFormat = self.datasets.__getitem__(i)

                self.database.Profile = ProfileManager().loagProfileByName(strFormat)
                self.database.loadDataset(strFormat, maxCount)

                if showDatasetStats:
                    print("")
                    SequenceStatsGenerator().prinStats(self.database.getDatabase(), strFormat)

                self.stats = StatsLogger(statsColumns, predictorNames, False)

                self.startTime = time.time() * 1000

                for id in range(len(self.predictors)):
                    if samplingType == self.HOLDOUT:
                        self.Holdout(param, id)
                    elif samplingType == self.KFOLD:
                        self.KFold(int(param), id)
                    elif samplingType == self.RANDOMSAMPLING:
                        self.RandomSubSampling(param, id)
                    else:
                        print("Unknown sampling type.")

                self.endTime = time.time() * 1000
                self.finalizeStats(showExecutionStats)

                if showResults == True:
                    print(self.stats.__str__())

            return self.stats

        except IOError as e:
            e.printStackTrace()


    def Holdout(self, ratio, classifierId):
        trainingSequences = self.getDatabaseCopy()
        testSequences = self.splitList(trainingSequences, ratio)

        ### DEBUG
        print("[DEBUG] Dataset size: {}".format(len(trainingSequences) + len(testSequences)))
        print("[DEBUG] Training: {0} and Test set: {1}".format(len(trainingSequences), len(testSequences)))

        self.PrepareClassifier(trainingSequences, classifierId)
        self.StartClassifier(testSequences, classifierId)


    def RandomSubSampling(self, ratio, classifierId):
        for i in range(10):
            self.Holdout(ratio, classifierId)
            MemoryLogger().addUpdate()
            # self.memoryLogger.addUpdate()

    def KFold(self, k, classifierId):
        if k < 2:
            raise RuntimeWarning("K needs to be 2 or more")
        dataSet = self.getDatabaseCopy()
        relativeRatio = 1 / float(k)
        absoluteRatio = int(len(dataSet) * relativeRatio)

        for i in range(k):
            posStart = i * absoluteRatio
            posEnd = posStart + absoluteRatio
            if i == (k-1):
                posEnd = len(dataSet)

            # trainingSequences = Queue()
            # testSequences = Queue()
            trainingSequences = []
            testSequences = []

            for j in range(len(dataSet)):
                toAdd = dataSet[j]

                if (j >= posStart) and (j < posEnd):
                    testSequences.append(toAdd)
                else:
                    trainingSequences.append(toAdd)

            self.PrepareClassifier(trainingSequences, classifierId)
            self.StartClassifier(testSequences, classifierId)
            MemoryLogger().addUpdate()
            # self.memoryLogger.addUpdate()


    def finalizeStats(self, showExecutionStats):
        for predictor in self.predictors:
            success = int(self.stats.get("Success", predictor.getTAG()))
            failure = int(self.stats.get("Failure", predictor.getTAG()))
            noMatch = int(self.stats.get("No Match", predictor.getTAG()))
            tooSmall = int(self.stats.get("Too Small", predictor.getTAG()))

            matchingSize = success + failure
            testingSize = matchingSize + noMatch + tooSmall

            self.stats.divide("Success", predictor.getTAG(), matchingSize)
            self.stats.divide("Failure", predictor.getTAG(), matchingSize)
            self.stats.divide("No Match", predictor.getTAG(), testingSize)
            self.stats.divide("Too Small", predictor.getTAG(), testingSize)

            self.stats.divide("Train Time", predictor.getTAG(), 100)
            self.stats.divide("Test Time", predictor.getTAG(), 100)

            # Adding overall success
            self.stats.set("Overall", predictor.getTAG(), success)
            self.stats.divide("Overall", predictor.getTAG(), testingSize)

            # Size of the predictor
            self.stats.set("Size (MB)", predictor.getTAG(), predictor.memoryUsage())
            self.stats.divide("Size (MB)", predictor.getTAG(), (100 * 1000 * 1000))

        if showExecutionStats:
            MemoryLogger().addUpdate()
            MemoryLogger().displayUsage()
            # self.memoryLogger.addUpdate()
            # self.memoryLogger.displayUsage()

            print("Execution time: {:.3f} seconds".format((self.endTime - self.startTime)/1000))

    def isGoodPrediction(self, consequent, predicted):
        hasError = False
        for it in predicted.getItems():
            isFound = False
            for re in consequent.getItems():
                if re.val.__eq__(it.val):
                    isFound = True
            if isFound == False:
                hasError = True

        return (hasError == False)

    def PrepareClassifier(self, trainingSequences, classifierId):
        start = time.time() * 1000
        self.predictors[classifierId].parameters.Profile = self.database.Profile    # adding profile info
        self.predictors[classifierId].Train(trainingSequences)  #actual training
        end = time.time() * 1000
        duration = float(end - start) / 1000
        self.stats.set("Train Time", self.predictors[classifierId].getTAG(), duration)

    def StartClassifier(self, testSequences, classifierId):
        start = time.time() * 1000
        for target in testSequences:
            if target.size() > self.database.Profile.paramInt("consequentSize"):
                consequent = target.getLastItems(self.database.Profile.paramInt("consequentSize"), 0)
                finalTarget = target.getLastItems(self.database.Profile.paramInt("windowSize"), self.database.Profile.paramInt("consequentSize"))

                predicted = self.predictors[classifierId].Predict(finalTarget)

                if predicted.size() == 0:
                    self.stats.inc("No Match", self.predictors[classifierId].getTAG())
                elif self.isGoodPrediction(consequent, predicted):
                    self.stats.inc("Success", self.predictors[classifierId].getTAG())
                else:
                    self.stats.inc("Failure", self.predictors[classifierId].getTAG())

            else:
                self.stats.inc("Too Small", self.predictors[classifierId].getTAG())

        end = time.time() * 1000
        duration = float(end - start) / 1000
        self.stats.set("Test Time", self.predictors[classifierId].getTAG(), duration)


    def splitList(self, toSplit, absoluteRatio):
        relativeRatio = int(len(toSplit) * absoluteRatio)
        sub = toSplit[relativeRatio:(len(toSplit))]
        two = list(sub)
        sub.clear()
        return two


    def getDatabaseCopy(self):
        return list(self.database.getDatabase().getSequences()[0:(self.database.getDatabase().size())])