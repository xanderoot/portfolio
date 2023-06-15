import math


def isPrime(input) :
    """ Warning: takes a long time with very large numbers
    
    Args:
        input (int): any int

    Returns:
        Boolean Value: True if prime False if not prime
    """    
    if input == 2: # If the input is 2, it is prime
        return True

    if input % 2 == 0 or input < 2: # If the input is even or less than 2, it is not prime
        return False

    prime = True # Initialize a variable to store the result

    moduloLimit = int(math.sqrt(input)) # Find the square root of the input as the upper limit for checking divisibility

    for i in range(3,moduloLimit + 1, 2) : # Loop through all the odd numbers from 3 to the square root of the input

        if input % i == 0: # If the input is divisible by any number, it is not prime
            prime = False
            break    

    return prime # Return the result


def repeatingCycleLength(p): 
    """
    Args:
        p (int): a prime number

    Returns:
        int: length of the repeating portion of the fraction
        
    """
    n = 1 # start with n = 1
    while True: # loop until we find a valid n
        if n > p - 1: # stop the loop if n exceeds p - 1
            return 0 # return None to indicate no cycle
        if (10**n - 1) % p == 0: # check if 10^n - 1 is divisible by p
            return n # return n as the length of the cycle
        else:
            n += 1 # increment n by 1 and try again

