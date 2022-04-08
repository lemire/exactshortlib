

import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
  
from exactshort.exactshort import *
from exactshort.mostsignificantdigits import *

z=5
M=8
A=4
B=6
base=2

short_divisor = largest_safe_divisor_range(z, M, A, B, base)
for w in range(A, B+1):
    assert (z//short_divisor * w) // (M//short_divisor) == (z*w)//M


for base in [2,10]:
    M = base
    maxdigits = 1
    while M < 512:
        M *= base
        maxdigits += 1
    for digits in range(1,maxdigits):
        print(".", end="", flush=True)  
        for z in range(2,M-1):
            for R in range(10, 100, 10):
                short_z = short_multiplier_for_exact_most_significant_digits(z, R, digits, base)
                too_short_z = short_z // base
                badcheck = False
                for w in range(0,R):
                    k = truncation_power(w,z,digits,base)
                    kp = truncation_power(w,short_z,digits,base)
                    version1 = (w*z) // base**k
                    version2 = (w*short_z)// base**kp
                    if version1 != version2 :
                        print("version1 = ", version1)
                        print("version2 = ", version2)
                        print("w=", w, "z = ", z, "short_z = ", short_z, "R =", R)
                        print("k=", k)
                        print("kp=", kp)
                        print("digits=", digits)
                        assert version1 == version2
    print()