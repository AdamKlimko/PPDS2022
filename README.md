# PPDS2022
Repository for the course Parallel programming and distributed systems at FEI STU 2022.
Each exercise has its own branch. The exercises are numbered 01 - 10.

#### Branches:
- 01 - Mutex
- 02 - Simple barrier
- 03 - Producer-consumer
- 04 - Lightswitch, Monitors-sensors
- 05 - Savages

## Feasting savages

### 1 Find out what combination of sync issues this is
This is a problem similar to the producer consumer problem. We have a number
of savages trying to eat and a number cooks who cook dinner for the savages.
We also have number of servings(in pot) which is the main shared resource that 
must be handled carefully when manipulating. Basically we need a mutex
to wrap around the read/write functionality manipulating the servings.
Then we need a barrier for the cooks to wait for each other to finish.
The cooks also need to wait for the pot to empty which is implemented as
a simple semaphore.

### 2 Write the pseudocode of the solution

    def init():
        mutex := Mutex()
        mutex_cook: = Mutex()
        servings := 0
        fullPot := Semaphore(0)
        emptyPot := Semaphore(0)
    
        barrier1 := SimpleBarrier()
        barrier2 := SimpleBarrier()
        barrier_cook := SimpleBarrier()
        cooks_finished := 0
    
        savages := [create_and_run_thread(savage, i) for i in range(N)]
        cooks := [create_and_run_thread(cook, i) for i in range(N)]

    
    def getServingFromPot(savage_id):
        print(f"savage {savage_id}: take serving from pot")
        servings := servings - 1
    
    def savage(savage_id):
        while True:
            barrier1.wait(f"savage{savage_id}: I came to dinner")
            barrier2.wait(f"savage{savage_id}: Everyone's here, we start feasting")
    
            mutex.lock()
            print(f"savage {savage_id}: servings left in pot = {servings}))
            if servings == 0:
                print(f"savage {savage_id}: pot is empty!")
                emptyPot.signal(N_COOKS)
                fullPot.wait()
            getServingFromPot(savage_id)
            mutex.unlock()

            print(f"savage {savage_id}: eating")

    
    def cook(cook_id):
        while True:
            barrier_cooks.wait() 
            empty_pot.wait()

            print(f'cook {i}: cooking')
            print(f'cook {i}: finished cooking')
    
            mutex_cook.lock()

            cooks_finished += 1
            if shared.cooks_finished == N_COOKS:
                print(f'cook {i}: put {N_SERVINGS} servings in pot')
                servings += N_SERVINGS
                fullPot.signal()
                cooks_finished := 0

            mutex_cook.unlock()

### 3 Place suitable statements to verify the functionality of the model
We add statements to map all important actions such as cook - cooking,finishing
or savage - waiting for dinner, taking from pot.

![img.png](img.png)

### 4 Choose the appropriate characteristics on which the model is based (numbers of threads, timings of activities, values of other variables).
See the code [savages_homework.py](savages_homework.py)