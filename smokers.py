from time import sleep
from random import randint
from fei.ppds import print, Semaphore, Mutex, Thread

class Shared(object):
    def __init__(self):
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)
        self.agentSem = Semaphore(1)

def make_cigarette():
    sleep(randint(0,10)/100)

def smoke():
    sleep(randint(0,10)/100)

def smoker_match(shared):
    while True:
        sleep(randint(0,10)/100)
        shared.paper.wait()
        shared.tobacco.wait()
        make_cigarette()
        shared.agentSem.signal()
        smoke('match')

def smoker_tobacco(shared):
    while True:
        sleep(randint(0,10)/100)
        shared.paper.wait()
        shared.match.wait()
        make_cigarette()
        shared.agentSem.signal()
        smoke()

def smoker_paper(shared):
    while True:
        sleep(randint(0,10)/100)
        shared.match.wait()
        shared.tobacco.wait()
        make_cigarette()
        shared.agentSem.signal()
        smoke()

def agent_1(shared):
    while True:
        sleep(randint(0, 10) / 100)
        shared.agentSem.wait()
        shared.paper.signal()
        shared.tobacco.signal()


def agent_2(shared):
    while True:
        sleep(randint(0,10)/100)
        shared.agentSem.wait()
        shared.paper.signal()
        shared.match.signal()

def agent_3(shared):
    while True:
        sleep(randint(0,10)/100)
        shared.agentSem.wait()
        shared.tobacco.signal()
        shared.match.signal()

def main():
    shared = Shared()

    smokers = []
    smokers.append(Thread(smoker_match, shared))
    smokers.append(Thread(smoker_tobacco, shared))
    smokers.append(Thread(smoker_paper, shared))

    agents = []
    agents.append(Thread(agent_1, shared))
    agents.append(Thread(agent_2, shared))
    agents.append(Thread(agent_3, shared))

    for t in smokers + agents:
        t.join()

if __name__ == '__main__':
    main()