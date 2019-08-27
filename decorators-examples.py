from time import time

def timer(func):
    def f(x, y=10):
        # I may change 'x' and 'y'on '*args', '**kwargs'.
        # Now this decorator works on any function that takes any arbitrary set
        # of positional and keyword parameters.
        '''How this function get 'x' and 'y'? Because add = timer(add) -
        which returns f(x, y). So in this case        add = f(x, y).'''
        before = time()
        rv = func(*args, **kwargs)
        after = time()
        print('elapsed:', after - before)
        return rv
    return f

@timer  # it is equivalent of 'add = timer(add)'
def add(x, y=10):
    return x + y
#add = timer(add)

@timer  # it is equivalent of 'sub = timer(sub)'
def sub(x, y=10):
    return x - y
#sub = timer(sub)

#-------------------------------------------------------------------------------
# Let's say I want to execute adding two times, then:
n = 2
def ntimes(f):
    def wrapper(*args, **kwargs):
        for _ in range(n):
            print(f'running {f.__name__}')
            rv = f(*args, **kwargs)
        return rv
    return wrapper

@ntimes  # it is equivalent of 'add = ntimes(add)'
def add(x, y=10):
    return x + y

@ntimes  # it is equivalent of 'sub = ntimes(sub)'
def sub(x, y=10):
    return x - y


'''# to generize the problem into 'n' times instead of 2 times:
def ntimes(n):
    def inner(f):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                print(f'running {f.__name__}')
                rv = f(*args, **kwargs)
                return rv
            return wrapper
        return inner

@ntimes(2)
def add(x, y=10):
    return x + y

@ntimes(3)
def sub(x, y=10):
    return x - y'''
#-------------------------------------------------------------------------------

print('add(10)',             add(10))
print('add(20, 30)',         add(20, 30))
print('add("a" + "b")',      add('a', 'b'))
print('add(10)',             sub(10))
print('add(10)',             sub(20, 30))

# In Python everything has run-time representation.
