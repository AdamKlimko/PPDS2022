from random import randint
from time import sleep
from fei.ppds import Mutex, Semaphore, Thread


class Storage(object):
    def __init__(self, size):
        self.finished = False
        self.mutex = Mutex()
        self.stored_items = Semaphore(0)
        self.free_space = Semaphore(size)


def producer(storage):
    while True:
        print('producing')
        sleep(randint(1,10)/10)
        storage.free_space.wait()
        if storage.finished:
            break
        storage.mutex.lock()
        sleep(randint(1,10)/10)
        storage.mutex.unlock()
        storage.stored_items.signal()


def consumer(storage):
    while True:
        storage.stored_items.wait()
        if storage.finished:
            break
        storage.mutex.lock()
        sleep(randint(1, 10) / 10)
        storage.mutex.unlock()
        print('consuming')
        sleep(randint(1, 10) / 10)


def main():
    s = Storage(10)
    c = [Thread(consumer, s) for _ in range (2)]
    p = [Thread(producer, s) for _ in range(5)]

    sleep(10)
    s.finished = True
    print('thread waiting to finish')
    s.stored_items.signal(100)
    s.free_space.signal(100)
    [t.join() for t in c+p]
    print('thread finished')


if __name__ == '__main__':
    main()
