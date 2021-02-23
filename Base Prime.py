import time
start = time.process_time()

a=1
while a < 10000:
 count = 0 
 num = 1
 while num < a:

 # To take input from the user
 #num = int(input("Enter a number: "))

 # prime numbers are greater than 1
  if num > 1:
   # check for factors
    for i in range(2,num):
        if (num % i) == 0:
            break
    else:
      count += 1
       
       
  num += 1
 
 print(num,count)
 
 a += 1
 
 
print(time.process_time() - start)

 
