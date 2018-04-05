from multipledispatch import dispatch

class Item(object):
    val = None

    @dispatch()
    def __init__(self):
        self.val = -1

    @dispatch(int)
    def __init__(self, value):
        self.val = value

    def clone(self):
        return Item(self.val)

    def __repr__(self):
        return str(self.val)

    def hashcode(self):
        return self.val.__hash__()

    def __hash__(self):
        return hash(self.val)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and self.val == other.val)