class decorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)


class C:
    # @decorator
    def method(self, x, y):
        print(x + y)


c = C()
c.method(3, 4)
C.method(c, 3, 4)
c.__class__.method(c, 3, 4)

print(C is c.__class__)

# c.method(c, 3, 4)


def decorator2(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@decorator2
def method(x, y):
    return x + y


# method(3, 4)