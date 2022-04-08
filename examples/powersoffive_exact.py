import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from exactshort.exactshort import *


def largest_divisor(z, M, R):
    r = minimal_ratio(z, M, R)
    Mp = 1
    while z % (Mp*2) <= r:
        Mp *= 2
    return Mp

m = 0
mi = 10000
for q in range(100,308+1):
    power = 5 ** q
    while power < (1<<64):
        power *= 2
    t = clog2(power//largest_divisor(power,1<<clog2(power),10**19))
    if t > m :
        m = t
        print(q,t)


print(m)