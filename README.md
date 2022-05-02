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
- 10 - CUDA optimization

## CUDA optimization

![](https://upload.wikimedia.org/wikipedia/en/b/b9/Nvidia_CUDA_Logo.jpg)

This exercise follows the course PPDS at FEI STU,
[exercise's page](https://uim.fei.stuba.sk/i-ppds/cvicenie-10-cuda-prudy-a-udalosti/).

For the last exercise we have a script that executes matrix transposition on multiple
matrices. In the file [not_optimized.py](not_optimized.py) this happens sequentially.
We add optimization using GPU streams in the 2nd file [optimized.py](optimized.py).
To see the result we need to run the script with the presence of a CUDA
compatible graphics card(nvidia).