from fei.ppds import Mutex, Thread
from collections import Counter


class Shared:
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.elms = [0] * end


def test(shared, mutex):
    while 1:
        mutex.lock()
        if shared.counter >= shared.end:
            mutex.unlock()
            break
        mutex.unlock()
        shared.elms[shared.counter] += 1
        shared.counter += 1


mutex = Mutex()

shared = Shared(1_000_000)
thread1 = Thread(test, shared, mutex)
thread2 = Thread(test, shared, mutex)

thread1.join()
thread2.join()

counter = Counter(shared.elms)
print(counter.most_common())
