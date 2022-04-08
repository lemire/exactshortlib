import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


def truncation_power(w,z,digits,base):
    """Computes the power k of b such that
    (w*z)//base**k is maximal and no larger than b**digits-1.
    Thus (w*z)//base**k * base**k is a truncated version of the
    product w*z using at most 'digits' digits.
    """
    if digits < 0:
      raise ValueError('digits must be non-negative')
    product = w * z
    if product == 0:
        return 0
    k = 0
    if digits >= 1 and product < base**(digits - 1):
        while product < base**(digits+k-1):
            k = k - 1
        return k
    while product > base**(digits+k) - 1:
        k = k + 1
    return k