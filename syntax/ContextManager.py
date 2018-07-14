class ContextManager:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwargs):
        self.gen = self.fn(*args, **kwargs)
        return self

    def __enter__(self):
        try:
            return next(self.gen)
        except:
            raise TypeError("{} is not a generator".format(self.gen.__name__))

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            return next(self.gen)
        except StopIteration:
            pass


@ContextManager
def test(x, y):
    print('start')
    try:
        yield x + y
    finally:
        print("exit")


with test(1, 2) as value:
    print(value)
    print('body')
