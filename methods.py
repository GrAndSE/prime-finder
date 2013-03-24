from abc import ABCMeta, abstractmethod
import re
import urllib
import urllib2

from utils import get_time


class Method(object):
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        self.measure_time = kwargs.get('measure_time', True)

    @get_time
    def find(self, index):
        return self._find(index) if index > 0 else None

    @abstractmethod
    def _find(self, index, **kwargs):
        pass


class Bruteforce(Method):
    @staticmethod
    def test(number):
        for div in xrange(2, int(number ** (.5)) + 1):
            if not number % div:
                return False
        return True

    def _find(self, index):
        counter = 1
        result = 2

        while counter < index:
            result += 1
            while not self.test(result):
                result += 1
            counter += 1
        return result


class Database(Method):
    def _find(self, index):
        url = 'http://primes.utm.edu/nthprime/index.php'
        request = urllib2.Request(url, urllib.urlencode({'n': index}))
        response = urllib2.urlopen(request).read()
        return int(re.findall('prime is ([0-9,]+).', response)[1].replace(',', ''))


class OptimizedEratosthenesSieve(Method):
    def __init__(self, piece_size=40000, *args, **kwargs):
        super(OptimizedEratosthenesSieve, self).__init__(*args, **kwargs)
        self.piece_size = piece_size
        self.last_indexes = {}
        self.primes = []

    def _find(self, index):
        if self.piece_size == 'prop':
            self.piece_size = index
        if index == 1:
            return 2

        step = 0
        while len(self.primes) < (index - 1):
            self._get_primes(self.piece_size * step)
            step += 1
        return self.primes[index - 1]

    def _strikeout(self, seq, prime, from_):
        for i in seq:
            self.sieve[i] = False

        # store last prime index if sequence exist
        try:
            self.last_indexes[prime] = seq[-1] + from_
        except IndexError:
            pass

    def _get_primes(self, from_=0):
        self.sieve = [True] * self.piece_size

        if self.primes:
            # strikeout previous prime numbers in current sieve
            for prime in self.primes:
                if prime in self.last_indexes:
                    begin = self.last_indexes[prime] + prime - from_
                else:
                    begin = prime ** 2 - from_

                if begin < self.piece_size:
                    self._strikeout(xrange(begin, self.piece_size, prime), prime, from_)
        else:
            # initial sieve - 0 and 1 aren't prime
            self.sieve[0] = self.sieve[1] = False

            # look over the sieve until square root of sieve size
            for i in xrange(int(self.piece_size ** (.5)) + 1):
                if self.sieve[i]:
                    # start strikeout from a square of prime number to sieve size
                    self._strikeout(xrange(i ** 2, self.piece_size, i), i, from_)

        # fetch prime numbers from unstroken cells
        self.primes.extend([i + from_ for i, flag in enumerate(self.sieve) if flag])
