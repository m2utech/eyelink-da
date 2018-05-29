
class Result:
    data = None

    def __init__(self):
        self.data = dict()

    def get(self, stat):
        if self.data.get(stat) == None:
            self.data[stat] = 0.0
        return self.data.get(stat)

    def set(self, stat, value):
        self.data[stat] = value