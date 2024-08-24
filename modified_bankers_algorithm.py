import threading
import time

#-----------------Modified Banker's algorithm--------------#

# this process takes long time
def process0():
    print("Process 0 start")
    A = 5  # do something with resource A

    # after use of resource A, release immediately
    print("p0 releasing 4 A")
    free[0][0] += 4
    updateWork(0)

    # simulate process running for 10 seconds
    time.sleep(10)

    # set safe to True and update work
    safe[0] = True
    updateWork(0)
    print("Process 0 finish\n")

# this process finishes quick
def process1():
    print("Process 1 start")
    A = 1  # do something with resource A

    # simulate process running for 1 second
    time.sleep(1)

    safe[1] = True
    updateWork(1)
    print("Process 1 finish\n")

# this function updates the work
def updateWork(i):
    global work, safe, totalResources
    worktemp = list(work)

    # if process is safe then clear and free the resources
    if safe[i] == True:
        next = [allocation[i][k] - free[i][k] for k in range(len(free[i]))]
    # else only free certain resources
    else:
        next = free[i]

    work = []
    # check that resources released are not more than total resources
    for k in range(len(next)):
        if worktemp[k] + next[k] > totalResources[k]:
            work.append(totalResources[k])
        else:
            work.append(worktemp[k] + next[k])


def main():

    # max               A B C 
    maximum =         [[4,2,2], # p0
                       [5,2,4]] # p1

    # allocation (global to share among the processes)
    global allocation
    #                   A B C
    allocation =      [[4,1,2], # p0
                       [4,2,4]] # p1

    # total resources
    global totalResources
    totalResources =   [5,4,5]

    # creating threads
    p0 = threading.Thread(target=process0)
    p1 = threading.Thread(target=process1)

    # calculate need
    need = [[0 for i in range(len(maximum[0]))] for j in range(len(maximum))] 
    for i in range(len(maximum)):
        for j in range(len(maximum[0])):
            need[i][j] = maximum[i][j] - allocation[i][j]

    # calculate total allocation
    totalAllocation = []
    sum = 0
    for i in range(len(allocation[0])):
        for j in range(len(allocation)):
            sum += allocation[j][i]
        totalAllocation.append(sum)
        sum = 0

    # calculate available
    available = []
    for i in range(len(totalAllocation)):
        available.append(totalResources[i] - totalAllocation[i])
        if available[i] < 0: available[i] = 0

    # initialize work, safe, and started arrays
    global work, safe, started, free
    work = list(available)
    safe = [False] * len(allocation)
    started = [False] * len(allocation)  # Track if a thread has been started

    # free is the number of resources taken by a process at a certain time (during process runtime)
    free = [[0 for i in range(len(maximum[0]))] for j in range(len(maximum))]

    print("maximum: \n" + str(maximum))
    print("allocation: \n" + str(allocation))
    print("total allocation: \n" + str(totalAllocation))
    print("total resources: \n" + str(totalResources))
    print("need: \n" + str(need))
    print("available and work:")
    print(available)
    print(work)
    print("safe: \n" + str(safe) + "\n")

    # find sequence
    i = 0  # start from process 0
    sequence = []  # sequence of execution
    safeCount = 0  # counter for safe processes

    start = time.time()  # start timer

    # start the processes
    while safeCount < len(safe):

        # check if need is less than work, the process is not safe, and not started
        if needLessThanWork(need, work, i) and not safe[i] and not started[i]:
            # start processes
            if i == 0: p0.start()
            if i == 1: p1.start()

            started[i] = True  # Mark the process as started
            sequence.append(i)
            safeCount += 1  # increment number of safe processes

            print("\nwork = " + str(work) + "\n")

        # check the next process
        i = (i + 1) % len(need)

    if safeCount == len(allocation):
        # join the processes
        p0.join()
        p1.join()

    totalTime = time.time() - start  # get time

    print("sequence: " + str(sequence))
    print("total time: " + str(totalTime))


# check if need is less than work
def needLessThanWork(need, work, i):
    for k in range(len(work)):
        if need[i][k] > work[k] and work[k] >= 0:
            return False
    return True


if __name__ == '__main__':
    main()
