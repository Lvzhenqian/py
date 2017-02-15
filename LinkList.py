class LinkNode:
    def __init__(self, elem, next_):
        self.elem = elem
        self.next = next_


class LinkList:
    def __init__(self):
        self._head = None
        self.count = 0

    def pop_top(self):
        if self._head is None:
            raise ValueError('not this values')
        value = self._head.elem
        self._head = self._head.next
        self.count -= 1
        return value

    def append(self, x):
        if self._head is None:
            self._head = LinkNode(x, None)
            return self._head
        p = self._head
        while p.next is not None:
            p = p.next
        p.next = LinkNode(x, None)
        self.count += 1
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
        self.count -= 1
        return values

    def index(self, v):
        p = self._head
        n = 0
        while p is not None:
            if v == p.elem:
                return n
            p = p.next
            n +=1

    def insert(self, index, elem):
        if index == 0:
            self._head = LinkNode(elem, self._head)
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


link = LinkList()
link.append(1)
link.append(2)
link.append(3)
link.append(4)
link.insert(1, 'a')
link.insert(3,'g')
link.insert(6,'a')
print(link.index('g'))
#print(link.pop())
#print(link.pop_last())
#print(link.count)
link.show()
