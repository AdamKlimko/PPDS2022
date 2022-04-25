#!/usr/bin/env python
"""Exercise 09 of the course PPDS at FEI STU Bratislava
In this exercise we explore the benefits of CUDA programming
"""

__author__ = "Adam Klimko"
__version__ = "1.0.0"
__email__ = "xklimko@stuba.sk"

from __future__ import division
from numba import cuda
import numpy
import math


# Shape of matrix (SIZE x SIZE)
SIZE = 8


@cuda.jit
def my_kernel_2D(input, output):
    """
    Function transposes input matrix and saves the result in output matrix
    :param input:  Matrix to transpose
    :param output: Dummy matrix of same size as output
    """
    x, y = cuda.grid(2)
    x_max, y_max = input.shape
    if x < x_max and y < y_max:
        output[x, y] = input[y, x]


matrix1 = numpy.random.randint(5, size=(SIZE, SIZE))
matrix2 = numpy.zeros((SIZE, SIZE))

threadsperblock = (SIZE, SIZE)
blockspergrid_x = math.ceil(matrix1.shape[0] / threadsperblock[0])
blockspergrid_y = math.ceil(matrix1.shape[1] / threadsperblock[1])
blockspergrid = (blockspergrid_x, blockspergrid_y)

print(matrix1)
my_kernel_2D[blockspergrid, threadsperblock](matrix1, matrix2)
print(matrix2)