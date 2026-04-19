from functools import wraps

def memoize(func):
    cache = dict()

    @wraps(func)
    def memoized_func(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return memoized_func

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

@memoize
def factorial(n):
    if n < 2:
        return 1
    return n * factorial(n-1)

@memoize
def power(a, b):
    if b < 2:
        return a ** b
    return a * power(a, b-1)

print(fibonacci(10))
print(factorial(5))
print(power(2, 8))

def test_memoize():
    @memoize
    def add(a, b):
        return a + b

    assert add(2, 3) == 5
    assert add(2, 3) == 5
    assert add(3, 4) == 7
    assert add(3, 4) == 7

test_memoize()

def test_fibonacci():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(2) == 1
    assert fibonacci(3) == 2
    assert fibonacci(4) == 3
    assert fibonacci(5) == 5

test_fibonacci()

def test_factorial():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(2) == 2
    assert factorial(3) == 6
    assert factorial(4) == 24
    assert factorial(5) == 120

test_factorial()

def test_power():
    assert power(2, 0) == 1
    assert power(2, 1) == 2
    assert power(2, 2) == 4
    assert power(2, 3) == 8
    assert power(2, 4) == 16

test_power()