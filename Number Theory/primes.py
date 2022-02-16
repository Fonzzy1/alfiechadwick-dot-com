import numpy as np
import multiprocessing

n = 1000000
c = 16 

split = round(n/c)

def determine_prime(x):
    for i in range(2,round(x/2)):
        if x % i == 0:
            return False
    print(x)

def split_jobs(min,max):
    for x in range(min,max):
        determine_prime(x)

with multiprocessing.Manager() as manager:
    processes = []
    for i in range(1,c):
         p = multiprocessing.Process(target=split_jobs, args=(split*(i-1),split*i))
         processes.append(p)
         p.start()
        
    for process in processes:
         process.join()

