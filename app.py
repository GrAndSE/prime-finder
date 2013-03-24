import re
from inspect import isclass
from optparse import OptionParser

import methods
from utils import capfirst


def get_available_methods():
    result = []
    for method_name in dir(methods):
        method = getattr(methods, method_name)
        if isclass(method) and issubclass(method, methods.Method) and method != methods.Method:
            result.append('-'.join(re.findall('[A-Z][a-z]*', method_name)).lower())
    return result


def main():
    parser = OptionParser(usage='Usage: %prog [index] [options]')
    parser.add_option(
        '-m', '--method', dest='method_name', default='optimized-eratosthenes-sieve',
        help='Available methods: %s' % ', '.join(get_available_methods()))
    (options, args) = parser.parse_args()

    try:
        index = int(args[0]) if len(args) else 10001
        method_name = '%s' % ''.join([capfirst(w) for w in options.method_name.split('-')])
        method = getattr(methods, method_name, None)()
    except ValueError:
        print 'Index must be positive integer'
        return
    except TypeError:
        print 'Method does not exist'
        return

    result, time = method.find(index)
    print 'Method: %s' % options.method_name
    print 'Index: %d' % index
    print 'Result: %d' % result
    print 'Time: %s' % time


if __name__ == '__main__':
    main()
