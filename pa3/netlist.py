#!/usr/bin/python3

import sys
import numpy as np
import math

def readNetlist(path):
    with open(path, "r") as f:
        G, N = map(int, next(f).split())

        gates = tuple(tuple(map(int, next(f).split()[2:])) for _ in range(G))

        P = int(next(f))

        # (net_id, x, y)
        pads = (next(f).split()[1:] for _ in range(P))
        pads = tuple((int(p[0]), float(p[1]), float(p[2])) for p in pads)

        return gates, N, pads

def writeCoordsFile(f, coords):
    coords = list(coords)
    fmt = "{{:{}d}} {{:11.8f}} {{:11.8f}}\n".format(math.ceil(math.log(len(coords), 10)))

    for i, p in enumerate(coords):
        f.write(fmt.format(i+1, p[0], p[1]))

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        gates, N, pads = readNetlist(sys.argv[1])
        print(gates)
        print()
        print(N)
        print()
        print(pads)
    else:
        print("USAGE: {} netlist".format(sys.argv[0]))
        exit(1)
