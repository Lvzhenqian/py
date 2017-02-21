class Node:
    def __init__(self,lchild,data,rchild):
        self.lchild= lchild
        self.data = data
        self.rchild=rchild

class TopHeap:
    def __init__(self):
        self._head = None
    def put(self,v,p):
        if self._head is None:
            self._head = Node(self._head,(v,p),None)
        return

