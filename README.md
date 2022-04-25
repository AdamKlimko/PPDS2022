# PPDS2022
Repository for the course Parallel programming and distributed systems at FEI STU 2022.
Each exercise has its own branch. The exercises are numbered 01 - 10.

#### Branches:
- 01 - Mutex
- 02 - Simple barrier
- 03 - Producer-consumer
- 04 - Lightswitch, Monitors-sensors
- 05 - Savages
- 06 - barbershop
- 07 - oops
- 08 - async programming
- 09 - CUDA intro

## Intro to CUDA

![](https://upload.wikimedia.org/wikipedia/en/b/b9/Nvidia_CUDA_Logo.jpg)

This exercise follows the course PPDS at FEI STU,
[exercise's page](https://uim.fei.stuba.sk/i-ppds/9-cvicenie-cuda-pomocou-numba/).

The code inside [main.py](main.py) demonstrates a simple use of CUDA to
perform a matrix transposition. It's accessing multiple threads and each 
thread computes one value from the matrix. The matrix must be square shaped.  
