import time
import multiprocessing
import math

'''

this is not a prime number generator or checker. its only usefulness is as a benchmarker

'''

start = time.time()

processesToCreate = 48  # doesn't always create that many processes
cyclesToRunPerThread = 10000000

# q = queue.Queue()

def prime(check):
    """ Warning: takes a long time with very large numbers
    
    Args:
        check (int): any int

    Returns:
        Boolean Value: True if prime False if not prime
    """
    if check == 2:  # If the input is 2, it is prime
        return True

    if check % 2 == 0 or check < 2:  # If the input is even or less than 2, it is not prime
        return False

    check = True  # Initialize a variable to store the result

    limit = int(
        math.sqrt(check))  # Find the square root of the input as the upper limit for checking divisibility

    for i in range(3, limit + 1, 2):  # Loop through all the odd numbers from 3 to the square root of the input

        if check % i == 0:  # If the input is divisible by any number, it is not prime
            check = False

            break

    return check  # Return the result


def process_function(number, cycles, n):
    i = number
    generated = 0

    while i < cycles:
        if prime(i):
            generated += 1
        i += 1
    end = time.time()
    # print(f"Process Index {number} completed in {(end - start):.2f} seconds.")
    # else:
    # print(generated)
    n.put(generated)


numbersGenerated = 0

if __name__ == '__main__':
    # multiprocessing.set_start_method('spawn')
    jobs = []
    manager = multiprocessing.Manager()
    n = manager.Queue()

    childNumber = 1

    divider = round(cyclesToRunPerThread / processesToCreate)

    while processesToCreate != 0:
        p = multiprocessing.Process(target=process_function,
                                    args=(divider * childNumber, divider * (childNumber + 1), n))
        jobs.append(p)
        p.start()
        processesToCreate -= 1
        # print(f"process {childNumber} started")
        childNumber += 1

    print("Process Creation completed.")

    for p in jobs:
        p.join()

    while not n.empty():
        item = n.get()
        # print(item)
        numbersGenerated += item

    print(f"\n{numbersGenerated} numbers generated")
    end = time.time()

    print(f"Time elapsed: {(end - start):.5f}\n")
