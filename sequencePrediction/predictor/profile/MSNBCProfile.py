from sequencePrediction.predictor.profile.Profile import Profile

class MSNBCProfile(Profile):

    def Apply(self):
        self.parameters["sequenceMinSize"] = "8"
        self.parameters["sequenceMaxSize"] = "999"
        self.parameters["removeDuplicatesMethod"] = "1"
        self.parameters["consequentSize"] = "2"
        self.parameters["windowSize"] = "5"

        # /////////////
        # CPT parameters
        # Training
        self.parameters["splitMethod"] = "1"  # 0 for no split", "1 for basicSplit", "2 for complexSplit
        self.parameters["splitLength"] = "6"  # max tree height
        self.parameters["minSup"] = "0.05"  # SEI compression, minSup to remove low supporting items
        # CCF compression
        self.parameters["CCFmin"] = "2"
        self.parameters["CCFmax"] = "4"
        self.parameters["CCFsup"] = "16"
        # Prediction
        self.parameters["recursiveDividerMin"] = "1"  # should be >= 0 and < recursiveDividerMax
        self.parameters["recursiveDividerMax"] = "5"  # should be > recusiveDividerMax and < windowSize
        self.parameters["minPredictionRatio"] = "0.0"  # should be over 0
        self.parameters["noiseRatio"] = "0.0"  # should be in the range ]0,1]

## Local test ##
if __name__=='__main__':
    MSNBCProfile().Apply()