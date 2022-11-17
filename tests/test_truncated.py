import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
  
from exactshort.exactshort import *
from exactshort.mostsignificantdigits import *

def select_top_digits(value, digits, base):
    if digits <= 0:
        raise ValueError("number of digits should be a positive integer")
    while value < base ** (digits-1):
        value *= base
    while value >= base ** digits:
        value //=base
    return value

z = 314159265358979 # 15 digits

for base in [2,10]:
    for digits in range(15,16):
        mi,ma = find_range_for_exact_most_significant_digits(z,digits,base)
        x = ma-1
        if x>mi:
            assert(select_top_digits(z*x, digits, base) == select_top_digits((z+1)*x, digits, base))

print("Good!")