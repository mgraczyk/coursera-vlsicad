#!/usr/bin/python3

import sys
import pcn
from bisect import bisect

import itertools
import operator
from collections import defaultdict
from itertools import chain


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
    maxTotal = min(values, key=key)
    return (v for v in values if key(v) == key(maxTotal))

def most_binate(cubes):
    counts = defaultdict(lambda: [0,0,0])

    for cube in cubes:
        for v in cube:
            counts[v][v>0] += 1
            counts[v][2] += 1

    binate = tuple((v,c) for v,c in counts.items() if c[0]>0 and c[1]>0)
    if len(binate) > 0:
        mosts = tuple(all_max(binate, key = lambda arg: arg[1][2]))

        assert(mosts)
        if len(mosts) == 1:
            choice = binate[0][0]
        else:
            balancers = all_min(binate, key = lambda arg: abs(arg[1][1] - arg[1][0]))

            assert(balancers)
            if len(balancers) == 1:
                choice = balancers[0][0]
            else:
                # Pick smallest index if there is a tie
                choice = min(map(operator.itemgetter(0), balancers), key=abs)
    else:
        mosts = tuple(all_max(counts.items(), key = lambda arg: arg[1][2]))

        assert(mosts)
        if len(mosts) == 1:
            choice = mosts[0][0]
        else:
            # Again, pick smallest index if there is a tie
            choice = min(map(operator.itemgetter(0), mosts), key=abs)

    return choice

def positiveCofactor(cubes, x):
    return tuple(
            tuple(c for c in cube if c != x)
                for cube in cubes if -x not in cube)

def negativeCofactor(cubes, x):
    return positiveCofactor(cubes, -x)

def cubes_var_and(cubes, var):
    indices = (bisect(cube,var) for cube in cubes)
    return tuple(tuple(cube + (var,)) for index, cube in zip(indices,cubes))

def cubes_or(left, right):
    return tuple(set(chain(left, right)))

def cubes_and(left, right):
    return (cube for cube in
            map(compose(set, operator.concat),
                itertools.product(left, right)))

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

    return tuple(tuple(sorted(cube,key=abs)) for cube in result)

Usage = """\
USAGE: {} FILE
"""

if __name__ == "__main__":
    if len(sys.argv) > 1:
        numVars, cubes = pcn.parse(sys.argv[1])
        cubesNot = complement(cubes)

        #print("Original:")
        #pcn.write(sys.stdout, numVars, cubes)

        #print("Round Trip:")
        #pcn.write(sys.stdout, numVars, complement(cubesNot))

        #print("Solution:")
        pcn.write(sys.stdout, numVars, cubesNot)
    else:
        print(Usage.format(sys.argv[0]))
