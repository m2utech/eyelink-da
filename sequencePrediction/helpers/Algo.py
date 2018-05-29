from multipledispatch import dispatch
from sequencePrediction.helpers.Result import Result

class Algo:
    name = None
    useStep = None
    steps = None
    currentStep = None
    result = None

    def __init__(self, name, useStep):
        self.useStep = useStep
        self.name = name
        if useStep:
            self.steps = list()
            self.currentStep = -1
        else:
            self.result = Result()

    def useSteps(self):
        return self.useStep

    def addStep(self):
        if self.useSteps():
            self.currentStep += 1
            if (len(self.steps) -1) < self.currentStep:
                self.steps.append(Result())

    def set(self, stat, value):
        if self.useSteps():
            self.steps.__getitem__(self.currentStep).set(stat, value)
        else:
            self.result.set(stat, value)

    @dispatch(str)
    def get(self, stat):
        if self.useSteps():
            return self.steps.__getitem__(self.currentStep).get(stat)
        else:
            return self.result.get(stat)

    @dispatch(int, str)
    def get(self, step, stat):
        if self.useSteps():
            return self.steps.__getitem__(step).get(stat)
        else:
            return self.result.get(stat)