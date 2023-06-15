import threading
import commonFunctions
import time
import queue

start = time.time()

threadsToCreate = 100
cyclesToRunPerThread = 10000000
#q = queue.Queue()
n = queue.Queue()

def thread_function(number,maxToRun):
    
    i = number
    totalGenerated = 0
    
    #local_time = time.localtime()
    #print(f"Thread {number} Started at {time.strftime('%H:%M:%S', local_time)}")
    
    while i < maxToRun:
        if commonFunctions.isPrime(i): 
            #q.put(i)
            totalGenerated += 1
        i += threadsToCreate
    n.put(totalGenerated)
    print(totalGenerated)

threads = []
numbersGenerated = 0
primes = []


for i in range(threadsToCreate):
    x = threading.Thread(target=thread_function, args=(i,cyclesToRunPerThread,))
    threads.append(x)
    x.start()
    
for x in threads: 
    x.join()
    
#while not q.empty():
   # item = q.get()
    #primes.append(item)

while not n.empty():
    item = n.get()
    numbersGenerated += item
    
#primes.sort()
    
print(f"{numbersGenerated} numbers generated")
#print(f"{primes}")

end = time.time()

print(f"Time elapsed: {(end - start):.5f}")