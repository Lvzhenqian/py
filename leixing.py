import inspect
from functools import wraps
def lexing(x,*tyep,**type_kwargs):
    def zxq(fn,*a,**b):
        @wraps(fn)
        def wrap(*args,**kwargs):
            sig = inspect.signature(fn)
            for i in a:
                param = sig.parameters[i]
                if param.annotation != x:
                    print('error not {}'.format(x))
                    return False
            for k,v in b.items():
                param2 = sig.parameters[k]
                if param2.annotation != x:
                    print('error not {}'.format(x))
                    return False
            ret = fn(*args,**kwargs)
            if type(ret) != x:
                print('error not {}'.format(x))
                return False
            return ret
        return wrap
    return zxq

@lexing(int)
def add(x:int,y:int)-> int:
    return x+y

print(add('5','6'))
print('#'*50)
print(add(5,6))
