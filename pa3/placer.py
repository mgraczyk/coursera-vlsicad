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

def getVars(gates, pads, weights, start, end, corner, width):
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

    padNets = np.array([p[0] for p in pads])
    padWeights = weights[padNets]
    padX = np.array([p[1] for p in pads])
    padY = np.array([p[2] for p in pads])

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

def solveSq(gates, pads, weights, start, end):
    A, bx, by = getVars(gates, pads, weights, start, end)

    csrA = A.tocsr()
    x = spsolve(csrA, bx)
    y = spsolve(csrA, by)

    return x,y

def solve(gates, N, pads):
    gates = tuple(np.array(g, dtype=np.int_) - 1 for g in gates)
    pads = tuple((np.int_(p[0]) - 1, p[1], p[2]) for p in pads)

    weights = np.zeros(N, dtype=np.float64)
   
    for n in range(N):
        for g in range(len(gates)):
            if n in gates[g]:
                weights[n] += 1
        for p in range(len(pads)):
            if n in pads[p]:
                weights[n] += 1
    
    weights -= 1
    weights = 1/weights

    x,y = solveSq(gates, pads, weights, 0, len(gates))
    
    gates = tuple(map(itemgetter(1),
            sorted(enumerate(gates), key=lambda i:x[i[0]])))


    return zip(x,y)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        gates, N, pads = netlist.readNetlist(sys.argv[1])
        coords = solve(gates, N, pads)

        netlist.writeCoordsFile(sys.stdout, coords)
        print()
    else:
        print("USAGE: {} netlist".format(sys.argv[0]))
        exit(1)
