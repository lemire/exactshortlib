import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from exactshort.remainder import *


########################################
########################################




def find_min_max_in_range_brute_skip_reverse(z, M, A, B):
    if A > B:
      raise ValueError('A must be no larger than B')
    minima = [B]
    maxima = [B]
    mi = (z*B)%M
    ma = (z*B)%M
    w = B
    last = w
    while w-1 >= A:
        w -= 1
        value = (z*w)%M
        if value > ma:
            gap = last - w
            last = w
            ma = value
            while w-1>= A and (z*(w-1))%M>= mi:
                w -= 1
                value = (z*w)%M
                if value > ma:
                    oldgap = gap
                    gap = last - w
                    if gap != oldgap:
                        maxima.append(last)
                    ma = value
                    last = w
            maxima.append(last)
        if value < mi:
            gap = last - w
            last = w
            #minima.append(lastmin)
            mi = value
            while w-1>= A and (z*(w-1))%M<= ma:
                w -= 1
                value = (z*w)%M
                if value < mi:
                    oldgap = gap
                    gap = last - w
                    if gap != oldgap :
                        minima.append(last)
                    mi = value
                    last = w
            minima.append(last)
    return (minima,maxima)


print("checking find_min_max_in_range_skip_reverse")

M = 4
z = 5
A = 4
B = 6
fast = find_min_max_in_range_reverse_skip(z,M,A,B)
slow = find_min_max_in_range_brute_skip_reverse(z,M,A,B)


if fast != slow:
    print("fast:",fast)
    print("slow:",slow)
    raise ValueError(str("bug z="+ str(z)+ " A ="+str(A)+ " B ="+str(B)))

for M in range (250,260):
  print(".",end="",flush=True)
  for A in range(2,256+1,5):
    for B in range(A,256+1,5):
        for z in range(1,256):
            fast = find_min_max_in_range_reverse_skip(z,M,A,B)
            slow = find_min_max_in_range_brute_skip_reverse(z,M,A,B)
            if fast != slow:
               print("fast:",fast)
               print("slow:",slow)
               raise ValueError(str("bug z="+ str(z)+ " A ="+str(A)+ " B ="+str(B)))

print("checking find_min_max_reverse ok")

###########################
###########################


def find_min_max_in_range_brute(z, M, A, B):
    minima = [A]
    maxima = [A]
    mi = (z*A)%M
    ma = (z*A)%M
    for w in range(A,B+1):
        value = (z*w)%M
        if value > ma:
            ma = value
            maxima.append(w)
        if value < mi:
            mi = value
            minima.append(w)
    return (minima,maxima)


def find_min_max_in_range_brute_skip(z, M, A, B):
    if A > B:
      raise ValueError('A must be no larger than B')
    minima = [A]
    maxima = [A]
    mi = (z*A)%M
    ma = (z*A)%M
    w = A
    lastmax = w
    lastmin = w
    last = w
    while w+1 <= B:
        w += 1
        value = (z*w)%M
        if value > ma:
            gap = w-last
            last = w
            ma = value
            while w+1 <= B and (z*(w+1))%M>= mi:
                w += 1
                value = (z*w)%M
                if value > ma:
                    oldgap = gap
                    gap = w-last
                    if gap != oldgap:
                        maxima.append(last)
                    ma = value
                    last = w
            maxima.append(last)
        if value < mi:
            gap = w-last
            last = w
            mi = value
            while w+1<= B and (z*(w+1))%M<= ma:
                w += 1
                value = (z*w)%M
                if value < mi:
                    oldgap = gap
                    gap = w-last
                    if gap != oldgap :
                        minima.append(last)
                    mi = value
                    last = w
            minima.append(last)
    return (minima,maxima)



########################################
########################################

print("checking find_min_max_in_range")

for M in range (250,260):
  print(".",end="",flush=True)
  for A in range(2,256+1,5):
    for B in range(A,256+1,5):
        for z in range(1,256):
            fast = find_min_max_in_range_skip(z,M,A,B)
            slow = find_min_max_in_range_brute_skip(z,M,A,B)
            if fast != slow:
               print("fast:",fast)
               print("slow:",slow)
               raise ValueError(str("bug z="+ str(z)+ " A ="+str(A)+ " B ="+str(B)))

print("checking find_min_max_in_range_skip ok")
######################
######################


def find_min_max_brute_verbose(z, M, b):
    """ We want to find the location of all of the minimum and
    maximum of (w * z + b) %M for w = 0, 1...
    """
    if M <= 0:
      raise ValueError('M must be positive')
    if z >= M or z < 0:
      raise ValueError('bad z, z should be in [0,M)')
    if b >= M or b < 0:
      raise ValueError('bad b, b should be in [0,M)')
    # When w = 1, we have that (w * z + b) % M = b % M
    mi = (b+z)%M
    ma = (b+z)%M
    fact_index = 0
    w = 1
    minima = [1]
    maxima = [1]
    while (z*w)%M !=0: # We will reach M/gcd(M,z)
        candidate = (z * (w + b))%M
        if candidate <= mi:
            mi = candidate
            print("found minimum ", mi, " at ", w)
            minima.append(w)
        if candidate >= ma:
            ma = candidate
            print("found maximum ", ma, " at ", w)
            maxima.append(w)
        w += 1
    return (minima, maxima)



def find_min_max_reverse_brute(z, M, Mrange):
    if M <= 0:
      raise ValueError('M must be positive')
    if z >= M or z < 0:
      raise ValueError('bad z, z should be in [0,M)')
    # When w = 1, we have that (w * z + b) % M = b % M
    mi = ((Mrange-1)*z)%M
    ma = ((Mrange-1)*z)%M
    w = Mrange-1
    minima = [w]
    maxima = [w]
    while w > 0:
        candidate = (z * w)%M
        if candidate < mi:
            mi = candidate
            minima.append(w)
        if candidate > ma:
            ma = candidate
            maxima.append(w)
        w -= 1
    return (minima, maxima)



########################################
########################################
print("checking find_min_max_reverse")


for R in range(125,256+1):
    for z in range(1,256):
        fast = find_min_max_reverse(z,256,R)
        slow = find_min_max_reverse_brute(z,256,R)
        if fast != slow:
            print(fast)
            print(slow)
            raise ValueError(str("bug z="+ str(z)+ " Mrange ="+str(R)))

print("checking find_min_max_reverse ok")

def find_min_max_brute(z, M, b):
    """ We want to find the location of all of the minimum and
    maximum of (w * z + b) %M for w = 0, 1...
    """
    if M <= 0:
      raise ValueError('M must be positive')
    if z >= M or z < 0:
      raise ValueError('bad z, z should be in [0,M)')
    if b >= M or b < 0:
      raise ValueError('bad b, b should be in [0,M)')
    # When w = 1, we have that (w * z + b) % M = b % M
    mi = (b+z)%M
    ma = (b+z)%M
    fact_index = 0
    w = 1
    minima = [1]
    maxima = [1]
    while True:
        candidate = (z * w + b)%M
        if candidate < mi:
            mi = candidate
            minima.append(w)
        if candidate > ma:
            ma = candidate
            maxima.append(w)
        if (z*w)%M ==0: # We will reach M/gcd(M,z)
            break
        w += 1
    return (minima, maxima)

print("checking find_min_max")
for M in range(200,300,10):
  print(".", end="", flush=True)
  for b in range(M):
    for z in range(1,M):
        fast = find_min_max(z,M,b)
        slow = find_min_max_brute(z,M,b)
        if fast != slow:
            print("fast:",fast)
            print("slow:",slow)
            raise ValueError(str("bug z = " + str(z)+ " b = " + str(b))+ " M = "+str(M))
print("checking find_min_max ok")


def gaps_brute(z, M):
    """ We want to find the location of all of the minimum and
    maximum of (w * z + b) %M for w = 0, 1...
    """
    if M <= 0:
      raise ValueError('M must be positive')
    # When w = 1, we have that (w * z + b) % M = b % M
    mi = (z)%M
    ma = (z)%M
    lambdal = []
    lastgap = 0
    lastmax = 1
    lastmin = 1
    fact_index = 0
    w = 1
    while w < M/math.gcd(M,z):
        candidate = (z * w)%M
        if candidate < mi:
            gap = w - lastmin
            lastmin = w
            if gap != lastgap:
                lambdal.append(gap)
            lastgap = gap
            mi = candidate
        if candidate > ma:
            status = +1
            gap = w - lastmax
            lastmax = w
            if gap != lastgap:
                lambdal.append(gap)
            lastgap = gap
            ma = candidate
        w += 1
    candidate = (z * w)%M
    if candidate < mi:
        gap = w - lastmin
        if gap != lastgap:
            lambdal.append(gap)
    if candidate > ma:
        gap = w - lastmax
        if gap != lastgap:
            lambdal.append(gap)
    return lambdal


print("checking gaps")
for M in range(250,300):
    for z in range(1,512):
        if z // M * M == z:
            continue
        slow = gaps_brute(z,M)
        fast = gaps(z,M)
        if fast != slow:
            print("fast:", fast)
            print("slow:", slow)
            raise ValueError(str("bug z = " + str(z)+ " M = " + str(M)))
print("checking gaps ok")




