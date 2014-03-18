#!/usr/bin/python3

import sys

import urp
import pcn

Usage = """\
USAGE: {} FILE
"""

if __name__ == "__main__":
    if len(sys.argv) > 1:
        numVars, cubes = pcn.parse(sys.argv[1])
        cubesNot = urp.complement(cubes)

        pcn.write(sys.stdout, numVars, cubesNot)
    else:
        print(Usage.format(sys.argv[0]))
