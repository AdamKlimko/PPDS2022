#!/usr/bin/env python
"""Exercise 6 of the course PPDS at FEI STU Bratislava
This exercise solves the barbershop synchronization problem.
One thread represents the barber and there is n threads
representing customers. The customers have to wait in a
waitroom for the barber to call them and give them a haircut.
We use a FIFO queue to make sure the customers get their hair
cut in the order they came to the waitroom.
"""

# Generic/Built-in
from random import randint
from time import sleep

# Other Libs
from fei.ppds import Mutex, Semaphore, Thread, print

__author__ = "Adam Klimko"
__version__ = "1.0.0"
__email__ = "xklimko@stuba.sk"


class Shared(object):
    """Shared class with variables shared between threads"""
    def __init__(self):
        self.customers = 0
        self.mutex = Mutex()
        self.queue = list()
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)
        self.customer_ready = Semaphore(0)


def get_haircut(i):
    print(f'Customer {i}: getting haircut')
    sleep(randint(5,10)/10)


def cut_hair():
    print(f'Barber: serving customer')
    sleep(randint(5,10)/10)


def customer(i, shared):
    """customer thread - the customers try to enter the barbershop
    if it's full they leave, if there is room they take a seat and
    wait for barber to serve them.
    """
    while True:
        # Customer comes to the barbershop
        shared.mutex.lock()
        if shared.customers >= MAX_CUSTOMERS:
            # If barbershop is full the customer unlocks lock and leaves
            # using continue to break out of while loop
            print(f'Customer {i}: barbershop full! Leaving')
            shared.mutex.unlock()
            sleep(randint(5,10)/5)
            continue
        # If there's room customer takes seat
        shared.customers += 1
        print(f'Customer {i}: taking seat in the waitroom')

        my_barber_ready = Semaphore(0)
        # Customer appends his own semaphore object that
        # makes him wait for the barber to call him.
        # This semaphore is put inside FIFO queue
        shared.queue.append(my_barber_ready)
        shared.mutex.unlock()

        # Rendezvous
        # Customer signals barber he is ready and waits for barber
        shared.customer_ready.signal()
        my_barber_ready.wait()

        get_haircut(i)

        shared.customer_done.signal()
        print(f'Customer {i}: is done')
        shared.barber_done.wait()

        shared.mutex.lock()
        shared.customers -= 1
        shared.mutex.unlock()

        print(f'Customer {i}: left the barbershop')
        sleep(randint(5,10)/5)


def barber(shared):
    """barber thread - the barber waits for the customers to come
    to him in the order they came to the barbershop. The barber
    takes one customer at a time and gives them a new fade haircut."""
    while True:
        print(f'Barber: waiting for customer')
        shared.customer_ready.wait()
        # Barber takes semaphore of the first customer in line
        # and signals to customer. pop(0) == pop(first)
        my_barber_ready = shared.queue.pop(0)
        my_barber_ready.signal()

        cut_hair()

        # Rendezvous
        # Barber waits for customer to signal done and signals done
        shared.customer_done.wait()
        shared.barber_done.signal()
        print(f'Barber: done')


# All customers in game
N_CUSTOMERS = 5
# Max customers inside barbershop
MAX_CUSTOMERS = 3


def main():
    shared = Shared()
    customers = [Thread(customer, i, shared) for i in range(1, N_CUSTOMERS+1)]
    barbers = [Thread(barber, shared) for i in range(1)]

    for t in customers + barbers:
        t.join()


if __name__ == '__main__':
    main()