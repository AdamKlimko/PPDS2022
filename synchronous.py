import queue
import time


def task(name, work_queue):
    while not work_queue.empty():
        path = work_queue.get()
        print(f"Task {name} reading file: {path}")
        time_start = time.perf_counter()
        with open(path, 'r') as file:
            file.read()
        elapsed = time.perf_counter() - time_start
        print(f"Task {name} elapsed time: {elapsed*1000:0.4}ms")
        yield


def main():
    work_queue = queue.Queue()
    files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt"]

    for file in files:
        work_queue.put(file)

    tasks = [task("One", work_queue), task("Two", work_queue)]

    done = False
    start_time = time.perf_counter()
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)
            if len(tasks) == 0:
                done = True
    elapsed = time.perf_counter() - start_time
    print(f"\nTotal elapsed time: {elapsed*1000:0.4}ms")


if __name__ == "__main__":
    main()