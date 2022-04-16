#!/usr/bin/env python
"""Exercise 8 of the course PPDS at FEI STU Bratislava
In this exercise we explore the benefits of async functions
in python using the asyncio library. This example tests
if using async has benefits in file manipulation.
"""

# Generic/Built-in
import queue
import time

__author__ = "Adam Klimko"
__version__ = "1.0.0"
__email__ = "xklimko@stuba.sk"


def task(name, work_queue):
    """Current task takes filepath from work_queue and reads
    the file. The elapsed time is printed out. This function
    is a generator.
    """
    while not work_queue.empty():
        path = work_queue.get()
        print(f"Task {name} reading file: {path}")
        time_start = time.perf_counter()
        with open(path, 'r') as file:
            file.read()
        elapsed = time.perf_counter() - time_start
        print(f"Task {name} elapsed time: {elapsed*1000:0.4}ms")
        yield


def main():
    work_queue = queue.Queue()
    files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt"]

    for file in files:
        work_queue.put(file)

    tasks = [task("One", work_queue), task("Two", work_queue)]

    done = False
    start_time = time.perf_counter()
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)
            if len(tasks) == 0:
                done = True
    elapsed = time.perf_counter() - start_time
    print(f"\nTotal elapsed time: {elapsed*1000:0.4}ms")


if __name__ == "__main__":
    main()