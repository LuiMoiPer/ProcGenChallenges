import math
class UniqueDeque:
    def __init__(self, move_dupes = False):
        self._nodes = {}
        self._head = None
        self._tail = None
        self._len = 0
        self._move_dupes = move_dupes
    
    def __len__(self):
        return self._len

    def __str__(self):
        out = []
        cursor = self._head
        while cursor is not None:
            out.append(cursor.data)
            cursor = cursor.next
        return str(out)

    def _remove_node(self, node):
        # update head and tail if needed
        if node == self._head:
            self._head = node.next
        if node == self._tail:
            self._tail = node.prev
        # remove the node
        prev = node.prev
        nxt = node.next
        node.prev = None
        node.next = None
        # mend the list
        if prev is not None:
            prev.next = nxt
        if nxt is not None:
            nxt.prev = prev

    def _move_right(self, item):
        if self._len < 1:
            return
        node = self._nodes[item]
        if node != self._tail:
            self._remove_node(node)
            self._append_node(node)

    def _move_left(self, item):
        if self._len < 1:
            return
        node = self._nodes[item]
        if node != self._head:
            self._remove_node(node)
            self._append_node_left(node)

    def _append_node(self, node):
        if self._len == 0:
            self._head = node
            self._tail = node
        else:
            # add new node to the list
            self._tail.next = node
            node.prev = self._tail
            # update tail
            self._tail = node

    def _append_node_left(self, node):
        if self._len == 0:
            self._head = node
            self._tail = node
        else:
            # add new node to the list
            node.next = self._head
            self._head.prev = node
            # update head
            self._head = node

    @property
    def move_dupes(self):
        return self._move_dupes

    @move_dupes.setter
    def move_dupes(self, value):
        self._move_dupes = value
  
    def append(self, item):
        updated = False
        if item not in self._nodes:
            # make node and store in seen
            node = DoublyLinkedNode(item)
            self._nodes[item] = node
            # add the node to the list
            self._append_node(node)
            self._len += 1
            updated = True
        elif item in self._nodes and self._move_dupes:
            self._move_right(item)
            updated = True
        return updated

    def append_left(self, item):
        updated = False
        if item not in self._nodes:
            # mack the node and update the dict
            node = DoublyLinkedNode(item)
            self._nodes[item] = node
            self._append_node_left(node)
            self._len += 1
            updated = True
        elif item in self._nodes and self._move_dupes:
            self._move_left(item)
            updated = True
        return updated
        
    def pop(self):
        if self._len == 0:
            return None
        elif self._len > 0:
            node = self._tail
            self._remove_node(node)
            item = node.data
            del self._nodes[item]
            self._len -= 1
        return item

    def pop_left(self):
        if self._len == 0:
            return None
        elif self._len > 0:
            node = self._head
            self._remove_node(node)
            item = node.data
            del self._nodes[item]
            self._len -= 1
        return item

    def remove(self, item):
        updated = False
        if item in self._nodes:
            self._remove_node(self._nodes[item])
            del self._nodes[item]
            self._len -= 1
            updated = True
        return updated


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

class Point2d:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __str__(self):
        return f"{self._x}:{self._y}"
    
    def __repr__(self):
        return f"Point2d({self._x}, {self._y})"
    
    def __add__(self, other):
        return Point2d(self._x + other.x, self._y + other.y)

    def __iadd__(self, other):
        self._x += other.x
        self._y += other.y
        return self

    def __sub__(self, other):
        return Point2d(self._x - other.x, self._y - other.y)

    def __isub__(self, other):
        self._x -= other.x
        self._y -= other.y
        return self

    def __mul__(self, other):
        return Point2d(self._x * other.x, self._y * other.y)

    def __imul__(self, other):
        self._x *= other.x
        self._y *= other.y
        return self

    def __truediv__(self, other):
        return Point2d(self._x // other.x, self._y // other.y)

    def __idiv__(self, other):
        self._x //= other.x
        self._y //= other.y
        return self

    @staticmethod
    def distance(a, b):
        return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def distance_from_origin(self):
        return math.sqrt(self._x ** 2 + self._y ** 2)

if __name__ == "__main__":
    pass

