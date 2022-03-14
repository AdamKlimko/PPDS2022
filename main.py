#!/usr/bin/env python
"""Exercise 4 of the course PPDS at FEI STU Bratislava

description
"""

# Generic/Built-in
from random import randint
from time import sleep

# Other Libs
from fei.ppds import Mutex, Semaphore, Thread, print, Event

__author__ = "Adam Klimko"
__version__ = "1.0.0"
__email__ = "xklimko@stuba.sk"


class CustomBarrier:
    def __init__(self, n):
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        self.event.wait()

    def signal(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.n:
            self.counter = 0
            self.event.signal()
        self.mutex.unlock()


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
        return self.counter

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()


def monitor(monitor_id, access_data, turnstile, ls_monitor, valid_data):
    valid_data.wait()

    while True:
        turnstile.wait()
        turnstile.signal()
        active_monitors_count = ls_monitor.lock(access_data)

        read_time = randint(40, 50) / 1000
        sleep(read_time)
        print('monitor: %02d | active monitors count= %02d | read time=  %02dms'
              %(monitor_id, active_monitors_count, read_time*1000))

        ls_monitor.unlock(access_data)


def sensor(sensor_id, rand_interval, access_data, turnstile, ls_sensor, valid_data):
    while True:
        turnstile.wait()
        sleep(randint(50, 60) / 1000)
        active_sensors_count = ls_sensor.lock(access_data)

        turnstile.signal()
        write_time = randint(rand_interval[0], rand_interval[1]) / 1000
        print('sensor:   %s | active sensors count=  %02d | write time= %02dms'
              %(sensor_id, active_sensors_count, write_time*1000))
        sleep(write_time)
        valid_data.signal()

        ls_sensor.unlock(access_data)


def main():
    barrier = CustomBarrier(3)
    access_data = Semaphore(1)
    turnstile = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_sensor = Lightswitch()

    monitors = [Thread(monitor, i, access_data, turnstile, ls_monitor, barrier) for i in range(8)]
    # sensors = [Thread(sensor, i, access_data, turnstile, ls_sensor, valid_data) for i in range(3)]
    sensor_p = Thread(sensor, 'P', [10, 20], access_data, turnstile, ls_sensor, barrier)
    sensor_t = Thread(sensor, 'T', [10, 20], access_data, turnstile, ls_sensor, barrier)
    sensor_h = Thread(sensor, 'H', [20, 25], access_data, turnstile, ls_sensor, barrier)


if __name__ == '__main__':
    main()