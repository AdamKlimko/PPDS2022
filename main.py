#!/usr/bin/env python
"""Exercise 4 of the course PPDS at FEI STU Bratislava

description
"""

# Generic/Built-in
from random import randint
from time import sleep

# Other Libs
from fei.ppds import Mutex, Semaphore, Thread

__author__ = "Adam Klimko"
__version__ = "1.0.0"
__email__ = "xklimko@stuba.sk"


class Lightswitch:
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, semaphore):
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()



if __name__ == '__main__':
    pass