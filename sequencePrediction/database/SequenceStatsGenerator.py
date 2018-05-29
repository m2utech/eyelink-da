class SequenceStatsGenerator(object):
    def __init__(self):
        pass

    def prinStats(self, database, name):
        print("---{}---".format(name))
        print("Number of sequences : \t{}".format(database.size()))

        maxItem = 0
        items = set()
        sizes = []
        differentitems = []
        appearXtimesbySequence = []

        for sequence in database.getSequences():
            sizes.append(sequence.size())
            mapIntegers = {}

            for item in sequence.getItems():
                count = mapIntegers.get(item.val)
                if count == None:
                    count = 0

                count = count + 1
                mapIntegers[item.val] = count
                items.add(item.val)

                if item.val > maxItem:
                    maxItem = item.val

            differentitems.append(len(mapIntegers.items()))

            for key, val in mapIntegers.items():
                appearXtimesbySequence.append(val)

        print("Number of distinct items: \t{}".format(len(items)))
        print("Largest item id: \t{}".format(maxItem))
        print("Itemsets per sequence: \t{}".format(self.calculateMean(sizes)))
        print("Distinct item per sequence: \t{}".format(self.calculateMean(differentitems)))
        print("Occurences for each item: \t{}".format(self.calculateMean(appearXtimesbySequence)))
        # datasetSize = ((database.size() * 4) + (database.size() * self.calculateMean(sizes) * 4) / (1000 * 1000))
        datasetSize = ((database.size()) + (database.size() * self.calculateMean(sizes)) / (1000 * 1000))
        print("Size of the dataset in MB: \t{}".format(datasetSize))



    def calculateMean(self, list):
        sum = 0
        for val in list:
            sum += val
        return sum / len(list)