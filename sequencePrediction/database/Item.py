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

    def hashCode(self):
        print(self.val.__hash__())
        return self.val.__hash__()
        # h = 0
        # for c in self.val:
        #     h = (31 * h + ord(c)) & 0xFFFFFFFF
        # return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000

    def equals(self, b):
        return self.val.__eq__(b.val)

    def __eq__(self, other):
        return self.val.__eq__(other.val)