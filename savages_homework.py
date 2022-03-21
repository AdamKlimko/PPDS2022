from time import sleep
from random import randint
from fei.ppds import print, Semaphore, Mutex, Thread

N_SAVAGES = 3
N_COOKS = 3
N_SERVINGS = 3

class SimpleBarrier(object):
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
    def __init__(self, servings):
        self.servings = servings
        self.mutex = Mutex()
        self.mutex_cook = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)
        self.barrier1 = SimpleBarrier(N_SAVAGES)
        self.barrier2 = SimpleBarrier(N_SAVAGES)
        self.barrier_cooks1 = SimpleBarrier(N_COOKS)
        self.barrier_cooks2 = SimpleBarrier(N_COOKS)
        self.cooks_finished = 0


def eat():
    sleep(randint(50, 200) / 100)


def savage(i, shared):
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
    while True:
        shared.barrier_cooks1.wait()
        # shared.barrier_cooks2.wait()

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