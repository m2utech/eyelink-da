class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return 'Node %s' % self.value


class LinkedList(list, object):
    def __init__(self):
        self.head = None
        self.tail = None

    def __repr__(self):
        result = ''
        node = self.head
        while node:
            result += ' %s' % node
            node = node.next
        return result

    def add(self, node):
        """Add a Node to the back of the LL."""
        if not self.head:
            self.head = node
        if self.tail:
            self.tail.next = node
        self.tail = node

    def remove(self, target_node):
        """Remove a Node instance from the list."""
        if target_node == self.head:
            self.head = self.head.next
            return
        previous_node = self.head
        current_node = self.head.next
        while current_node:
            if current_node == target_node:
                previous_node.next = current_node.next
                return
            previous_node = current_node
            current_node = current_node.next
        raise ValueError

if __name__ == '__main__':
    # Instantiate.
    linked_list = LinkedList()
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)

    # Add.
    linked_list.add(node1)
    linked_list.add(node2)
    linked_list.add(node3)
    linked_list.add(node4)
    print(linked_list)
    #   Node 1 Node 2 Node 3 Node 4

    # Remove.
    linked_list.remove(node3)
    print(linked_list)
    #   Node 1 Node 2 Node 4
    linked_list.remove(node1)
    print(linked_list)
    #   Node 2 Node 4