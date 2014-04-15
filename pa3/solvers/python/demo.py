#!/usr/bin/env python
# encoding: utf-8
"""
Solve linear system using SciPy

Sparse matrix:
http://docs.scipy.org/doc/scipy/reference/sparse.html

Solving linear system:
http://docs.scipy.org/doc/scipy/reference/tutorial/linalg.html
"""

import numpy
from numpy import array
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


def main():
    print("Solve small matrix...")
    R = array([0, 0, 1, 1, 1, 2, 2])
    C = array([0, 1, 0, 1, 2, 1, 2])
    V = array([4.0, -1.0, -1.0,  4.0, -1.0, -1.0, 4.0])
    b = array([3.0, 2.0, 3.0])
    A = coo_matrix((V, (R, C)), shape=(3, 3))
    # convert to csr format for efficiency
    x = spsolve(A.tocsr(), b)
    print("x = ", x)

    print("Solve psd matrix...")
    # skip the first row (n, nnz)
    A = numpy.genfromtxt('../data/psd.txt', skiprows=1)
    b = numpy.genfromtxt('../data/b.txt')
    coo = coo_matrix((A[:, 2], (A[:, 0], A[:, 1])))
    x = spsolve(coo.tocsr(), b)
    print('x = ', x)

    print("Solve big matrix...")
    A = numpy.genfromtxt('../data/mat_helmholtz.txt', skiprows=1)
    coo = coo_matrix((A[:, 2], (A[:, 0], A[:, 1])))
    n = coo.shape[0]
    b = numpy.ones(n)
    x = spsolve(coo.tocsr(), b)
    print('x = ', x)

if __name__ == '__main__':
    main()
