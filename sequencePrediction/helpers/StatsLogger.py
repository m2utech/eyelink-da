from sequencePrediction.helpers.Algo import Algo
from multipledispatch import dispatch

class StatsLogger(object):
    statsNames = None
    algorithms = None
    useSteps = None

    def __init__(self, statsNames, algoNames, useSteps):
        self.statsNames = statsNames
        self.algorithms = list()
        self.useSteps = useSteps
        for algoName in algoNames:
            self.algorithms.append(Algo(algoName, useSteps))

    def addStep(self):
        for algo in self.algorithms:
            algo.addStep()

    def set(self, stat, algoName, value):
        self.getAlgoByName(algoName).set(stat, value)

    def inc(self, stat, algoName):
        value = self.getAlgoByName(algoName).get(stat)
        value += 1
        self.getAlgoByName(algoName).set(stat, value)

    def divide(self, stat, algoName, divisor):
        value = self.getAlgoByName(algoName).get(stat)
        value = value / divisor
        self.getAlgoByName(algoName).set(stat, value)

    @dispatch(str, str)
    def get(self, stat, algoName):
        return self.getAlgoByName(algoName).get(stat)

    @dispatch(str, str, int)
    def get(self, stat, algoName, step):
        return self.getAlgoByName(algoName).get(step, stat)

    def getAlgoByName(self, algoName):
        for algo in self.algorithms:
            if algo.name ==algoName:  ######## compareTo convert!!!
                return algo
        return None


    # def __str__(self):
    #     output = ""
    #     if not self.useSteps:
    #         output += "\t\t"
    #         for algo in self.algorithms:
    #             output += "" + algo.name + "\t"
    #         output += "\n"
    #
    #         for stat in self.statsNames:
    #             empty = "          "
    #             output += (stat + empty[:len(stat)]) if len(stat) < 9 else stat[0:9]
    #             for algo in self.algorithms:
    #                 value = algo.get(stat) * 100
    #                 output += "\t" + "00.000" if value == 0.0 else '{:.3f}'.format(value)
    #             output += '\n'
    #     return output

    def __str__(self):
        output = []
        if not self.useSteps:
            output.append("\t\t\t")
            for algo in self.algorithms:
                output.append("{}\t".format(algo.name))
            output.append("\n")

            for stat in self.statsNames:
                empty = "            "
                # output.append((stat + empty[:len(stat)]) if len(stat) < 9 else stat[0:9])
                output.append(stat + empty[:(11%len(stat))])
                for algo in self.algorithms:
                    value = algo.get(stat) * 100.0
                    output.append("\t")
                    output.append("00.000" if value == 0.0 else '{:.3f}'.format(value))
                output.append('\n')
        return "".join(output)


    def toJsonString(self):
        output = ""
        if not self.useSteps:
            output += "\"algorithm\": ["
            for algo in self.algorithms:
                output += "\"" + algo.name + "\","
            output = output[0:(len(output)-1)]
            output += "], "

            output += "\"results\": ["
            for stat in self.statsNames:
                output += "{\"name\": \"" + stat + "\","
                output += "\"data\": ["
                for algo in self.algorithms:
                    value = algo.get(stat) * 100
                    output += "" + "00.000" if value == 0.0 else '{:.3f}'.format(value) + ","
                output = output[0:(len(output)-1)]
                output += "]},"
            output = output[0:(len(output)-1)]
            output += "]"
        return "{" + output + "}"