# PPDS2022
Repository for the course Parallel programming and distributed systems at FEI STU 2022.
Each exercise has its own branch. The exercises are numbered 01 - 10.

#### Branches:
- 01 - Mutex
- 02 - Simple barrier
- 03 - Producer-consumer
- 04 - Lightswitch, Monitors-sensors
- 05 - Savages
- 06 - barbershop
- 07 - oops
- 08 - async programming

## Asynchronous programming

Exercise 8 looks at the impact of asynchronous programming on 
our python programs. The [course's website](https://uim.fei.stuba.sk/i-ppds/8-cvicenie-asynchronne-programovanie/) goes through examples
where it is a good idea to use asynchronous programming.

#### But what about file io ?

In our example we have two python scripts [synchronous.py](synchronous.py) and
[asynchronous.py](asynchronous.py). 

##### Synchronous

The first script is using an extended 
generator that is calling on 2 tasks. These tasks take files from a queue and
read the file's contents. They take turns and read them synchronously. The average
 time it takes to read the 4 sample text files is **35ms**.  

##### Asynchronous

The second script uses native coroutines and asyncio and aiofile libraries. The tasks 
1 and 2 work as coroutines. The average time is **41.5ms**.

#### Conclusion

As we have seen in on the [course's website](https://uim.fei.stuba.sk/i-ppds/8-cvicenie-asynchronne-programovanie/)
asynchronous programming can be used when the program is waiting on something else to
complete its action. The best example is using http requests. Since the program can't
continue without the needed data, it's best to fire multiple requests asynchronously
than waiting for them to execute one by one in serial fashion.

When reading multiple files on the other hand, the use of asynchronous programming
does not have a good impact. In fact the program may even slow down as it did in our case.
The whole file's content bust be read no matter what, so it is best to read it all at once.
Since we have one thread available, reading files asynchronously only takes more time,
because the processor jumps between reading multiple files.



