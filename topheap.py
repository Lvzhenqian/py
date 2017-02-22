import random


class TopHeap:
    def __init__(self):
        self._data = []

    def put(self, value, p):
        i = len(self._data)
        self._data.append((value, p))
        pi = (i - 1) // 2
        while pi >= 0 and p > self._data[pi][1]:
            self._data[i], self._data[pi] = self._data[pi], self._data[i]
            i = pi
            pi = (i - 1) // 2

    def pop(self):
        if not self._data:
            return None
        if len(self._data) == 1:
            return self._data[0][0]
        x = 0
        ret = self._data[x][1]
        self._data[x] = self._data.pop()
        li = 2 * x + 1
        ri = 2 * x + 2
        while self._data and li < len(self._data):
            ci = li
            if ri < len(self._data) and self._data[ri][1] > self._data[li][1]:
                ci = ri
            if self._data[ci][1] > self._data[x][1]:
                self._data[ci], self._data[x] = self._data[x], self._data[ci]
                x = ci
                li = 2 * x + 1
                ri = 2 * x + 2
            else:
                break
        return ret


heap = TopHeap()

for i in [random.randint(0, 100) for x in range(20)]:
    heap.put('c', i)
for _ in range(20):
    print(heap.pop())
