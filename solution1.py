from fei.ppds import Mutex, Thread
from collections import Counter


class Shared:
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.elms = [0] * end


def test(shared, mutex):
    # thread acquires lock
    mutex.lock()
    while shared.counter < shared.end:
        shared.elms[shared.counter] += 1
        shared.counter += 1
    # thread frees lock
    mutex.unlock()


# test multiple times since parallel programming problems occur randomly
def try_ten_times():
    for i in range(10):
        mutex = Mutex()
        shared = Shared(1_000_000)

        thread1 = Thread(test, shared, mutex)
        thread2 = Thread(test, shared, mutex)

        thread1.join()
        thread2.join()

        counter = Counter(shared.elms)
        print(counter.most_common())


try_ten_times()
