import time


def get_time(func):
    def inner(self, *args, **kwargs):
        if self.measure_time:
            start = time.time()
            result = func(self, *args, **kwargs)
            return result, '%fs' % float((time.time() - start))
        return func(self, *args, **kwargs)
    return inner


def capfirst(word):
    return word[0].upper() + word[1:]
