import itertools

ai = range(8)
bi = range(8)

[print("{}{} {}".format(bin(ai)[2:].zfill(3), bin(bi)[2:].zfill(3), bin(ai*bi%13)[2:].zfill(4)))
        for ai,bi in itertools.product(a,b)]
