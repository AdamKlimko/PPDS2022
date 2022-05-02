#!/usr/bin/env python
"""Exercise 10 of the course PPDS at FEI STU Bratislava
In this exercise we explore the benefits of CUDA streams
"""

from __future__ import division
__author__ = "Adam Klimko"
__version__ = "1.0.0"
__email__ = "xklimko@stuba.sk"

from time import perf_counter
from numba import cuda

import numpy

# Shape of matrix (SIZE x SIZE)
SIZE = 32
N_MATRICES = 15


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


if __name__ == '__main__':
    input_matrices = []
    output_matrices = []
    data_gpu_in = []
    data_gpu_out = []
    gpu_out = []
    streams = []
    start_events = []
    end_events = []

    # Initialize IO matrices
    for _ in range(N_MATRICES):
        streams.append(cuda.stream())
        input_matrices.append(numpy.random.randint(5, size=(SIZE, SIZE)))
        output_matrices.append(numpy.zeros((SIZE, SIZE)))
        start_events.append(cuda.event())
        end_events.append(cuda.event())

    start_time = perf_counter()

    # Data to GPU
    for k in range(N_MATRICES):
        data_gpu_in.append(cuda.to_device(input_matrices[k], stream=streams[k]))
        data_gpu_out.append(cuda.to_device(output_matrices[k], stream=streams[k]))

    # Run
    for k in range(N_MATRICES):
        block_dim = (SIZE // 32, SIZE // 32)
        grid_dim = (32, 32)
        start_events[k].record(streams[k])
        my_kernel_2D[grid_dim, block_dim, streams[k]](data_gpu_in[k], data_gpu_out[k])

    for k in range(N_MATRICES):
        end_events[k].record(streams[k])

    # Data from GPU
    for k in range(N_MATRICES):
        gpu_out.append(data_gpu_in[k].copy_to_host(stream=streams[k]))

    end_time = perf_counter()

    kernel_times = []

    for k in range(N_MATRICES):
        kernel_times.append(cuda.event_elapsed_time(start_events[k], end_events[k]))

    print(f'Total time: {round(end_time - start_time, 2)}s')
    print('Mean kernel duration (milliseconds): %f' % numpy.mean(kernel_times))
    print('Mean kernel standard deviation (milliseconds): %f' % numpy.std(kernel_times))