import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from random import randint
from time import sleep
from fei.ppds import Mutex, Semaphore, Thread


class Storage(object):
    """Shared storage object used for manipulation by producers and consumers"""
    def __init__(self, size):
        self.finished = False
        self.mutex = Mutex()
        self.stored_items = Semaphore(0)
        self.free_space = Semaphore(size)
        self.items_consumed = 0


def producer(storage):
    """Producer produces item and adds it into storage if there is space"""
    while True:
        # produce item
        sleep(randint(1,10) / 1000)
        storage.free_space.wait()
        if storage.finished:
            break
        storage.mutex.lock()
        # add item to storage
        sleep(randint(1, 10) / 1000)
        storage.mutex.unlock()
        storage.stored_items.signal()


def consumer(storage, time):
    """Consumer gets item from storage and consumes it"""
    while True:
        storage.stored_items.wait()
        if storage.finished:
            break
        storage.mutex.lock()
        # take item from storage
        sleep(randint(1, 10) / 1000)
        storage.mutex.unlock()
        # consume item
        sleep(time / 100)
        storage.items_consumed += 1


def draw_plot(x, y, z, x_title, y_title, z_title):
    ax = plt.axes(projection='3d')
    ax.plot_trisurf(x, y, z, linewidth=0.2,
                    antialiased=True, cmap='viridis', edgecolor='green')
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    ax.set_zlabel(z_title)
    plt.show()


def print_results(x, y, z):
    print(x)
    print(y)
    print(z)


def main():
    """used for experimenting with
    different parameters
    """
    x = []
    y = []
    z = []
    done = 0

    for consumer_count in range (10):

        for consume_time in range (0,50,5):

            items = []
            for i in range (10):

                storage = Storage(10)
                consumers = [Thread(consumer, storage, consume_time) for _ in range(consumer_count)]
                producers = [Thread(producer, storage) for _ in range(5)]
                sleep(1/10)
                storage.finished = True
                storage.stored_items.signal(100)
                storage.free_space.signal(100)
                [t.join() for t in consumers + producers]
                items.append(storage.items_consumed)

            items_avg = np.average(items)
            x.append(consumer_count)
            y.append(consume_time)
            z.append(items_avg*10)
            done += 1
            print(done.__str__() + '%')

    draw_plot(y, x, z, 'Consume time s/100', 'Consumers count',  'Items consumed per second')
    print_results(x, y, z)


if __name__ == '__main__':
    main()


