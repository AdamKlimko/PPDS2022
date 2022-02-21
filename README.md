# PPDS2022
Repository for the course **Parallel programming and distributed systems** at FEI STU 2022.
Each exercise has its own branch. The excercises are numbered 01 - 10.
To run the scripts use **Python version 3.10**
---
## Lab 1
The goal of lab 1 is to implement 3 solutions for parallel incrementation of elements 
inside an array using Mutex. The problem is that when 2 threads are incrementing the
same array and using the same iterator, what MAY happen is that one thread gets to 
end of array first, increments the iterator(counter) so that counter = array length and at 
the same time the other thread tries to access value from array using that iterator.
In that case we get index out of range exception because the iterator is too large.
### Solution 1
The first solution although it works it kind of defeats the idea of parallel code
execution. Here we have mutex.lock() at the beginning of function and mutex.unlock()
at the very end, and they cover the whole while loop. So the first thread to acquire this
lock increments the whole array on its own. When the second thread comes there is nothing
left to do
### Solution 2
The function test() first implemented as: "while shared.counter < shared.end:".
But this solution does not let us put the mutex.unlock() method
in the required place which is where one thread gets to the end of array first.
We change it for an infinite while loop with if {end of array} then break. We wrap
the whole inside of while loop with mutex. This way the 2 threads wait on each other
with incrementing the counter and incrementing the single array values. They basically
take turns in executing the code.
### Solution 3
In the 3rd solution we surround only the if statement with mutex. This is enough for
preventing the threads from accessing the out of range index.