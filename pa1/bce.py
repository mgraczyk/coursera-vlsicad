#!/usr/bin/python3

import sys
import os

import pcn
import urp

class BCE(object):
    def __init__(self, inPath, outPath):
        self.inPath = inPath
        self.outPath = outPath
        self.eqs = {}
        self.operations = {
            "r": self.read_pcn,
            "!": self.do_not,
            "+": self.do_or,
            "&": self.do_and,
            "p": self.write_pcn,
            "q": self.quit
        }

        self.done = False

    def process(self, commandFilePath):
        with open(commandFilePath, "r") as f:
            for line in f:
               command, *args = line.split()
               self.operations[command](*args)
               
               if self.done:
                   return

    def read_pcn(self, fNum):
       _, self.eqs[fNum] = pcn.parse(os.path.join(self.inPath, fNum + ".pcn"))

    def write_pcn(self, fNum):
        with open(os.path.join(self.outPath, fNum + ".pcn"), "w") as f:
            pcn.write(f, None, self.eqs[fNum])

    def do_not(self, resultNum, inNum):
        self.eqs[resultNum] = urp.complement(self.eqs[inNum])

    def do_or(self, resultNum, leftNum, rightNum):
        self.eqs[resultNum] = urp.cubes_or(self.eqs[leftNum], self.eqs[rightNum])

    def do_and(self, resultNum, leftNum, rightNum):
        self.eqs[resultNum] = urp.cubes_and(self.eqs[leftNum], self.eqs[rightNum])

    def quit(self):
        self.done = True


Usage = """\
USAGE: {} COMMAND_FILE
"""

if __name__ == "__main__":
    if len(sys.argv) > 1:
        solutionDir = "BCESolutions"
        thisSolDir = os.path.join(solutionDir, sys.argv[1][-5])
        try:
            os.mkdir(thisSolDir)
        except OSError:
            # It's okay if it's already there
            pass

        bce = BCE("BooleanCalculatorEngine", thisSolDir)
        bce.process(sys.argv[1])
    else:
        print(Usage.format(sys.argv[0]))
