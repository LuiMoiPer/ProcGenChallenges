class UniqueDeque:
    def __init__(self, move_dupes = False):
        self._seen = {}
        self._head = None
        self._tail = None
        self._len = 0
        self._move_dupes = move_dupes
    
    def __len__(self):
        return self._len

    def _move_right(self, item):
        raise NotImplementedError

    def _move_left(self, item):
        raise NotImplementedError

    def append(self, item):
        if item not in self._seen:
            pass
        elif item in self._seen and self._move_dupes:
            pass
        else:
            pass
        raise NotImplementedError

    def append_left(self, item):
        if item not in self._seen:
            pass
        elif item in self._seen and self._move_dupes:
            pass
        else:
            pass
        raise NotImplementedError
        
    def pop(self):
        raise NotImplementedError

    def pop_left(self):
        raise NotImplementedError

    def remove(self, item):
        raise NotImplementedError    


class DoublyLinkedList:
    def __init__(self):
        self._head = None
        self._tail = None
        self._len = 0

    def __len__(self):
        return self._len

    def append(self, item):
        node = DoublyLinkedNode(item)
        if self._len == 0:
            self._head = node
            self._tail = node
        else:
            # add new node to the list
            self._tail.next = node
            node.prev = self._tail
            # update tail
            self._tail = node
        self._len += 1

    def append_left(self, item):
        node = DoublyLinkedNode(item)
        if self._len == 0:
            self._head = node
            self._tail = node
        else:
            # add new node to the list
            node.next = self._head
            self._head.prev = node
            # update head
            self._head = node
        self._len += 1
        
    def pop(self):
        if self._len == 0:
            return None

        # update tail
        node = self._tail
        self._tail = self._tail.prev
        # disconnect the new and old tail
        node.prev = None
        self._tail.next = None
        self._len -= 1
        
        return node.data

    def pop_left(self):
        if self._len == 0:
            return None

        # update head
        node = self._head
        self._head = self._head.next
        # disconnect the new and old head
        node.next = None
        self._head.prev = None
        self._len -= 1
        
        return node.data
        

class DoublyLinkedNode:
    def __init__(self, data = None):
        self._prev = None
        self._next = None
        self._data = data

    @property
    def prev(self):
        return self._prev

    @prev.setter
    def prev(self, node):
        # check class
        self._prev = node

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, node):
        # check class
        self._next = node

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, d):
        self._data = d

if __name__ == "__main__":
    pass

