
class Profile(object):
    def __init__(self):
        self.parameters = {}

    def paramDouble(self, name):
        value = self.parameters.get(name)
        return None if value == None else float(self.parameters.get(name))

    def paramInt(self, name):
        value = self.parameters.get(name)
        return None if value == None else int(self.parameters.get(name))

    def paramFloat(self, name):
        value = self.parameters.get(name)
        return None if value == None else float(self.parameters.get(name))

    def paramBool(self, name):
        value = self.parameters.get(name)
        boolean = True if (self.parameters.get(name)).lower() in "true" else False
        return None if value == None else boolean

    def Apply(self):
        self.parameters["sequenceMinSize"] = "6"
        self.parameters["sequenceMaxSize"] = "999"
        self.parameters["removeDuplicatesMethod"] = "1"
        self.parameters["consequentSize"] = "1"
        self.parameters["windowSize"] = "5"

        # //CPT parameters Training
        self.parameters["splitMethod"] = "0" # 0 for no split", "1 for basicSplit", "2 for complexSplit
        self.parameters["splitLength"] = "999" # max tree height

        # //Prediction
        self.parameters["recursiveDividerMin"] = "4" # should be >= 0 and < recursiveDividerMax
        self.parameters["recursiveDividerMax"] = "99" # should be > recusiveDividerMax and < windowSize
        self.parameters["minPredictionRatio"] = "2.0f" # should be over 0
        self.parameters["noiseRatio"] = "1.0f" # should be in the range ]0,1]

        # //best prediction from the count table
        self.parameters["firstVote"] = "1" # 1 for confidence", "2 for lift
        self.parameters["secondVote"] = "2" # 0 for none", "1 for support", "2 for lift
        self.parameters["voteTreshold"] = "0.0" # confidence threshold to validate firstVote", "else it uses the secondVote

        # //Countable weight system
        self.parameters["countTableWeightMultiplier"] = "2" # 0 for no weight (1)", "1 for 1/targetSize", "2 for level/targetSize
        self.parameters["countTableWeightDivided"] = "1" # 0 for no divider", "1 for x/(#ofBranches for this sequence)

        # //Others
        self.parameters["useHashSidVisited"] = "true"
        self.parameters["branchTraversalTopToBottom"] = "true" # used for branches with duplicates", "set to true to allow with duplicates
        self.parameters["removeUnknownItemsForPrediction"] = "true" # remove items that were never seen before from the Target sequence before LLCT try to make a prediction

    def tostring(self):
        output = "\n--- Global Parameters---\n"
        for paramKey, paramVal in self.parameters.items():
            output += "{} \t {} \n".format(paramKey, paramVal)
        return output