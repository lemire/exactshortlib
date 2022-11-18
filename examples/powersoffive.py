import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


from exactshort.exactshort import *
from exactshort.mostsignificantdigits import *

def get_power5(q):
    """ For -342 to 308... computes a 128-bit truncated approximation."""
    if q < 0:
        power5 = 5 ** -q
        z = 0
        while( (1<<z) < power5) :
           z += 1
        if(q >= -27):
           b = z + 127
           c = 2 ** b // power5 + 1
           return c
        else:
            b = 2 * z + 2 * 64
            c = 2 ** b // power5 + 1
            # truncate
            while(c >= (1<<128)):
                c //= 2
            return c
    else:
        power5 = 5 ** q
        # move the most significant bit in position
        while(power5 < (1<<127)):
            power5 *= 2
        # *truncate*
        while(power5 >= (1<<128)):
            power5 //= 2
        return power5

#
# Given a large integer, we want that
#  ( w * z )
# has 52+3 = 55 bits of accuracy.
#
# To be able to ensure that, we want
#  ( w * z ) % 2^L
#
# to be less than than 2^L - w - 1
#
# Because any contribution from the truncated
# bits of z will be at most w - 1.
#
# What about equispaced minima ?
# Enough to check the first and last.
#

smallest = 1<<256
lower = 0
for q in range(-342,308+1):
    a,b = find_range_for_exact_most_significant_digits(get_power5(q),55,2)
    if b < smallest:
        smallest = b
    if lower < a:
        lower = a
print(hex(lower),hex(smallest))
