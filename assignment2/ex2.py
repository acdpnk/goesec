#!/usr/bin/env python3

# crack simple RSA encryption

import sys

e = 211
n = 67063
c = 19307

def isprime(number):
    i = 2
    while i <= number/2:
        if number % i == 0:
            return False
        i += 1
    return True

def factorize(number):
    factors = []
    i = 2
    while i <= number:
        if isprime(i) == True:
            while number % i == 0:
                factors.append(i)
                number = number / i
        i += 1
    return factors

factors = factorize(n)

if len(factors) != 2:
    print("nope")
    sys.exit(1)

(p,q) = factors
print("p = %s\nq = %s" % (p,q))

euler = (p - 1)*(q - 1)

d = pow(e,euler-1,n)

print("d = %s" % d)

m = pow(c,d,n)

print("m = %s" % m)

# test
print("test: %s" % (pow(pow(m,e,n),d,n) == m))

input()
