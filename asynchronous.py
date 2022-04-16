import asyncio
import time
import aiofile


async def task(name, work_queue):
    while not work_queue.empty():
        path = await work_queue.get()
        print(f"Task {name} reading file: {path}")
        time_start = time.perf_counter()
        async with aiofile.async_open(path, mode='r') as file:
            await file.read()
        elapsed = time.perf_counter() - time_start
        print(f"Task {name} elapsed time: {elapsed*1000:0.4}ms")


async def main():
    work_queue = asyncio.Queue()
    paths = ["file3.txt", "file2.txt", "file1.txt", "file4.txt"]

    for path in paths:
        await work_queue.put(path)

    start_time = time.perf_counter()
    await asyncio.gather(
        task("One", work_queue),
        task("Two", work_queue)
    )
    elapsed = time.perf_counter() - start_time
    print(f"\nTotal elapsed time: {elapsed*1000:0.4}ms")


if __name__ == "__main__":
    asyncio.run(main())