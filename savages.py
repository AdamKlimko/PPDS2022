from time import sleep
from random import randint
from fei.ppds import print, Semaphore, Mutex, Thread

N = 3
M = 20

class SimpleBarrier(object):
    def __init__(self):
        self.N = N
        self.cnt = M
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self, each = None, last = None):
        self.mutex.lock()
        self.cnt += 1
        self.mutex.unlock()

class Shared():
    def __init__(self, m):
        self.servings = m
        self.mutex = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)


def eat(i):
    # print(f'savage {i}: start eat')
    sleep(randint(50, 200) / 100)


def savage(i, shared):
    sleep(randint(1,100)/100)
    while True:
        shared.b1.wait()
        shared.b2.wait()

        shared.mutex.lock()
        if shared.servings == 0:
            print(f'savage {i}: pot empty!')
            shared.empty_pot.signal()
            shared.full_pot.wait()
        print(f'savage {i}: take from pot')
        shared.servings -= 1
        shared.mutex.unlock()
        eat(i)


def cook(shared):
    while True:
        shared.empty_pot.wait()
        print('cook cooking')
        sleep(randint(50, 200) / 100)
        print(f'cook: {M} servings --> pot')
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