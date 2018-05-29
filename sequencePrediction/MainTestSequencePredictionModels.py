import sys, os
sys.path.insert(0, os.path.abspath('../'))
# print(sys.path)
from sequencePrediction.predictor.Evaluator import Evaluator
from sequencePrediction.predictor.CPTplus.CPTPlusPredictor import CPTPlusPredictor

# class ModelsTest(object):
#     def __init__(self, samplingType, param):
#         self.samplingType = samplingType
#         self.param = param
#         self.showResults = True
#         self.showDatasetStats = True
#         self.showExecutionStats = True
#
#     def start(self, , dirPath, datasetName, maxCount):
#         self.evaluator = Evaluator(dirPath)
#         self.loadDataset(datasetName, maxCount)
#         self.setPredictor(predictor, opt)
#
#
#     def loadDataset(self, datasetName, maxCount):
#         for name in datasetName:
#             self.evaluator.addDataset(name, maxCount)
#
#     def setPredictor(self, predictor):
#         if predictor == "CPT+":
#             self.evaluator.addPredictor(CPTPlusPredictor(predictor, "CCF:true CBS:true"))


if __name__=='__main__':
    dirPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datasets")
    # ..\sequencePrediction\datasets
    datasetName = ['BMS', 'MSNBC', 'SIGN', 'FIFA', 'KOSARAK', 'BIBLE', 'LEVIATHAN']
    maxCount = 100

    # modelTest = ModelsTest(Evaluator.KFOLD, 10)
    # modelTest.start()

    evaluator = Evaluator(dirPath)

    evaluator.addDataset("BMS", 100)
    evaluator.addDataset("MSNBC", 100)
    evaluator.addDataset("SIGN", 100)
    evaluator.addDataset("FIFA", 100)
    evaluator.addDataset("KOSARAK", 100)
    evaluator.addDataset("LEVIATHAN", 100)
    # evaluator.addDataset("BIBLE", 100)

    evaluator.addPredictor(CPTPlusPredictor("CPT+", "CCF:false CBS:false"))
    # evaluator.addPredictor(CPTPlusPredictor("CPT+", "CCF:true CBS:false"))
    # evaluator.addPredictor(CPTPlusPredictor("CPT+", "CCF:false CBS:true"))
    # evaluator.addPredictor(CPTPlusPredictor("CPT+", "CCF:true CBS:true"))

    # evaluator.Start(Evaluator.HOLDOUT, 0.9, True, True, True)
    results = evaluator.Start(Evaluator.KFOLD, 10, True, True, True)
    # evaluator.Start(Evaluator.RANDOMSAMPLING, 0.9, True, True, True)
