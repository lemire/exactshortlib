import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from exactshort.remainder import *

from fractions import Fraction

def minimal_ratio(z, M, R):
    """ We want to compute the minimum of (z*w)%M / w
    over w in [1,R-1].
    """
    minima = find_min_max_reverse_skip(z, M, R)[0]
    mi = Fraction((z*minima[0])%M, minima[0])
    for w in minima:
        if w == 0:
            continue
        v =  Fraction((z*w)%M, w)
        if v < mi:
            mi = v
    return mi


def largest_safe_divisor_power2(z, M, R):
    """ Given that M is a power of two,
    this returns the largest divisor  M' so that
    (z//M' * w) // (M-M') =  (z * w) // M for all w in [0,R). 
    This function always succeeds but it may return 1. """
    if M <= 0:
        raise ValueError('M must be positive')
    if M & (M-1) != 0:
        raise ValueError('M must be a power of two')
    if z < 0:
        raise ValueError('z must be positive')
    if (z % M) == 0:
        return M
    mr = minimal_ratio(z, M, R)
    Mp = 1
    while ( z % (2*Mp) <= mr ) and (Mp < M):
        Mp *= 2
    return Mp

def is_power_of_ten(z):
    while(z>1):
        if z%10 != 0: 
            return False
        z //= 10
    return True

def is_power_of_base(z, base):
    while(z>1):
        if z%base != 0: 
            return False
        z //= base
    return True


def minimal_ratio_range(z, M, A, B):
    """ We want to compute the minimum of (z*w)%M / w
    over w in [A,B].
    """
    if A > B:
        raise ValueError('A should be smaller than B')    
    minima = find_min_max_in_range_reverse_skip(z, M, A, B)[0]
    mi = Fraction((z*minima[0])%M, minima[0])
    for w in minima:
        if w == 0:
            continue
        v =  Fraction((z*w)%M, w)
        if v < mi:
            mi = v
    return mi


def largest_safe_divisor_range(z, M, A, B, base):
    """ Given that M is a power of base,
    this returns the largest divisor  M' so that
    (z//M' * w) // (M/M') =  (z * w) // M for all w in [A,B]. 
    This function always succeeds but it may return 1. """
    if M <= 0:
        raise ValueError('M must be positive')
    if not(is_power_of_base(M,base)):
        raise ValueError('M must be a power of ten')
    if z < 0:
        raise ValueError('z must be positive')
    # We want to compute the minimum of (z*w)%M / w
    # over w in [A,B].
    mr = minimal_ratio_range(z, M, A, B)
    Mp = 1
    while ( z % (base*Mp) <= mr ) and (Mp < M):
        Mp *= base
    return Mp

def largest_safe_divisor_power10(z, M, R):
    """ Given that M is a power of ten,
    this returns the largest divisor  M' so that
    (z//M' * w) // (M-M') =  (z * w) // M for all w in [0,R). 
    This function always succeeds but it may return 1. """
    if M <= 0:
        raise ValueError('M must be positive')
    if not(is_power_of_ten(M)):
        raise ValueError('M must be a power of ten')
    if z < 0:
        raise ValueError('z must be positive')
    if (z % M) == 0:
        return M
    mr = minimal_ratio(z, M, R)
    Mp = 1
    while ( z % (10*Mp) <= mr ) and (Mp < M):
        Mp *= 10
    return Mp

def largest_safe_divisor_power(z, M, R, base):
    """ Given that M is a power of base,
    this returns the largest divisor  M' so that
    (z//M' * w) // (M-M') =  (z * w) // M for all w in [0,R). 
    This function always succeeds but it may return 1. """
    if M <= 0:
        raise ValueError('M must be positive')
    if not(is_power_of_base(M,base)):
        raise ValueError('M must be a power of ten')
    if z < 0:
        raise ValueError('z must be positive')
    if (z % M) == 0:
        return M
    mr = minimal_ratio(z, M, R)
    Mp = 1
    while ( z % (base*Mp) <= mr ) and (Mp < M):
        Mp *= base
    return Mp

def find_max_safe(z, M):
    """ This returns the maximum value R such that
    (z*w) % M < M - w + 1 for M > 1.
    for w in [0,R) up to R= M/gcd(M,z).

    If we have a maximum where 
    (z*w) % M < M - w + 1
    then all previous values are fine because
    (z*w) % M will be smaller and M - w + 1 larger.

    """
    if M <= 0:
        raise ValueError('M must be positive')
    if z < 0:
        raise ValueError('z must be positive')
    if (z % M) == 0:
        return M
    off = 0 # which cycle
    while off<M:
      w = 1
      a = z % M
      if (z)%M >= M - 1 - off + 1:
        return 1 + off
      alpha = 1
      b = z % M
      beta = 1
      while True:
        v = (a + b) % M
        if v < a:
            t = a // (M-b)
            if a % (M-b) == 0:
                t -= 1
                a = (a + t*b) %M
                w = w + alpha + t * beta
                break
            w = w + alpha + (t-1) * beta
            alpha = w
            a = (a + t*b) %M
        else: # elif v>b:
            t = (M-b-1)//a
            #
            p = w + beta
            if ( (z * p)%M >= M - (p + off - 1)):
                return p + off
            # last is at w + beta + (t-1) * alpha
            p = w + beta + (t-1) * alpha
            if ( (z * p)%M >= M - (p + off - 1)):
                # do a binary search, O(t)
                def test(x):
                    """ return true if we exceed!"""
                    ptmp =  w + beta + (x-1) * alpha
                    return (z * ptmp)%M >= M - (ptmp + off - 1)
                low = 1
                high = t
                while low + 1 < high:
                    midpoint = (low + high) // 2
                    if test(midpoint):
                        high = midpoint
                    else:
                        low = midpoint
                return w + beta + (high-1) * alpha + off
            #
            w = w + beta + (t-1) * alpha
            beta = w
            b = (b + t*a) %M
      if off == 0:
          # b < M - w + 1
          # w < M - b + 1
          cycle_length = M//math.gcd(M,z)
          # We possible can skip quite a number of iterations
          off = (M - b + 1) // cycle_length * cycle_length
          if off == 0:
              off += cycle_length
      else:
          off += M//math.gcd(M,z)
    return M

def clog10(z):
    """ This returns the smallest integer L such that (z//10**L)==0.
    It returns the number of decimal digits required to represent z. """
    assert z >= 0
    L = 0
    while((z//10**L)>0):
        L = L + 1
    return L


def clog2(z):
    """ This returns the smallest integer L such that (z>>L)==0. 
    It returns the number of bits required to represent z. """
    assert z >= 0
    L = 0
    while((z>>L)>0):
        L = L + 1
    return L




def find_range_for_exact_most_significant_digits(z, digits, base):
    """ 
    Find the interval of values w such that
    the most significant 'digits' (z*w) are exact even if z is a truncated value.
    The lower bound is included, the upper bound is not included. Might return None
    if there is no solution.
    """
    if digits <= 0:
        raise ValueError('digits must be positive')
    # lower bound: w*z > base**(digits-1)
    lower_bound = (base**(digits-1) + z - 1) // z
    assert lower_bound * z >= base**(digits-1)
    # upper bound: 
    k = 0
    while True:
        A = (base**(digits+k-1) + z - 1) // z
        assert (A-1) * z < base**(digits+k-1)
        assert A * z >= base**(digits+k-1)
        B = (base**(digits+k)) // z
        if B * z == base**(digits+k):
            B -= 1
        assert B * z < base**(digits+k)
        if(B<A):
            k = k + 1
            continue
        assert B >= A
        M = base ** k
        assert (A * z)//M >= base**(digits-1)
        assert (B * z)//M < base**(digits)
        minima,maxima = find_min_max_in_range_annotated(z,M,A,B)
        currentmax = 0
        for beta,times,gap in maxima:
            if((beta*z)%M>= M-beta+1):
                # seek the first break
                upper_bound=beta
                if times > 0:
                    deltagap = (beta*z)%M - (M-beta+1)
                    deltabottom = gap +((gap*z)%M)
                    mt = deltagap//deltabottom
                    upper_bound = beta - deltagap//deltabottom * gap
                    assert ((upper_bound*z)%M>= M-upper_bound+1)
                if upper_bound <= lower_bound:
                    return None
                assert ((upper_bound*z)%M>= M-upper_bound+1)
                return (lower_bound,upper_bound)
        ###
        # We may also fail when M-w+1<=0.
        if M+1 <= B:
            upper_bound = M + 1
            if upper_bound <= lower_bound:
                return None
            return (lower_bound,upper_bound)
        k = k + 1


def short_multiplier_for_exact_most_significant_digits(z, R, digits, base):
    """ find a short multiplier, find the a short multiplier version of `z`, such that we have `digits` accurate digits in base `base` when computing `w*z` for `w` in  `[0,R)`."""
    if digits <= 0:
        raise ValueError('digits must be positive')
    running_short_divisor = None
    # upper bound: 
    k = 0
    while True:
        A = (base**(digits+k-1) + z - 1) // z
        assert (A-1) * z < base**(digits+k-1)
        assert A * z >= base**(digits+k-1)
        B = (base**(digits+k)) // z 
        assert B * z < base**(digits+k)
        if A > R - 1:
            break
        if B > R - 1:
            B = R - 1
        if(B<A):
            k = k + 1
            continue
        M = base ** k
        assert (A * z)//M >= base**(digits-1)
        assert (B * z)//M < base**(digits)
        short_divisor = largest_safe_divisor_range(z, M, A, B, base)
        #for w in range(A, B+1):
        #    assert (z//short_divisor * w) // (M//short_divisor) == (z*w)//M
        if running_short_divisor is None:
            running_short_divisor = short_divisor
        # We need to pick the smallest 'short_divisor'
        if short_divisor < running_short_divisor:
            running_short_divisor = short_divisor
        k = k + 1
    if running_short_divisor is None:
        return z # anomaly
    return z//running_short_divisor
