from time import sleep
from random import randint
from fei.ppds import print, Semaphore, Mutex, Thread

N = 3
M = 20

class SimpleBarrier(object):
    def __init__(self, N):
        self.N = N
        self.cnt = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self, each = None, last = None):
        self.mutex.lock()
        self.cnt += 1
        if each:
            print(each)
        if self.cnt == self.N:
            if last:
                print(last)
            self.cnt = 0
            self.barrier.signal(self.N)
        self.mutex.unlock()
        self.barrier.wait()


class Shared(object):
    def __init__(self, m):
        self.servings = m
        self.mutex = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)
        self.barrier1 = SimpleBarrier(N)
        self.barrier2 = SimpleBarrier(N)


def eat():
    sleep(randint(50, 200) / 100)


def savage(i, shared):
    sleep(randint(1,100)/100)
    while True:
        shared.barrier1.wait()
        shared.barrier2.wait(each = f'savage {i}: waiting for dinner',
                             last = f'savage {i}: everybody eating')

        shared.mutex.lock()
        if shared.servings == 0:
            print(f'savage {i}: pot empty!')
            shared.empty_pot.signal()
            shared.full_pot.wait()
        print(f'savage {i}: take from pot')
        shared.servings -= 1
        shared.mutex.unlock()
        eat()


def cook(shared):
    while True:
        shared.empty_pot.wait()
        print('cook cooking')
        sleep(randint(50, 200) / 100)
        print(f'cook: put {M} servings in pot')
        shared.servings += M
        shared.full_pot.signal()


def main():
    shared = Shared(0)
    savages = []
    for i in range(N):
        savages.append(Thread(savage, i, shared))
    savages.append(Thread(cook, shared))

    for t in savages:
        t.join()


if __name__ == '__main__':
    main()