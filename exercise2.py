from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore
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

def rendezvous(thread_name):
    sleep(randint(1, 10) / 10)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    print('ko: %s' % thread_name)
    sleep(randint(1, 10) / 10)

"""Function showing an infinite loop
using two simple barriers. All threads first
do rendezvous() and wait at the first barrier.
Then they all do ko() and wait at the second barrier.
The cycle repeats.
"""
def barrier_example(b1, b2, thread_name):
    while True:
        rendezvous(thread_name)
        b1.wait()
        ko(thread_name)
        b2.wait()


THREADS = 10
sb1 = SimpleBarrier(THREADS)
sb2 = SimpleBarrier(THREADS)
threads = list()
for i in range(THREADS):
    t = Thread(barrier_example, sb1, sb2, 'Thread %d' % i)
    threads.append(t)

for t in threads:
    t.join()