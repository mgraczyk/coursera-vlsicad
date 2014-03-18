

import pcn

import itertools
import operator
from collections import defaultdict
from itertools import chain
from itertools import starmap

def compose(func_1, func_2, unpack=False):
    """
    compose(func_1, func_2, unpack=False) -> function

    The function returned by compose is a composition of func_1 and func_2.
    That is, compose(func_1, func_2)(5) == func_1(func_2(5))
    """
    if not callable(func_1):
        raise TypeError("First argument to compose must be callable")
    if not callable(func_2):
        raise TypeError("Second argument to compose must be callable")

    if unpack:
        def composition(*args, **kwargs):
            return func_1(*func_2(*args, **kwargs))
    else:
        def composition(*args, **kwargs):
            return func_1(func_2(*args, **kwargs))
    return composition

def complement_cube(cube):
    return tuple((-v,) for v in cube)

def all_max(values, key=None):
    maxTotal = max(values, key=key)
    return (v for v in values if key(v) == key(maxTotal))

def all_min(values, key=None):
    minTotal = min(values, key=key)
    return (v for v in values if key(v) == key(minTotal))

def most_binate(cubes):
    counts = defaultdict(lambda: [0,0,0])

    for cube in cubes:
        for v in cube:
            counts[abs(v)][v>0] += 1
            counts[abs(v)][2] += 1

    binate = tuple((v,c) for v,c in counts.items() if c[0]>0 and c[1]>0)
    if len(binate) > 0:
        # Pick smallest index if there is a tie
        mostBinate = tuple(all_max(binate, key = lambda arg: arg[1][2]))
        balancers = all_min(mostBinate, key = lambda arg: abs(arg[1][1] - arg[1][0]))

        choice = min(map(operator.itemgetter(0), balancers))
    else:
        # Again, pick smallest index if there is a tie
        mostUnate = all_max(counts.items(), key = lambda arg: arg[1][2])
        choice = min(map(operator.itemgetter(0), mostUnate))

    return choice

def generalCofactor(cubes, x):
    return tuple(
            tuple(c for c in cube if c != x)
                for cube in cubes if -x not in cube)

def positiveCofactor(cubes, position):
    assert(position > 0)
    return generalCofactor(cubes, position)

def negativeCofactor(cubes, position):
    assert(position > 0)
    return generalCofactor(cubes, -position)

def cubes_var_and(cubes, var):
    return tuple(tuple(chain(cube, (var,))) for cube in cubes)

def cubes_or(left, right):
    return tuple(set(chain(left, right)))

def cubes_and(left, right):
    allTerms = itertools.product(left, right)

    return tuple(map(tuple, starmap(compose(set, chain),
                allTerms)))

def complement(cubes):
    # check if F is simple enough to complement it directly and quit
    if len(cubes) == 0:
        # Boolean equation "0"
        # Return a single don't care cube
        result = tuple(tuple())
    elif len(cubes) == 1:
        # One cube list, use demorgan's law
        result = complement_cube(cubes[0])

    elif any(len(c) == 0 for c in cubes):
        # Boolean F = stuff + 1
        # Return empty cube list, or "1"
        result = tuple()
    else:
        x = most_binate(cubes)
        
        pCubes = complement(positiveCofactor(cubes, x))
        nCubes = complement(negativeCofactor(cubes, x))

        p = cubes_var_and(pCubes, x)
        n = cubes_var_and(nCubes, -x)
        result = cubes_or(p, n)

    return result
