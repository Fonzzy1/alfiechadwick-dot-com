max_value = 1000000

i = 4

primes = [2,3]

while i <= max_value:
    factors = []
    for p in primes:
        if i % p == 0:
            factors.append(p)
    if len(factors) == 0:
        primes.append(i)
        print(i)
    i+=1


with open('primes - '+ str(max_value), 'w') as f:
    for item in primes:
        f.write("%s\n" % item)


