from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex
from fei.ppds import print


"""Barrier implemented using a Semaphore object
On wait() function, all the threads increment counter
until counter equals n of threads. The last thread
signals that N threads can go through the barrier. Then all
threads go through the barrier, continuing in code execution.
"""
class SimpleBarrier:
    def __init__(self, n):
        self.N = n
        self.C = 0
        self.M = Mutex()
        self.T = Semaphore(0)

    def wait(self):
        self.M.lock()
        self.C += 1
        if self.C == self.N:
            self.C = 0
            self.T.signal(self.N)
        self.M.unlock()
        self.T.wait()


def barrier_example(barrier, thread_id):
    sleep(randint(1, 10) / 10)
    print("before barrier %d" % thread_id)
    barrier.wait()
    print("after barrier %d" % thread_id)


THREADS = 5
sb = SimpleBarrier(THREADS)
threads = [Thread(barrier_example, sb, i) for i in range(THREADS)]
[t.join() for t in threads]
