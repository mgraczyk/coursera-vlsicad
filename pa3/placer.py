#!/usr/bin/python

import os
import sys
import numpy as np

from scipy.sparse import coo_matrix
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

from operator import itemgetter
from itertools import repeat
from itertools import chain

import netlist

def getVars(gates, pads, weights, start, end, botL, topR):
    sz = end - start

    # Create the C matrix
    C = np.zeros((sz, sz), dtype=np.float64)
    bx = np.zeros(sz, dtype=np.float64)
    by = np.zeros(sz, dtype=np.float64)

    for g in range(start, end):
        for j in range(g+1, end):
            C[g,j] = np.sum(weights[
                        np.intersect1d(gates[g], gates[j], assume_unique=True)
                    ])

    # Make it symmetric
    C = np.add(C, C.T)

    C[np.diag_indices_from(C)] -= np.sum(C, 1)

    padNets = [p[0] for p in pads]
   
    padNets = np.array(padNets)
    padWeights = weights[padNets]

    padX = np.array([max(min(p[1], topR[0]), botL[0]) for p in pads])
    padY = np.array([max(min(p[2], topR[1]), botL[1]) for p in pads])

    padWeightedX = padWeights*padX
    padWeightedY = padWeights*padY


    for g in range(start, end):
        isect = np.intersect1d(gates[g], padNets, assume_unique=True)
        ipsect = np.in1d(padNets, gates[g], assume_unique=True)
        toPadWeights = weights[isect]
        C[g,g] -= np.sum(toPadWeights)
        bx[g] = np.sum(padWeightedX*ipsect)
        by[g] = np.sum(padWeightedY*ipsect)

    return coo_matrix(-C), bx, by

def solveSq(gates, pads, weights, start, end, botL, topR):
    A, bx, by = getVars(gates, pads, weights, start, end, botL, topR)

    csrA = A.tocsr()
    x = spsolve(csrA, bx)
    y = spsolve(csrA, by)

    return x,y

def solve(gates, N, pads):
    """ 
        gates are the gates to place.
        N is the number of nets.
        pads are the positions of the pads
    """

    gates = tuple(np.array(g, dtype=np.int_) - 1 for g in gates)
    pads = tuple((np.int_(p[0]) - 1, p[1], p[2]) for p in pads)

    weights = np.zeros(N, )
  
    allConnections = np.array(tuple(chain(chain.from_iterable(gates), (p[0] for p in pads))))
    weights = np.float64(1.0)/(np.bincount(allConnections) - 1)

    x,y = solveSq(gates, pads, weights, 0, len(gates), (0,0), (100,100))
    xOrder = np.argsort(x)
    yOrder = np.argsort(y)

    gates = tuple(map(itemgetter(1),
            sorted(enumerate(gates), key=lambda i:x[i[0]])))

    return zip(x,y)

def solve_fake(gates, N, pads):
    x = []
    xP = 1.0/16

    rem = len(gates)
    while rem > 0:
      x.append(100*xP)
      xP += 1.0/8
      if xP > 1.0:
        xP = 1.0/16
      rem -= 1

    return zip(x,x)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        gates, N, pads = netlist.readNetlist(sys.argv[1])
        coords = solve(gates, N, pads)

        netlist.writeCoordsFile(sys.stdout, coords)
        print()
    else:
        print("USAGE: {} netlist".format(sys.argv[0]))
        exit(1)
