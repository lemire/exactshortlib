import math


def global_max_min(z, M, R):  
    """ We  want to find the maximum and the minimum of of (w * z) % M 
    for w = 1, ..., R-1
    """
    if M <= 0:
        raise ValueError('M must be positive')
    if z < 0:
        raise ValueError('z must be positive')
    if (z % M) == 0:
       raise ValueError('z should not be a multiple of M')
    w = 1
    a = z % M
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
                w = w + alpha + (t-1) * beta
                break
            w = w + alpha + (t-1) * beta
            alpha = w
            a = (a + t*b) %M
        else: # elif v>b:
            t = (M-b-1)//a
            w = w + beta + (t-1) * alpha
            beta = w
            b = (b + t*a) %M
    return (a,b)

def gaps(z, M):  
    """ We  want to find the locations of all of the minimum and
    maximum of (w * z) % M for w = 1, ..., M/gcd(z,M)
    """
    if M <= 0:
        raise ValueError('M must be positive')
    if z < 0:
        raise ValueError('z must be positive')
    if (z % M) == 0:
       raise ValueError('z should not be a multiple of M')
    w = 1
    lambdal = []
    a = z % M
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
                lambdal.append(w)
                w = w + alpha + (t-1) * beta
                break
            lambdal.append(w)
            w = w + alpha + (t-1) * beta
            alpha = w
            a = (a + t*b) %M
        else: # elif v>b:
            t = (M-b-1)//a
            lambdal.append(w)
            w = w + beta + (t-1) * alpha
            beta = w
            b = (b + t*a) %M
    return lambdal

def find_min_max(z, M, b):
    """ We want to find the location of all of the minimum and
    maximum of (w * z + b) %M for w = 1...
    """
    if M <= 0:
      raise ValueError('M must be positive')
    facts = gaps(z,M)
    # When w = 0, we have that (w * z + b) %M = b % M
    mi = (z+b)%M
    ma = (z+b)%M
    fact_index = 0
    minima = [1]
    maxima = [1]
    w = 1
    while True:
        offindex = facts[fact_index]
        candidate = (z * (w + offindex) + b)%M
        if w + offindex > M:
            break
        if candidate < mi:
            # we have a new minimum.
            w += offindex
            minima.append(w)
            mi = candidate
        elif candidate > ma:
            # we have a new maximum.
            w += offindex
            maxima.append(w)
            ma = candidate
        else:
            fact_index += 1
            if fact_index == len(facts):
                break
    return (minima,maxima)

def find_min_max_skip(z, M, b):
    """ We want to find the location of all of the minimum and
    maximum of (w * z + b) %M for w = 1... But we skip intermediates
    in sequences of equispaced extrema.
    """
    if M <= 0:
      raise ValueError('M must be positive')
    facts = gaps(z,M)
    # When w = 0, we have that (w * z + b) %M = b % M
    mi = (z+b)%M
    ma = (z+b)%M
    fact_index = 0
    minima = [1]
    maxima = [1]
    w = 1
    while True:
        offindex = facts[fact_index]
        candidate = (z * (w + offindex) + b)%M
        if w + offindex > M:
            break
        if candidate < mi:
            # we have a new minimum.
            w += offindex
            minima.append(w)
            mi = candidate
            #
            off = (z * offindex)%M
            times = mi // (M-off)
            if times > 0:
               mi = (mi + times*off)%M
               w += times * offindex
               minima.append(w)
        elif candidate > ma:
            # we have a new maximum.
            w += offindex
            maxima.append(w)
            ma = candidate
            #
            off = (z * offindex)%M
            times = (M-1-ma) // off
            if times > 0:
               ma = ma + times*off
               w += times * offindex
               maxima.append(w)
        else:
            fact_index += 1
            if fact_index == len(facts):
                break
    return (minima,maxima)

def find_min_max_skip(z, M, b):
    """ We want to find the location of all of the minimum and
    maximum of (w * z + b) %M for w = 1... But we skip intermediates
    in sequences of equispaced extrema.
    """
    if M <= 0:
      raise ValueError('M must be positive')
    facts = gaps(z,M)
    # When w = 0, we have that (w * z + b) %M = b % M
    mi = (z+b)%M
    ma = (z+b)%M
    fact_index = 0
    minima = [1]
    maxima = [1]
    w = 1
    while True:
        offindex = facts[fact_index]
        candidate = (z * (w + offindex) + b)%M
        if w + offindex > M:
            break
        if candidate < mi:
            # we have a new minimum.
            w += offindex
            minima.append(w)
            mi = candidate
            #
            off = (z * offindex)%M
            times = mi // (M-off)
            if times > 0:
               mi = (mi + times*off)%M
               w += times * offindex
               minima.append(w)
        elif candidate > ma:
            # we have a new maximum.
            w += offindex
            maxima.append(w)
            ma = candidate
            #
            off = (z * offindex)%M
            times = (M-1-ma) // off
            if times > 0:
               ma = ma + times*off
               w += times * offindex
               maxima.append(w)
        else:
            fact_index += 1
            if fact_index == len(facts):
                break
    return (minima,maxima)



def find_min_max_in_range_annotated(z, M, A, B):
    """ We want to find the location of all of the minimum and
    maximum of (w * z) %M for w = A...B But we anotate intermediates
    in sequences of equispaced extrema.
    """
    if B < A:
      raise ValueError('A must be smaller or equal than B')
    if M <= 0:
      raise ValueError('M must be positive')
    minima = [(A,0,0)]
    maxima = [(A,0,0)]
    if z%M == 0:
        # If z is a multiple of M, then (w * z) %M == 0 for all w
        return (minima,maxima)
    facts = gaps(z,M)
    # When w = 0, we have that (w * z + b) %M = b % M
    mi = (z*A)%M
    ma = (z*A)%M
    fact_index = 0
    b = A * z
    w = 0
    while True:
        offindex = facts[fact_index]
        candidate = (z * (w + offindex) + b)%M
        if w + offindex > B-A:
            break
        if candidate < mi:
            # we have a new minimum.
            w += offindex
            mi = candidate
            ### Move forward as far as it will go
            basis = (z * w + b)%M
            off = (z*offindex)%M
            times = basis // (M-off)
            if A+w+times*offindex>B:
                times = (B - A - w)//offindex
            w += offindex * times
            mi = (z * w + b)%M
            minima.append((w+A, times, offindex))
        elif candidate > ma:
            # we have a new maximum.
            w += offindex
            ma = candidate
            ### Move forward as far as it will go
            basis = (z * w + b)%M
            off = (z*offindex)%M
            times = (M-1-basis) // off
            if A+w+times*offindex>B:
                times = (B - A - w)//offindex
            w += offindex * times
            ma = (z * w + b)%M
            maxima.append((w+A, times, offindex))
        else:
            fact_index += 1
            if fact_index == len(facts):
                break
    return (minima,maxima)

def find_min_max_in_range_skip(z, M, A, B):
    """ We want to find the location of all of the minimum and
    maximum of (w * z) %M for w = A...B But we skip intermediates
    in sequences of equispaced extrema.
    """
    if B < A:
      raise ValueError('A must be smaller or equal than B')
    if M <= 0:
      raise ValueError('M must be positive')
    minima = [A]
    maxima = [A]
    if z%M == 0:
        return (minima,maxima)
    facts = gaps(z,M)
    # When w = 0, we have that (w * z + b) %M = b % M
    mi = (z*A)%M
    ma = (z*A)%M
    fact_index = 0
    b = A * z
    w = 0
    while True:
        offindex = facts[fact_index]
        candidate = (z * (w + offindex) + b)%M
        if w + offindex > B-A:
            break
        if candidate < mi:
            # we have a new minimum.
            w += offindex
            mi = candidate
            ### Move forward as far as it will go
            basis = (z * w + b)%M
            off = (z*offindex)%M
            times = basis // (M-off)
            if A+w+times*offindex>B:
                times = (B - A - w)//offindex
            w += offindex * times
            mi = (z * w + b)%M
            minima.append(w+A)
        elif candidate > ma:
            # we have a new maximum.
            w += offindex
            ma = candidate
            ### Move forward as far as it will go
            basis = (z * w + b)%M
            off = (z*offindex)%M
            times = (M-1-basis) // off
            if A+w+times*offindex>B:
                times = (B - A - w)//offindex
            w += offindex * times
            ma = (z * w + b)%M
            maxima.append(w+A)
        else:
            fact_index += 1
            if fact_index == len(facts):
                break
    return (minima,maxima)

def find_min_max_in_range_reverse_skip(z, M, A, B):
    if B < A:
      raise ValueError('A must be smaller or equal than B')
    if M <= 0:
      raise ValueError('M must be positive')
    minima = [B]
    maxima = [B]
    if z%M == 0:
        return (minima,maxima)
    zp = (M-z)%M
    facts = gaps(zp,M)
    mi = (z*B)%M
    ma = (z*B)%M
    fact_index = 0
    ##
    # We set the offset:
    b = B * z
    ##
    w = 0
    while True:
        offindex = facts[fact_index]
        candidate = (zp * (w + offindex) + b)%M
        assert (zp * (w + offindex) + b)%M == (z * (B-w-offindex))%M
        if B-w-offindex < A:
            break
        if candidate < mi:
            # we have a new minimum.
            w += offindex
            mi = candidate
            ### Move forward as far as it will go
            basis = (zp * w + b)%M
            off = (zp*offindex)%M
            times = basis // (M-off)
            if B-w-offindex*times<A:
                times = (B-A-w)//offindex
            w += offindex * times
            mi = (zp * w + b)%M
            minima.append(B-w)
        elif candidate > ma:
            # we have a new maximum.
            w += offindex
            ma = candidate
            ### Move forward as far as it will go
            basis = (zp * w + b)%M
            off = (zp*offindex)%M
            times = (M-1-basis) // off
            if B-w-times*offindex<A:
                times = (B - A - w)//offindex
            w += offindex * times
            ma = (zp * w + b)%M
            maxima.append(B-w)
        else:
            fact_index += 1
            if fact_index == len(facts):
                break
    return (minima,maxima)

def find_min_max_reverse(z, M, R):
    """ computing the running max,min of (w*z)%M for w from R-1 down to 0."""
    if M <= 0:
      raise ValueError('M must be positive')
    if R > M or R <= 0:
      raise ValueError('bad R, R should be in [1,M]')
    minima, maxima = find_min_max(M-z,M,(R*z)%M)
    def flip(arr):
        arr = list(filter((R).__gt__,arr))
        return [R-arr[i] for i in range(len(arr))]
    return (flip(minima), flip(maxima))

def find_min_max_reverse_skip(z, M, R):
    """ computing the running max,min of (w*z)%M for w from R-1 down to 0. We skip
    intermediate equispaced extrema. """
    if M <= 0:
      raise ValueError('M must be positive')
    if R > M or R <= 0:
      raise ValueError('bad R, R should be in [1,M]', R, M)
    minima, maxima = find_min_max_skip(M-(z%M),M,(R*z)%M)
    def flip(arr):
        arr = list(filter((R).__gt__,arr))
        return [R-arr[i] for i in range(len(arr))]
    return (flip(minima), flip(maxima))