from multipledispatch import dispatch
from database.Item import Item

class Sequence(object):
    items = None
    id = int()

    @dispatch(int)
    def __init__(self, id):
        self.id = id
        self.items = []

    @dispatch(object)
    def __init__(self, aSequence):
        self.id = aSequence.id
        self.items = []
        for item in aSequence.getItems():
            self.items.append(Item(item.val))

    @dispatch(int, list)
    def __init__(self, id, items):
        self.id = id
        self.items = items if items != None else []

    def getId(self):
        return self.id

    def getItems(self):
        return self.items

    def setItems(self, newItems):
        self.items = newItems

    def get(self, index):
        return self.items[index]

    def size(self):
        return len(self.items)

    def addItem(self, item):
        self.items.append(item)


    def getLastItems(self, length, offset):
        truncatedSequence = Sequence(0)
        size = self.size() - offset
        if not self.items:
            return None
        elif length > size:
            truncatedList = self.items[0:size]
            truncatedSequence.setItems(truncatedList)
        else:
            truncatedList = self.items[(size - length):size]
            truncatedSequence.setItems(truncatedList)
        return truncatedSequence

    ## TODO: print, toString function
    def print(self):
        print(self.__str__())

    # override
    def __str__(self):
        r = []
        for it in self.items:
            r.append("(")
            if type(it) == int:
                r.append(it)
            else:
                r.append(it.val)
            r.append(") ")
        return "".join(map(str, r))


    def setID(self, newid):
        self.id = newid

    def clone(self):
        copy = Sequence(self.id)
        for item in self.items:
            copy.items.append(item.clone())
        return copy

    def __eq__(self, obj):
        if obj == None:
            return None
        else:
            other = obj
            return self.equals(other)

    def equals(self, other):
        if (self.id != other.id) or (len(self.items) != len(other.items)):
            return False
        for i in range(len(self.items)):
            if (self.items[i].__eq__(other.items[i])) == False:
                return False
        return True


    def __hash__(self):
        prime = 31
        result = 1
        result = prime * result + self.id
        result = prime * result + self.hashCode(self.items)
        return result

    def hashCode(self, items):
        h = 0
        for c in items:
            h += c.__hash__()
        return h


    # def hashCode(self, item):
    #     h = 0
    #     for c in item:
    #         h = (31 * h + ord(str(c.val))) & 0xFFFFFFFF
    #     return (((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000)






if __name__ == '__main__':
    a = Sequence(-1)
    a.addItem(Item(1))
    a.addItem(Item(2))
    a.addItem(Item(3))

    b = Sequence(-1)
    b.addItem(Item(1))
    b.addItem(Item(2))
    b.addItem(Item(3))

    c = b.clone()

    print(a.__hash__())
    print(b.__hash__())
    print(c.__hash__())

    seen = set()
    seen.add(b)

    if a in seen:
        print("Seen a")
    if b in seen:
        print("Seen b (obviously)")
    if c in seen:
        print("Seen c")
    if b.__eq__(a):
        print("a == b")
    if b.equals(c):
        print("b == c")



