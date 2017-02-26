class Propery:
    def __init__(self, fn, fset=None, fdel=None):
        self.fn = fn
        self.fset = fset
        self.fdel = fdel

    def __get__(self, instance, owner):
        if instance is not None:
            return self.fn(instance)
        return self

    def __set__(self, instance, value):
        if callable(instance):
            self.fset(instance,value)
        else:
            raise AttributeError('{} can not assigneable'.format(self.fset.__name__))

    def __delete__(self, instance):
        if callable(self.fdel):
            self.fdel(instance)
        else:
            raise AttributeError('{} can not deleteable'.format(self.fdel.__name__))

    def setter(self, fset):
        self.fset = fset
        return self

    def delete(self, fdel):
        self.fdel = fdel
        return self


class B:
    def __init__(self):
        self.__status = 'close'

    @Propery
    def status(self):
        return self.__status

    @status.delete  #status = Propery(status)
    def status(self):
        return self.__status

    @status.setter
    def status(self, v):
        self.__status = v


b = B()
print(b.status)
b.status = 'abc'