from itertools import islice
from itertools import chain

def parse(filePath):
    with open(filePath, "rb") as f:
        # First line is size of array
        try:
            lines = iter(f)
            numVars = int(next(lines))
            cubeCount = int(next(lines))
            cubes = [None]*cubeCount
            
            for i in range(cubeCount):
                line = next(lines)
                cubes[i] = tuple(islice(map(int, line.split()), 1, None))

            return (numVars, tuple(cubes))

        except Exception as error:
            raise AssertionError("Bad pcn file {}".format(filePath)) from error

def write(f, numVars, cubes):
    endl = "\n"

    f.write(str(max(max(map(abs, cube)) for cube in cubes)))
    f.write(endl)
    f.write(str(len(cubes)))
    f.write(endl)

    for cube in cubes:
        f.write(' '.join(map(str, chain((len(cube),), sorted(cube, key=abs)))))
        f.write(endl)

    f.write(endl)

