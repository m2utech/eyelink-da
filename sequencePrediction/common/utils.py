from multipledispatch import dispatch
from database.Item import Item
from database.Sequence import Sequence

@dispatch(Item)
def objToInt(item):
    if not item:
        return None
    else:
        return item.val


@dispatch(Sequence)
def objToTuple(item):
    if item == None:
        return None
    else:
        element = list()
        for i in item:
            element.append(i.val)
        return tuple(element)

@dispatch(list)
def objToTuple(item):
    if not item:
        return None
    else:
        element = list()
        for i in item:
            element.append(i.val)
        return tuple(element)