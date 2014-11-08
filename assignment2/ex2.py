#!/usr/bin/env python3

# cracking simple Diffie-Hellman Key Exchange

import sys

g = 10
n = 1783
X = 929
Y = 626

x = y = 0

while True:
    if X == (g**x)%n:
        print("x:\t%s" % x)
        break
    else:
        x += 1

while True:
    if Y == (g**y)%n:
        print("y:\t%s" % y)
        break
    else:
        y += 1

if not (X**y)%n == (Y**x)%n == (g**(x*y))%n:
    print("nope")
    sys.exit(1)

print("key:\t%s" % ((X**y)%n) )
