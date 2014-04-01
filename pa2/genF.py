#!/usr/bin/python

import itertools
from itertools import product
from itertools import repeat

script = """\
.i 6
.o 1
.ilb x1 x2 x3 x4 x5 x6
.ob F
"""

def get_F():
    binary = (0,1)
    return "\n".join(
        "{}\t{}".format(
            "".join(map(str, seq)),
            int(sum(seq) in (2,3,4)))
        for seq in product(*repeat(binary, 6)))

if __name__ == "__main__":
    print(script + get_F())
