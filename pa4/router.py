#!/usr/bin/python3

import sys
import os
import numpy as np
import math

import netlist

import heapq

from itertools import repeat

Barrier = -1

# In order, directions are r,u,l,d, layer up, layer down)
# TODO: Vias
dVects = np.array((
        (0,1,0),
        (0,0,1),
        (0,-1,0),
        (0,0,-1)),
        dtype=np.int8)
directions = np.array(tuple(range(len(dVects))), dtype=np.uint8)

visitMark = np.uint8(1)

def trace_backward(predInv, source, dest):
    route = []

    cur = dest
    while not (cur == source).all():
        route.append(cur)
        cur = cur - dVects[predInv[tuple(cur)]]

    route.append(source)
    return tuple(map(tuple, reversed(route)))

def route_one(source, dest, costs, visited, bendp, viap):
    # Store (cost, direction, layer, x, y) in the queue
    # TODO: Can we use np.array here?
    oset = [(costs[tuple(source)], None, tuple(source))]
    heapq.heapify(oset)

    predInv = np.zeros(costs.shape, dtype=np.uint8)

    while oset:
        u = heapq.heappop(oset)
        cost, prevD, cur = u
        #print("considering {}".format(cur))

        for pred in directions:
            if pred == prevD:
                continue

            dv = dVects[pred]
            neigh = (cur[0] + dv[0], cur[1] + dv[1], cur[2] + dv[2])
            #print("visiting {}".format(neigh))

            if visited[neigh]:
                continue

            visited[neigh] = visitMark
            predInv[neigh] = pred

            if (neigh == dest).all():
                print("Routed net {} -> {}".format(source, dest))
                return trace_backward(predInv, source, dest)
            else:
                heapq.heappush(oset, (cost + costs[neigh], pred, neigh))

    print("Failed to route net {} -> {}".format(source, dest))
    return []

def pad_netlist(nl):
    padding = np.array((-1,1,1,-1,1,1), dtype=np.int8)
    return tuple(net + padding for net in nl)

def unpad_route(route):
    unpadding = np.array((1,-1,-1), dtype=np.int8)
    return tuple(s + unpadding for s in route)

def route(nl, data, bendp=0, viap=0):
    # pad the array with barriers to make core router simpler
    data = np.pad(data, ((0,0),(1,1),(1,1)), mode='constant', constant_values=(Barrier, Barrier))
    nl = pad_netlist(nl)

    barriers = np.array(data == Barrier, dtype=np.uint8)
    routes = []
    for net in nl:
        routes.append(route_one(net[0:3], net[3:], data, np.copy(barriers), bendp, viap))
        for pos in routes[-1]:
            barriers[pos] = visitMark

    return map(unpad_route, routes)

def do_routing(basename):
    nl = netlist.read_nl(basename + ".nl")
    bendp, viap, data = netlist.read_grid(basename + ".grid")
    routes = route(nl, data, bendp=bendp, viap=viap)

    resultsDir = "results"
    try:
        os.makedirs(resultsDir)
    except:
        pass

    netlist.write_routes(os.path.join(resultsDir, basename + ".route"), routes)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        for case in sys.argv[1:]:
            do_routing(case)
    else:
        print("USAGE: {} input_basename".format(sys.argv[0]))
        exit(1)
