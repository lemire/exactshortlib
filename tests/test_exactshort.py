import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
  
from exactshort.exactshort import *
from exactshort.mostsignificantdigits import *


def largest_safe_divisor_power2_brute(z, M, R):
    Mp = M
    for w in range(1,R):
        while (z*w)//M != ((z//Mp)*w)//(M//Mp):
            Mp //= 2
        if Mp == 1:
            break
    return Mp

print("checking largest_safe_divisor_power2")
M = 256
for z in range(1,M):
    print(".", end="", flush=True)  
    for R in range(2,M,3):
        fast = largest_safe_divisor_power2(z,M,R)
        slow = largest_safe_divisor_power2_brute(z,M,R)
        if fast != slow:
            print("slow:", slow)
            print("fast:", fast)
            raise ValueError(str("bug z="+ str(z)+" M="+str(M)))

print("checking largest_safe_divisor_power2 ok")


def find_max_safe_brute(z, M):
    """ This returns the smallest value R such that
    (z*w) % M < M - w + 1 for M > 1.
    for w in [0,R)
    """
    for w in range(1,M):
        if (z*w)%M >= M-w+1:
            return w
    return M

print("checking find_max_safe")
M=256
z=39
for w in range(1,M):
    if (z*w)%M >= M-w+1:
        break
print(find_max_safe(z,M))
for M in range(10,500,1):
    print(".", end="", flush=True)  
    for z in range(1,M*2):
        fast = find_max_safe(z,M)
        slow = find_max_safe_brute(z,M)
        if fast != slow:
            print("slow:", slow)
            print("fast:", fast)
            raise ValueError(str("bug z="+ str(z)+" M="+str(M)))

print("checking find_max_safe ok")



from fractions import Fraction

def minimal_ratio_brute(z, M, R):
    best_ratio = Fraction((z%M),1)
    for w in range(1,R):
        v = Fraction(((z*w)%M),w)
        if v < best_ratio:
            best_ratio = v
    return best_ratio


########################################
########################################
print("checking minimal_ratio")

for M in range(200,300,10):
  print(".", end="", flush=True)  
  for R in range(125,M):
    for z in range(1,M):
        fast = minimal_ratio(z,M,R)
        slow = minimal_ratio_brute(z,M,R)
        if fast != slow:
            raise ValueError(str("bug z="+ str(z)+ " R ="+str(R)))

print("checking minimal_ratio ok")