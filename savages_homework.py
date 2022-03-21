#!/usr/bin/env python
"""Exercise 5 of the course PPDS at FEI STU Bratislava
This is a problem similar to producer-consumer, with the addition of
counting the items that are being shared among threads and
waiting for the item count to get to a certain value.

The whole exercise can be found at:
https://uim.fei.stuba.sk/i-ppds/5-cvicenie-problem-fajciarov-problem-divochov-%f0%9f%9a%ac/
"""

# Generic/Built-in
from random import randint
from time import sleep

# Other Libs
from fei.ppds import Mutex, Semaphore, Thread, print

__author__ = "Adam Klimko"
__version__ = "1.0.0"
__email__ = "xklimko@stuba.sk"


N_SAVAGES = 3
N_COOKS = 2
N_SERVINGS = 5


class SimpleBarrier(object):
    """A simple barrier class. N of threads wait at barrier. When N threads
    arrive, then they can pass through
    """
    def __init__(self, n_savages):
        self.n_savages = n_savages
        self.cnt = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self, each = None, last = None):
        self.mutex.lock()
        self.cnt += 1
        if each:
            print(each)
        if self.cnt == self.n_savages:
            if last:
                print(last)
            self.cnt = 0
            self.barrier.signal(self.n_savages)
        self.mutex.unlock()
        self.barrier.wait()


class Shared(object):
    """Shared class with variables shared between threads"""
    def __init__(self, servings):
        self.servings = servings
        self.mutex = Mutex()
        self.mutex_cook = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)
        self.barrier1 = SimpleBarrier(N_SAVAGES)
        self.barrier2 = SimpleBarrier(N_SAVAGES)
        self.barrier_cooks = SimpleBarrier(N_COOKS)
        self.cooks_finished = 0


def eat():
    sleep(randint(50, 200) / 100)


def savage(i, shared):
    """Savages wait for everyone to arrive at dinner. When all are present they start eating.
    If the pot is empty, they wake up the cooks"""
    sleep(randint(1,100)/100)
    while True:
        shared.barrier1.wait()
        shared.barrier2.wait(each = f'savage {i}: waiting for dinner',
                             last = f'savage {i}: everybody at dinner')

        shared.mutex.lock()
        if shared.servings == 0:
            print(f'savage {i}: pot empty!')
            shared.empty_pot.signal(N_COOKS)
            shared.full_pot.wait()
        print(f'savage {i}: take from pot')
        shared.servings -= 1
        shared.mutex.unlock()
        eat()


def cook(i, shared):
    """The cooks are woken up by savages when pot is empty. They start cooking and wait on each other
    to finish their parts. When all finished, the last one signals savages the pot is full"""
    while True:
        shared.barrier_cooks.wait()

        shared.empty_pot.wait()
        print(f'cook {i}: cooking')
        sleep(randint(50, 200) / 100)
        print(f'cook {i}: finished cooking')

        shared.mutex_cook.lock()
        shared.cooks_finished += 1
        if shared.cooks_finished == N_COOKS:
            print(f'cook {i}: put {N_SERVINGS} servings in pot')
            shared.servings += N_SERVINGS
            shared.full_pot.signal()
            shared.cooks_finished = 0
        shared.mutex_cook.unlock()


def main():
    shared = Shared(0)
    savages = [Thread(savage, i, shared) for i in range(N_SAVAGES)]
    cooks = [Thread(cook, i, shared) for i in range(N_COOKS)]

    for t in savages + cooks:
        t.join()


if __name__ == '__main__':
    main()