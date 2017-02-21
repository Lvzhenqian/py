class LinkNode:
    count = 0

    def __init__(self, elem, next_=None):
        self.elem = elem
        self.next = next_
        LinkNode.count += 1


class LinkList:
    def __init__(self):
        self._head = None

    def pop_top(self):
        if self._head is None:
            raise ValueError('not this values')
        value = self._head.elem
        self._head = self._head.next
        LinkNode.count -= 1
        return value

    def append(self, x):
        if self._head is None:
            self._head = LinkNode(x)
            return self._head
        p = self._head
        while p.next is not None:
            p = p.next
        p.next = LinkNode(x)
        return self._head

    def pop(self):
        if self._head is None:
            raise ValueError('empty Linklist')
        p = self._head
        if p.next is None:
            values = p.elem
            self._head = None
            return values
        while p.next.next is not None:
            p = p.next
        values = p.next.elem
        p.next = None
        LinkNode.count -= 1
        return values

    def index(self, v):
        p = self._head
        n = 0
        while p is not None:
            if v == p.elem:
                return n
            p = p.next
            n += 1

    def insert(self, index, elem):
        if index == 0:
            self._head = LinkNode(elem, self._head)
            return self._head
        p = self._head
        i = 0
        while i < index - 1 and p.next is not None:
            p = p.next
            i += 1
        p.next = LinkNode(elem, p.next)
        return self._head

    def show(self):
        p = self._head
        while p is not None:
            print(p.elem, end='')
            if p.next is not None:
                print(', ', end='')
            p = p.next
        print()

    @property
    def count(self):
        return LinkNode.count


class Llist(LinkList):
    def __init__(self):
        super().__init__()
        self._rear = None

    def insert(self, index, elem):
        if self._head is None:
            self._head = LinkNode(elem, self._head)
            self._rear = self._head
            return
        elif index == 0:
            self._head = LinkNode(elem, self._head)
            return
        p = self._head
        i = 0
        while i < index - 1 and p.next is not None:
            p = p.next
            i += 1
        p.next = LinkNode(elem, p.next)
        return self._head

    def append(self, x):
        if self._head is None:
            self._head = LinkNode(x, self._head)
            self._rear = self._head
        else:
            self._rear.next = LinkNode(x)
            self._rear = self._rear.next

    def pop(self):
        if self._head is None:
            raise ValueError('empty Linklist')
        p = self._head
        if p.next is None:
            values = p.elem
            self._head = None
            return values
        while p.next.next is not None:
            p = p.next
        values = p.next.elem
        p.next = None
        self._rear = p
        LinkNode.count -= 1
        return values


link = Llist()
for i in range(10):
    link.insert(0, i)
link.show()
for n in range(20):
    link.append(n)
print(link.pop())
link.show()
