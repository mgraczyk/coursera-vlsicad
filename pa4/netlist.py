#!/usr/bin/python3

import sys
import numpy as np
import math

def read_grid(path):
    with open(path, "r") as f:
        # Grid size, bend penalty, via penalty
        cols, rows, bendp, viap = map(float, next(f).split())

        data = np.loadtxt(f, dtype=np.int8).reshape((-1, rows, cols))
        data = np.swapaxes(data, 1, 2)

        return bendp, viap, data

def parse_net(netStr):
    # (layer1, x1, y1, layer2, x2, y2)
    netArr = netStr.split()
    return np.array(netArr[1:], dtype=np.uint16)

def read_nl(path):
    with open(path, "r") as f:
        numNets = int(next(f))

        nets = tuple(parse_net(next(f)) for _ in range(numNets))
        return nets

def write_routes(path, netlist):
    with open(path, "w") as f:
        netlist = list(netlist)
        f.write(str(len(netlist)) + "\n")

        for num, net in enumerate(netlist):
            f.write(str(num+1) + "\n")

            if net:
                lastLayer = net[0][0]
                for cell in net:
                    # Check for vias
                    if lastLayer != cell[0]:
                        f.write("3 {} {}".format(cell[1], cell[2]))
                        f.write("\n")

                    f.write(" ".join(map(str, cell)))
                    f.write("\n")
                    lastLayer = cell[0]
            f.write("0\n")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        basename = sys.argv[1]
        nl = read_nl(basename + ".nl")
        bendp, viap, data = read_grid(basename + ".grid")
        print(bendp, viap)
        print()
        print(data)
        print()
        print(data.shape)
        print()
        print(nl)
    else:
        print("USAGE: {} input_basename".format(sys.argv[0]))
        exit(1)
