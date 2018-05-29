class Node:
    def __init__(self, data, next_node=None, prev_node=None):
        self.data = data
        self.next_node = next_node
        self.prev_node = prev_node


class LinkedList(list):
    def __init__(self):
        self.head = None
        self.tail = None
        self._head = None

    def __len__(self):
        count = 0
        _head = self.head
        while _head:
            count += 1
            self._head = _head.next_node
        return count

    def __iter__(self):
        self._head = self.head
        return self

    def next(self):
        if not self._head:
            raise StopIteration
        data = self._head.data
        self._head = self._head.next_node
        return data

    def __str__(self):
        _head = self.head
        value = []
        value.append("[")
        while _head:
            value.append(str(_head.data))
            value.append(", ")
            _head = _head.next_node
        value.append("]")
        return "".join(map(str, value))

    def __del__(self):
        self.clear()

    def __add__(self, other):
        _Link = LinkedList()
        _head = self.head
        while _head:
            _Link.append(_head.data)
            _head = _head.next_node
        _Link.extend(other)
        return _Link

    def first(self):
        return self.head.data

    def last(self):
        return self.tail.data

    def append(self, data):
        node = Node(data)
        if not self.head:
            self.head = node
        else:
            self.tail.next_node = node
            node.prev_node = self.tail
        self.tail = node

    def appendleft(self, data):
        node = Node(data)
        if not self.tail:
            self.tail = node
        else:
            self.head.prev_node = node
            node.next_node = self.head
        self.head = node

    def appendright(self, data):
        self.append(data)

    def extend(self, iterable):
        for node in iterable:
            self.append(node)

    def extendleft(self, iterable):
        _tail = iterable.tail
        while _tail:
            self.appendleft(_tail.data)
            _tail = _tail.prev_node

    def extendright(self, iterable):
        self.extend(iterable)

    def pop(self):
        value = self.tail.data
        self.tail.prev_node.next_node = None
        self.tail = self.tail.prev_node
        return value

    def popleft(self):
        value = self.head.data
        self.head.next_node.prev_node = None
        self.head = self.head.next_node
        return value

    def popright(self):
        return self.pop()

    def push(self, data):
        self.append(data)

    def pushright(self, data):
        self.append(data)

    def pushleft(self, data):
        self.appendleft(data)

    def find(self, data, node=False):
        _head = self.head
        _tail = self.tail
        while (_head or _tail) and _head.prev_node != _tail and _head != _tail:
            if _head.data == data:
                if node:
                    return _head
                else:
                    return True
            if _tail.data == data:
                if node:
                    return _tail
                else:
                    return True
            _head = _head.next_node
            _tail = _tail.prev_node

        if _head == _tail:
            if _head.data == data:
                if node:
                    return _head
                else:
                    return True
        return False

    def remove(self, data):
        node = self.find(data, True)
        if not node:
            return
        node.prev_node.next_node = node.next_node
        node.next_node.prev_node = node.prev_node

    def clear(self):
        self.head = None
        self.tail = None

    def valueat(self, index):
        if index < 0:
            raise IndexError('Negative Index')
        _index = 0
        _head = self.head
        while _head:
            if _index == index:
                return _head.data
            _head = _head.next_node
            _index += 1
        raise IndexError('index out of range')

    def index(self, data):
        _head = self.head
        _index = 0
        while _head:
            if _head.data == data:
                return _index
            _head = _head.next_node
            _index += 1
        return -1

    def reverse(self):
        _head = self.head
        while _head:
            temp = _head.prev_node
            _head.prev_node = _head.next_node
            _head.next_node = temp
            _head = _head.prev_node
        temp = self.head
        self.head = self.tail
        self.tail = temp

    def insert(self, data, index):
        _index = 0
        _head = self.head
        while _head:
            if _index == index:
                node = Node(data)
                _head.prev_node.next_node = node
                node.next_node = _head
                node.prev_node = _head.prev_node
                _head.next_node.prev_node = node
                return
            _head = _head.next_node
            _index += 1
        raise IndexError('index out of range')