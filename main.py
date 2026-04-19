class Memoization:
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]
        else:
            result = self.func(*args)
            self.cache[args] = result
            return result

    def clear_cache(self):
        self.cache.clear()

def memoize(func):
    return Memoization(func)

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def test_memoization():
    print(fibonacci(10))
    print(fibonacci(10))
    print(fibonacci(5))
    print(fibonacci(20))
    memoization_instance = Memoization(fibonacci)
    print(memoization_instance(10))
    memoization_instance.clear_cache()
    print(memoization_instance(10))

class DecoratorTest:
    def __init__(self):
        self.decorate_me = self.decorator(self.decorate_me_test)

    def decorator(self, func):
        def wrapper(*args, **kwargs):
            print("Something is happening before the function is called.")
            result = func(*args, **kwargs)
            print("Something is happening after the function is called.")
            return result
        return wrapper

    def decorate_me_test(self):
        print("This function is being decorated.")

def main():
    test = DecoratorTest()
    test.decorate_me()
    test_memoization()

class CachingTest:
    def __init__(self):
        self.cache = {}

    def caching_test(self, func):
        def wrapper(*args, **kwargs):
            if args in self.cache:
                return self.cache[args]
            else:
                result = func(*args, **kwargs)
                self.cache[args] = result
                return result
        return wrapper

    def cached_add(self):
        @self.caching_test
        def add(a, b):
            return a + b
        return add

def another_test():
    caching_test_instance = CachingTest()
    add = caching_test_instance.cached_add()
    print(add(2, 3))
    print(add(2, 3))

if __name__ == "__main__":
    main()
    another_test()