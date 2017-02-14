

class LinkList:
    q,n = None,None
    def put(self,x):
        if self.q is None:
            self.q = {'data':x,'next':None}
        else:
            self.n = {'data':x,'next':self.q}
            self.q = self.n
        return self.q

l = LinkList()
print(l.put(1))
print(l.put(2))
print(l.put(3))
print(l.put(4))