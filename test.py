class Dict:
    def __init__(self, k, v):
        self.k = k
        self.v = v

    def get(self, k):
        if k == self.k:
            return self.v


d = Dict('abc', '22')
print(d.get('abc'))
print(d.__dict__)
