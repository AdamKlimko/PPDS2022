from fei.ppds import Mutex, Thread
from collections import Counter


class Shared:
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.elms = [0] * end


def test(shared, mutex):
    while 1:
        # thread acquires lock
        mutex.lock()
        if shared.counter >= shared.end:
            # first thread to reach array end frees lock and breaks out of while loop
            mutex.unlock()
            break
        shared.elms[shared.counter] += 1
        shared.counter += 1
        # thread frees lock
        mutex.unlock()


mutex = Mutex()

shared = Shared(100_000_000)
thread1 = Thread(test, shared, mutex)
thread2 = Thread(test, shared, mutex)

thread1.join()
thread2.join()

counter = Counter(shared.elms)
print(counter.most_common())
