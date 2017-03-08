class LinkedListUnderflow(Exception):
    def __init__(self, value):
        self.value = value


class DoubleNode:
    def __init__(self, elem, prev=None, next=None):
        self.elem = elem
        self.prev = prev
        self.next = next


class DLlist:
    def __init__(self):
        self._head = None
        self._rear = None

    def prepend(self, elem):
        p = DoubleNode(elem, None, self._head)
        if self._head is None:
            self._rear = p
        else:
            p.next.prev = p
        self._head = p

    def append(self, elem):
        p = DoubleNode(elem, self._rear, None)
        if self._head is None:
            self._head = p
        else:
            p.next.prev = p
        self._rear = p

    def pop(self):
        if self._head is None:
            raise LinkedListUnderflow("not in list")
        e = self._head.elem
        self._head = self._head.next
        if self._head is not None:
            self._head.prev = None
        return e

    def pop_last(self):
        if self._head is None:
            raise LinkedListUnderflow("not in list")
        e = self._rear.elem
        self._rear = self._rear.prev
        if self._rear is None:
            self._head = None
        else:
            self._rear.next = None
        return e


d = DLlist()
d.append(1)
d.prepend('a')
d.append('b')
print(d.pop())
