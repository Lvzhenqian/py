class Dict:
    def __init__(self, n):
        self.n = n
        self._slot = [[] for _ in range(n)]

    def setin(self, k, v):
        i = hash(k) % self.n
        if not self._slot[i] is None:
            for n, (key, value) in enumerate(self._slot[i]):
                if key == k:
                    self._slot[i][n] = (k, v)
                    return
        self._slot[i].append((k, v))

    def pop(self, k):
        if self._slot is None:
            raise ValueError('Dict is empty')
        index = hash(k) % self.n
        for i in self._slot[index]:
            if i[0] == k:
                return i[1]
        else:
            return 'not this values'


d = Dict(7)
# d.setin('a',12)
# d.setin('a',11)
d.setin(18,'hash')
d.setin(46,'hash')
print(d._slot)
# print(d.pop('a'))
# print(d.pop('aaaa'))

class Dict2:
    def __init__(self, m):
        self.n = m
        self._slot = [None for x in range(m)]

    def put(self, k, v):
        p = 0
        index = 0
        while self._slot[index] and p < self.n -1:
            index = (hash(k) + p) % self.n
            p += 1
        if not self._slot[index]:
            self._slot[index] = (k, v)
        else:
            raise KeyError('slot is full.')
        return True

    def pop(self, k):
        p = 0
        index = 0
        while self._slot[index][0] != k and p < self.n:
            index = (hash(k) + p) % self.n
            p += 1
        return self._slot[index][1]


d2 = Dict2(7)
d2.put(18, '18haha')
d2.put(46, '46haha')
d2.put('a','c')
print(d2._slot)
print(d2.pop(18))
print(d2.pop(46))