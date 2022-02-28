# PPDS2022
Repository for the course Parallel programming and distributed systems at FEI STU 2022.
Each exercise has its own branch. The exercises are numbered 01 - 10.
---
Lab 2 contains exercises that use barriers
## Exercise 1
### Semaphore
Barrier implemented using a Semaphore object
On wait() function, all the threads increment counter
until counter equals n of threads. The last thread
signals that N threads can go through the barrier. Then all
threads go through the barrier, continuing in code execution.
### Event
Barrier implemented using an Event object.
On wait() function, all the threads increment counter
until counter equals n of threads. The last thread
signals and event, which opens the barrier. Then all
threads go through the barrier, continuing in code execution.
## Exercise 2
Barrier implementation in an infinite loop using two barrier objects(SimpleBarrier)
that divide the executed code inside the loop.
